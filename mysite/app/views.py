import random
from django.shortcuts import render
import urllib.parse

from django.template import Context

from .scripts.yttool import Youtube, SearchReader, DetailReader, CommentReader


class Args(object):
    debug = 0


def search(request, slug=''):
    """
    Поиск по YouTube на запрос от пользователя сайта. По умолчанию - страница с рандомным словом в поиске
    """
    args = Args()
    yt = Youtube(args)
    keyword = slug or urllib.parse.quote(request.GET.get('search', ''))
    try:
        word_file = "/home/django/my-project/mysite/app/scripts/keywords.csv"
        words = open(word_file).read().splitlines()
    except:
        words = ['lol', 'pop', 'news', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
                 'x', 'c', 'v', 'b', 'n', 'm']
    random_word = random.choice(words)
    if not keyword:
        keyword = random_word
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": keyword})
    cfg = yt.getpageinfo(url)
    lst = SearchReader(args, yt, cfg)
    data = lst.recursesearch()
    data = data[:18]
    context = {"data": data, }
    return render(request, 'base.html', context=context)


def post_detail(request, slug):
    """
    Вывод содержимого видео с YouTube
    """
    args = Args()
    yt = Youtube(args)
    url = "https://www.youtube.com/watch?v=%s" % slug
    cfg = yt.getpageinfo(url)
    lst = DetailReader(args, yt, cfg)
    data = lst.output()
    desc = data['description']
    try:
        desc = desc.replace("\n", '<br>')
    except:
        desc = ''
    comment = CommentReader(args, yt, cfg)
    comments = comment.recursecomments()

    context = {"data": data, "comments": comments, 'desc': desc}
    return render(request, 'post_detail.html', context=context)


def about(request):
    return render(request, 'about.html')


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')


def contacts(request):
    return render(request, 'contacts.html')


def sitemap(request):
    return render(request, 'sitemap.xml')


def robots(request):
    return render(request, 'robots.txt')
