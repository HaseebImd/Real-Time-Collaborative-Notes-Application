# notes/views.py
from django.shortcuts import render
from .models import Note

def note_detail(request, note_id):
    note = Note.objects.get(id=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})
from django.shortcuts import render

# Create your views here.
