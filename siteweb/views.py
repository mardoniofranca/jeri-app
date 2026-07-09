from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormCliente, FormAtendimento
from .models import Cliente, Atendimento, Movimentacao
from django.http import HttpResponse
from .models import Cliente_Hist
from django.core.paginator import Paginator


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/menu')

        else:

            messages.error(
                request,
                'Usuário ou senha inválidos'
            )
    return render(request, 'login.html')



@login_required
def menu_view(request):
    return render(request, 'menu.html')



@login_required
def cliente_view(request):
    return render(request, 'cliente.html')


@login_required
def atendimento_view(request):
    return render(request, 'atendimento.html')