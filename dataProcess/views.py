# -*- coding: utf-8 -*-

# Create your views here.

from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from .models import JobsType
from elasticsearch import Elasticsearch

client = Elasticsearch(hosts=["http://elastic:12345678@123.57.180.7"])
# redis_cli = redis.StrictRedis()

response = client.search(
    index="jobs",
    body={
    }
)

# Todo: 首页展示随机500条数据
class IndexView(View):
    def get(self):
        response = client.search(
            index="jobs",
            body={
                "query": {
                "match_all": {}
                },
                "size": 500
            }
        )
        results = response["hits"]["hits"]
        i = 0
        data={}
        for info in results:
            data[i] = info["_source"]
            i = i + 1
        return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

# Todo: 热门搜索词条返回数据

# Todo: 搜索词条返回数据

# Todo: 模糊搜索
