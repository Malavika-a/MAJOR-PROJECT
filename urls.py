from django.urls import path
from . import views
from django.contrib import admin
urlpatterns = [
    path('', views.index, name='index'),
    path('studentregistration', views.Studentregistration, name='studentregistration'),
    path('insrtructorregistration', views.insrtructorregistration, name='insrtructorregistration'),
    path('login', views.Login, name='login'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('studentdashboard', views.studentdashboard, name='studentdashboard'),
    path('logout', views.logout, name='logout'),
    path('studentviewprofile', views.studentviewprofile, name='studentviewprofile'),
    path('studentupdate', views.studentupdate, name='studentupdate'),
    path('studentchangepassword', views.studentchangepassword, name='studentchangepassword'),
    path('coursesenrolled/<id>', views.coursesenrolled, name='coursesenrolled'),
    path('availablecourses/<id>', views.availablecourses, name='availablecourses'),
    path('viewenrolledcourses/<id>', views.viewenrolledcourses, name='viewenrolledcourses'),
    path('feedback', views.feedback, name='feedback'),
    # path('searchbar', views.searchbar, name='searchbar'),

    path('instructordashboard', views.instructordashboard, name='instructordashboard'),
    path('instructorviewprofile', views.instructorviewprofile, name='instructorviewprofile'),
    path('instructorchangepassword', views.instructorchangepassword, name='instructorchangepassword'),
    path('instructorallotedcourses', views.instructorallotedcourses, name='instructorallotedcourses'),
    path('instructorviewfeedback', views.instructorviewfeedback, name='instructorviewfeedback'),
    path('instructorupdate', views.instructorupdate, name='instructorupdate'),

]