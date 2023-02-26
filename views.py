from datetime import date
from hashlib import sha256
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import RegisteredStudent, Course, RegisteredInstructor, Feedback # Login


# Create your views here.



def index(request):
    return render(request, "index.html")


def Studentregistration(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already Exist...!")
            return redirect('studentregistration')
        else:
            data=User.objects.create_user(username=email,first_name=firstname,last_name=lastname,email=email,password=password)
            std=RegisteredStudent(user_id=data,phone=phone)
            data.save()
            std.save()
            return redirect('login')

    return render(request, 'student_register.html')


def Login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=authenticate(username=email,password=password)
        if user is not None:
            login(request,user)
            if RegisteredStudent.objects.filter(user_id=request.user.id).exists():
                return redirect("studentdashboard")
        else:
            messages.info(request,"Invalid credentials")
            return redirect('login')
    #
    #         for i in log:
    #             Utype = i.usertype
    #             request.session.flush()
    #             request.session['usr'] = i.id
    #             print(3)
    #
    #         if Utype == 'Student':
    #             print(4)
    #             return redirect('studentdashboard')
    #
    #         else:
    #             messages.success(request, 'Access Denied!!!')
    #             return redirect('login')
    #
    #     elif (RegisteredInstructor.objects.filter(email=email, password=passw)):
    #         log = RegisteredInstructor.objects.filter(email=email, password=passw)
    #         for i in log:
    #             Utype = i.usertype
    #             request.session.flush()
    #             request.session['usr'] = i.id
    #
    #         if Utype == 'Instructor':
    #             return redirect('instructordashboard')
    #         else:
    #             messages.success(request, 'Access Denied!!!')
    #             return redirect('login')

    return render(request, 'login.html')

def logout(request):
    if 'usr' in request.session:
        request.session.flush()
    return redirect("login")


def forgotpassword(request):
    # if request.method == "POST":
    #     email = request.POST['email']
    #     data = Login.objects.get(email=email)
    #     if data:
    #         password = request.POST['new_password']
    #         cpassword = request.POST['con_password']
    #         if password == cpassword:
    #             data.password = password
    #             data.save()
    #             messages.success(request,'Password Reset Successful')
    #
    #         else:
    #             messages.error(request,'Password Mismatch')
    return render(request, 'forgotpassword.html')




def studentdashboard(request):
    # if 'usr' in request.session:
    #     id=request.session['usr']
    #     user=RegisteredStudent.objects.filter(id=id)
    #     return render(request,'studentdashboard.html',{'user':user})
    return redirect(login)

def studentviewprofile(request):
    # if 'usr' in request.session:
    #     id=request.session['usr']
    #     user = RegisteredStudent.objects.filter(id=id)
    #     v = RegisteredStudent.objects.filter(id=id)
    #     return render(request, 'studentviewprofile.html', {'user': user,'v': v})
    return redirect(login)


def studentupdate(request):
    # if 'usr' in request.session:
    #     id=request.session['usr']
    #     user = RegisteredStudent.objects.filter(id=id)
    #     data = RegisteredStudent.objects.get(id=id)
    #     if request.method == "POST":
    #         firstname = request.POST['firstname']
    #         lastname = request.POST['lastname']
    #         phone = request.POST['phone']
    #         email = request.POST['email']
    #         data.firstname = firstname
    #         data.lastname = lastname
    #         data.phone = phone
    #         data.email = email
    #         data.save()
    #         messages.success(request, 'Updated successfully')

        # return render(request, 'studentupdate.html', {'user': user})
    # return redirect(login)
    pass

def studentchangepassword(request):
    # if 'usr' in request.session:
    #     id=request.session['usr']
    #     user = RegisteredStudent.objects.filter(id=id)
    #     if request.method == "POST":
    #         old_password = request.POST['password']
    #         if Login.objects.filter(password=old_password):
    #             new_password = request.POST['new_password']
    #             confirm_password = request.POST['confirm_password']
    #             if new_password == confirm_password:
    #                 data = Login.objects.get(id=id)
    #                 data.password = new_password
    #                 data.save()
    #                 messages.success(request,'Password Changed Successfully')
    #             else:
    #                 messages.error(request,'Password Mismatch')
    #
    #         else:
    #             messages.error(request,'Old Password Not Matching')
    #     return render(request, 'studentchangepassword.html', {'user': user})
    return redirect(login)


def coursesenrolled(request, id):
    # if 'usr' in request.session:
    #     user = RegisteredStudent.objects.filter(id=id)
    #     c = Course.objects.filter(course_status='enrolled')
    #     return render(request, 'coursesenrolled.html', {'user': user, 'c': c})
    return redirect(login)


def availablecourses(request, id):
    # if 'usr' in request.session:
    #     user = RegisteredStudent.objects.filter(id=id)
    #     c = Course.objects.all()
    #     return render(request, 'availablecourses.html', {'c': c, 'user': user})
    return redirect(login)



def viewenrolledcourses(request, id):
    # user = RegisteredStudent.objects.filter(id=id)
    # c = Course.objects.filter(course_status='enrolled')
    # r = Course.objects.get(id=id)
    # r.course_status = 'enrolled'
    # r.save()
    # print("enrolled")
    # return render(request, 'coursesenrolled.html', {'user': user, 'c': c})
    pass




def feedback(request):
    # if 'usr' in request.session:
    #     id=request.session['usr']
    #     user = RegisteredStudent.objects.filter(id=id)
    #     c = Course.objects.all()
    #     if request.method == "POST":
    #         email = request.POST['email']
    #         feedback1 = request.POST['feedback']
    #         course = request.POST['course']
    #         f = Feedback()
    #         f.email = email
    #         f.feedback = feedback1
    #         f.feeddate = date.today()
    #         f.course_name = course
    #         f.save()
    #
    #     return render(request, 'feedback.html', {'user': user, 'c': c})
    return redirect(login)

# def searchbar(request):
#     if request.method == 'GET':
#         query = request.GET.get('query')
#         if query:
#             multiple_q = Q(Q(coursename__icontains=query) | Q(amount__icontains=query))
#             user1 = Course.objects.filter(multiple_q)
#             return render(request, 'searchbar.html', {'user':user1})
#         else:
#             messages.info(request, 'No search result!!!')
#             print("No information to show")
#     return render(request, 'searchbar.html', {})













def insrtructorregistration(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        cv=request.FILES.get('cv')
        certificate=request.FILES.get('certificate')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        passwords=sha256(password2.encode()).hexdigest()

        if RegisteredInstructor.objects.filter(email=email).exists():
            messages.success(request, "Email already Exist...!")
            return redirect('instructordashboard')
        else:
            RegisteredInstructor(firstname=firstname,lastname=lastname, phone=phone, email=email,cv=cv, certificate=certificate, password=passwords).save()
            l = Login(email=email, password=passwords)
            l.Utype = 'instructor'
            l.save()
            print('success')
            messages.success(request, "registered successfully")
            return redirect('login')

    return render(request, 'register.html')


def instructordashboard(request):
    if 'usr' in request.session:
        id=request.session['usr']
        ins = RegisteredInstructor.objects.filter(id=id)
        return render(request, 'instructordashboard.html', {'ins': ins})
    return redirect(login)


def instructorviewprofile(request):
    if 'usr' in request.session:
        id=request.session['usr']
        ins = RegisteredInstructor.objects.filter(id=id)
        return render(request, 'instructorviewprofile.html', {'ins': ins})
    return redirect(login)


def instructorchangepassword(request):
    if 'usr' in request.session:
        id=request.session['usr']
        ins = RegisteredInstructor.objects.filter(id=id)
        if request.method == "POST":
            old_password = request.POST['old_password']
            if Login.objects.filter(password=old_password):
                new_password = request.POST['new_password']
                confirm_password = request.POST['confirm_password']
                if new_password == confirm_password:
                    data = Login.objects.get(id=id)
                    data.password = new_password
                    data.save()
        return render(request, 'instructorchangepwd.html', {'ins': ins})
    return redirect(login)

def instructorallotedcourses(request):
    if 'usr' in request.session:
        id=request.session['usr']
        ins = RegisteredInstructor.objects.filter(id=id)
        c = Course.objects.filter(instructor_id=id)
        return render(request, 'instructorassignedcourses.html', {'ins': ins, 'c': c})
    return redirect(login)

def instructorviewfeedback(request):
    if 'usr' in request.session:
        id=request.session['usr']
        ins = RegisteredInstructor.objects.filter(id=id)
        feed = Feedback.objects.all()
        return render(request, 'instructorviewfeedback.html', {'ins': ins, 'feed': feed})

    return redirect(login)

def instructorupdate(request):
    if 'usr' in request.session:
        id=request.session['usr']
        ins = RegisteredInstructor.objects.filter(id=id)
        data = RegisteredInstructor.objects.get(id=id)
        if request.method == "POST":
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            phone = request.POST['phone']
            email = request.POST['email']
            data.firstname = firstname
            data.lastname = lastname
            data.phone = phone
            data.email = email
            data.save()


        return render(request, 'instructorupdate.html', {'ins': ins})

    return redirect(login)
    #
    #
    #
    #
    #
    #
    #
    # if 'usr' in request.session:
    #     id=request.session['usr']
    #
    # return redirect(login)
    #
    #
    #
    #
    #
    # if 'usr' in request.session:
    #     id=request.session['usr']
    #
    # return redirect(login)