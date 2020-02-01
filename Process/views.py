from django.shortcuts import render,get_object_or_404
from django.db import connection
from .models import fileupload
from .form import fileUploadForm
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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import csv
import pandas as pd
#import vader algorithm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer






# Create your views here.
def home_page(request):
    list1.clear()
    list2.clear()
    return render(request,'Process/home_page.html')


def about(request):
    list1.clear()
    list2.clear()
    return render(request,'Process/about.html')

def mail(request):
    file = Filedata.objects.latest('id')
    form1 = file.positive
    form2 = file.negative
    form3 = file.neutral
    form4 = file.filetype
    form5 = file.process_date
    host = "smtp.gmail.com"
    port = 587
    username = ""
    password = ""
    from_email = ''
    to_list = ['']
    try:
        email_conn = smtplib.SMTP(host, port)
        email_conn.ehlo()
        email_conn.starttls()
        email_conn.login(username, password)
        the_msg = MIMEMultipart("alternative")
        the_msg['Subject'] = "Report"
        the_msg["From"] = from_email
        #the_msg["To"]  = to_list[0]
        plain_txt = "Testing the message"
        html_txt ="""\
        <html>

<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
        crossorigin="anonymous">
    <style>
        @page {
            @bottom-right {
                content: counter(page) " of " counter(pages);
            }
        }
        .table-bordered > tbody > tr > td{
            border:1px solid black;
}
    </style>
</head>
        <div class="container" style="page-break-before: always;">
        <div class="row">
            
        </div><br>
        
       
        
        <table class="table table-bordered table-condensed">
            <tbody>
              
                <tr>
                    <td>
                        <h6>
                            <strong>File name:</strong>
                        </h6>
                        <span>"""+str(form4)+"""</span><br>
                        <span><small class="text-muted">"""+str(form5)+"""</small></span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h6>
                            <strong>Rating:</strong>
                        </h6>
                        <span>Positive:""" +str(form1)+"""</span><br>
                        <span>Negative: """+str(form2)+"""</span><br>
                        <span>Neutral: """+str(form3)+"""</span>
                    </td>
                </tr>
              </tbody>
            </table><br>
                
    </div>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>

        """
        part_1 = MIMEText(plain_txt, 'plain')
        part_2 = MIMEText(html_txt, "html")
        the_msg.attach(part_1)
        the_msg.attach(part_2)
        email_conn.sendmail(from_email, to_list, the_msg.as_string())
        email_conn.quit()
    except smtplib.SMTPException:
        print("error sending message")


    return render(request,'Process/Analysis.html')
















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



list1 = []
list2 = []



def Analysis(request):

    file = fileupload.objects.latest('id')
    filename = str(file.filename)
    filetype = str(file.filetype)
    print(filetype)
    analyzer = SentimentIntensityAnalyzer()
    
    global list2
    global list1
    list1.clear()
    list2.clear()
    count = 0
    pos_count = 0
    neg_count = 0
    neu_count = 0

    df = pd.read_csv('Media/'+filetype)
    df = df.drop(columns=['id', 'name', 'asins', 'brand', 'categories', 'keys', 'manufacturer',
           'reviews.date', 'reviews.dateAdded', 'reviews.dateSeen',
           'reviews.didPurchase', 'reviews.doRecommend', 'reviews.id',
           'reviews.numHelpful', 'reviews.rating', 'reviews.sourceURLs',
           'reviews.title', 'reviews.userCity',
           'reviews.userProvince', 'reviews.username'])
    df1 = df.to_csv('demo.csv', index=False)
    df1 = pd.read_csv('demo.csv')

    with open('demo.csv', 'rt', encoding='utf-8', errors='ignore') as f:
        
        data = csv.reader(f)
        next(data)
        analyzer = SentimentIntensityAnalyzer()

        for line in data:

            line = str(line)
            list1.append(line)
            vs = analyzer.polarity_scores(line)
            
            if vs['compound'] > 0.3:
                pos_count += 1
                list2.append('Positive')
                print(" {}] {:-<65} ===> (POSITIVE {}%) ".format(str(count+1), line, vs['pos']*100), end='\n')

            elif vs['compound'] < -0.3:
                neg_count += 1
                list2.append('Negative')
                print(" {}] {:-<65} ===> (NEGATIVE {}%) ".format(str(count+1), line, vs['neg']*100), end='\n')

            elif 0.3 >= vs['compound'] >= -0.3:
                neu_count += 1
                list2.append('Neutral')
                print(" {}] {:-<65} ===> (NEUTRAL {}%) ".format(str(count+1), line, vs['neu']*100), end='\n')

            count += 1

    print("\n")

    print("Total count = {} sentences".format(count))
    print("Positive Accuracy = {}% , {} positive sentences".format(pos_count / count * 100.0, pos_count))
    print("Negative Accuracy = {}% , {} negative sentences".format(neg_count / count * 100.0, neg_count))
    print("Neutral Accuracy = {}% , {} neutral sentences".format(neu_count / count * 100.0, neu_count))

    print("\n")
    pos=pos_count / count * 100.0
    neg=neg_count / count * 100.0
    neu=neu_count / count * 100.0

    f_save=Filedata()
    print(f_save)
    f_save.filename=filename
    print(f_save.filename)
    f_save.filetype=filetype
    f_save.positive=pos
    print(f_save.positive)
    f_save.negative=neg
    f_save.neutral=neu
    
    f_save.save()

    return render(request,'Process/Analysis.html')










def back(request):
    return render(request,'Process/Analysis.html')







'''def Analysis(request):
    file = fileupload.objects.latest('id')
    filename = str(file.filename)
    filetype = str(file.filetype)
    print(filetype)
    analyzer = SentimentIntensityAnalyzer()
    global list2
    global list1
    
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
            list1.append(line)
            vs = analyzer.polarity_scores(line)
            if vs['compound'] > 0.3:
                pos_correct += 1
                pos_count += 1
                list2.append('positive')
                print(" - {:-<65} ===> (POSITIVE {}%) ".format(line, vs['pos']*100), end='\n')
            if vs['compound'] < -0.3:
                neg_correct += 1
                neg_count += 1
                list2.append('negative')
                print(" - {:-<65} ===> (NEGATIVE {}%) ".format(line, vs['neg']*100), end='\n')
            if (vs['compound'] <= 0.3 and vs['compound'] >= -0.3):
                neu_correct += 1
                neu_count += 1
                list2.append('neutral')
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

    f_save=Filedata()
    print(f_save)
    f_save.filename=filename
    print(f_save.filename)
    f_save.filetype=filetype
    f_save.positive=pos
    print(f_save.positive)
    f_save.negative=neg
    f_save.neutral=neu
    
    f_save.save()

    return render(request,'Process/Analysis.html')'''

    
listall=list1
listall2=list2

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
    form = Filedata.objects.latest('id')
    form1 = form.positive
    form2 = form.negative
    form3 = form.neutral
    return render(request,'Process/piechart.html', {'form':form1, 'form2':form2, 'form3':form3})


def Individual(request):
    list1=listall
    list2=listall2
    totallist = zip(list1,list2)
    return render(request,'Process/Individual.html',{'list1':totallist})



def history(request):
    history=Filedata.objects.all()
    return render(request,'Process/history.html',{'history':history})


class fileListView(ListView):
    list1.clear()
    list2.clear()
    model = fileupload
    template_name = 'Process/filelist.html'
    context_object_name = 'file'
    ordering = ['-upload_date'] 
    paginate_by = 2

class UserFileListView(ListView):
    list1.clear()
    list2.clear()
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
    list1.clear()
    list2.clear()
    model = fileupload

    fields = ['filename','filetype']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
