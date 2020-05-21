from django.shortcuts import render
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import requests
from random import choice


def search(request):
    """
    Поиск по YouTube на запрос от пользователя сайта
    """
    keyword = urllib.parse.quote(request.GET.get('search', ''))

    if not keyword:
        keyword = 'news'

    page = str(urlopen(("https://www.youtube.com/results?search_query=%s&disable_polymer=1" % keyword)).read(),
               encoding='utf-8')
    page_source = page.split()

    temp = 0

    link_output = []  # OUTPUT VIDEO LINKS FROM SEARCH
    title_output = []  # OUTPUT TITLE LINKS FROM SEARCH


    for index in range(0, len(page_source) - 1):
        element = page_source[index]
        element_next = page_source[index + 1]
        if (element[0:23] == 'data-sessionlink="itct=') and (element_next[0:7] == 'title="'):
            buffer = ""
            init = page_source[index + 1]
            buffer += init
            sub_index = index + 2
            end = index + 22
            while sub_index < end:
                this_element = page_source[sub_index]
                next_element = page_source[sub_index + 1]
                if (this_element[len(this_element) - 1]) == '"':
                    if next_element == 'rel="spf-prefetch"':
                        buffer += (" " + this_element)
                        title_output.append(buffer)
                        break
                else:
                    buffer += (" " + this_element)
                sub_index += 1

    for element in page_source:
        if element[0:15] == 'href="/watch?v=' and len('www.youtube.com' + element[6:len(element) - 1]) == 35:
            temp += 1
            if temp % 2 == 0:
                link_output += ['www.youtube.com' + element[6:len(element) - 1]]

    data = []

    for index in range(0, len(link_output)-1):
        # Replace
        title_output[index]=title_output[index].replace('&#39;', "")
        title_output[index] = title_output[index].replace('&quot;', '"')

        link_and_title = [link_output[index], title_output[index][6:]]
        data.append(link_and_title)

    context = {"search_query": keyword,
               "data": data,
               }
    return render(request, 'base.html', context=context)


def post_detail(request, slug):
    """
    Вывод содержимого видео с YouTube на основе Embed-кода, полученного с GET-запроса в URL
    """
    id=slug
    RESPONSE = {
        'id': str,
        'title': str,
        'upload_date': str,
        'duration': str,
        'description': str,
        'uploader': {
            'name': str,
        },
        'statistics': {
            'views': int,
            'likes': int,
            'dislikes': int
        }
    }

    def remove_comma(string):
        return ''.join(string.split(','))

    def make_soup(url):
        '''
        Читает содержимое по указанному URL и возвращает объект Python на основе
        структуры содержимого (HTML).
        '''
        # Прокси
        ##########################################################################
        useragents_list = open(
            "/home/django/my-project/mysite/app/scraper/useragents.txt").read().split('\n')
        proxy_list = open(
            "/home/django/my-project/mysite/app/scraper/proxies.txt").read().split('\n')
        useragent = {'User-Agent': choice(useragents_list)}
        proxy = {'http': 'http://' + choice(proxy_list)}
        ##########################################################################
        html = requests.get(url, headers=useragent, proxies=proxy)
        return BeautifulSoup(html.text, 'lxml')

    def scrape_video_data(id):
        '''
        Забирает данные со страницы видео YouTube, чей идентификатор передается в URL,
        и возвращает объект JSON в качестве ответа.
        '''

        youtube_video_url = 'https://www.youtube.com/watch?v=' + id

        soup = make_soup(youtube_video_url).find(id='watch7-content')

        if len(soup.contents) > 1:
            video = RESPONSE
            uploader = video['uploader']
            statistics = video['statistics']

            video['id'] = id
            # get data from tags having `itemprop` attribute
            for tag in soup.find_all(itemprop=True, recursive=False):
                key = tag['itemprop']
                if key == 'name':
                    # get video's title
                    video['title'] = tag['content']
                elif key == 'duration':
                    # get video's duration
                    video['duration'] = tag['content']
                    video['duration'] = video['duration'].replace('PT', '').replace('M', ' мин. ').replace('S',
                                                                                                           ' сек.')
                elif key == 'datePublished':
                    # get video's upload date
                    video['upload_date'] = tag['content']
                elif key == 'genre':
                    # get video's genre (category)
                    video['genre'] = tag['content']
                # elif key == 'thumbnailUrl':
                #     # get video thumbnail URL
                #     video['thumbnail_url'] = tag['href']
                elif key == 'interactionCount':
                    # get video's views
                    statistics['views'] = int(tag['content'])

                # elif key == 'channelId':
                #     # get uploader's channel ID
                #     uploader['channel_id'] = tag['content']
            # get video description
            description_para = soup.find('p', id='eow-description')
            for br in description_para.find_all('br'):
                br.replace_with('\n')
            video['description'] = description_para.get_text()

            # get like count
            like_button = soup.find('button', class_='like-button-renderer-like-button-unclicked')
            statistics['likes'] = remove_comma(like_button.span.string)

            # get dislike count
            dislike_button = soup.find('button', class_='like-button-renderer-dislike-button-unclicked')
            statistics['dislikes'] = remove_comma(dislike_button.span.string)

            # get uploader's name
            uploader_div = soup.find('div', class_='yt-user-info')
            uploader['name'] = uploader_div.a.get_text()
            # is the uploader verified?
            verified_span = uploader_div.span
            uploader['is_verified'] = verified_span is not None

            # get uploader's thumbnail URL
            # uploader['thumbnail_url'] = soup.find('span', class_='yt-thumb-clip').img['data-thumb']

            return RESPONSE
        return ({
            'error': 'Video with the ID {} does not exist'.format(id)
        })
    context = {"data": RESPONSE,
               'embed':id}

    try:
        scrape_video_data(id)
    except:
        return render(request, 'post_detail_if_block_IP.html', context=context)

    return render(request, 'post_detail.html', context=context)


def sitemap(request):
    return render(request, 'sitemap.xml')
