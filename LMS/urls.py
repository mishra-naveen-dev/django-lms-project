
from django.contrib import admin
from django.urls import path,include
from .import views,user_login
from django.conf import settings
from django.conf.urls.static import static
# from .views import home, toggle_theme


urlpatterns = [
    path('admin/', admin.site.urls),
    
    

    path('base', views.BASE, name='base'),
    path('404', views.PAGE_NOT_FOUND, name='404'),

    path('', views.HOME, name='home'),
      
    path('courses', views.SINGLE_COURSE, name='single_cousre'),
    path('courses/filter_course',views.filter_course,name="filter_course"),
    path('courses/<int:course_id>',views.COURSE_DETAILS,name="course_details"),

    path('contact',views.CONTACT_US,name='contact_us'),
    path('about',views.ABOUT_US,name='about_us'),
    path('search', views.SEARCH_COURSE, name='search_cousre'),
    path('accounts/register', user_login.REGISTER, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin',user_login.Do_LOGIN,name='doLogin'),
    path('accounts/profile', user_login.PROFILE,name='profile'),
    path('checkout/<int:course_id>',views.CHECKOUT,name='checkout'),
    path('my-course',views.MY_COURSE,name='my_course'),
    # path('verify_payment',views.VERIFY_PAYMENT,name='verify_payment'),
    path('course/watch-course/<int:course_id>',views.WATCH_COURSE,name='watch_course'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
