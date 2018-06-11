import datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

from blog.models import Blog
from read_statistics.utils import get_seven_days_date, get_today_hot_data, get_yesterday_hot_data
from .forms import LoginForm, RegForm


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_date(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    # gain the hot blogs' data in seven days
    for_7_days_hot_data = cache.get('for_7_days_hot_data')
    if for_7_days_hot_data is None:
        for_7_days_hot_data = get_seven_days_hot_blogs()
        cache.set('for_7_days_hot_data', for_7_days_hot_data, 3600)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['for_7_days_hot_data'] = for_7_days_hot_data
    return render(request, 'home.html', context)



def get_seven_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gt=date). \
        values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs


def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            # 创建用户
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            password_again = reg_form.cleaned_data['password_again']
            user = User.objects.create_user(username, email, password)
            user.save()
            #登陆用户
            #user = auth.authenticate(user=user, password=password)
            print(user)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
