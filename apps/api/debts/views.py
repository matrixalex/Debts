from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from apps.debts.models import Debt
from apps.debts.serializers import DebtSerializer
from apps.users.models import CustomUser


class GetListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, user_id):
        data = {'status': True, 'message': ''}
        user = request.user
        to_user = CustomUser.objects.get(pk=user_id)
        debts = Debt.objects.filter(
            Q(is_deleted=False) & ((Q(user=user) & Q(to_user=to_user)) | (Q(user=to_user) & Q(to_user=user))))
        debts = debts.order_by('-created_at')
        data['debts'] = []
        for d in debts:
            if d.user.id == user.id:
                d_dict = DebtSerializer(d).data
                d_dict['is_positive'] = False
                data['debts'].append(d_dict)
            elif d.to_user.id == user.id:
                d_dict = DebtSerializer(d).data
                d_dict['is_positive'] = True
                data['debts'].append(d_dict)
        return Response(data=data, status=HTTP_200_OK)


class AddView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = {'status': False, 'message': 'Неизвестная ошибка'}
        user = request.user
        price = abs(float(request.data.get('price').replace(',', '.').strip()))
        text = request.data.get('text') or ''
        if price == 0:
            data['message'] = 'Некорректный долг'
            return Response(data=data, status=HTTP_200_OK)
        is_common_debt = request.data.get('is_common_debt')
        if type(is_common_debt) == str:
            is_common_debt = True if is_common_debt in ['1', 'true'] else False
        print('is_common_debt', is_common_debt)
        if is_common_debt:
            print('for')
            users = CustomUser.objects.filter(Q(is_deleted=False) & Q(is_superuser=False))
            for u in users:
                if u.id != user.id:
                    Debt.objects.create(user=u, to_user=user, text=text, price=int(price / 3))
        else:
            print('no for')
            to_user_id = request.data.get('to_user')
            try:
                to_user = CustomUser.objects.get(pk=to_user_id)
            except:
                data['message'] = 'Пользователь не найден'
                return Response(data=data, status=HTTP_200_OK)
            if to_user.id == user.id:
                data['message'] = 'Невозможно добавить долг самому себе'
                return Response(data=data, status=HTTP_200_OK)
            Debt.objects.create(user=to_user, to_user=user, text=text, price=price)

        data['status'] = True
        data['message'] = ''
        return Response(data=data, status=HTTP_200_OK)
