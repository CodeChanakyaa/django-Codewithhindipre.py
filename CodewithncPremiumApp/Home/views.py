import stripe
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail


def goHome(request):
    data = {
        'title': 'Home Page',
        'courses': CourseModel.objects.all().order_by('-id')[0:4],
    }
    return render(request, 'index.html', data)


def goAbout(request):
    data = {
        'title': 'About Page',
    }
    return render(request, 'about.html', data)


@login_required(redirect_field_name='next', login_url='/userlogin/')
def goCourses(request):
    AllCourses = CourseModel.objects.all()
    if request.method == 'GET':
        search_topic = request.GET.get('search')

        if search_topic != None:
            AllCourses = CourseModel.objects.filter(
                course_name__contains=search_topic)

    data = {
        'title': 'Courses Page',
        'courses': AllCourses,
    }
    return render(request, 'courses.html', data)


@login_required(redirect_field_name='next', login_url='/userlogin/')
def goCourseModules(request, slug):
    course = CourseModel.objects.get(slug=slug)

    data = {
        'title': 'Course Page',
        'course': course,
        'modules': CourseModulesModel.objects.filter(course=course),
    }
    return render(request, 'coursemodules.html', data)


@login_required(login_url='/userlogin/')
def goModule(request, slug):
    data = {
        'title': 'Course Module',
        'module': CourseModulesModel.objects.get(course_module_slug=slug),
    }
    return render(request, 'module.html', data)


@login_required(login_url='/userlogin/')
def goContact(request):
    Message = ""
    try:
        if request.method == 'POST':

            if request.POST.get('name') == "" or request.POST.get('email') == "" or request.POST.get('subject') == "" or request.POST.get('message') == "":
                error = True
                return render(request, 'contact.html', {'title': 'Contact Page', 'error': error})

            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            form = ContactModel(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            form.save()
            Message = 'Message Submitted Successfully'

            # email sending to user
            subject = 'CodeWithNc Contact Submition Auto Reply'
            message_to = f'Dear {name},\n\nIts just a mail to inform you that your message is recieved, no need to reply'
            email_from = settings.EMAIL_HOST_USER
            email_to = [email]

            send_mail(subject, message_to, email_from,
                      email_to, fail_silently=False)

            # email sending to perticuler
            subject_specific = 'CodeWithNc New Contact Submission'
            message_specific = f'CodeWithNc, \n\nIts just a mail to inform you that new message received from {name}, with \n\nEmail : {email} \n\nMessage : {message}'
            email_to_specific = ['apps24adda@gmail.com',]

            send_mail(subject_specific, message_specific, email_from,
                      email_to_specific, fail_silently=False)

    except Exception as e:
        print(e)

    data = {
        'title': 'Contact Page',
        'message': Message,
    }
    return render(request, 'contact.html', data)


def goUser(request):
    message = ""
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            if request.POST.get('email') == "" or request.POST.get('password') == "":
                error = True
                return render(request, 'user.html', {'title': 'Login Page', 'error': error})

            user_obj = User.objects.filter(username=email).first()
            if user_obj is None:
                message = ("Email not registered")
                return render(request, 'user.html', {'title': 'Login Page', 'message': message})

            user_obj = authenticate(request, username=email, password=password)

            if user_obj is not None:
                login(request, user_obj)
                next = request.GET.get('next')
                if next is not None:
                    return redirect(next)
                else:
                    return redirect(request.path_info)
            else:
                message = "Incorrect Password"

    except Exception as e:
        print(e)

    data = {
        'title': 'User Page',
        'message': message,
    }
    return render(request, 'user.html', data)


@login_required(login_url='/userlogin/')
def goLogout(request):
    logout(request)
    return redirect('/')


def goSignup(request):
    message = ""
    try:
        if request.method == 'POST':
            first_name = request.POST.get('userfirstname')
            last_name = request.POST.get('userlastname')
            email = request.POST.get('useremail')
            password = request.POST.get('userpassword')

            if request.POST.get('userfirstname') == "" or request.POST.get('userlastname') == "" or request.POST.get('useremail') == "" or request.POST.get('userpassword') == "":
                error = True
                return render(request, 'signup.html', {'title': 'Signup Page', 'error': error})

            user_obj = User.objects.filter(username=email).first()

            if user_obj:
                message = ("Email Already Exists")
                return render(request, 'signup.html', {'title': 'Signup Page', 'message': message})

            user_obj = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user_obj.set_password(password)
            user_obj.save()
            message = "Account successfully created"

            # profile creation with free membership
            profile = ProfileModel(user=user_obj)
            profile.save()

    except Exception as e:
        print(e)

    data = {
        'title': 'Signup Page',
        'message': message,
    }
    return render(request, 'signup.html', data)


stripe.api_key = settings.STRIPE_SECURE_KEY


@login_required(login_url='/userlogin/')
def checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Premium',
                },
                'unit_amount': 55900,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'http://localhost:8000/premium?response={settings.PAYMENT_RESPONSE}',
        cancel_url='http://localhost:8000/premium/',
    )
    return redirect(session.url, code=303)


@login_required(login_url='/userlogin/')
def goPremium(request):
    try:
        if request.GET.get('response') == 'True':
            profile = ProfileModel.objects.filter(user = request.user).first()
            profile.is_pro = True
            profile.subscription_type = 'Premium'
            profile.save()
            return redirect('/premium/')

    except Exception as e:
        print(e)

    data = {
        'title': 'Subscription Page',
    }
    return render(request, 'premium.html', data)


def goBlogs(request):
    AllBlogs = BlogModel.objects.all()
    if request.method == 'GET':
        search = request.GET.get('search')

        if search != None:
            AllBlogs = BlogModel.objects.filter(blog_name__contains=search)

    data = {
        'title': 'Blogs Page',
        'blogs': AllBlogs,
    }
    return render(request, 'blog.html', data)


def blogDetail(request, slug):
    data = {
        'title': 'Blog Page',
        'blog': BlogModel.objects.get(slug=slug),
    }
    return render(request, 'blogdetail.html', data)
