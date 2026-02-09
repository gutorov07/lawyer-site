# lawyer_site/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Service, LawyerInfo
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
import datetime
from django.core.mail import send_mail, BadHeaderError  # ← ДОБАВЬТЕ ЭТО
from django.conf import settings  # ← ДОБАВЬТЕ ЭТО
import yagmail

def home(request):
    """Рабочая версия с yagmail"""
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        question = request.POST.get('question', '').strip()
        
        if name and phone:
            try:
                # 1. Инициализируем yagmail
                # Вместо 'ваш-пароль-приложения' используйте реальный пароль приложения Gmail
                yag = yagmail.SMTP('mspelmen5@gmail.com', 'vyxx xmfs tadr ftus')
                
                # 2. Подготовка содержимого письма
                contents = [
                    f"📋 НОВАЯ ЗАЯВКА С САЙТА",
                    f"",
                    f"👤 Имя: {name}",
                    f"📱 Телефон: {phone}",
                    f"❓ Вопрос: {question if question else 'Не указан'}",
                    f"⏰ Время: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}",
                    f"",
                    f"СРОЧНО: позвонить клиенту!"
                ]
                
                # 3. Отправляем письмо
                yag.send(
                    to='mspelmen5@gmail.com',  # куда отправлять
                    subject=f'Заявка от {name}',  # БЕЗ emoji в теме
                    contents=contents
                )
                
                print(f"✅ Письмо отправлено через yagmail")
                messages.success(request, f'✅ Спасибо, {name}! Мы вам перезвоним.')
                
            except Exception as e:
                print(f"❌ Ошибка отправки email: {e}")
                
                # 4. Сохраняем в файл как backup
                with open('contact_requests.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.datetime.now()}] {name} | {phone} | {question}\n")
                
                print(f"✅ Заявка сохранена в файл: {name}, {phone}")
                messages.success(request, f'✅ Спасибо, {name}! Заявка принята.')
        else:
            messages.error(request, '❌ Заполните все обязательные поля')
        
        return redirect('home')
    
    return render(request, 'lawyer_site/home.html')


def about(request):
    lawyers = LawyerInfo.objects.filter(is_active=True)
    context = {
        'lawyers': lawyers,
        'title': 'О нашей компании'
    }
    return render(request, 'lawyer_site/about.html', context)

def services(request):
    """Страница всех услуг"""
    
    # Обработка POST запроса (отправка формы)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        question = request.POST.get('question', '').strip()
        email = request.POST.get('email', '').strip()
        service = request.POST.get('service', '').strip()  # Добавь эту переменную!
        
        # Проверка обязательных полей
        if not all([name, phone, email]):
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
            return redirect('services')
        
        # Отправка email
        try:
            send_mail(
                subject=f'Новая заявка на консультацию: {name}',
                message=f'Имя: {name}\nТелефон: {phone}\nEmail: {email}\nУслуга: {service}\nВопрос: {question}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['mspelmen5@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Заявка отправлена! Мы свяжемся с вами в ближайшее время.')
        except Exception as e:
            messages.error(request, f'Ошибка при отправке: {str(e)}')
        
        return redirect('services')  # Редирект на ту же страницу
    
    # Обработка GET запроса (показ страницы)
    else:
        context = {
            'title': 'Наши услуги',
            # добавь другие данные, если нужны
            # 'services_list': Service.objects.all(),
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

