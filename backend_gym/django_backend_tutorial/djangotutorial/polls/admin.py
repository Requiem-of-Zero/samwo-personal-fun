from django.contrib import admin
from .models import Question, Choice
# Register your models here.

<<<<<<< HEAD
admin.site.register(Question)
admin.site.register(Choice)
=======
# admin.site.register(Question)
# admin.site.register(Choice)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {"fields": ["question_text"]}),
    #     ("Date information", {"fields": ["pub_date"]}),
    # ]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
>>>>>>> ae4c6a1618eea4f6be8616ef900b2a43465028a7
