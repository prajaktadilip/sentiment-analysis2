from django.shortcuts import render
from .models import graph
# Create your views here.

def piechart(request):
    form = graph.objects.latest('id')
    form1 = form.positive
    form2 = form.negative
    form3 = form.neutral
    return render(request, 'piechart/piechart1.html', {'form':form1, 'form2':form2, 'form3':form3})
