from django.shortcuts import render

# Create your views here.
def edit(req):
    return render(req, 'edit.html')