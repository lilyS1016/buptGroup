from django.db import models

# Create your models here.
from elasticsearch_dsl import Completion, Keyword, Text, Double

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["http://elastic:12345678@123.57.180.7"])


class JobsType():
    # 设置index名称和document名称
    class Index:
        name = "jobs"
        doc_type = "_doc"

    id = Keyword()
    company = Text(analyzer="ik_smart")
    name = Text(analyzer="ik_max_word")
    location = Text(analyzer="ik_smart")
    type = Keyword()
    category = Text(analyzer="ik_smart")
    description = Text(analyzer="ik_max_word")
    requirement = Text(analyzer="ik_max_word")
    url = Keyword()
