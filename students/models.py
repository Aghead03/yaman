from django.db import models
from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    
    class Gender(models.TextChoices):
        MALE = 'male',
        FEMALE = 'female',
    
    class HowKnewUs(models.TextChoices):
        FRIEND = 'friend', 
        SOCIAL = 'social',
        AD = 'ad',
        OTHER = 'other',
    
    class Academic_Track(models.TextChoices):
        Literary = 'Literary'
        Scientific = 'Scientific'
        Ninth = 'Ninth'
    
    # Basic Information
    full_name = models.CharField( max_length=100)
    
    gender = models.CharField( max_length=6, choices=Gender.choices)
    branch = models.CharField( max_length=10, choices=Academic_Track.choices)
    birth_date = models.DateField()
    student_number = models.CharField(max_length=20) 
    nationality = models.CharField( max_length=50)
    registration_date = models.DateField(default=datetime.now)
    # Father Information
    father_name = models.CharField( max_length=100)
    father_job = models.CharField( max_length=100, blank=True, null=True)
    father_phone = models.CharField(max_length=20)
    # Mother Information
    mother_name = models.CharField( max_length=100, blank=True, null=True)
    mother_job = models.CharField( max_length=100, blank=True, null=True)
    mother_phone = models.CharField( max_length=20)
    # Address Information
    address = models.TextField()
    home_phone = models.CharField( max_length=20)
    # Previous Education
    previous_school = models.CharField( max_length=100, blank=True, null=True)
    elementary_school = models.CharField( max_length=100, blank=True, null=True)
    # Other Information
    how_knew_us = models.CharField(
        max_length=10, 
        choices=HowKnewUs.choices, 
        blank=True, 
        null=True
    )
    notes = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return self.full_name
    

