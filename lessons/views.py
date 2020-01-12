from django.shortcuts import render

def new(request):
    return render(request, 'new.html')

def edit(request):
    return render(request, 'edit.html')

def view(request):
    return render(request, 'view.html')