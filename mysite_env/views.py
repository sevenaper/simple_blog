from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_date
from blog.models import Blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_date(blog_content_type)
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    return render_to_response('home.html', context)
