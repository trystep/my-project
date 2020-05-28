def sitemap_gen(path):
    new_key = open(path, "r", encoding="utf-8")
    new_sitemap = open('text.txt', 'w', encoding="utf-8")

    for line in new_key:
        new_url="""
    <url>
        <loc>http://parf-vlog.ru/?search="""+line.replace('\n','')+"""</loc>
        <lastmod>2020-05-28</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""

        new_sitemap.write(new_url)

    new_key.close()
    new_sitemap.close()


sitemap_gen('new_key.csv')
