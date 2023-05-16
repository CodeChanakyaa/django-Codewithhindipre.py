from django.urls import path
from .views import *

urlpatterns = [
    path('', goHome, name="goHome"),

    path('about/', goAbout, name="goAbout"),
    
    path('courses/', goCourses, name="goCourses"),
    
    path('coursemodules/<slug>', goCourseModules, name="goCourseModules"),
    
    path('coursemodule/<slug>', goModule, name="goModule"),
    
    path('contact/', goContact, name="goContact"),
    
    path('userlogin/', goUser, name="goUser"),
    
    path('userlogout/', goLogout, name="goLogout"),
    
    path('signup/', goSignup, name="goSignup"),
 
    path('premium/', goPremium, name="goPremium"),

    path('blogs/', goBlogs, name="goBlogs"),

    path('blog/<slug>', blogDetail, name="blogDetail"),

    path('create-checkout-session/', checkout_session, name="checkout_session"),

]