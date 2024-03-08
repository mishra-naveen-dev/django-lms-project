
from django.contrib import admin
from django.urls import path,include
from .import views,user_login
from django.conf import settings
from django.conf.urls.static import static
# from .views import home, toggle_theme


urlpatterns = [
    path('admin/', admin.site.urls),
    
    

    path('base', views.BASE, name='base'),

    path('', views.HOME, name='home'),
      
    path('courses', views.SINGLE_COURSE, name='single_cousre'),
    path('product/filter_course',views.filter_course,name="filter_course"),
    path('contact',views.CONTACT_US,name='contact_us'),
    path('about',views.ABOUT_US,name='about_us'),

    path('accounts/register', user_login.REGISTER, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin',user_login.Do_LOGIN,name='doLogin'),
    path('accounts/profile', user_login.PROFILE,name='profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
