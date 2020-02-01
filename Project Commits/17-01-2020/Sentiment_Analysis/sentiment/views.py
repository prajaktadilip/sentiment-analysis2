import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from .models import fileupload, overall_rating1, individual_rating
from .form import fileUploadForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
import random
import datetime
import time
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
    template_name = 'sentiment/home.html'
    context_object_name = 'file'
    ordering = ['-upload_date'] 
    paginate_by = 4

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
        filename = form.cleaned_data.get('filename')
        filetype = str(form.cleaned_data.get('filetype'))
        messages.success(self.request, f'Uploaded filename is "{filename}" and filetype is {filetype}!')
        return super().form_valid(form)


class fileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = fileupload
    success_url = '/'
    
    def test_func(self):
        fileupload = self.get_object()
        if self.request.user == fileupload.user:
            return True
        return False

def about(request):
    return render(request,'sentiment/about.html')

class PocessingDetail(ListView):
    model = [fileupload, individual_rating]
    template_name = 'sentiment/search.html'
    ordering = ['-upload_date'] 
    success_url = '/'

    def get_queryset(self):
        filename = self.request.GET.get('q')
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        object_list = fileupload.objects.filter(Q(filename__icontains=filename))

        filename1 = str(filename)
        filename = str('media/filefolder/{}'.format(filename))
        sfile = filename1.split('.')
        print(sfile)
        sfile1 = str(sfile[0])
        print(sfile)

        analyzer = SentimentIntensityAnalyzer()
        translator = Translator()

        count = 0
        pos_count = 0
        pos_correct = 0
        neg_count = 0
        neg_correct = 0
        neu_count = 0
        neu_correct = 0
        rat = 0
        rat_count = 0

        print("\n")
        with open(filename,'r',encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for line in csv_reader:
                rating = float(line[4])
                trans = translator.translate(line[5]).text

                vs = analyzer.polarity_scores(trans)
                if vs['compound'] > 0.3:
                    pos_correct += 1
                    pos_count += 1
                    print(" - {:-<65} ===> {}% ".format(trans, vs), end='\n')
                    print(" - {:-<65} ===> (POSITIVE {}%) ".format(trans, vs['pos']*100), end='\n')
                if vs['compound'] < -0.3:
                    neg_correct += 1
                    neg_count += 1
                    print(" - {:-<65} ===> {}% ".format(trans, vs), end='\n')
                    print(" - {:-<65} ===> (NEGATIVE {}%) ".format(trans, vs['neg']*100), end='\n')
                if (vs['compound'] <= 0.3 and vs['compound'] >= -0.3):
                    neu_correct += 1
                    neu_count += 1
                    print(" - {:-<65} ===> {}% ".format(trans, vs), end='\n')
                    print(" - {:-<65} ===> (NEUTRAL {}%) ".format(trans, vs['neu']*100), end='\n')
                print(rating)
                rat += rating
                print(rat)
                count += 1

        print("\n")
        print("Total count = {} sentences".format(count))
        print("Positive Accuracy = {}% , {} positive sentences".format(pos_correct / count * 100.0, pos_count))
        print("Negative Accuracy = {}% , {} negative sentences".format(neg_correct / count * 100.0, neg_count))
        print("Neutral Accuracy = {}% , {} neutral sentences".format(neu_correct / count * 100.0, neu_count))        
        print("Rating Accuracy = {}% , {} Rating sentences".format(rat / count * 10.0 + rat / count * 10.0, count))
        print("\n")

        pos = pos_correct/count*100.0
        neg = neg_correct/count*100.0
        neu = neu_correct/count*100.0
        rating = rat/count*10.0 + rat/count*10.0

        overall_rating1.objects.create(filename=sfile1,rating=rating,positive=pos,negative=neg,neutral=neu)

        with open(filename,'r',encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for line in csv_reader:
                product_id = line[0]
                product_name = line[1]
                review_date = line[2]
                category = line[3]
                rating = line[4]
                review_text = line[5]
                trans = translator.translate(line[5]).text
                vs = analyzer.polarity_scores(trans)
                pos = vs['pos']*100
                neg = vs['neg']*100
                neu = vs['neu']*100
                individual_rating.objects.create(filename=sfile1,product_id=product_id,product_name=product_name,review_date=review_date,review_text=review_text,process_review=trans,rating=rating,positive=pos,negative=neg,neutral=neu)


        return redirect('home')
        '''
        def piechart(pos,neg,neu):

            #model = overall_rating
            #over = overall_rating.objects.filter(filename='review.csv')
            
            xdata = ['Positive','Negative','Neutral']
            ydata = [pos,neg,neu]

            extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
            chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
            charttype = "pieChart"

            data = {
                'charttype': charttype,
                'chartdata': chartdata,
            }
            return render_to_response('sentiment/search.html', data)

        piechart(pos,neg,neu)
        #with connection.cursor() as cursor:
            #cur.execute('create table {} if not exists (product_id int, product_name varchar(50), review_date date, category varchar(30), review_text varchar(250), rating double, positive double, negative double, neutral double)'.format(filename1))
            #cursor.execute('create tabel overall_result if not exists (filename varchar(30) foreign key references fileupload(filename), positive double, negative double, neutral double)')
            
        '''

def filehome(request):
    context = {
        'ov': overall_rating1.objects.all()
    }
    return render(request,'sentiment/filehome.html',context)

class fileoverallListView(ListView):
    model = overall_rating1
    template_name = 'sentiment/filehome.html'
    context_object_name = 'ov'
    ordering = ['-process_date'] 
    paginate_by = 6

class UserPostListView(ListView):
    model = overall_rating1
    template_name = 'sentiment/user_file.html'
    context_object_name = 'ov'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return overall_rating1.objects.filter(user=user).order_by('-process_date')

class fileoverallDetailView(DetailView):
    model = overall_rating1


class fileoverallDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = overall_rating1
    success_url = '/filehome/'

    def test_func(self):
        return True
    
def individualhome(request):
    context = {
        'ir': individual_rating.objects.all()
    }
    return render(request,'sentiment/individualhome.html',context)

class individualListView(ListView):
    model = individual_rating
    template_name = 'sentiment/individualhome.html'
    context_object_name = 'ir'
    ordering = ['-id'] 
    paginate_by = 6

class filenameListView(ListView):
    model = individual_rating
    template_name = 'sentiment/filename.html'
    context_object_name = 'ir'

    def get_queryset(self):
        filename = get_object_or_404(individual_rating, filename=self.kwargs.get('filename'))
        filename = str(filename)
        print(filename)
        sfile = str(filename.split("."))
        print(sfile)
        return individual_rating.objects.filter(filename=sfile).order_by('-id')

class individualDetailView(DetailView):
    model = individual_rating


class individualDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = individual_rating
    success_url = '/individualhome/'

    def test_func(self):
        return True