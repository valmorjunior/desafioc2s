from django.contrib import admin
from .models import Automovel

@admin.register(Automovel)
class AutomovelAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ano_fabricacao', 'ano_modelo', 'preco', 'disponivel')
    list_filter = ('marca', 'combustivel', 'transmissao', 'disponivel')
    search_fields = ('modelo', 'descricao')
    list_per_page = 20
