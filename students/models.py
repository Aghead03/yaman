from django.db import models
from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Student(models.Model):
    
    class Gender(models.TextChoices):
        MALE = 'male', 'ذكر'
        FEMALE = 'female', 'أنثى'
    
    class HowKnewUs(models.TextChoices):
        FRIEND = 'friend', 'صديق'
        SOCIAL = 'social', 'وسائل التواصل الاجتماعي'
        AD = 'ad', 'إعلان'
        ADS = 'ads', 'إعلانات طرقية'
        OTHER = 'other', 'أخرى'
    
    class Academic_Track(models.TextChoices):
        LITERARY = 'أدبي', 'الأدبي'
        SCIENTIFIC = 'علمي', 'العلمي'
        NINTH_GRADE = 'تاسع', 'الصف التاسع'
    
    # Basic Information
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=Gender.choices)
    branch = models.CharField(max_length=10, choices=Academic_Track.choices)
    birth_date = models.DateField()
    student_number = models.CharField(max_length=20) 
    nationality = models.CharField(max_length=50)
    registration_date = models.DateField(default=datetime.now)
    tase3 = models.IntegerField(default=0)
    disease = models.TextField(blank=True, default="none")
    
    # Father Information
    father_name = models.CharField(max_length=100)
    father_job = models.CharField(max_length=100, blank=True)
    father_phone = models.CharField(max_length=20)
    
    # Mother Information
    mother_name = models.CharField(max_length=100, blank=True)
    mother_job = models.CharField(max_length=100, blank=True)
    mother_phone = models.CharField(max_length=20)
    
    # Address Information
    address = models.TextField()
    home_phone = models.CharField(max_length=20)
    
    # Previous Education
    previous_school = models.CharField(max_length=100, blank=True)
    elementary_school = models.CharField(max_length=100, blank=True)
    
    # Other Information
    how_knew_us = models.CharField(
        max_length=100, 
        choices=HowKnewUs.choices, 
        blank=True, 
        null=True
    )
    notes = models.TextField(blank=True)
    added_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="تم الإضافة بواسطة"
    )
    
    @property
    def grades(self):
        """جميع علامات الطالب"""
        return self.grade_set.all()
    
    def __str__(self):
        return self.full_name