from django.contrib import admin
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio



admin.site.register(Categoria)
admin.site.register(Flashcard)
# Register your models here.

admin.site.register(Desafio)
admin.site.register(FlashcardDesafio)
