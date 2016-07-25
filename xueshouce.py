# -*- coding: utf-8 -*-

from bs4 import SoupStrainer
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
    <body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story" mean="22">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.
<p class="story">..=-=</p></p>

<p class="story">...</p>
"""

only_a_tags = SoupStrainer("a")

only_tags_with_id_link2 = SoupStrainer(id="link2")


def is_short_string(string):
    return len(string) < 10

only_short_strings = SoupStrainer(string=is_short_string)
a=BeautifulSoup(html_doc, "lxml").find("body").select("p[mean]")
b=BeautifulSoup(html_doc, "html.parser").find("body").find_all("p",recursive=False)
print(a)
# for item in a:
#     print(item)
#     print("==========")
# print("1111111111111111111111")
# for item in b:
#     print(item)
#     print("==========")
print("sssss".replace(u'\xa0', u' ')  )