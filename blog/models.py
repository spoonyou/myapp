from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

class Category(models.Model): #在数据库中创建一个categirt的表格
    name = models.CharField(max_length=100) #列名为name。还有一个列id（自动创建）
    def __str__(self):
        return self.name

class Tag(models.Model): #标签
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=70,verbose_name='标题') #文章标题

    body = models.TextField() #正文用TextField，存储长文本

    created_time = models.DateTimeField(verbose_name="创建时间") #文章创建时间和最后一次修改时间
    modified_time = models.DateTimeField(verbose_name="修改时间")

    #文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    #指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category) #ForeignKey:一对多关系
    tags = models.ManyToManyField(Tag, blank=True) #ManyToManyField：多对多关系

    views = models.PositiveIntegerField(default=0) #文章的阅读量

    author = models.ForeignKey(User)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1  #每次阅读阅读量加1
        self.save(update_fields=['views']) #将增加的阅读量保存在字段是views的数据库中

    def save(self, *args, **kwargs):
        """自动生成摘要，复写save方法"""
        if not self.excerpt: #如果没有自己加摘要
            md = markdown.Markdown(extensions=[ #用渲染body文本
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            #strip_tags去掉HTML文本的全部HTML标签
            #从文本摘取前54个字符给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        #调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']



