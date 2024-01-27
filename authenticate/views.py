# views.py
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.views import View

from authenticate.form import SignUpForm

class SignUpView(View):
    template_name = "register.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authenticate:login')

        return render(request, self.template_name, {"form": form})


class LoginForm(View):
    template_name = "login.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('homepage:home')
        return render(request, self.template_name)

    def post(self, request):
        if request.method == "POST":
            uname = request.POST.get("username")
            passw = request.POST.get("password")

            print(f"Username: {uname}\n"
                  f"Password: {passw}")

            auth = {
                "username": uname,
                "password": passw
            }
            user = authenticate(request, username=uname, password=passw)

            if user is not None:
                login(request, user)
                request.session['auth'] = auth

                return redirect('homepage:home')

        return redirect('authenticate:login')


def signOut(request):
    request.session.delete()

    logout(request)
    return redirect('authenticate:login')