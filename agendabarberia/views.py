from django.shortcuts import render, redirect, get_object_or_404
from .forms import BarberiaForm, CustomUserCreationForm
from .models import Barberia, Cita
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden



# Barberia acciones


@login_required
def barberias(request):
    barberias = Barberia.objects.all()
    user = request.user 
    citas = Cita.objects.filter(usuario=user)
    notificaciones_citas = citas.count()
    return render(request, 'barberias.html', {'barberias': barberias, 'user':user, 'notificaciones':notificaciones_citas})




@login_required
def registrar_barberia(request):
    if request.method == 'POST':
        form = BarberiaForm(request.POST, request.FILES)
        if form.is_valid():
            barberia = form.save(commit=False)
            barberia.usuario = request.user  # Asigna el usuario actual
            barberia.save()
            return redirect('barberias')
    else:
        form = BarberiaForm()
    return render(request, 'registrar-barberia.html', {'form': form})



@login_required
def perfil_barberia(request, barberia_id):
    barberia = get_object_or_404(Barberia, pk=barberia_id)
    user = request.user
    citas = Cita.objects.filter(usuario=user)
    notificaciones_citas = citas.count()
    return render(request, 'perfil-barberia.html', {'barberia': barberia, 'notificaciones': notificaciones_citas})



@login_required
def editar_barberia(request, barberia_id):
    barberia = get_object_or_404(Barberia, pk=barberia_id)

    # Verifica si el usuario actual es el creador de la barbería
    if request.user != barberia.usuario:
        # Puedes redirigir a alguna página o mostrar un mensaje de error
        return render(request, 'error.html', {'message': 'No tienes permisos para editar esta barbería.'})

    if request.method == 'POST':
        form = BarberiaForm(request.POST, request.FILES, instance=barberia)
        if form.is_valid():
            form.save()
            return redirect('perfil-barberia', barberia_id=barberia_id)
    else:
        form = BarberiaForm(instance=barberia)

    return render(request, 'editar_barberia.html', {'form': form, 'barberia': barberia})



@login_required
def eliminar_barberia(request, barberia_id):
    barberia = get_object_or_404(Barberia, pk=barberia_id)

    # Verifica si el usuario actual es el propietario de la barbería
    if request.user == barberia.usuario:
        barberia.delete()
        return redirect('barberias')
    else:
       
        return HttpResponseForbidden("No tienes permisos para eliminar esta barbería.")



# Inicio de sesion

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}')
                return redirect('barberias')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    
    form = AuthenticationForm()
    return render(request,'iniciar-sesion.html', {"form":form})



def registrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciar-sesion')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registrar-usuario.html', {'form': form})


#reservas

def reservas(request):
    current_user = request.user
    citas = Cita.objects.filter(usuario=current_user)
    notificaciones_citas = citas.count()
    return render(request, 'reservas.html', {'citas': citas, 'notificaciones': notificaciones_citas})

# def reservas(request):
#     return render(request, 'reservas.html')


@login_required
def solicitar_cita(request, barberia_id):
    barberia = Barberia.objects.get(id=barberia_id)
    current_user = request.user

    # Realizar la lógica para crear la cita con la información disponible
    peticion = Cita.objects.create(usuario=current_user, barberia=barberia)

    # Redirigir a la página que muestra las citas de esta barbería
    citas = Cita.objects.filter(barberia=barberia)
    for objeto in citas:
        barberia_titulo = objeto.barberia.titulo
        barberia_ubicacion = objeto.barberia.ubicacion

        print(f"Barberia: {barberia_titulo}")
    return render(request, 'reservas.html', {'citas': citas, 'peticion:':peticion})



#eliminar cita
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    cita.delete()
    return redirect('reservas')

    


def error(request):
    return render(request, 'error.html')