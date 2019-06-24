import codecs
import os

from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
# Create your views here.
from Article.models import Category, Ad, Article, Item
from news import settings

HTML_DIR = os.path.join(settings.BASE_DIR,'templates/html')

#import logging
#logger = logging.getLogger("django") # 为loggers中定义的名称

def globl_init(request):
    #取分类
    category_list = Category.objects.order_by("-id")
    #广告
    ad_list = Ad.objects.all()
    #热门新闻
    hot_articles=Article.objects.filter(is_active=True).order_by("-id")[0:5]

    return locals()

def index(request):
    article_list = Article.objects.order_by("-id")[0:20]
    return render(request,'index.html',locals())

def category(request):
    categoryid = request.GET.get('cid')
    item_list = Item.objects.filter(categorys=categoryid)
    article_list = Article.objects.filter(item__categorys=categoryid)
    article_list = get_page(request,article_list)
    curr_url = request.get_full_path()
    nPos = curr_url.find('&page')
    if nPos >0:
        curr_url = request.get_full_path()[0:nPos]
    else:
        curr_url = request.get_full_path()
    return render(request,'category.html',locals())

def article(request):
    id = request.GET.get('id')
    articlehtml = 'article_{}.html'.format(id)
    article_html = os.path.join(HTML_DIR,articlehtml)
    if not os.path.exists(article_html):
        article = Article.objects.get(id = id)
        category_list = Category.objects.all()
        #广告
        ad_list = Ad.objects.all()
        #热门新闻
        hot_articles = Article.objects.filter(is_active=True)[0:5]
        content = render_to_string('article.html',locals())
        with codecs.open(article_html,'w',encoding='utf-8')as static_file:
            static_file.write(content)

    return render(request,article_html,locals())

def search(request):
    strquery = request.GET.get('query')
    article_list = Article.objects.filter(
        Q(title__contains=strquery) | Q(content__contains=strquery))

    return render(request,'index.html',locals())

def item(request):
    categoryid =  request.GET.get('cid')
    itemid = request.GET.get('itemid')
    item_list = Item.objects.filter(categorys=categoryid)
    article_list = Article.objects.filter(item=itemid)
    article_list = get_page(request,article_list)
    curr_url = request.get_full_path()
    nPos = curr_url.find('&page')
    if nPos >0:
        curr_url = request.get_full_path()[0:nPos]
    else:
        curr_url = request.get_full_path()
    return render(request,'category.html',locals())

def tag(request):
    tagid = request.GET.get('tagid')

    article_list = Article.objects.filter(tags=tagid)
    article_list = get_page(request,article_list)
    curr_url = request.get_full_path()
    nPos = curr_url.find('&page')
    if nPos >0:
        curr_url = request.get_full_path()[0:nPos]
    else:
        curr_url = request.get_full_path()
    return render(request,'tag.html',locals())

def get_page(request,object_list):
    pagesize =10
    paginator = Paginator(object_list,pagesize)
    try:
        page = int(request.GET.get('page',1))
        object_list = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        object_list = paginator.page(1)
    return object_list











