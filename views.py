from datetime import date

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.utils.text import slugify
from hashlib import sha256

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import VideoForm
from .models import RegisteredStudent, RegisteredInstructor, Feedback, Videos, Courses, Course_purchase, \
    Category, Cart, Product  # Login
from .tokens import generate_token
from django.core.paginator import Paginator, EmptyPage,InvalidPage


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
            return redirect('yogaapp:studentregistration')
        else:
            data=User.objects.create_user(username=email,password=password)
            std=RegisteredStudent(user_id=data,phone=phone,first_name=firstname,last_name=lastname,email=email)
            data.is_active=False
            data.save()
            std.save()
            messages.info(request, "We have sent you a mail ,please confirm your mail id")
          # Welcome mail

            subject='Welcome Message'
            message=f'Hi {firstname} , \nWelcome to yogastudio.\n We have sent you a confirmation mail please confirm it.'
            from_mail=settings.EMAIL_HOST_USER
            to_list=[data.username]
            send_mail(subject, message, from_mail, to_list, fail_silently=True)


            # Confirmation mail

            current_site = get_current_site(request)
            email_subject = "Yogastudio Confirmation mail"
            message2 = render_to_string('email_confirmation.html', {

                'name': std.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(data.pk)),
                'token': generate_token.make_token(data)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [data.username],
            )
            email.fail_silently = True
            email.send()




            return redirect('yogaapp:login')

    return render(request, 'student_register.html')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        data = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        data = None

    if data is not None and generate_token.check_token(data,token):
        data.is_active = True


        data.save()

        messages.success(request, "Your Account has been activated!!")
        return redirect('yogaapp:login')
    else:
        return render(request,'activation_failed.html')




def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=authenticate(username=email,password=password)
        if user is not None:
            if user.is_active==True:
                login(request,user)
                if RegisteredStudent.objects.filter(user_id=request.user.id).exists():
                    return redirect("yogaapp:studentdashboard")
                    # return HttpResponse("Student login")
                elif RegisteredInstructor.objects.filter(user_id=request.user.id).exists():
                    # return HttpResponse("Instructor login")
                    return redirect("yogaapp:instructordashboard")
                else:
                    messages.info("Please contact admin")
                    return redirect('yogaapp:login')
            else:
                messages.info("Please confirm your email id")

        else:
            messages.info(request,"Invalid credentials")
            return redirect('yogaapp:login')

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect("yogaapp:login")

def Passwdemail(request):
    if request.method=="POST":
        email=request.POST['email']
        user=User.objects.get(username=email)
        std=RegisteredStudent.objects.get(user_id=user.id)
        current_site = get_current_site(request)
        email_subject = "Yogastudio Confirmation mail"
        message2 = render_to_string('password_reset.html', {

            'name': std.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.username],
        )
        email.fail_silently = True
        email.send()
        messages.info(request,"We have sent you a confirmation mail please confirm your email")

        return redirect("yogaapp:passwd_email")
    return render(request,"Passwdemail.html")

def forgotpassword(request,uidb64):
    if request.method == "POST":
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        print(uid)
        password = request.POST['new_password']
        cpassword = request.POST['con_password']
        if password == cpassword:
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successful')
            return redirect("yogaapp:login")

        else:
            messages.error(request,'Password Mismatch')
    return render(request, 'forgotpassword.html')

def Password_reset(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        data = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        data = None

    if data is not None and generate_token.check_token(data,token):
        return redirect('yogaapp:forgotpassword',uidb64)
    else:
        return render(request,'activation_failed.html')



@login_required
def studentdashboard(request,c_slug=None,v_slug=None):
    std=RegisteredStudent.objects.get(user_id=request.user.id)
    print(std.first_name)
    c_videos = None
    video_key=None
    if c_slug!=None:
        course=get_object_or_404(Courses,slug=c_slug)
        print(course.pk)
        videos=Videos.objects.filter(course_id=course.pk)

        paginator=Paginator(videos,2)     # 10 videos per page
        try:
            page=int(request.GET.get('page','1'))
        except:
            page=1
        try:
            videos=paginator.page(page)
        except (EmptyPage,InvalidPage):
            videos=paginator.page(paginator.num_pages)
        if v_slug and c_slug!=None:
            video = get_object_or_404(Videos, slug=v_slug)
            print(video.course_id)
            return render(request, 'studentdashboard.html',{"c_videos":videos,"video_key": video,"std":std})

        return render(request, 'studentdashboard.html',{"c_videos":videos,"std":std})

    else:
        id=request.user.id
        courses=Courses.objects.all()
        std=RegisteredStudent.objects.get(user_id=id)
        return render(request,'studentdashboard.html',{'std':std,'courses':courses})


def studentviewprofile(request):
    user= RegisteredStudent.objects.get(user_id=request.user.id)
    return render(request, 'studentviewprofile.html', {'user': user})



def studentupdate(request):
        user=User.objects.get(id=request.user.id)
        std = RegisteredStudent.objects.get(user_id=request.user.id)
        if request.method == "POST":
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            phone = request.POST['phone']
            # new_email = request.POST['email']

            std.firstname = firstname
            std.lastname = lastname
            std.phone = phone
            std.save()
            messages.success(request, 'Profile updated successfully')
            return redirect("yogaapp:studentviewprofile")
            # std.email = new_email
            # if new_email==user.username:
            #     std.save()
            # else:
            #     current_site = get_current_site(request)
            #     email_subject = "Email Update Confirmation mail."
            #     message2 = render_to_string('email_confirmation.html', {
            #
            #         'name': std.first_name,
            #         'domain': current_site.domain,
            #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #         'token': generate_token.make_token(user)
            #     })
            #     email = EmailMessage(
            #         email_subject,
            #         message2,
            #         settings.EMAIL_HOST_USER,
            #         [new_email],
            #     )
            #     email.fail_silently = True
            #     email.send()
            #
            # messages.success(request, 'Please confirm your updated email')
        return render(request,'studentupdate.html', {'std': std})



def studentchangepassword(request):

        if request.method=="POST":
            old_password = request.POST.get('passwd', False)
            user=authenticate(username=request.user.username,password=old_password)
            if user!=None:
                new_password = request.POST['new_password']
                confirm_password = request.POST['confirm_password']
                if new_password == confirm_password:
                    data = User.objects.get(id=request.user.id)
                    data.set_password(new_password)
                    data.save()
                    messages.success(request,'Password Changed Successfully')
                    return redirect("yogaapp:login")
                else:
                    messages.error(request,'Password Mismatch')
            else:
                messages.error(request,'Old Password Not Matching')
        return render(request, 'studentchangepassword.html')



def coursesenrolled(request):
    c = Course_purchase.objects.filter(user_id=request.user.id).values_list('course_id',flat=True)
    print(list(c))
    courses=Courses.objects.filter(id__in=c)
    return render(request, 'coursesenrolled.html', { 'c': courses})




def availablecourses(request):
    user = RegisteredStudent.objects.get(user_id=request.user.id)
    c = Courses.objects.all()
    return render(request, 'availablecourses.html', {'c': c, 'user': user})





def Course_endroll(request,c_slug):
    user = RegisteredStudent.objects.filter(user_id=request.user.id)
    c = Courses.objects.get(slug=c_slug)
    endroll=Course_purchase(course_id=c.id,user_id=request.user.id,end_date=c.end_date)
    endroll.save()
    return redirect("yogaapp:coursesenrolled")


def feedback(request):

    c = Course_purchase.objects.filter(user_id=request.user.id).values_list('course_id',flat=True)
    print(list(c))
    courses=Courses.objects.filter(id__in=c)
    if request.method == "POST":
        feedback= request.POST['feedback']
        course = request.POST['course']
        selected_course=Courses.objects.get(id=course)
        f = Feedback(user_id=request.user.id,feedback=feedback,course=selected_course)
        f.save()
    return render(request, 'feedback.html',{"c":courses})


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
        # password2 = request.POST.get('password2')
        # passwords=sha256(password2.encode()).hexdigest()

        if User.objects.filter(username=email).exists():
            messages.info(request, "Email already Exist...!")
            return redirect('yogaapp:insrtructorregistration')
        else:
            user=User.objects.create_user(username=email,password=password)
            inst=RegisteredInstructor(user_id=user,first_name=firstname,last_name=lastname, phone=phone,cv=cv, certificate=certificate,email=email)
            user.save()
            inst.save()

            # Welcome mail

            subject = 'Welcome Message'
            message = f'Hi {firstname} , \nWelcome to yogastudio.'
            from_mail = settings.EMAIL_HOST_USER
            to_list = [user.username]
            send_mail(subject, message, from_mail, to_list, fail_silently=True)

            # Confirmation mail

            current_site = get_current_site(request)
            email_subject = "Yogastudio Confirmation mail"
            message2 = render_to_string('email_confirmation.html', {

                'name': inst.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [user.username],
            )
            email.fail_silently = True
            email.send()



            return redirect('yogaapp:login')
    return render(request, 'register.html')


def instructordashboard(request):
        ins = RegisteredInstructor.objects.get(user_id=request.user.id)
        return render(request, 'instructordashboard.html', {'ins': ins})



def instructorviewprofile(request):
        ins = RegisteredInstructor.objects.get(user_id=request.user.id)
        return render(request, 'instructorviewprofile.html', {'ins': ins})



def instructorchangepassword(request):
        if request.method == "POST":
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if new_password == confirm_password:
                user=authenticate(username=request.user.username,password=old_password)
                if user!=None:
                    data = User.objects.get(username=user)
                    data.set_password(new_password)
                    data.save()
                    messages.info(request,"Password updated successfully")
                    return redirect("yogaapp:instructordashboard")
            else:
                messages.info(request, "Invalid password")

        return render(request, 'instructorchangepwd.html')

# Allotted Students

def instructorallotedstudents(request):

        ins = RegisteredInstructor.objects.get(user_id=request.user.id)
        c = Courses.objects.get(user_id_id=request.user.id)
        purchase_stds=Course_purchase.objects.filter(course_id=c.id).values_list('user_id',flat=True)
        std=RegisteredStudent.objects.filter(user_id__in=purchase_stds)
        print(list(std))
        return render(request, 'instructorassignedstudents.html',{'course':c,'std':std})


def instructorviewfeedback(request):
        ins = RegisteredInstructor.objects.filter(user_id=request.user.id)
        course=Courses.objects.get(user_id=request.user.id)
        feed = Feedback.objects.filter(course_id=course.id)
        std_ids=feed.values_list("user_id",flat=True)
        std=RegisteredStudent.objects.filter(user_id__in=std_ids)
        std_feed=zip(feed,std)
        return render(request, 'instructorviewfeedback.html', {'ins': ins, 'std_feed': std_feed})



def instructorupdate(request):
        data = User.objects.get(id=request.user.id)
        ins = RegisteredInstructor.objects.get(user_id=request.user.id)
        if request.method == "POST":
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            phone = request.POST['phone']
            ins.first_name = firstname
            ins.last_name = lastname
            ins.phone = phone
            ins.save()
            messages.success(request,"Profile update successfully")
            return redirect("yogaapp:instructorviewprofile")
        return render(request, 'instructorupdate.html', {'ins': ins})



def AddVideo(request):
    form=VideoForm()
    if request.method=='POST':
        form=VideoForm(request.POST,request.FILES)
        if form.is_valid():
            title=form.cleaned_data['title']
            course=form.cleaned_data['course']
            video=form.cleaned_data['video']
            Videos(title=title,slug=slugify(title),course=course,video=video).save()
            return redirect("yogaapp:instructordashboard")
    return render(request,"Add_Video.html",{"form":form})

def Course_cancel(request,course_id):
    course=get_object_or_404(Course_purchase,course_id=course_id,user_id=request.user.id)
    course.delete()
    return redirect("yogaapp:coursesenrolled")


def product(request):
    category = Category.objects.all()
    product = Product.objects.all()


    return render(request, 'products.html',{'data':category,'product':product})

def singleproduct(request,id):
    prod = Product.objects.filter(id=id)
    return render(request, 'singleproduct.html',{'prod':prod})



@login_required(login_url='login')
def addcart(request,id):
      user = request.user.id
      item=Product.objects.get(id=id)
      if item.stock>0:
            if Cart.objects.filter(user_id=user,product_id=item).exists():
                  messages.success(request, 'Product Already in the cart ')
                  return redirect("yogaapp:product")
            else:
                  product_qty=1
                  price=item.price * product_qty

                  new_cart=Cart(user_id=user,product_id=item.id,product_qty=product_qty,price=price)
                  new_cart.save()
                  messages.success(request, 'Product added to the Cart ')
                  return redirect("yogaapp:product")
                  # return render(request,'product.html')



# Cart Quentity Plus Settings
def plusqty(request,id):
    cart=Cart.objects.filter(id=id)
    for cart in cart:
        if cart.product.stock > cart.product_qty:
            cart.product_qty +=1
            cart.price=cart.product_qty * cart.product.price
            cart.save()
            return redirect("yogaapp:cart")
        # messages.success(request, 'Out of Stock')
        return redirect("yogaapp:cart")

# Cart Quentity minus Settings
def minusqty(request,id):
    cart=Cart.objects.filter(id=id)
    for cart in cart:
        if cart.product_qty > 1 :
            cart.product_qty -=1
            cart.price=cart.product_qty * cart.product.price
            cart.save()
            return redirect("yogaapp:cart")
        return redirect("yogaapp:cart")



# View Cart Page
@login_required(login_url='login')
def cart(request):
    user = request.user.id
    cart=Cart.objects.filter(user_id=user)
    totalitem=0
    total=0
    for i in cart:
        total += i.product.price * i.product_qty
        totalitem = len(cart)

    category=Category.objects.all()
    # subcategory=Subcategory.objects.all()
    return render(request,'addtocart.html',{'cart':cart,'total':total,'category':category,'totalitem':totalitem})

# Remove Items From Cart
def de_cart(request,id):
    Cart.objects.get(id=id).delete()
    return redirect("yogaapp:cart")
