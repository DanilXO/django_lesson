from django.contrib import admin

# Register your models here.
from django.utils import timezone

from polls.models import Question, Choice


def make_published_now(modeladmin, request, queryset):
    queryset.update(pub_date=timezone.now())
make_published_now.short_description = "Mark selected polls as published now"

# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']

# admin.site.register(Choice)

# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    search_fields = ['question_text']
    list_filter = ['pub_date']
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    actions = [make_published_now]
admin.site.register(Question, QuestionAdmin)
