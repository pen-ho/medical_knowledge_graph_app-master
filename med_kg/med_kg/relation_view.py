# -*- coding: utf-8 -*-
from django.shortcuts import render
from util.pre_load import neo4jconn
    # , name_dict

import json


# 电影实体查询
def search_entity(request):
    ctx = {}
    # 根据传入的实体名称搜索出关系
    if (request.GET):
        entity = request.GET['user_text']
        entity = entity.strip()
        entity = entity.lower()
        entity = ''.join(entity.split())

        # actor_name_dict, movie_name_dict = name_dict[0], name_dict[1]
        #
        # if entity in actor_name_dict.keys():
        #     entity = actor_name_dict.get(entity)
        # if entity in movie_name_dict.keys():
        #     entity = movie_name_dict.get(entity)

        entityRelation = neo4jconn.get_entity_info(entity)
        if len(entityRelation) == 0:
            # 若数据库中无法找到该实体，则返回数据库中无该实体
            ctx = {'title': '<h2>知识库中暂未添加该实体</h1>'}
            return render(request, 'entity_search.html', {'ctx': json.dumps(ctx, ensure_ascii=False)})
        else:
            return render(request, 'entity_search.html', {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})
    # 需要进行类型转换
    return render(request, 'entity_search.html', {'ctx': ctx})


# 关系查询
def search_relation(request):
    # actor_name_dict, movie_name_dict = name_dict[0], name_dict[1]

    ctx = {}
    if (request.GET):
        # 实体1
        entity1 = request.GET['entity1_text']
        entity1 = entity1.strip()
        entity1 = entity1.lower()
        entity1 = ''.join(entity1.split())

        # if entity1 in actor_name_dict.keys():
        #     entity1 = actor_name_dict.get(entity1)
        # if entity1 in movie_name_dict.keys():
        #     entity1 = movie_name_dict.get(entity1)

        # 关系
        relation = request.GET['relation_name_text']
        # 将关系名转为大写
        # 		relation = relation.upper()
        # 对relation 中文名转英文名 hzp
        if relation == '推荐食谱':
            relation = 'recommand_eat'
        elif relation == '忌吃食物':
            relation = 'no_eat'
        elif relation == '推荐药品':
            relation = 'recommand_drug'
        elif relation == '症状':
            relation = 'has_symptom'
        elif relation == '宜吃食物':
            relation = 'do_eat'
        elif relation == '常用药物':
            relation = 'common_drug'
        elif relation == '生产药品':
            relation = 'drugs_of'
        elif relation == '诊断检查':
            relation = 'need_check'
        elif relation == '并发症':
            relation = 'acompany_with'
        elif relation == '所属科室':
            relation = 'belongs_to'

        # 实体2
        entity2 = request.GET['entity2_text']
        entity2 = entity2.strip()
        entity2 = entity2.lower()
        entity2 = ''.join(entity2.split())

        # if entity2 in actor_name_dict.keys():
        #     entity2 = actor_name_dict.get(entity2)
        # if entity2 in movie_name_dict.keys():
        #     entity2 = movie_name_dict.get(entity2)

        # 保存返回结果
        searchResult = {}

        # 1.若只输入entity1,则输出与entity1有直接关系的实体和关系
        if (len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0):
            searchResult = neo4jconn.findRelationByEntity1(entity1)
            if (len(searchResult) > 0):
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 2.若只输入entity2则,则输出与entity2有直接关系的实体和关系
        if (len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0):
            searchResult = neo4jconn.findRelationByEntity2(entity2)
            if (len(searchResult) > 0):
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 3.若输入entity1和relation，则输出与entity1具有relation关系的其他实体
        if (len(entity1) != 0 and len(relation) != 0 and len(entity2) == 0):
            searchResult = neo4jconn.findOtherEntities(entity1, relation)
            if (len(searchResult) > 0):
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 4.若输入entity2和relation，则输出与entity2具有relation关系的其他实体
        if (len(entity2) != 0 and len(relation) != 0 and len(entity1) == 0):
            searchResult = neo4jconn.findOtherEntities2(entity2, relation)
            if (len(searchResult) > 0):
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 5.若输入entity1和entity2,则输出entity1和entity2之间的关系
        if (len(entity1) != 0 and len(relation) == 0 and len(entity2) != 0):
            searchResult = neo4jconn.findRelationByEntities(entity1, entity2)
            if (len(searchResult) > 0):
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 6.若输入entity1,entity2和relation,则输出entity1、entity2是否具有相应的关系
        if (len(entity1) != 0 and len(entity2) != 0 and len(relation) != 0):
            print(relation)
            searchResult = neo4jconn.findEntityRelation(entity1, relation, entity2)
            if (len(searchResult) > 0):
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 7.若全为空
        if (len(entity1) != 0 and len(relation) != 0 and len(entity2) != 0):
            pass

        ctx = {'title': '<h1>暂未找到相应的匹配</h1>'}
        return render(request, 'relation.html', {'ctx': ctx})

    return render(request, 'relation.html', {'ctx': ctx})
