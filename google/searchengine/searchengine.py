This tutorial will show you the basic of Django when we will make a google search engine front end in the framework. I've googled out an interesting python module called [http://www.connellybarnes.com/code/web_search/ web_search] which allows to get search results from few search engines and dmoz.

- Download  '''web_search.py''' from that page

- Create a new project called “google”

{{{
django-admin.py startproject google
}}}
- Create a new application called "searchengine":
{{{
python manage.py startapp searchengine
}}}
- Put '''web_search.py''' file in '''searchengine''' folder

- Create '''templates''' folder in the main project folder

- Edit '''settings.py''' and set TEMPATES_DIR to:
{{{
TEMPLATE_DIRS = (
    'templates/'
)
}}}
- Start the development server:
{{{
python manage.py runserver 8080
}}}

We have preconfigured django project that is ready for the search engine code. We will have to make a template with a form where we will be able to enter the search term, and display the results if any.
- Create in '''templates''' file called '''search.html''' with the code:
{{{
<form action="/" method="post">
<input type="text" name="term" size="30"> <input type="submit" value="Search">
</form>
}}}
A simple form that sends the data to / (main url)

- Edit '''searchengine/views.py''' to get:
{{{
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect

def search(request):

    if request.POST:
	print request.POST['term']
	return HttpResponseRedirect("/")
    else:
	return render_to_response('search.html')
}}}
We have a simple view which returns a template “search.html” if no POST data is available and redirects to the / main page when the POST data is available.

- Hook the view to the main URL by editing '''urls.py''' and entering the code:

{{{
from django.conf.urls.defaults import *

urlpatterns = patterns('',
(r'^/?$', 'google.searchengine.views.search'),
)
}}}
When we enter the main page - http://localhost:8080/ we will see the form. When we enter a term and send the form we will be redirected to the main page. The form works. Note the:
{{{
print request.POST['term']
}}}
in the view. You should see the term from the form in the terminal with running django server. '''request.POST''' is a dictionary like object which we can easily access (key is the form field name).

We have the term in the view but we have to do something with it – do google search. '''web_search.py''' module is easy in use, an example:
{{{
from web_search import google
for (name, url, desc) in google('search term', 20):
	print name, url
}}}
we need to use this code, pass the term form the form and then pass the search results to a template and send them to the browser. Edit our '''view.py''' to:
{{{
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
# from project.application.web_search....
from google.searchengine.web_search import google

def search(request):

    if request.POST:
	return render_to_response('search.html', {'result': google(request.POST['term'], 10)})
	#return HttpResponseRedirect("/")
    else:
	return render_to_response('search.html')
}}}
Now we don't redirect but we send the '''search.html''' template with a variable called '''result''' that has the search results. To see the results we need to modify the '''search.html''' template:
{{{
<form action="/" method="post">
<input type="text" name="term" size="30"> <input type="submit" value="Search">
</form><hr>
{% if result %}
	{% for res in result %}
	<li>{{ res }}</li>
	{% endfor %}
{% endif %}
}}}
The '''if result''' tag will pass if the variable exist (if we POSTed the data) the '''for''' will show all data from the search. Test it. You will see that each result is a list:
{{{
('Wine Development HQ', 'http://www.winehq.com/', 'Wine is a free implementation of Windows on Unix. WineHQ is a collection of resources for Wine developers and users.')
}}}
element 0 – page title, element 1 – page URL, element 2 – page description. To make it look as it should we edit our '''for''' loop to:
{{{
{% for res in result %}
	<a href="{{ res.1 }}"><b>{{ res.0 }}</b></a><br>
	{{ res.2 }}<br><br>
{% endfor %}
}}}