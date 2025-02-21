from django.contrib import *
from django.core.checks import *
from django.forms.widgets import *
from pyexpat.errors import *
from django.shortcuts import *
from . forms import *
from django.views import *
from youtubesearchpython import*
import requests
import wikipedia
 


def home(request):
    return render(request,'dashboard/home.html')

def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST.get('is_finished', False) == 'on'
                
                homeworks = Homework(
                    user=request.user,
                    subject=request.POST['subject'],
                    title=request.POST['title'],
                    description=request.POST['description'],
                    due=request.POST['due'],
                    is_finished=finished
                )
                homeworks.save()
                messages.success(request, f'Homework Added From {request.user.username}!!!')
            except Exception as e:
                print(f"Error occurred: {e}")  # Logging error

    else:
        form = HomeworkForm()

    homework = Homework.objects.filter(user=request.user)
    homework_done = len(homework) == 0

    context = {
        'homeworks': homework,
        'homeworks_done': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)

def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")



def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")



def youtube(request):
    if request.method == "POST":
        form = Dashboardfom(request.POST)
        text = request.POST.get('text', '')  

        
        video = VideosSearch(text, limit=15)
        result_list = []

        
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            
            
            desc = ''
            if 'descriptionSnippet' in i and i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)

        
        context = {
            'form': form,
            'results': result_list
        }
        return render(request, "dashboard/youtube.html", context)
    else:
        form = Dashboardfom()

    context = {'form': form}
    return render(request, "dashboard/youtube.html", context)



def books(request):
    form = Dashboardfom()
    result_list = []

    if request.method == "POST":
        text = request.POST.get('text', '').strip()  
        if text:  
            url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
            try:
                r = requests.get(url)
                r.raise_for_status()  

                answer = r.json()
                items = answer.get('items', [])

                for i in range(min(10, len(items))):  
                    volume_info = items[i].get('volumeInfo', {})
                    result_dict = {
                        'title': volume_info.get('title', 'N/A'),  
                        'subtitle': volume_info.get('subtitle', 'N/A'),
                        'description': volume_info.get('description', 'N/A'),
                        'count': volume_info.get('pageCount', 'N/A'),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('averageRating', 'N/A'),  
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''), 
                        'preview': volume_info.get('previewLink', ''),
                    }
                    result_list.append(result_dict)
            except requests.RequestException as e:
                result_list.append({'error': str(e)})

    context = {'form': form, 'results': result_list}
    return render(request, "dashboard/books.html", context)





def dictionary(request):
    if request.method =="POST":
        form = Dashboardfom(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+text
        r = requests.get(url)
        answer=r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms= answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':  audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form':form,
                'input': ''

            }
        return render(request, "dashboard/dictionary.html", context)
    else:
        form = Dashboardfom()
        context={
            'form':form
        }
        
    return render(request, "dashboard/dictionary.html", context)    


def wiki(request):
    if request.method == 'POST':
        text= request.POST['text']
        form = Dashboardfom(request.POST)
        search = wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'limk': search.url,
            'details': search.summary
        }
        return render (request,"dashboard/wiki.html",context)
    else:
      form = Dashboardfom()
      context={
               'form': form

             }
    return render (request,"dashboard/wiki.html",context)

def register(request):
    if request.method == 'POST':
        if form.valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account created for{username}!")
            return redirect("login")
    else:
         form = UserRegistrationForm()
    context={
               'form':form
                     }
    return render (request,"dashboard/register.html",context)


def profile(request):
    homework = Homework.objects.filter(is_finished=False,user=request.user)
    if len(Homework)==0:
        homework_done=True
    else:
        homework_done=False
   
    context={
        'homework':homework,
        'homework_done':homework_done,
    }
    return render(request,"dashboard/profile.html",context)

    
