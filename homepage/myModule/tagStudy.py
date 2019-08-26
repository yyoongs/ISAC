import json
from gensim.models import Word2Vec
from settings import APP_STATIC
import os

with open(os.path.join(APP_STATIC, 'tagging_data.json'),  encoding = "UTF-8") as c:
    tagging_data = json.load(c)

# tag data 학습 시키기 위함
taglist = []
for _ in tagging_data:
    taglist.append(_['qKeyword'])

model = Word2Vec(taglist, size=20, window=5, min_count=5)