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

# 模拟数据存储在内存中的词条搜索次数字典
search_data = {
    '后端开发': 10,
    '前端': 5,
    '算法工程师': 8,
    '嵌入式开发': 2,
    'Java实习生': 6,
    '数据分析': 4,
}


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
        data = {}
        for info in results:
            data[i] = info["_source"]
            i = i + 1
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


# 热门搜索词条返回数据
def get_top_searches(request):
    # 获取搜索次数最多的5个词条
    top_searches = sorted(search_data.items(), key=lambda x: x[1], reverse=True)[:5]
    response_data = {key: value for key, value in top_searches}

    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})

# Todo: 搜索词条返回数据

# Todo: 模糊搜索
