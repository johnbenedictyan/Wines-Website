from django.shortcuts import render, redirect
from .models import UserAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm, AccountDetailForm
from django.contrib import auth, messages
from project4 import settings


@login_required
def account_details(request):
    current_user = UserAccount.objects.all().get(pk=request.user.id)
    if request.method == "GET":
        account_details_form = AccountDetailForm(instance=current_user)
        return render(request, "account.html", {
            "current_user": current_user,
            "account_details_form": account_details_form
        })
    else:
        dirty_account_details_form = AccountDetailForm(
            request.POST,
            instance=current_user
        )
        if dirty_account_details_form.is_valid():
            dirty_account_details_form.save()
            messages.success(
                request,
                "Your user details has been successfully updated!"
            )
            return redirect(settings.HOME_URL)
        else:
            return render(
                request,
                "account.html",
                {
                    "account_details_form": dirty_account_details_form
                }
            )


def registration(request):
    if request.method == 'GET':
        registration_form = RegisterForm()
        return render(request,
                      'register.html',
                      {
                          'registration_form': registration_form
                      }
                      )
    else:
        dirty_registration_form = RegisterForm(request.POST)
        if dirty_registration_form.is_valid():
            dirty_registration_form.save()
            username = dirty_registration_form.cleaned_data.get('username')
            raw_password = dirty_registration_form.cleaned_data.get(
                'password1')
            user = authenticate(
                username=username,
                password=raw_password
            )
            login(
                request,
                user
            )
            return redirect(settings.HOME_URL)
        else:
            messages.error(
                request,
                "We are unable to create your account!"
            )
            return render(request,
                          'register.html',
                          {
                              'registration_form': dirty_registration_form
                          })


def log_in(request):
    if request.method == "GET":
        log_in_form = LoginForm()
        return render(request,
                      'login.html',
                      {
                          'log_in_form': log_in_form
                      }
                      )
    else:
        next_url = request.GET.get('next')
        input_username = request.POST.get('username')
        input_password = request.POST.get('password')
        user = auth.authenticate(
            username=input_username,
            password=input_password
        )
        if user is not None:
            auth.login(
                user=user,
                request=request
            )
            messages.success(
                request,
                "Welcome back"
            )
            if next_url:
                return redirect(next_url)
            else:
                return redirect(settings.HOME_URL)
        else:
            messages.error(
                request,
                "Invalid log_in"
            )
            return redirect(settings.LOGIN_URL)
        return


@login_required
def log_out(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("/")
