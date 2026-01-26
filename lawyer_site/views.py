# lawyer_site/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Service, LawyerInfo

def home(request):
    """Главная страница"""
    services = Service.objects.filter(is_active=True)[:3]  # 3 последние услуги
    context = {
        'services': services,
        'title': 'Главная страница'
    }
    return render(request, 'lawyer_site/home.html', context)

def about(request):
    lawyers = LawyerInfo.objects.filter(is_active=True)
    context = {
        'lawyers': lawyers,
        'title': 'О нашей компании'
    }
    return render(request, 'lawyer_site/about.html', context)

def services(request):
    """Страница всех услуг"""
    services_list = Service.objects.filter(is_active=True).order_by('order')
    context = {
        'services': services_list,
        'title': 'Наши услуги'
    }
    return render(request, 'lawyer_site/services.html', context)

def service_detail(request, service_id):
    """Детальная страница услуги"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    context = {
        'service': service,
        'title': service.title
    }
    return render(request, 'lawyer_site/service_detail.html', context)

def contact(request):
    """Страница контактов"""
    context = {
        'title': 'Контакты'
    }
    return render(request, 'lawyer_site/contact.html', context)