from django.shortcuts import redirect


def index(request):
    # test
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    return redirect('/debts')
