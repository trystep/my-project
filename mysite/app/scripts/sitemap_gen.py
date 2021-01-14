def sitemap_gen(path):
    new_key = open(path, "r", encoding="utf-8")
    new_sitemap = open('new_url_for_sitemap.txt', 'w', encoding="utf-8")

    for line in new_key:
        new_url = """
    <url>
        <loc>https://www.clipic.ru/?search=""" + line.replace('\n', '').replace('&', '') + """</loc>
        <lastmod>2021-01-13</lastmod>
        <priority>0.8</priority>
    </url>"""

        new_sitemap.write(new_url)

    new_key.close()
    new_sitemap.close()


sitemap_gen('keywords.csv')
