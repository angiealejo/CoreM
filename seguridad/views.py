# -*- coding: utf-8 -*-

# Librerias django

# Django Atajos
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
# from django.core.exceptions import SuspiciousOperation
from django.core.exceptions import PermissionDenied

# Django Seguridad
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

# Django Messages
from django.contrib import messages

# Django paginacion:
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# Django Generic Views
from django.views.generic.base import View
# from django.views.generic import ListView

# Django Autorizacion
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password

# Formularios:
from .forms import UsuarioCreateForm
from .forms import UsuarioEditForm
from .forms import ProfileForm

# Modelos
from .forms import Profile

# API Rest:
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

# API Rest - Serializadores:
from .serializers import UserSerializer
from .serializers import ProfileSerializer
from .serializers import ProfileExcelSerializer


class Login(View):

    def __init__(self):
        self.template_name = 'login.html'

    def get(self, request):

        if request.user.is_authenticated():
            return redirect(reverse('dashboards:inicio'))

        else:
            return render(request, self.template_name, {})

    def post(self, request):

        usuario = request.POST.get('username')
        contrasena = request.POST.get('password')

        user = authenticate(username=usuario, password=contrasena)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect(reverse('dashboards:inicio'))
            else:
                messages.warning(
                    request,
                    "Cuenta DESACTIVADA, favor de contactara a su administrador"
                )

        else:
            messages.error(request, "Cuenta usuario o contraseña no valida")

        return render(request, self.template_name, {})


# ----------------- USUARIO ----------------- #

@method_decorator(login_required, name='dispatch')
class UsuarioListView(View):

    def __init__(self):
        self.template_name = 'usuario/lista.html'

    def get(self, request):

        if not request.user.is_staff:
            raise PermissionDenied

        query = request.GET.get('q')
        if query:
            usuarios_lista = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(profile__puesto__icontains=query) |
                Q(profile__clave__icontains=query)
            )
        else:
            usuarios_lista = User.objects.all()

        paginator = Paginator(usuarios_lista, 10)
        page = request.GET.get('page')

        try:
            usuarios = paginator.page(page)
        except PageNotAnInteger:
            usuarios = paginator.page(1)
        except EmptyPage:
            usuarios = paginator.page(paginator.num_pages)

        contexto = {
            'usuarios': usuarios
        }

        return render(request, self.template_name, contexto)


@method_decorator(login_required, name='dispatch')
class UsuarioCreateView(View):

    def __init__(self):
        self.template_name = 'usuario/crear.html'

    def obtener_UrlImagen(self, _imagen):
        imagen = ''

        if _imagen:
            imagen = _imagen.url

        return imagen

    def get(self, request):
        formulario = UsuarioCreateForm()
        formulario_profile = ProfileForm()

        contexto = {
            'form': formulario,
            'form_profile': formulario_profile,
            'operation': "Nuevo"
        }
        if not request.user.is_staff:
            raise PermissionDenied
        return render(request, self.template_name, contexto)

    def post(self, request):

        formulario = UsuarioCreateForm(request.POST)
        formulario_profile = ProfileForm(
            request.POST,
            request.FILES
        )
        almacenista = request.POST.get('almacenista')
        if formulario.is_valid() and formulario_profile.is_valid():

            datos_formulario = formulario.cleaned_data

            usuario = User.objects.create_user(
                username=datos_formulario.get('username'),
                password=datos_formulario.get('password')
            )
            usuario.first_name = datos_formulario.get('first_name')
            usuario.last_name = datos_formulario.get('last_name')
            usuario.email = datos_formulario.get('email')
            usuario.is_active = datos_formulario.get('is_active')

            usuario.is_staff = datos_formulario.get('is_staff')

            if datos_formulario.get('is_staff'):
                usuario.is_superuser = True
            else:
                usuario.is_superuser = False

            usuario.save()

            if almacenista:
                almacenista = Group.objects.get(name='almacenista')
                almacenista.user_set.add(usuario)

            datos_profile = formulario_profile.cleaned_data

            usuario.profile.puesto = datos_profile.get('puesto')
            usuario.profile.clave = datos_profile.get('clave')
            usuario.profile.fecha_nacimiento = datos_profile.get(
                'fecha_nacimiento'
            )
            usuario.profile.imagen = datos_profile.get('imagen')
            usuario.profile.firma = datos_profile.get('firma')
            usuario.profile.save()

            return redirect(
                reverse('seguridad:usuarios_lista')
            )

        else:
            contexto = {
                'form': formulario,
                'form_profile': formulario_profile,
                'operation': "Nuevo"
            }
            return render(request, self.template_name, contexto)


@method_decorator(login_required, name='dispatch')
class UsuarioEditView(View):

    def __init__(self):
        self.template_name = 'usuario/modificar.html'
        self.cuenta = ''

    def obtener_UrlImagen(self, _imagen):
        imagen = ''

        if _imagen:
            imagen = _imagen.url

        return imagen

    def get(self, request, pk):

        if not request.user.is_staff:
            raise PermissionDenied

        usuario = get_object_or_404(User, pk=pk)
        self.cuenta = usuario.username
        almacenista = False
        formulario = UsuarioEditForm(
            initial={
                'username': usuario.username,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
                'is_staff': usuario.is_staff,
                'is_active': usuario.is_active,
            }
        )

        formulario_profile = ProfileForm(
            instance=usuario.profile
        )
        if usuario.groups.filter(name='almacenista').exists():
            almacenista = True
        contexto = {
            'form': formulario,
            'form_profile': formulario_profile,
            'cuenta': self.cuenta,
            'imagen': self.obtener_UrlImagen(usuario.profile.imagen),
            'firma': self.obtener_UrlImagen(usuario.profile.firma),
            'operation': "Editar",
            'almacenista': almacenista
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):

        usuario = get_object_or_404(User, pk=pk)
        self.cuenta = usuario.username

        formulario = UsuarioEditForm(request.POST)

        formulario_profile = ProfileForm(
            request.POST,
            request.FILES,
            instance=usuario.profile
        )
        almacenista = request.POST.get('almacenista')
        if formulario.is_valid() and formulario_profile.is_valid():

            datos_formulario = formulario.cleaned_data
            usuario.first_name = datos_formulario.get('first_name')
            usuario.last_name = datos_formulario.get('last_name')
            usuario.email = datos_formulario.get('email')
            usuario.is_staff = datos_formulario.get('is_staff')
            usuario.is_active = datos_formulario.get('is_active')

            if datos_formulario.get('is_staff'):
                usuario.is_superuser = True
            else:
                usuario.is_superuser = False

            if datos_formulario.get('password'):
                usuario.password = make_password(
                    datos_formulario.get('password'))

            usuario.save()

            usuario.profile = formulario_profile.save(commit=False)
            usuario.profile.save()

            alm = Group.objects.get(name='almacenista')
            if almacenista:
                alm.user_set.add(usuario)
            else:
                alm.user_set.remove(usuario)

            return redirect(
                reverse('seguridad:usuarios_lista')
            )

        contexto = {
            'form': formulario,
            'form_profile': formulario_profile,
            'imagen': self.obtener_UrlImagen(usuario.profile.imagen),
            'firma': self.obtener_UrlImagen(usuario.profile.firma),
            'cuenta': self.cuenta,
            'operation': "Editar"
        }
        return render(request, self.template_name, contexto)


@method_decorator(login_required, name='dispatch')
class UsuarioPerfilView(View):

    def __init__(self):
        self.template_name = 'usuario/perfil.html'
        self.cuenta = ''
        self.operacion = ''

    def obtener_UrlImagen(self, _imagen):
        imagen = ''

        if _imagen:
            imagen = _imagen.url

        return imagen

    def get(self, request, pk):

        usuario = get_object_or_404(User, pk=pk)
        self.cuenta = usuario.username

        formulario = UsuarioEditForm(
            initial={
                'username': usuario.username,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
                'is_staff': usuario.is_staff,
                'is_active': usuario.is_active,
            }
        )

        formulario_profile = ProfileForm(
            instance=usuario.profile
        )

        if request.user.username != usuario.username:
            formulario.fields['first_name'].disabled = True
            formulario.fields['last_name'].disabled = True
            formulario.fields['password'].disabled = True
            formulario.fields['email'].disabled = True
            formulario.fields['is_staff'].disabled = True
            formulario.fields['is_active'].disabled = True
            formulario_profile.fields['puesto'].disabled = True
            formulario_profile.fields['clave'].disabled = True
            formulario_profile.fields['fecha_nacimiento'].disabled = True
            formulario_profile.fields['imagen'].disabled = True
            formulario_profile.fields['firma'].disabled = True
            formulario_profile.fields['comentarios'].disabled = True
            self.operacion = 'Revision de Perfil'
        else:
            self.operacion = 'Perfil'

        contexto = {
            'form': formulario,
            'form_profile': formulario_profile,
            'cuenta': self.cuenta,
            'imagen': self.obtener_UrlImagen(usuario.profile.imagen),
            'firma': self.obtener_UrlImagen(usuario.profile.firma),
            'operation': self.operacion
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):

        usuario = get_object_or_404(User, pk=pk)
        self.cuenta = usuario.username

        formulario = UsuarioEditForm(request.POST)

        formulario_profile = ProfileForm(
            request.POST,
            request.FILES,
            instance=usuario.profile
        )

        if request.user.username == usuario.username:

            if formulario.is_valid() and formulario_profile.is_valid():

                datos_formulario = formulario.cleaned_data
                usuario.first_name = datos_formulario.get('first_name')
                usuario.last_name = datos_formulario.get('last_name')
                usuario.email = datos_formulario.get('email')
                usuario.is_staff = datos_formulario.get('is_staff')
                usuario.is_active = datos_formulario.get('is_active')

                if datos_formulario.get('is_staff'):
                    usuario.is_superuser = True
                else:
                    usuario.is_superuser = False

                if datos_formulario.get('password'):
                    usuario.password = make_password(
                        datos_formulario.get('password'))

                usuario.save()

                usuario.profile = formulario_profile.save(commit=False)
                usuario.profile.save()

                return redirect(
                    reverse('dashboards:inicio')
                )

        contexto = {
            'form': formulario,
            'form_profile': formulario_profile,
            'imagen': self.obtener_UrlImagen(usuario.profile.imagen),
            'firma': self.obtener_UrlImagen(usuario.profile.firma),
            'cuenta': self.cuenta,
            'operation': "Perfil"
        }
        return render(request, self.template_name, contexto)


class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username', 'is_active')


# ----------------- PROFILE ----------------- #

class ProfileAPI(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    filter_backends = (DjangoFilterBackend,)


class ProfileExcelAPI(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileExcelSerializer
