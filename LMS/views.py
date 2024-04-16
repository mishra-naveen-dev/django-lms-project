from django.shortcuts import get_object_or_404, redirect,render
from app.models import Categories,Course,Level,Video,UserCourse,Payment,CourseResource,Categoriestheory
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum

from .settings import *
# import razorpay
from time import time

# client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    category=Categories.objects.all().order_by('id')[0:6]
    theory=Categoriestheory.objects.all().order_by('id')[0:6]
    course=Course.objects.filter(status='PUBLISH').order_by('-id')
    courser=CourseResource.get_all_category(CourseResource)
    # print(course)
    context={
        'category':category,
        'course':course,
        'theory':theory,
        'courser':courser, # type: ignore
    }
    return render(request,'Main/home.html',context)

def SINGLE_COURSE(request):
    category=Categories.get_all_category(Categories) # type: ignore
    # theory=Theory.get_all_category(Theory)
    level=Level.objects.all()
    course = Course.objects.all()
    FeeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context={
        'category':category,
        # 'theory':theory,
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
    # tcourse = TheoryCourse.objects.filter(title__icontains = query)
    category=Categories.get_all_category(Categories)
   
    context = {
        'course':course,
        'category':category,
        # 'tcourse ':tcourse ,
    }
    return render(request,'search/search.html',context)

def COURSE_DETAILS(request, course_id):
  
    category=Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__id=course_id).aggregate(sum=Sum('time_duration'))

    course = Course.objects.filter(pk=course_id)

    check_enroll = None
    user  = request.user
    if user.is_authenticated:
        try:
            check_enroll = UserCourse.objects.get(
                user=request.user,course=course_id
            )
        except UserCourse.DoesNotExist:
            pass   

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
def CHECKOUT(request, course_id):
    course=Course.objects.get(pk=course_id)
    action=request.GET.get('action')
    order= None
    
    
    if course.price==0:
        usercourse=UserCourse(
            user=request.user,
            course=course
        )
        usercourse.save()
        messages.success(request,'Course has Suceessfully Enrolled !')
        return redirect('my_course')
    elif action == 'create_payment':
        if request.method == "POST":
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')   
            country=request.POST.get('country')
            address=request.POST.get('address')
            address_1=request.POST.get('address')
            city=request.POST.get('city')
            state=request.POST.get('state')
            postcode=request.POST.get('postcode')
            phone=request.POST.get('phone')
            email=request.POST.get('email')
            order_comments=request.POST.get('order_comments')

            amount = (course.price) * 100
            currency="INR"
            notes={
                "name":f'{first_name} {last_name}',
                "country":country,
                "address":f'{address} {address_1}',
                "city":city,
                "state":state,
                "postcode":postcode,
                "phone":phone,
                "email":email,
                "order_comments":order_comments,
            }
            receipt=f"Edu-{int(time())}"
            order=client.order.create({
                'receipt':receipt,
                'amount':amount,
                'currency':currency,
                'notes':notes,
                
            })

            payment =Payment(
                course=course,
                user=request.user,
                order_id=order.get('id')
            )
            payment.save()

    context={
           'course':course,
           'order':order,
    }
    
    return render(request,'checkout/checkout.html',context)


def MY_COURSE(request):
    course=UserCourse.objects.filter(user = request.user)

    context={
        'course':course,
    }
    return render(request,'course/my-course.html',context)
def WATCH_COURSE(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    lecture_number = request.GET.get("lecture", 1)
    video = Video.objects.get(course=course.id, serial_number=lecture_number)

    if video is None:
        return redirect('404')

    context={
        'course':course,
        'video':video,
        # 'lecture':lecture,
    }        
    return render(request, 'course/watch-course.html',context)
# def toggle_theme(request):
#     current_theme = request.session.get('theme', 'light-theme')
#     new_theme = 'dark-theme' if current_theme == 'light-theme' else 'light-theme'
#     request.session['theme'] = new_theme
#     return redirect('home')