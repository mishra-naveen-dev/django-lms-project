from django.contrib import admin
from .models import *
# Register your models here.

class What_u_learn_TabularInline(admin.TabularInline):
    model = What_u_learn


class Requirements_TabularInline(admin.TabularInline):
    model=Requirements

class course_admin(admin.ModelAdmin):
    inlines=(What_u_learn_TabularInline,Requirements_TabularInline)


admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,course_admin)
admin.site.register(Level)
admin.site.register(What_u_learn)
admin.site.register(Requirements)

