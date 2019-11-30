from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.shortcuts import render
from django.template.context_processors import csrf
import os, sys
sys.path.append(os.path.abspath(os.path.split(__file__)[0]))

import models
models.HasAdmin()

# 表单
def index_form(request):
  return render(request, 'login.html')

def index_init(request):
  context = csrf(request)
  return render(request, 'admin_init.html')

def index(request):
  if models.HasAdmin() == True:
    return index_form(request)
  elif len(request.POST) > 0:
    return index_form(request)
  
  context = csrf(request)
  return render(request, 'login.html', context)
