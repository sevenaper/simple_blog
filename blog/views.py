from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType


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
    return render_to_response('blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        blog.readed_num += 1
        blog.save()
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(
        create_time__gt=get_object_or_404(Blog, pk=blog_pk).create_time).last()
    context['next_blog'] = Blog.objects.filter(
        create_time__lt=get_object_or_404(Blog, pk=blog_pk).create_time).first()
    response = render_to_response('blog_detail.html', context)
    response.set_cookie('blog_%s_readed' % blog_pk, 'True', max_age=300)
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

    return render_to_response('blogs_with_type.html', context)


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
    return render_to_response('blogs_with_date.html', context)
