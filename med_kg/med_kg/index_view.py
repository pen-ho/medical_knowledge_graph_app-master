# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
#from django.views.decorators import csrf


def index(request):
    context = {}
    return render(request, 'index.html', context)
