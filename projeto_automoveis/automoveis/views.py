from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Automovel

def index(request):
    """View para a página inicial."""
    try:
        total = Automovel.objects.count()
        return render(request, 'automoveis/index.html', {
            'total_automoveis': total,
            'marcas': Automovel.MARCA_CHOICES,
            'combustiveis': Automovel.COMBUSTIVEL_CHOICES,
        })
    except Exception as e:
        return render(request, 'automoveis/index.html', {
            'error': str(e),
            'total_automoveis': 0,
            'marcas': Automovel.MARCA_CHOICES,
            'combustiveis': Automovel.COMBUSTIVEL_CHOICES,
        })

def api_automoveis(request):
    """API simples para listar automóveis."""
    automoveis = Automovel.objects.all()[:20]  # Limitando a 20 para não sobrecarregar
    
    data = [{
        'id': auto.id,
        'marca': auto.get_marca_display(),
        'modelo': auto.modelo,
        'ano_fabricacao': auto.ano_fabricacao,
        'preco': float(auto.preco),
        'disponivel': auto.disponivel
    } for auto in automoveis]
    
    return JsonResponse(data, safe=False)


def busca_rapida(request):
    """View para processar a busca rápida de automóveis."""
    if request.method == 'POST':
        # Inicializa a query
        query = Q()
        
        # Processa os filtros
        marca = request.POST.get('marca')
        if marca:
            query &= Q(marca=marca)
            
        modelo = request.POST.get('modelo')
        if modelo:
            query &= Q(modelo__icontains=modelo)
            
        combustivel = request.POST.get('combustivel')
        if combustivel:
            query &= Q(combustivel=combustivel)
            
        disponivel = request.POST.get('disponivel')
        if disponivel == 'on':
            query &= Q(disponivel=True)
        
        # Executa a consulta básica
        queryset = Automovel.objects.filter(query)
        
        # Aplica ordenação
        ordenacao = request.POST.get('ordenacao')
        if ordenacao:
            if ordenacao == 'preco_asc':
                queryset = queryset.order_by('preco')
            elif ordenacao == 'preco_desc':
                queryset = queryset.order_by('-preco')
            elif ordenacao == 'km_asc':
                queryset = queryset.order_by('quilometragem')
            elif ordenacao == 'km_desc':
                queryset = queryset.order_by('-quilometragem')
            elif ordenacao == 'ano_asc':
                queryset = queryset.order_by('ano_fabricacao')
            elif ordenacao == 'ano_desc':
                queryset = queryset.order_by('-ano_fabricacao')
        
        # Limita a 50 resultados para não sobrecarregar
        automoveis = queryset[:50]
        
        # Formata os resultados
        data = [{
            'id': auto.id,
            'marca': auto.get_marca_display(),
            'modelo': auto.modelo,
            'ano_fabricacao': auto.ano_fabricacao,
            'combustivel': auto.get_combustivel_display(),
            'cor': auto.cor,
            'quilometragem': auto.quilometragem,
            'preco': float(auto.preco),
            'disponivel': auto.disponivel
        } for auto in automoveis]
        
        return JsonResponse(data, safe=False)
    
    # Se não for POST, retorna lista vazia
    return JsonResponse([], safe=False)
