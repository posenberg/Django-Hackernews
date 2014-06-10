from django.forms import ModelForm

from stories.models import Story

class StoryForm(ModelForm):
	class Meta:
		model = Story
		#below takes away things we don't want that initially show up on our form ie 'points' and 'moderator'
		exclude = ('points', 'moderator',)

