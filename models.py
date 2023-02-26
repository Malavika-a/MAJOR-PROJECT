from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('approved', 'Approved'),
    ('pending', 'Pending'),
)

# Create your models here.
class RegisteredStudent(models.Model):
    user_id=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    # email=models.ForeignKey(User,on_delete=models.CASCADE,unique=True)
    usertype = models.CharField(max_length=20, default='Student')
    phone = models.BigIntegerField()
    status = models.CharField(max_length=15, default='pending', choices=STATUS_CHOICES)





# class Login(models.Model):
#     email = models.EmailField(max_length=254, unique=False)
#     password = models.CharField(max_length=150)
#     Utype = models.CharField(max_length=20)
#     last_login = models.DateTimeField(auto_now=True)




class RegisteredInstructor(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    usertype = models.CharField(max_length=20, default='Instructor')

    phone = models.BigIntegerField()

    cv = models.FileField(upload_to="file")
    certificate = models.FileField(upload_to="file")

    status = models.CharField(max_length=15, default='pending', choices=STATUS_CHOICES)




class Course(models.Model):

    coursename = models.CharField(max_length=50,default='')
    startdate = models.DateField()
    duration = models.CharField(max_length=50,null=True)
    amount = models.IntegerField()
    instructor = models.ForeignKey(RegisteredInstructor,blank=True, null=True,on_delete=models.CASCADE)
    course_status=models.CharField(max_length=15,default='')
    def __str__(self):
        return self.coursename


class Feedback(models.Model):
    coursename= models.ForeignKey(Course,blank=True, null=True,on_delete=models.CASCADE)
    email = models.EmailField()
    feedback = models.TextField()
    feedbackdate = models.DateField(auto_now_add=True)
    course_name= models.CharField(max_length=40,blank=True, null=True)
