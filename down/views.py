from django.shortcuts import render , get_object_or_404 ,redirect
from django.http import HttpResponse,Http404
from django import forms
import requests
from django.db import models
from django.conf import settings
from django.templatetags.static import static
from bs4 import BeautifulSoup 
import os
from django.core.files import File
from django.views.static import serve
from django.core.files.storage import FileSystemStorage , Storage
import mimetypes
class newpic(forms.Form):
    task = forms.CharField(label="URL",widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))
# Create your views here.
class down(forms.Form):
    task = forms.CharField(label="URL")


def one(request):
    if 'last' in request.POST:
        p = settings.MEDIA_ROOT
        x=os.path.join(p,"instadownload.jpg")
        if os.path.exists(x):
            os.remove(x)
            return redirect('start/')
        else :
            return redirect('start/')

        
            
    return render(request,"i.html")

def index(request):
    if request.method == "POST":
        p = settings.MEDIA_ROOT
        x=os.path.join(p,"instadownload.jpg")
        if os.path.exists(x):
            os.remove(x)
        form = newpic(request.POST)
        if form.is_valid():
            n=form.cleaned_data["task"]
            r=requests.get(n)
            x=r.text
            s=BeautifulSoup(x,'lxml')
            photo_url = s.find("meta", property="og:image")['content']
            requests_url = requests.get(photo_url)
            fs = FileSystemStorage() 
             
            f = fs.open(p, 'ab')
            f.write(requests_url.content)
            f.close()
            path = settings.MEDIA_ROOT
            img_list = os.listdir(path)
            context = {"images":img_list}
            return HttpResponse('hello')
    return render(request,"index.html",{"form": newpic()})
def two(request):
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path)
    context = {"images":img_list}
    return render(request,"index1.html",context)



