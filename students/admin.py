from django.contrib import admin
from . models import Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display=('id','full_name','branch','student_number','father_name','mother_name','notes')




admin.site.register(Student,StudentAdmin)