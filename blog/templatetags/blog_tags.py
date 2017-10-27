from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag # 装饰为register.simple_tag。这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了。
def get_recent_posts(num = 5): #最新文章
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag #归档
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag #分类
def get_categories():
    #计数post的文章数，存到num_posts中，再过滤掉小于0的文章
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
