from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from django.contrib import auth
from ..forms import StudentSignUpForm

class SignUpView(TemplateView):
    template_name = 'registration/register.html'
    



def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:teacher_home')
        else:
            return redirect('students:student_home')
    return render(request, 'classroom/home.html')

class LoginView(View):
    def get(self,request):
        return render(request,'registration/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:

            user = auth.authenticate(username=username , password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + 
                                    user.username + ' you are now logged in')
                    if request.user.is_teacher:
                        print("teacher")
                        return redirect('teachers:teacher_home')
                    else:
                        print("student")
                        return redirect('students:student_home')
                messages.error(
                    request, 'Account is not active, please check your email')
                return render(request,'registration/login.html')
            messages.error(
                request, 'Invalid credentials, try again')
            return render(request,'registration/login.html')
        messages.error(
            request, 'Please fill all the fields')
        return render(request,'registration/login.html')
    




