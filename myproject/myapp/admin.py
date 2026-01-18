from django.contrib import admin
from .models import Document, ChatMessage


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file_type', 'email', 'phone')
    search_fields = ('name', 'email', 'phone', 'address')
    list_filter = ('file_type', 'gender')
    readonly_fields = ('raw_ocr_text', 'enhanced_text')
    
    fieldsets = (
        ('File Information', {
            'fields': ('uploaded_file', 'file_type')
        }),
        ('Extracted Fields', {
            'fields': ('name', 'dob', 'address', 'city', 'state', 'phone', 'email', 'gender', 'date')
        }),
        ('OCR Processing', {
            'fields': ('raw_ocr_text', 'enhanced_text'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'question_preview', 'created_at')
    search_fields = ('question', 'answer')
    list_filter = ('created_at',)
    readonly_fields = ('document', 'question', 'answer', 'created_at')
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'

