from django.shortcuts import redirect,render
from app.models import Categories,Course,Level,Video,UserCourse
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    category=Categories.objects.all().order_by('id')[0:6]
    course=Course.objects.filter(status='PUBLISH').order_by('-id')
    print(course)
    context={
        'category':category,
        'course':course,
    }
    return render(request,'Main/home.html',context)

def SINGLE_COURSE(request):
    category=Categories.get_all_category(Categories) # type: ignore
    level=Level.objects.all()
    course = Course.objects.all()
    FeeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context={
        'category':category,
        'level':level,
        'course':course,
        'FeeCourse_count':FeeCourse_count,
        'PaidCourse_count':PaidCourse_count,
    }
    return render(request,'Main/single_course.html',context)

def filter_course(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
  
    # print(category)
    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif category:
        course= Course.objects.filter(category__id__in = category).order_by('-id')
    elif level:
          course = Course.objects.filter(level__id__in = level).order_by('-id')    
    else:
        course= Course.objects.all().order_by('-id')
    
    context ={
        'course':course
    }
    t = render_to_string('ajax/course.html',context)
    return JsonResponse({'data': t})

def CONTACT_US(request):
    category=Categories.get_all_category(Categories)

    context={
        'category':category,

    }
    return render(request,'Main/contact_us.html',context)

def ABOUT_US(request):
    category=Categories.get_all_category(Categories)

    context={
        'category':category,

    }
    return render(request,'Main/about_us.html',context)

def SEARCH_COURSE(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    category=Categories.get_all_category(Categories)
   
    context = {
        'course':course,
        'category':category,
    }
    return render(request,'search/search.html',context)

def COURSE_DETAILS(request,slug):
  
    category=Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))

    course_id=Course.objects.get(slug=slug)
    course = Course.objects.filter(slug=slug)

    try:
        check_enroll = UserCourse.objects.get(user=request.user,course=course_id)
    except UserCourse.DoesNotExist:
        check_enroll=None    


    if course.exists():
        course=course.first();
    else:
        return redirect('404')
    
    context={
        'course':course,
        'category':category,
        'time_duration':time_duration,
        'check_enroll':check_enroll,
    }
    return render(request,'course/course_details.html',context)

def PAGE_NOT_FOUND(request):
    category=Categories.get_all_category(Categories)
    context={
      
        'category':category,
    }
    return render(request,'error/404.html',context)    
def CHECKOUT(request,slug):
    course=Course.objects.get(slug=slug)
    
    
    if course.price==0:
        usercourse=UserCourse(
            user=request.user,
            course=course
        )
        usercourse.save()
        messages.success(request,'Course has Suceessfully Enrolled !')
        return redirect('my_course')
    return render(request,'checkout/checkout.html')


def MY_COURSE(request):
    course=UserCourse.objects.filter(user = request.user)

    context={
        'course':course,
    }
    return render(request,'course/my-course.html',context)
 
# def toggle_theme(request):
#     current_theme = request.session.get('theme', 'light-theme')
#     new_theme = 'dark-theme' if current_theme == 'light-theme' else 'light-theme'
#     request.session['theme'] = new_theme
#     return redirect('home')