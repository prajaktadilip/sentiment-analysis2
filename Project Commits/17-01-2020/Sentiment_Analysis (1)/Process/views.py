from django.shortcuts import render,get_object_or_404
from django.db import connection
from .models import fileupload
from .form import fileUploadForm,File_data
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Filedata
from googletrans import Translator
import csv
#import vader algorithm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer






# Create your views here.
def home_page(request):
	return render(request,'Process/home_page.html')


def about(request):
	return render(request,'Process/about.html')



'''class PocessingDetail(ListView):
    model = fileupload
    template_name = 'process/Analysis.html'
    ordering = ['-upload_date'] 

    def get_queryset(self):
        filename = self.request.GET.get('q')
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        object_list = fileupload.objects.filter(Q(filename__icontains=filename))

        filename1 = str(filename)
        filename = str('media/filefolder/{}'.format(filename))
        sfile = filename.split('.')
        print(sfile)
        sfile = str(sfile[0])
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

        overall_rating1.objects.create(filename=filename1,rating=rating,positive=pos,negative=neg,neutral=neu)'''





def Analysis(request):
    file = fileupload.objects.latest('id')
    filename = str(file.filename)
    filetype = str(file.filetype)
    print(filetype)
    analyzer = SentimentIntensityAnalyzer()

    count = 0
    pos_count = 0
    pos_correct = 0
    neg_count = 0
    neg_correct = 0
    neu_count = 0
    neu_correct = 0

    print("\n")
    with open('Media/'+filetype, 'r') as p:
        for line in p.read().split('\n'):
            vs = analyzer.polarity_scores(line)
            if vs['compound'] > 0.3:
                pos_correct += 1
                pos_count += 1
                print(" - {:-<65} ===> (POSITIVE {}%) ".format(line, vs['pos']*100), end='\n')
            if vs['compound'] < -0.3:
                neg_correct += 1
                neg_count += 1
                print(" - {:-<65} ===> (NEGATIVE {}%) ".format(line, vs['neg']*100), end='\n')
            if (vs['compound'] <= 0.3 and vs['compound'] >= -0.3):
                neu_correct += 1
                neu_count += 1
                print(" - {:-<65} ===> (NEUTRAL {}%) ".format(line, vs['neu']*100), end='\n')
            count += 1

    print("\n")
    print("Total count = {} sentences".format(count))
    print("Positive Accuracy = {}% , {} positive sentences".format(pos_correct / count * 100.0, pos_count))
    print("Negative Accuracy = {}% , {} negative sentences".format(neg_correct / count * 100.0, neg_count))
    print("Neutral Accuracy = {}% , {} neutral sentences".format(neu_correct / count * 100.0, neu_count))
    print("\n")


    pos=pos_correct / count * 100.0
    neg=neg_correct / count * 100.0
    neu=neu_correct / count * 100.0

    f_save=File_data.save(commit=False)
    print(file_save)
    f_save.filename=filename
    print(f_save.filename)
    f_save.filetype=filetype
    f_save.positive=pos
    print(f_save.positive)
    f_save.negative=neg
    f_save.neutral=neu
    
    f_save.save()
    return render(request,'Process/Analysis.html')

    




'''class fileoverallListView(ListView):
    model = overall_rating1
    template_name = 'sentiment/filehome.html'
    context_object_name = 'ov'
    ordering = ['-process_date'] 
    paginate_by = 4

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
        return True'''


#def analyzed_data(request):














def piechart(request):
    return render(request,'Process/piechart.html')

def Individual(request):
    return render(request,'Process/Individual.html')






class fileListView(ListView):
    model = fileupload
    template_name = 'Process/filelist.html'
    context_object_name = 'file'
    ordering = ['-upload_date'] 
    paginate_by = 2

class UserFileListView(ListView):
    model = fileupload
    template_name = 'Process/user_fileupload.html'
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
