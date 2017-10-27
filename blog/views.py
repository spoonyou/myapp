from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView

# def index(request):
#     post_list = Post.objects.all().order_by('-created_time') #按时间排序的所有文章记录，然后传给index.html
#     return render(request, 'blog/index.html', context={'post_list':post_list})

class IndexView(ListView):
    # model指定为Post,告诉Django我要获取的模型是Post
    model = Post
    #template_name指定这个视图渲染的模板
    template_name = 'blog/index.html'
    #context_object_name 指定获取的模型列表数据保存的变量名。这个变量会被传递给模板
    context_object_name = 'post_list'

    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        return context
    def pagination_data(self, paginator, page, is_paginated):

        first = False
        last = False

        left = []
        right = []

        left_has_more = False
        right_has_more = False

        page_number = page.number
        page_range = paginator.page_range
        total_pages = paginator.num_pages

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number-3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number-3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'first':first,
            'last': last,
            'right_has_more': right_has_more,
            'left_has_more': left_has_more,
            'right': right,
            'left': left,
        }
        return data

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.increase_views() #让被访问文章的阅读量加1

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    tag_list = post.tags.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list,
               'tag_list':tag_list,
               }
    return render(request, 'blog/detail.html', context=context)

def archives(request, year, month): #归档页面
    """Python 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表，
    所以 Django 要求我们把点替换成了两个下划线，即 created_time__year"""
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')#用filter过滤出该分类下的全部文章
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

def user_post(request, pk):
    post_list = Post.objects.filter(author_id=pk).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

