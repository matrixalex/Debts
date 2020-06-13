from django.db.models import Q
from django.shortcuts import render, redirect

from apps.debts.models import Debt
from apps.users.models import CustomUser


def my_debts(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    if request.user.is_superuser:
        return redirect('/admin')

    class FinancialRelation(object):
        def __init__(self, user):
            self.user = user
            self.debts = []
            self.is_positive = False
            self.summary = 0

    class CustomDebt(object):
        def __init__(self, debt):
            self.debt = debt
            self.price = debt.price
            self.text = debt.text
            self.created_at = debt.created_at
            self.is_positive = False

    data = {}
    user = request.user
    debts = Debt.objects.filter(Q(is_deleted=False) & Q(user=user)).order_by('-created_at')
    debts_count = len(debts)
    print('я должен', debts)
    relations = []
    relations_id = []
    summary = 0
    for d in debts:
        if d.to_user.id not in relations_id:
            relation = FinancialRelation(d.to_user)
            c_d = CustomDebt(d)
            relation.debts.append(c_d)
            relation.summary -= d.price
            summary -= d.price
            relations_id.append(d.to_user.id)
            relations.append(relation)
        else:
            for rel in relations:
                if rel.user.id == d.to_user.id:
                    c_d = CustomDebt(d)
                    rel.debts.append(c_d)
                    rel.summary -= d.price
                    summary -= d.price

    debts = Debt.objects.filter(Q(is_deleted=False) & Q(to_user=user)).order_by('-created_at')
    debts_count += len(debts)
    print('мне должны', debts)
    for d in debts:
        if d.user.id not in relations_id:
            relation = FinancialRelation(d.user)
            c_d = CustomDebt(d)
            c_d.is_positive = True
            relation.summary += d.price
            relations_id.append(d.user.id)
            relations.append(relation)
            summary += d.price
        else:
            for rel in relations:
                if rel.user.id == d.user.id:
                    c_d = CustomDebt(d)
                    c_d.is_positive = True
                    rel.debts.append(c_d)
                    rel.summary += d.price
                    summary += d.price

    for rel in relations:
        if rel.summary > 0:
            rel.is_positive = True
        rel.summary = abs(rel.summary)
        rel.debts = sorted(rel.debts, key=lambda instance: instance.created_at, reverse=True)
    data['users'] = []
    users = CustomUser.objects.filter(Q(is_deleted=False))
    for u in users:
        if u.id != user.id and not u.is_superuser:
            data['users'].append(u)
    data['user'] = user
    data['debts'] = relations
    data['is_positive'] = True if summary > 0 else False
    data['summary'] = abs(summary)
    data['debts_count'] = debts_count
    return render(request, 'debts.html', context=data)
