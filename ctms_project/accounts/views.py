from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings

from .forms import CTMSAuthenticationForm
from audit.mixins import log_action


def login_view(request):
    form = CTMSAuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            # BUG Cat-H: remember_me is read but has NO effect on session expiry
            remember_me = request.POST.get('remember_me')  # noqa: F841 — value intentionally unused
            log_action(request, 'accounts', user.id, 'LOGIN', {})
            auth_login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            # BUG Cat-G: failed login is NOT logged (no log_action call here)
            form.add_error(None, 'Invalid username or password.')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    log_action(request, 'accounts', request.user.id, 'LOGOUT', {})
    auth_logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
