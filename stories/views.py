# Create your views here.
import datetime #standard library

#3rd party library
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required

#app modules
from stories.models import Story
from stories.forms import StoryForm




#top paramater has 180 is the number of top stories you want ot get back
# consider is a parameter that takes the latest 1000 stories.

#score function take a story object. Return some type of score to let you know where the story should
# be ranked.
def score(story, gravity=1.8, timebase=120):
	#points of the story divided by age of the story
	points = (story.points - 1)**0.8
	#figure age of hte story
	now = datetime.datetime.utcnow().replace(tzinfo=utc)#gives us a proper timezone aware utc object #NOTE all of Django's fields are stored in UTC time
	age = int((now - story.created_at).total_seconds())/60 # this get a time delta object # total_seconds( ) a float, so we want int
	return points/(age+timebase)**1.8#adds two hours to the base #avoids divide by zero errors

def top_stories(top=180, consider=1000):
	#have the stories storted in a list
	#.order_by() function ... use -created_at for descending order
	#							  +created_at for ascending order
	latest_stories = Story.objects.all().order_by('-created_at')[:consider]
	ranked_stories = sorted([(score(story), story) for story in latest_stories], reverse=True)
	return [story for _, story in ranked_stories][:top] #slice with :top with our top parameter 

#def index(request):
#from django.template import loader, Context
#	stories = top_stories(top=50)
#	template = loader.get_template('stories/index.html')
#	context = Context({'stories': stories})
#	response = template.render(context)
#	return HttpResponse(response)

#shortened version using render_to_response
def index(request):
	stories = top_stories(top=50)
	if request.user.is_authenticated():
		#id__in is an operation. Get id for each story in the top story list.
		liked_stories = request.user.liked_stories.filter(id__in=[story.id for story in stories])
	else:
		#set liked_stories to an empty list.
		liked_stories = []
	return render(request, 'stories/index.html', {
		 #passing attributes stories and user
		'stories': stories,
		'user':request.user,
		'liked_stories': liked_stories
		}) 

		#call the render_to_response method. 
		#Pass in name of template, then dict for the context of template. 
		#('stories/index.html', {'stories': stories})

#Note: Here we are using the login_required constructor from the django.contrib.auth.decorators module
@login_required
def story(request):
	if request.method == 'POST':
		#call the class constructor and pass a dict. In this case StoryForm is the constructor. The dict is the form name and form dict.
		form = StoryForm(request.POST)
		if form.is_valid():
			story = form.save(commit=False)
			story.moderator = request.user
			story.save()
			return HttpResponseRedirect('/')
	else:
		form = StoryForm()
	return render(request, 'stories/story.html', {'form': form})

@login_required
#create a vote view function that takes a request object.
def vote(request):
	story = get_object_or_404(Story, pk=request.POST.get('story'))
	#receiving story id in our requests. Use that to get the correct instance of our story object. Increment the points and save it to our database.
	# problem we might run into - what if we have a story object or story id that doesn't really exists
	# should return a 404 page error, Django has this built in shortcut ```from django.shortcuts import get_object_or_404```
	# use Story class with get_object_or_404 method and pass in the Story model, then pass in our criteria primary key "pk"
	story.points += 1
	story.save()
	user = request.user
	user.liked_stories.add(story)
	user.save()
	return HttpResponse()