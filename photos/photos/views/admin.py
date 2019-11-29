from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.shortcuts import render
from django.template.context_processors import csrf

# 表单
def index_form(request):
  return render(request, 'login.html')

def index_init(request):
  context = csrf(request)
  return render(request, 'admin_init.html')

def index(request):
  if len(request.POST) > 0:
    return index_form(request)
  context = csrf(request)
  return render(request, 'login.html', context)
