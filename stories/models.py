from urlparse import urlparse

from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Story(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField()
	points = models.IntegerField(default=1)
	moderator = models.ForeignKey(User, related_name='moderated_stories') 
	#many to many relationship -> voters
	#if you want to access all those users liked, 'liked_stories' is an attribute
	voters=models.ManyToManyField(User, related_name='liked_stories')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@property
	def domain(self):
		return urlparse(self.url).netloc

	def __unicode__(self):
		return self.title

	class Meta:
		# Otherwise it will read as "Storys" in the admin panel
		# For more meta information on class Meta: check out:
		# https://docs.djangoproject.com/en/1.6/ref/models/options/
		verbose_name_plural = "stories"