from django.db import models


class Document(models.Model):
    """Stores uploaded documents and their extracted data"""
    uploaded_file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10)  # 'image' or 'pdf'
    raw_ocr_text = models.TextField(blank=True)
    enhanced_text = models.TextField(blank=True)
    
    # Structured fields extracted from the form
    name = models.CharField(max_length=200, blank=True)
    dob = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=50, blank=True)
    date = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"Document {self.id} - {self.name or 'Unnamed'}"


class ChatMessage(models.Model):
    """Stores chat history for a document"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chat_messages')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Chat for Doc {self.document.id}: {self.question[:50]}"

