# -*- coding: utf-8 -*-

# Create your views here.

from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from .models import JobsType
from elasticsearch import Elasticsearch
from elasticsearch_dsl import query, Search

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
def get_searched_data(request):  # 获取搜索的单词或词条名称或数字值或词条内容的Json格式的响应数据。
    key_words = request.GET.get("key_words", None)  # 获取当前关键字。
    company = request.GET.get("company", None)  # 获取当前公司名称
    location = request.GET.get("location", None)  # 获取位置。
    type = request.GET.get("type", None)  # 获取类型
    category = request.GET.get("category", None)  # 获取分类
    page = int(request.GET.get("pageNum",1))  # 获取页码
    pageSize =int( request.GET.get("pageSize",10))  # 获取页面大小
    s = Search(using=client,index="jobs") 
    if(key_words!=None):
        s = s.query("multi_match", query=key_words, fields=["name", "description","requirement"])
    if(type!=None):
        s = s.query("match", type=type)
    if(category!=None):
        s = s.query("match", category=category)
    if(company!=None):
        s = s.query("match", company=company)    
    if(location!=None):
        s = s.query("match", location=location)
    s = s [(page-1)*pageSize:(page-1)*pageSize+pageSize] #分页
    search_data[key_words]=search_data.get(key_words,0)+1
    response_data = s.execute().to_dict()["hits"] # 执行查询，返回结果集。
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})
    
# Todo: 模糊搜索
