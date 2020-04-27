from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import os
from django.views.decorators.http import require_http_methods
import json
import py2neo

from . import models

neo_connection = models.Neo4j()  # 预加载Neo4j
neo_connection.connectDB()


@require_http_methods(["GET"])
def match_all(request):
    try:
        res = {}
        db = neo_connection
        res['data'] = db.searchAll()
        res['flag'] = 1
        print(len(res['data']))
        return JsonResponse(res)
    except Exception as e:
        res = {'data': str(e), 'flag': 0}
        return JsonResponse(res)


def reduce_duplicate(data):
    seen = set()
    res = []
    for d in data:
        a = d['e1'].items()
        b = d['e2'].items()
        c = d['r'].items()
        t = []
        for i in a:
            t.append(i)
        for i in b:
            t.append(i)
        for i in c:
            t.append(i)
        t = tuple(t)
        if t not in seen:
            seen.add(t)
            res.append(d)
    return res


def manage_raw_data(raw_data):
    data = []
    print(raw_data)  # 怀疑
    for i in raw_data:
        for j in i['rels']:
            # j.toString()
            l = list(py2neo.data.walk(j))
            e1 = dict(l[0])
            e1['type'] = str(l[0].labels)[1:]
            e2 = dict(l[2])
            e2['type'] = str(l[2].labels)[1:]
            tmp = {
                'e1': e1,
                'r': dict(l[1]),
                'e2': e2,
            }
            data.append(tmp)
    return data


@require_http_methods('POST')
def search_by_title(request):
    try:
        title = request.POST.get('title')
        level = request.POST.get('level')
        res = {}
        db = neo_connection
        #  将多层查询的数据进行整理
        data = manage_raw_data(db.searchByTitle(title, level))
        res['data'] = reduce_duplicate(data)  # 去重
        res['flag'] = 1
        print(len(res['data']))
        return JsonResponse(res)
    except Exception as e:
        res = {'data': str(e), 'flag': 0}
        return JsonResponse(res)


@require_http_methods('POST')
def search_by_keyword(request):
    try:
        keyword = request.POST.get('keyword')
        level = request.POST.get('level')
        res = {}
        db = neo_connection
        #  将多层查询的数据进行整理
        data = manage_raw_data(db.searchByKeyword(keyword, level))
        res['data'] = reduce_duplicate(data)  # 去重
        res['flag'] = 1
        print(len(res['data']))
        return JsonResponse(res)
    except Exception as e:
        res = {'data': str(e), 'flag': 0}
        return JsonResponse(res)


@require_http_methods('POST')
def search_by_author(request):
    try:
        author = request.POST.get('author')
        level = request.POST.get('level')
        res = {}
        db = neo_connection
        #  将多层查询的数据进行整理
        data = manage_raw_data(db.searchByAuthor(author, level))
        res['data'] = reduce_duplicate(data)  # 去重
        res['flag'] = 1
        print(len(res['data']))
        return JsonResponse(res)
    except Exception as e:
        res = {'data': str(e), 'flag': 0}
        return JsonResponse(res)


@require_http_methods("POST")
def search_title_by_algorithm(request):
    try:
        algorithm=''
        if len(request.POST) != 0:
            algorithm = request.POST.get('algorithm')
        res = {}
        db = neo_connection
        #  将多层查询的数据进行整理
        data = manage_raw_data(db.searchTitleByAlgorithm(algorithm))
        res['data'] = reduce_duplicate(data)  # 去重
        print(len(res['data']))
        res['flag'] = 1
        return JsonResponse(res)
    except Exception as e:
        res = {'data': str(e), 'flag': 0}
        return JsonResponse(res)

# relationCountDict = {}
#
#
# def sortDict(relationDict):
#     for i in range(len(relationDict)):
#         relationName = relationDict[i]['rel']['type']
#         relationCount = relationCountDict.get(relationName)
#         if (relationCount is None):
#             relationCount = 0
#         relationDict[i]['relationCount'] = relationCount
#     relationDict = sorted(relationDict, key=lambda item: item['relationCount'], reverse=True)
#
#     return relationDict
#
#
# @require_http_methods(["POST"])
# def extractPic(request):
#     files = request.FILES.get('pic', None)
#     for file in files:
#         print(files)
#     return HttpResponse(".\static\img\chart-texture.jpg");
#
#
# @require_http_methods(["GET"])
# def search_entity(request):
#     ctx = {}
#     # 根据传入的实体名称搜索出关系
#     if (request.GET):
#         entity = request.GET['user_text']
#         # 连接数据库
#         db = neo_connection
#         entityRelation = db.getEntityRelationbyEntity(entity)
#         if len(entityRelation) == 0:
#             # 若数据库中无法找到该实体，则返回数据库中无该实体
#             ctx = {'title': '<h1>数据库中暂未添加该实体</h1>'}
#             print("数据库无")
#             return JsonResponse(ctx)
#             # return render(request, 'entity.html', {'ctx': json.dumps(ctx, ensure_ascii=False)})
#         else:
#             # 返回查询结果
#             # 将查询结果按照"关系出现次数"的统计结果进行排序
#             entityRelation = sortDict(entityRelation)
#             response = {}
#             response['entityRelation'] = entityRelation
#             print("查找成功")
#             return JsonResponse(response)
#             # return render(request,'entity.html',{'entityRelation':json.dumps(entityRelation,ensure_ascii=False)})
#
#
# # return render(request, "entity.html", {'ctx': ctx})
#
#
# def search_relation(request):
#     ctx = {}
#     if (request.GET):
#         db = neo_connection
#         entity1 = request.GET['entity1_text']
#         relation = request.GET['relation_name_text']
#         entity2 = request.GET['entity2_text']
#         relation = relation.lower()
#         searchResult = {}
#         # 若只输入entity1,则输出与entity1有直接关系的实体和关系
#         if (len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0):
#             searchResult = db.findRelationByEntity(entity1)
#             searchResult = sortDict(searchResult)
#             if (len(searchResult) > 0):
#                 return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
#
#         # 若只输入entity2则,则输出与entity2有直接关系的实体和关系
#         if (len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0):
#             searchResult = db.findRelationByEntity2(entity2)
#             searchResult = sortDict(searchResult)
#             if (len(searchResult) > 0):
#                 return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
#         # 若输入entity1和relation，则输出与entity1具有relation关系的其他实体
#         if (len(entity1) != 0 and len(relation) != 0 and len(entity2) == 0):
#             searchResult = db.findOtherEntities(entity1, relation)
#             searchResult = sortDict(searchResult)
#             if (len(searchResult) > 0):
#                 return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
#         # 若输入entity2和relation，则输出与entity2具有relation关系的其他实体
#         if (len(entity2) != 0 and len(relation) != 0 and len(entity1) == 0):
#             searchResult = db.findOtherEntities2(entity2, relation)
#             searchResult = sortDict(searchResult)
#             if (len(searchResult) > 0):
#                 return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
#         # 若输入entity1和entity2,则输出entity1和entity2之间的最短路径
#         if (len(entity1) != 0 and len(relation) == 0 and len(entity2) != 0):
#             searchResult = db.findRelationByEntities(entity1, entity2)
#             if (len(searchResult) > 0):
#                 print(searchResult)
#                 searchResult = sortDict(searchResult)
#                 return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
#         # 若输入entity1,entity2和relation,则输出entity1、entity2是否具有相应的关系
#         if (len(entity1) != 0 and len(entity2) != 0 and len(relation) != 0):
#             searchResult = db.findEntityRelation(entity1, relation, entity2)
#             if (len(searchResult) > 0):
#                 return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
#         # 全为空
#         if (len(entity1) != 0 and len(relation) != 0 and len(entity2) != 0):
#             pass
#         ctx = {'title': '<h1>暂未找到相应的匹配</h1>'}
#         return render(request, 'relation.html', {'ctx': ctx})
#
#     return render(request, 'relation.html', {'ctx': ctx})
