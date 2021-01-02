import random

from django.shortcuts import render
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import requests
from random import choice
from .scripts.yttool import detail_view, search_view, Youtube, SearchReader, DetailReader, CommentReader
from RandomWordGenerator import RandomWord


class Args(object):
    debug = 0


def search(request, slug=''):
    """
    Поиск по YouTube на запрос от пользователя сайта. По умолчанию - страница с рандомным словом в поиске
    """
    args = Args()
    yt = Youtube(args)
    keyword = slug or urllib.parse.quote(request.GET.get('search', ''))
    word_file = "/home/singleton/my_folder/pet-projects/my-project/mysite/app/scripts/keywords.csv"
    WORDS = open(word_file).read().splitlines()
    random_word = random.choice(WORDS)
    if not keyword:
        keyword = random_word
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": keyword})
    cfg = yt.getpageinfo(url)
    lst = SearchReader(args, yt, cfg)
    data = lst.recursesearch()
    context = {"data": data, }
    return render(request, 'base.html', context=context)


def post_detail(request, slug):
    """
    Вывод содержимого видео с YouTube
    """
    RESPONSE = {'id': str,
                'title': str,
                'owner': str,
                'view_count': str,
                'duration': str,
                'sentiment': str,
                'publish_date': str,
                'upload_date': str,
                'description': str,
                }

    args = Args()
    yt = Youtube(args)
    url = "https://www.youtube.com/watch?v=%s" % slug
    cfg = yt.getpageinfo(url)
    lst = DetailReader(args, yt, cfg)
    data = lst.output()

    comment = CommentReader(args, yt, cfg)
    comments = comment.recursecomments()

    context = {"data": data, "comments": comments}
    return render(request, 'post_detail.html', context=context)


def sitemap(request):
    return render(request, 'sitemap.xml')
