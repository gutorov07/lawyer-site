/* static/js/script.js */
// Базовые JavaScript функции

document.addEventListener('DOMContentLoaded', function() {
    console.log('Сайт загружен');
    
    // Анимация кнопок
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Валидация формы контактов
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const phone = document.getElementById('phone');
            const phoneRegex = /^[\d\s\-\+\(\)]+$/;
            
            if (!phoneRegex.test(phone.value)) {
                alert('Пожалуйста, введите корректный номер телефона');
                e.preventDefault();
            }
        });
    }
});