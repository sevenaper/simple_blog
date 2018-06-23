import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Blog
from comment.forms import CommentForm
from comment.models import Comment
from .models import BlogType
from user.forms import RegForm,LoginForm

# Create your views here.
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, 10)  # 十个博客进行分页
    page_num = request.GET.get('page', 1)  # get请求获取页码
    page_of_blogs = paginator.get_page(page_num)
    current_page = page_of_blogs.number
    if paginator.num_pages == 1:
        page_range = [1]
    elif current_page == 1 or current_page == 2:
        if paginator.num_pages <= 5:
            page_range = list(range(1, paginator.num_pages))
        else:
            page_range = list([1, 2, 3, 4, 5])
    elif current_page == paginator.num_pages or current_page == paginator.num_pages - 1:
        if paginator.num_pages <= 5:
            page_range = list(range(1, paginator.num_pages))
        else:
            page_range = list([paginator.num_pages - 4, paginator.num_pages - 3, paginator.num_pages - 2,
                               paginator.num_pages - 1, paginator.num_pages])
    else:
        page_range = list(range(max(current_page - 1, 1), current_page)) + \
                     list(range(current_page, min(current_page + 1, paginator.num_pages) + 1))
    if page_range and page_range[0] >= 3:
        page_range.insert(0, '...')
    if page_range and paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range and page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range and page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates(
        'create_time', 'month', order='DESC')
    for_7_days_hot_data = cache.get('for_7_days_hot_data')
    if for_7_days_hot_data is None:
        for_7_days_hot_data = get_seven_days_date()
        cache.set('for_7_days_hot_data', for_7_days_hot_data, 3600)
    context['for_7_days_hot_data'] = for_7_days_hot_data
    return render(request, 'blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    context['login_form'] = LoginForm

    context['previous_blog'] = Blog.objects.filter(
        create_time__gt=get_object_or_404(Blog, pk=blog_pk).create_time).last()
    context['next_blog'] = Blog.objects.filter(
        create_time__lt=get_object_or_404(Blog, pk=blog_pk).create_time).first()
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog_pk})
    response = render(request, 'blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_pk, 'true', max_age=300)
    return response


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list, 10)  # 十个博客进行分页
    page_num = request.GET.get('page', 1)  # get请求获取页码
    page_of_blogs = paginator.get_page(page_num)
    current_page = page_of_blogs.number
    if paginator.num_pages == 1:
        page_range = [1]
    elif current_page == 1 or current_page == 2:
        if paginator.num_pages <= 5:
            page_range = list(range(1, paginator.num_pages))
        else:
            page_range = list([1, 2, 3, 4, 5])
    elif current_page == paginator.num_pages or current_page == paginator.num_pages - 1:
        if paginator.num_pages <= 5:
            page_range = list(range(1, paginator.num_pages))
        else:
            page_range = list([paginator.num_pages - 4, paginator.num_pages - 3, paginator.num_pages - 2,
                               paginator.num_pages - 1, paginator.num_pages])
    else:
        page_range = list(range(max(current_page - 1, 1), current_page)) + \
                     list(range(current_page, min(current_page + 1, paginator.num_pages) + 1))
    if page_range and page_range[0] >= 3:
        page_range.insert(0, '...')
    if page_range and paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range and page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range and page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blog_dates'] = Blog.objects.dates(
        'create_time', 'month', order='DESC')
    context['blog_type'] = blog_type
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blogs_all_list'] = blogs_all_list

    for_7_days_hot_data = cache.get('for_7_days_hot_data')
    if for_7_days_hot_data is None:
        for_7_days_hot_data = get_seven_days_date()
        cache.set('for_7_days_hot_data', for_7_days_hot_data, 3600)
    context['for_7_days_hot_data'] = for_7_days_hot_data

    return render(request, 'blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(
        create_time__year=year, create_time__month=month)

    paginator = Paginator(blogs_all_list, 10)  # 十个博客进行分页
    page_num = request.GET.get('page', 1)  # get请求获取页码
    page_of_blogs = paginator.get_page(page_num)
    current_page = page_of_blogs.number
    if paginator.num_pages == 1:
        page_range = [1]
    elif current_page == 1 or current_page == 2:
        if paginator.num_pages <= 5:
            page_range = list(range(1, paginator.num_pages))
        else:
            page_range = list([1, 2, 3, 4, 5])
    elif current_page == paginator.num_pages or current_page == paginator.num_pages - 1:
        if paginator.num_pages <= 5:
            page_range = list(range(1, paginator.num_pages))
        else:
            page_range = list([paginator.num_pages - 4, paginator.num_pages - 3, paginator.num_pages - 2,
                               paginator.num_pages - 1, paginator.num_pages])
    else:
        page_range = list(range(max(current_page - 1, 1), current_page)) + \
                     list(range(current_page, min(current_page + 1, paginator.num_pages) + 1))
    if page_range and page_range[0] >= 3:
        page_range.insert(0, '...')
    if page_range and paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range and page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range and page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blog_types'] = BlogType.objects.all()
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blogs_all_list'] = blogs_all_list
    context['blog_dates'] = Blog.objects.dates(
        'create_time', 'month', order='DESC')
    context['year'] = year
    context['month'] = month

    for_7_days_hot_data = cache.get('for_7_days_hot_data')
    if for_7_days_hot_data is None:
        for_7_days_hot_data = get_seven_days_date()
        cache.set('for_7_days_hot_data', for_7_days_hot_data, 3600)
    context['for_7_days_hot_data'] = for_7_days_hot_data
    print(for_7_days_hot_data)
    return render(request, 'blogs_with_date.html', context)


def get_seven_days_date():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gt=date). \
        values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs


def blog_tags(request):
    context = {}
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'tag.html', context)


def contact(request):
    return render(request, 'contact.html')
