"""
URL Configuration for myapp
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload/', views.upload_document, name='upload_document'),
    path('api/documents/', views.list_documents, name='list_documents'),
    path('api/documents/<int:document_id>/', views.get_document, name='get_document'),
    path('api/documents/<int:document_id>/chat/', views.chat_with_document, name='chat_with_document'),
    path('api/documents/<int:document_id>/chat/history/', views.get_chat_history, name='get_chat_history'),
    path('api/documents/<int:document_id>/download/json/', views.download_json_report, name='download_json'),
    path('api/documents/<int:document_id>/download/txt/', views.download_text_report, name='download_txt'),
]
