from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from braces.views import CsrfExemptMixin
from Debts.settings import DEFAULT_FROM_EMAIL
from apps.users.models import CustomUser
import random as r

from apps.users.serializers import CustomUserSerializer


class LoginView(generics.GenericAPIView, CsrfExemptMixin):
    serializer_class = CustomUser
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        user = request.user
        return render(request, 'login.html')

    def post(self, request):
        """
            Авторизация пользователя в системе

            :param request: Мета данные
            :return: dict - {
                status: bool - успешность выполнения авторизации,
                message: str - сообщение об ошибке
            }
        """
        print('login')
        data = {'status': False, 'message': 'Неизвестная ошибка', 'allow_to_restore_password': False}
        email = request.data.get('email')
        users = CustomUser.objects.filter(username=email)
        if len(users) == 0:
            data['message'] = 'Пользователь с таким Email не найден'
            return Response(data=data, status=HTTP_200_OK)
        password = request.data.get('password')
        print(password)
        user = auth.authenticate(username=email, password=password)
        print(user)
        if user:
            if user.is_deleted:
                data['message'] = 'Пользователь удален'
                return Response(data=data, status=HTTP_200_OK)
            auth.login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            data['user'] = CustomUserSerializer(user).data
            data['status'] = True
            data['message'] = ''
            print('logging')
            return Response(data=data, status=HTTP_200_OK)
        else:
            data['email'] = email
            data['allow_to_restore_password'] = True
            data['message'] = 'Неверно введен пароль'
            return Response(data=data, status=HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        auth.logout(request)
        return redirect('/auth/login')
