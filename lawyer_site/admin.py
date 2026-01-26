# lawyer_site/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Service, LawyerInfo, Case, Certificate, Article, ContactRequest, FAQ


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_active', 'price_display', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('title', 'short_description', 'full_description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'short_description', 'full_description', 'category')
        }),
        ('Цена и сроки', {
            'fields': ('price_from', 'price_to', 'duration')
        }),
        ('Внешний вид', {
            'fields': ('icon', 'image', 'order')
        }),
        ('Статус и SEO', {
            'fields': ('is_active', 'is_featured', 'meta_title', 'meta_description')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def price_display(self, obj):
        return obj.get_price_display()
    price_display.short_description = 'Цена'


@admin.register(LawyerInfo)
class LawyerInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name_display', 'position', 'phone', 'experience_years', 'is_active', 'is_featured')
    list_filter = ('position', 'is_active', 'is_featured')
    search_fields = ('first_name', 'last_name', 'middle_name', 'specialization', 'email', 'phone')
    filter_horizontal = ('services',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'middle_name', 'photo')
        }),
        ('Профессиональная информация', {
            'fields': ('position', 'specialization', 'bio', 'experience_years', 'education', 'services')
        }),
        ('Контактная информация', {
            'fields': ('email', 'phone', 'office')
        }),
        ('Социальные сети', {
            'fields': ('vk_link', 'telegram_link')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def full_name_display(self, obj):
        return obj.full_name()
    full_name_display.short_description = 'ФИО'


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'service', 'case_date', 'status', 'is_published', 'is_featured')
    list_filter = ('status', 'is_published', 'is_featured', 'service')
    search_fields = ('title', 'client', 'description', 'challenge', 'solution', 'result')
    filter_horizontal = ('lawyers',)
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'case_date'


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'lawyer', 'issuer', 'issue_date', 'expiry_date', 'is_active')
    list_filter = ('is_active', 'issue_date')
    search_fields = ('title', 'issuer', 'certificate_number', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'issue_date'
    
    def is_valid_display(self, obj):
        return obj.is_valid()
    is_valid_display.short_description = 'Действителен'
    is_valid_display.boolean = True


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'views_count', 'published_at')
    list_filter = ('category', 'is_published', 'is_featured', 'allow_comments')
    search_fields = ('title', 'excerpt', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    date_hierarchy = 'published_at'
    list_per_page = 20


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'request_type', 'status', 'is_processed', 'created_at')
    list_filter = ('status', 'request_type', 'is_processed')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at', 'ip_address', 'user_agent', 'processed_at')
    list_per_page = 20
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_processed:
            return self.readonly_fields + ('assigned_to', 'notes')
        return self.readonly_fields
    
    def mark_as_processed(self, request, queryset):
        updated = queryset.update(status='completed', is_processed=True)
        self.message_user(request, f"Отмечено как обработанное: {updated} запросов")
    mark_as_processed.short_description = "Пометить как обработанные"
    
    actions = [mark_as_processed]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'category', 'order', 'is_active', 'is_general')
    list_filter = ('category', 'is_active', 'is_general')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active', 'is_general')
    
    def question_preview(self, obj):
        return obj.question[:100] + '...' if len(obj.question) > 100 else obj.question
    question_preview.short_description = 'Вопрос'