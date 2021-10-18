from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

class AdminLoginView(View):
    def get(self, request):
        return render(request, 'admin/login.html')

    def post(self, request):
        email_username = request.POST.get('email_username')
        password = request.POST.get('password')
        remember = request.POST.get('remember_check')

        user  = authenticate(request, username = email_username, password = password)

        if user is not None:
            if remember is None:
                self.request.session.set_expiry(0)
            login(request, user)
            return redirect('/admin/')

        else:
            try:
                username = User.objects.get(email = email_username)
            except:
                return render(request, 'admin/login.html', {"message" : "Couldn't sign you in. Please check your credentials and try again."})
            else:        
                user  = authenticate(request, username = username, password = password)

                if user is not None:
                    if remember is None:
                        self.request.session.set_expiry(0)
                    login(request, user)
                    return redirect('/admin/')

                else:
                    return render(request, 'admin/login.html', {'message' : 'Email/Username or Password does not match. Please check your credentials and try again.'})  

