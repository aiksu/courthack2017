import os
import string

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LawBot.settings")

django.setup()

from grab import Grab
from core.models import Dictonary

g = Grab()
g.setup(hammer_mode=False)

for letter in string.ascii_lowercase:
    for page in range(10000):
        g.go('http://thelawdictionary.org/letter/%s/page/%d/' % (letter, page))
        posts = g.css_list('.post')
        if len(posts) == 0:
            print('end of letter: %s' % letter)
            break
        for post in posts:
            try:
                title = post.cssselect('h2.title a')[0].get('title')
                desc = post.cssselect('article p')[0].text
                Dictonary.objects.create(
                    title=title,
                    description=desc
                )
                print(title)
            except:
                print('error')
        print('---------------\nletter %s page %d complete' % (letter, page))


# total = 0
# total_latlan_none = 0
# for type in ['dental-clinics', 'dental-labs']:
#     for l in links:
#         try:
#             state_href = l.get('href')
#             for i in range(10000):
#                 g.go('http://www.yellowpages.com/%s/%s/?page=%s' % (state_href, type, str(i + 1)))
#                 info = g.css_list('[id^=lid] .info')
#                 if len(info) == 0:
#                     break
#                 for e in info:
#                     data = []
#                     data.append(e.cssselect('.business-name span')[0].text)
#                     try:
#                         data.append(e.cssselect('.adr [itemprop=streetAddress]')[0].text)
#                     except:
#                         data.append('-')
#                     try:
#                         data.append(e.cssselect('.adr [itemprop=addressRegion]')[0].text)
#                     except:
#                         data.append('-')
#                     try:
#                         data.append(e.cssselect('.adr [itemprop=postalCode]')[0].text)
#                     except:
#                         data.append('-')
#                     try:
#                         data.append(e.cssselect('[itemprop=telephone]')[0].text)
#                     except:
#                         data.append('-')
#                     links = e.cssselect('.links')[0]
#                     try:
#                         data.append(links.cssselect('.track-visit-website')[0].get('href'))
#                     except:
#                         data.append('-')
#                     try:
#                         yp_href = e.cssselect('.business-name')[0].get('href')
#                         g.go('http://www.yellowpages.com%s' % yp_href)
#                         latlan = g.css_list('[id=bpp-static-map]')[0]
#                         lat = latlan.get('data-lat')
#                         lan = latlan.get('data-lng')
#                     except:
#                         lat = None
#                         lan = None
#                         total_latlan_none += 1
#                         print('lat,lan=None')
#                     try:
#                         # DentalPoint.objects.create(
#                         #     name=data[0],
#                         #     street=data[1],
#                         #     region=data[2],
#                         #     postal=data[3],
#                         #     phone=data[4],
#                         #     website=data[5],
#                         #     lat=lat,
#                         #     lan=lan,
#                         #     is_clinic=type == 'dental-clinics',
#                         #     is_lab=type == 'dental-labs'
#                         # )
#                         total += 1
#                         print('%s. %s. %s, %s' % (str(total), state_href, type, data[0]))
#                     except:
#                         print('error on create')
#                 print('page %s ready' % str(i + 1))
#         except:
#             pass
# print('done')
# print('lat,lan=None: ' + str(total_latlan_none))
