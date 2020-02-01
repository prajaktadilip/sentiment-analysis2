from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from .models import fileupload
from .form import fileUploadForm
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView,
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

def home(request):
    context = {
        'file': fileupload.objects.all()
    }
    return render(request,'sentiment/home.html',context)

class fileListView(ListView):
    model = fileupload
    template_name = 'sentiment/filelist.html'
    context_object_name = 'file'
    ordering = ['-upload_date'] 
    paginate_by = 2

class UserFileListView(ListView):
    model = fileupload
    template_name = 'sentiment/user_fileupload.html'
    context_object_name = 'file'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return fileupload.objects.filter(user=user).order_by('-upload_date')


class fileDetailView(DetailView):
    model = fileupload


class fileCreateView(LoginRequiredMixin ,CreateView):
    model = fileupload

    fields = ['filename','filetype']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request,'sentiment/about.html')

def sentiment_process():
    pass

def sen(self, request):
    with connection.cursor() as cursor:
        table_name = input('#')
        cursor.execute('create table {} (id int, name varchar(30))'.format(table_name))