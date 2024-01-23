from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib.messages import add_message, constants
# Create your views here.

def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect("usuarios/logar")
    if request.method == "GET":
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)
        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')
        if categoria_filtrar:
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)
        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)
            
        return render(request, 'novo_flashcard.html', {"categorias": categorias, "dificuldades": dificuldades, "flashcards": flashcards })
    
    elif request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
        pergunta = request.POST.get("pergunta") 
        resposta = request.POST.get("resposta")
        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            add_message(request, constants.ERROR, "Preencha as perguntas e respostas")
            return redirect('/flashcard/novo_flashcard/')
        categoria = request.POST.get("categoria")
        dificuldade = request.POST.get("dificuldade")
        return HttpResponse('teste')
    flashcard = Flashcard(
        user=request.user, 
        pergunta=pergunta,
        responsta=resposta,
        categoria_id=categoria, 
        dificuldade=dificuldade, 
    )
    flashcard.save()
    add_message(request, constants.SUCCESS, "Flashcard cadastrado com sucesso.")
    return redirect('/flashcard/novo_flashcard/')
    # if request.method == "POST":
    #     if request.user.is_authenticated:
    #         user = request.user
    #     pergunta = request.POST.get("pergunta") 
    #     resposta = request.POST.get("resposta")
    #     if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
    #         add_message(request, constants.ERROR, "Preencha as perguntas e respostas")
    #         return redirect('/flashcard/novo_flashcard/')
    #     categoria = request.POST.get("categoria")
    #     dificuldade = request.POST.get("dificuldade")
        
    #     Categoria(user=user, pergunta=pergunta, resposta=resposta, categoria=categoria, dificuldade=dificuldade).save()
    #     add_message(request, constants.SUCCESS, "Dados salvos com sucesso!!")
    #     return HttpResponse(f"{pergunta}, {resposta}, {categoria}, {dificuldade}")
    # else:        
    #     return render(
    #         request,
    #         'novo_flashcard.html',{"categorias":categorias, "flashcards": flashcards, "dificuldades":Flashcard.DIFICULDADE_CHOICES}
    #     )

    
def deletar_flashcard(request, id):
    # validar o user 
    card = Flashcard.objects.get(id=id)
    card.delete()
    add_message(request, constants.SUCCESS, "Flashcard deletado com sucesso.")
    return redirect('novo_flashcard')
    

def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        return render(
            request,
            'iniciar_desafio.html',
            {'categorias': categorias, 'dificuldades': dificuldades},
        )
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade,
        )
        desafio.save()

        desafio.categoria.add(*categorias)

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)
            .order_by('?')
        )

        if flashcards.count() < int(qtd_perguntas):
            return redirect('/flashcard/iniciar_desafio/')

        flashcards = flashcards[: int(qtd_perguntas)]
        
        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f,
            )
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()

        return redirect(f'/flashcard/desafio/{desafio.id}')
    

def listar_desafio(request):
    desafios = Desafio.objects.filter(user=request.user)
    return render(
        request,
        'listar_desafio.html',
        {
            'desafios': desafios,
        },
    )

def desafio():
    ...