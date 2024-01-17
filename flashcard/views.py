from django.http import HttpResponse
from django.shortcuts import render
from .models import Categoria
# Create your views here.

def novo_flashcard(request):
    if request.method == 'GET':
        return render(
            request,
            'novo_flashcard.html',
        )
    elif request.method == "POST":
        cat = Categoria.objects.all()
        
        pergunta = request.POST.get("pergunta") 
        resposta = request.POST.get("resposta")
        categoria = request.POST.get("categoria")
        dificuldade = request.POST.get("dificuldade")

        return HttpResponse(f"{pergunta}, {resposta}, {categoria}, {dificuldade}")
