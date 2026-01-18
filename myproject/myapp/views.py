"""
API Views for document upload, processing, and chat functionality
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os

from .models import Document, ChatMessage
from .ocr_utils import extract_text_document
from .llm_utils import process_ocr_text, answer_query


def index(request):
    """Home page with upload interface"""
    return render(request, 'index.html')


@api_view(['POST'])
def upload_document(request):
    """
    Upload and process a document (image or PDF)
    - Runs OCR to extract text
    - Uses LLM to enhance and extract structured fields
    - Saves to database
    """
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    uploaded_file = request.FILES['file']
    
    # Validate file type
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext not in ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        return Response(
            {'error': 'Invalid file type. Please upload PDF or image file.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Determine file type
    file_type = 'pdf' if file_ext == '.pdf' else 'image'
    
    try:
        # Create document record
        document = Document.objects.create(
            uploaded_file=uploaded_file,
            file_type=file_type
        )
        
        # Get file path
        file_path = document.uploaded_file.path
        
        # Step 1: Run OCR
        ocr_result = extract_text_document(file_path, psm=6, oem=3, lang='eng')
        raw_ocr_text = ocr_result['combined_text']
        document.raw_ocr_text = raw_ocr_text
        
        # Step 2: Process with LLM
        llm_result = process_ocr_text(raw_ocr_text)
        document.enhanced_text = llm_result['enhanced_text']
        
        # Step 3: Save extracted fields
        fields = llm_result['fields']
        document.name = fields.get('name', '')
        document.dob = fields.get('dob', '')
        document.address = fields.get('address', '')
        document.city = fields.get('city', '')
        document.state = fields.get('state', '')
        document.phone = fields.get('phone', '')
        document.email = fields.get('email', '')
        document.gender = fields.get('gender', '')
        document.date = fields.get('date', '')
        
        document.save()
        
        # Return success with extracted data
        return Response({
            'success': True,
            'document_id': document.id,
            'message': 'Document processed successfully',
            'extracted_data': {
                'name': document.name,
                'dob': document.dob,
                'address': document.address,
                'city': document.city,
                'state': document.state,
                'phone': document.phone,
                'email': document.email,
                'gender': document.gender,
                'date': document.date,
            },
            'enhanced_text': document.enhanced_text
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Error processing document: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_document(request, document_id):
    """Get document details and extracted data"""
    document = get_object_or_404(Document, id=document_id)
    
    return Response({
        'id': document.id,
        'file_type': document.file_type,
        'extracted_data': {
            'name': document.name,
            'dob': document.dob,
            'address': document.address,
            'city': document.city,
            'state': document.state,
            'phone': document.phone,
            'email': document.email,
            'gender': document.gender,
            'date': document.date,
        },
        'enhanced_text': document.enhanced_text
    })


@api_view(['POST'])
def chat_with_document(request, document_id):
    """
    Chat with a document - ask questions about extracted data
    """
    document = get_object_or_404(Document, id=document_id)
    
    question = request.data.get('question', '').strip()
    if not question:
        return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Build context from enhanced text and structured fields
        fields = {
            'name': document.name,
            'dob': document.dob,
            'address': document.address,
            'city': document.city,
            'state': document.state,
            'phone': document.phone,
            'email': document.email,
            'gender': document.gender,
            'date': document.date,
        }
        
        context = (
            "Structured fields:\n" + str(fields) + "\n\n" + 
            "Clean text:\n" + document.enhanced_text
        )
        
        # Get answer from LLM
        answer = answer_query(question, context)
        
        # Save chat message
        chat_message = ChatMessage.objects.create(
            document=document,
            question=question,
            answer=answer
        )
        
        return Response({
            'question': question,
            'answer': answer,
            'created_at': chat_message.created_at
        })
        
    except Exception as e:
        return Response({
            'error': f'Error processing question: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_chat_history(request, document_id):
    """Get all chat messages for a document"""
    document = get_object_or_404(Document, id=document_id)
    messages = document.chat_messages.all()
    
    return Response({
        'document_id': document.id,
        'messages': [
            {
                'question': msg.question,
                'answer': msg.answer,
                'created_at': msg.created_at
            }
            for msg in messages
        ]
    })


@api_view(['GET'])
def list_documents(request):
    """List and search documents"""
    documents = Document.objects.all().order_by('-id')
    
    # Search by name, email, or phone
    search = request.GET.get('search', '')
    if search:
        documents = documents.filter(
            name__icontains=search
        ) | documents.filter(
            email__icontains=search
        ) | documents.filter(
            phone__icontains=search
        )
    
    return Response({
        'count': documents.count(),
        'documents': [
            {
                'id': doc.id,
                'name': doc.name or 'Unnamed',
                'dob': doc.dob,
                'email': doc.email,
                'phone': doc.phone,
                'city': doc.city,
                'state': doc.state,
                'gender': doc.gender,
                'file_type': doc.file_type
            }
            for doc in documents
        ]
    })


@api_view(['GET'])
def download_json_report(request, document_id):
    """Download document data as JSON"""
    from django.http import JsonResponse
    
    document = get_object_or_404(Document, id=document_id)
    
    data = {
        'document_id': document.id,
        'file_type': document.file_type,
        'extracted_fields': {
            'name': document.name,
            'dob': document.dob,
            'address': document.address,
            'city': document.city,
            'state': document.state,
            'phone': document.phone,
            'email': document.email,
            'gender': document.gender,
            'date': document.date,
        },
        'raw_ocr_text': document.raw_ocr_text,
        'enhanced_text': document.enhanced_text,
    }
    
    response = JsonResponse(data, json_dumps_params={'indent': 2})
    response['Content-Disposition'] = f'attachment; filename="document_{document_id}_report.json"'
    return response


@api_view(['GET'])
def download_text_report(request, document_id):
    """Download document data as TXT"""
    from django.http import HttpResponse
    
    document = get_object_or_404(Document, id=document_id)
    
    # Build text report
    report = f"""
DOCUMENT EXTRACTION REPORT
{'='*50}

Document ID: {document.id}
File Type: {document.file_type}

EXTRACTED FIELDS:
{'='*50}
Name: {document.name}
Date of Birth: {document.dob}
Address: {document.address}
City: {document.city}
State: {document.state}
Phone: {document.phone}
Email: {document.email}
Gender: {document.gender}
Date: {document.date}

RAW OCR TEXT:
{'='*50}
{document.raw_ocr_text}

ENHANCED TEXT:
{'='*50}
{document.enhanced_text}
"""
    
    response = HttpResponse(report, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="document_{document_id}_report.txt"'
    return response

