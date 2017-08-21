#coding:utf-8
from datetime import datetime
from elasticsearch import Elasticsearch

# 连接es，默认端口是9200
es = Elasticsearch([
    {"host": "192.168.1.111", "port": 9200},
    {"host": "192.168.1.102", "port": 9200},
    {"host": "192.168.1.111", "port": 9201},
])

# # 创建索引，如果已经存在了，就返回400
# # 这个索引可以现在创建，也可以在后面插入数据时再临时创建
# es.indices.create(index="my-index")

# # 插入数据
# es.index(index="my-index", doc_type="test_type", id=1, body={
#     "any": "data01", "timestamp": datetime.now()
# })      # doc_type是文档类型
# es.index(index="my-index", doc_type="test_type", id=42, body={
#     "any": "data", "timestamp": datetime.now()
# })

# 查询数据，两种get、search
res = es.get(index="my-index", doc_type="test_type", id=1)
print(res)
print(res["_source"])

res = es.search(index="my-index", body={"query": {"match_all": {}}})
print(res)

for hit in res["hits"]["hits"]:
    print(hit["_source"])

res = es.search(index="my-index", body={"query": {"match": {"any": "data"}}})
for hit in res["hits"]["hits"]:
    print(hit["_source"])

cnt = es.count(index="my-index", q="data*")
print(cnt)