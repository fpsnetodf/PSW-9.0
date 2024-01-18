from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Categoria, Flashcard
from django.contrib.messages import add_message, constants
# Create your views here.

def novo_flashcard(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
        pergunta = request.POST.get("pergunta") 
        resposta = request.POST.get("resposta")
        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            add_message(request, constants.ERROR, "Preencha as perguntas e respostas")
            return redirect('/flashcard/novo_flashcard/')
        categoria = request.POST.get("categoria")
        dificuldade = request.POST.get("dificuldade")
        
        Categoria(user=user, pergunta=pergunta, resposta=resposta, categoria=categoria, dificuldade=dificuldade).save()
        add_message(request, constants.SUCCESS, "Dados salvos com sucesso!!")
        return HttpResponse(f"{pergunta}, {resposta}, {categoria}, {dificuldade}")
    else:        
        return render(
            request,
            'novo_flashcard.html',
            {'categorias': Categoria.objects.all(),
            "dificuldades": Flashcard.DIFICULDADE_CHOICES}
        )