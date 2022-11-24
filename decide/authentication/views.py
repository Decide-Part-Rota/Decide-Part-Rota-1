from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

from .serializers import UserSerializer
from .forms import PersonForm, LoginForm
from .models import Person


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)


def loginForm(request):
    form = LoginForm()
    return render(request, 'login.html', {'loginForm':form})
'''
def registerForm(request):
    form = RegisterForm()

    return render(request, 'register.html', {'registerForm':form})
'''

def welcome(request):
    return render(request, 'welcome.html')
    
def register(request):
    form= PersonForm()
    if request.method=="POST":
        form=PersonForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email= form.cleaned_data.get('email')
            sex = form.cleaned_data.get('sex')
            age = form.cleaned_data.get('age')
            user1=User(username=username,password=password1,email=email)
            user1.save()
            person1=Person(user=user1,sex=sex,age=age)
            person1.save()

            return redirect('/')
    return render(request,'register.html',{'form':form})   

'''
def register(request):
    
    form = PersonForm(request.POST)
    if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.person.sex = form.cleaned_data.get('sex')
            user.person.age = form.cleaned_data.get('age')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            User = authenticate(username=username, password=password)
            login(request, User)

            return redirect('/')

    else:
         form = PersonForm()

    context = {'form':form}
    return render(request, 'register.html', context)




def nuevoUsuario(request):
    print(request.GET)
    username = request.GET["username"]
    mail = request.GET["email"]
    contrasenya = request.GET["password"]
    sexo = request.GET["sexo"]
    edad = request.GET["edad"]

    nuevoUsuario = User(username=username, email=mail,password=contrasenya)
    nuevoUsuario.save()

    nuevaPersona = Persona(usuario=User.objects.get(username=username), sexo=sexo, edad=edad)
    nuevaPersona.save()

    return render(request, 'welcome.html')




def registerForm(request):
    form = RegisterForm()

    if request.method=='POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.clean_data['username']
            return redirect('/')
    else:
        form = UserCreationForm()

    context = {'form':form}

    return render(request, 'register.html', context)
'''

