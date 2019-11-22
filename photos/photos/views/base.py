from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.shortcuts import render


def index(request):
  return HttpResponse("Hello, world.")
