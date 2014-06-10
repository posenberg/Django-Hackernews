from django.contrib import admin
from stories.models import Story

#def lower_case_title(obj):
#	return obj.title.lower()

class StoryAdmin(admin.ModelAdmin):
	
	#list_display attribute is part of ModelAdmin class
	list_display = ('__unicode__', 'domain', 'moderator', 'created_at', 'updated_at')
	
	#list_filter atribute allows the users to filter 
	list_filter = ('created_at', 'updated_at')
	
	search_fields = ('title', 'moderator__username', 'moderator__first_name', 'moderator__last_name')

	
	#for tuples, there needs to be a trailing comma ,) if there is only 1 attribute 
	#fields = ('title','url','created_at','updated_at')
	readonly_fields = ('created_at', 'updated_at')

	

	fieldsets = [

		('Story', {
			'fields': ('title', 'url', 'points')
		}),
		
		('Moderator', {
			'classes': ('collapse',),
			'fields': ('moderator',)
		}),

		('Change History', {
			#find more classes on Admin Site Link>ModelAdmin
			
			#classes
			'classes': ('collapse',),
			
			#fieldset 
			'fields': ('created_at', 'updated_at',)
			})
	]


admin.site.register(Story, StoryAdmin)