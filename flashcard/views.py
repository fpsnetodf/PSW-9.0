from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
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

def desafio(request, id):
    desafio = Desafio.objects.get(id=id)

    if request.method == 'GET':
        return render(
            request,
            'desafio.html',
            {
                'desafio': desafio,
            },
        )
    
def responder_flashcard(request, id):
    flashcard_desafio = FlashcardDesafio.objects.get(id=id)
    acertou = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')
    flashcard_desafio.respondido = True
    flashcard_desafio.acertou = True if acertou == '1' else False
    flashcard_desafio.save()
    return redirect(f'/flashcard/desafio/{desafio_id}/')