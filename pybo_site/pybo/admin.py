from django.contrib import admin
from .models import Question
from .models import Answer

#admin.site.register(Question);

class QuestionAdmin(admin.ModelAdmin):
	search_fields = ['subject']
	list_display = ['id', 'subject', 'create_date']

class AnswerAdmin(admin.ModelAdmin):
	search_fields = ['content']
	list_display = ['id', 'content','question' ,'create_date']
	
admin.site.register(Question, QuestionAdmin)

admin.site.register(Answer, AnswerAdmin);



# Register your models here.
