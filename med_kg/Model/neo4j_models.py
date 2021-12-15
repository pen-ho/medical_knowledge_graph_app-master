# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship, NodeMatcher


class Neo4j_Handle():
    graph = None
    matcher = None

    def __init__(self):
        print("Neo4j Init ...")

    def connectNeo4j(self):
        self.graph = Graph("http://127.0.0.1:7474", username="neo4j", password="pen")
        # self.graph = Graph("http://127.0.0.1:7474", username="neo4j", password="123")
        self.matcher = NodeMatcher(self.graph)

    # 一.实体查询
    def get_entity_info(self, name) -> list:
        '''
        查找该entity所有的直接关系
        :param name:
        :return:
        '''

        data = self.graph.run(
            "match (source)-[rel]-(target)  where source.name = $name " +
            "return rel ", name=name).data()

        # print(data)  # pen
        json_list = []
        for an in data:
            result = {}
            rel = an['rel']
            relation_type = list(rel.types())[0]
            start_name = rel.start_node['name']
            end_name = rel.end_node['name']
            result["source"] = start_name
            if relation_type == 'need_check':
                relation_type = '诊断检查'
            elif relation_type == 'acompany_with':
                relation_type = '并发症'
            elif relation_type == 'belongs_to':
                relation_type = '所属科室'
            elif relation_type == 'drugs_of':
                relation_type = '生产药品'
            elif relation_type == 'common_drug':
                relation_type = '常用药品'
            elif relation_type == 'do_eat':
                relation_type = '宜吃食物'
            elif relation_type == 'has_symptom':
                relation_type = '症状'
            elif relation_type == 'recommand_drug':
                relation_type = '推荐药品'
            elif relation_type == 'no_eat':
                relation_type = '忌吃食物'
            elif relation_type == 'recommand_eat':
                relation_type = '推荐食谱'
            result['rel_type'] = relation_type
            result['target'] = end_name
            json_list.append(result)
        print(json_list)
        return json_list

    # 三.关系查询都是直接1度关系
    # 1.关系查询:实体1(与实体1有直接关系的实体与关系)
    def findRelationByEntity1(self, entity1):
        answer = self.graph.run(
            "match (source)-[rel]-(target)  where source.name = $name " +
            "return rel ", name=entity1).data()

        answer_list = []
        for an in answer:
            result = {}
            rel = an['rel']
            relation_type = list(rel.types())[0]
            start_name = rel.start_node['name']
            end_name = rel.end_node['name']
            result["source"] = {'name': start_name}
            result['type'] = relation_type
            result['target'] = {'name': end_name}
            answer_list.append(result)

        return answer_list

    # 2.关系查询：实体2
    def findRelationByEntity2(self, entity1):
        answer = self.graph.run(
            "match (source)-[rel]-(target)  where target.name = $name " +
            "return rel ", name=entity1).data()

        answer_list = []
        for an in answer:
            result = {}
            rel = an['rel']
            relation_type = list(rel.types())[0]
            start_name = rel.start_node['name']
            end_name = rel.end_node['name']
            result["source"] = {'name': start_name}
            result['type'] = relation_type
            result['target'] = {'name': end_name}
            answer_list.append(result)

        return answer_list

    # 3.关系查询：实体1+关系
    def findOtherEntities(self, entity1, relation):
        answer = self.graph.run(
            "match (source)-[rel:" + relation + "]->(target)  where source.name = $name " +
            "return rel ", name=entity1).data()

        answer_list = []
        for an in answer:
            result = {}
            rel = an['rel']
            relation_type = list(rel.types())[0]
            start_name = rel.start_node['name']
            end_name = rel.end_node['name']
            result["source"] = {'name': start_name}
            result['type'] = relation_type
            result['target'] = {'name': end_name}
            answer_list.append(result)

        return answer_list

    # 4.关系查询：关系+实体2
    def findOtherEntities2(self, entity2, relation):

        answer = self.graph.run(
            "match (source)-[rel:" + relation + "]->(target)  where target.name = $name " +
            "return rel ", name=entity2).data()

        answer_list = []
        for an in answer:
            result = {}
            rel = an['rel']
            relation_type = list(rel.types())[0]
            start_name = rel.start_node['name']
            end_name = rel.end_node['name']
            result["source"] = {'name': start_name}
            result['type'] = relation_type
            result['target'] = {'name': end_name}
            answer_list.append(result)

        return answer_list

    # 5.关系查询：实体1+实体2
    def findRelationByEntities(self, entity1, entity2):
        answer = self.graph.run(
            "match (source)-[rel]-(target)  where source.name= $name1 and target.name = $name2 " +
            "return rel ", name1=entity1, name2=entity2).data()

        answer_list = []
        for an in answer:
            result = {}
            rel = an['rel']
            relation_type = list(rel.types())[0]
            start_name = rel.start_node['name']
            end_name = rel.end_node['name']
            result["source"] = {'name': start_name}
            result['type'] = relation_type
            result['target'] = {'name': end_name}
            answer_list.append(result)

        return answer_list

    # 6.关系查询：实体1+关系+实体2(实体-关系->实体)
    def findEntityRelation(self, entity1, relation, entity2):
        answer = self.graph.run(
            "match (source)-[rel:" + relation + "]->(target)  where source.name= $name1 and target.name = $name2 " +
            "return rel ", name1=entity1, name2=entity2).data()

        answer_list = []
        for an in answer:
            result = {}
            rel = an['rel']
            relation_type = list(rel.types())[0]
            start_name = rel.start_node['name']
            end_name = rel.end_node['name']
            result["source"] = {'name': start_name}
            result['type'] = relation_type
            result['target'] = {'name': end_name}
            answer_list.append(result)

        return answer_list

# 四、医药问答系统 hzp
    def gt_med_answer(self, question, classifier, parser):
        """
        输入问题，解析出问题意图，以及返回答案
        :param question:
        :param classifier:
        :param parser:
        :return:
        """
        # classifier = QuestionClassifier()
        # parser = QuestionPaser()
        # searcher = AnswerSearcher()
        answer_dict = {}
        answer_name = []
        answer_list = []
        answer_txt = ''
        answer = '您好，我是医药智能助理。你的问题无法精确回复，请反馈给人工客服。祝您身体健康。'
        res_classify = classifier.classify(question)  # 意图类别：基于词典的意图识别会错 因为现在ner 用了实体链接，这里要改。todo 20211114
        print('res_classify', res_classify)
        if not res_classify:  # 问句的意图类型 和 领域词 都找不到，直接给出无法回答的提示
            answer_dict['answer'] = [answer]
            answer_dict['list'] = []
            return answer_dict
        # list todo 下面函数要改，要返回是否用了语义匹配的症状，有要返回到文本答案中。
        # 找到语义最匹配的症状是 XXX, 症状XXX 可能患的疾病是...
        res_sql = parser.parser_main(res_classify, question)  # 根据提及实体和问句意图得到查询的sql
        print('res_sql', res_sql)
        if len(res_sql) != 0:
            query_list = res_sql[0]['sql']  # 问题解释器 只能对应一个意图 todo 改
            query = query_list[0]
            print('query', query)
            question_type = res_sql[0]['question_type']
            answer = self.graph.run(query).data()
            print('answer', answer)
        else:
            # parser 解释不出来
            answer_dict['answer'] = [answer]
            answer_dict['list'] = []
            question_type = ''
        # 每个意图的返回都要根据特定去写# 一共18种
        # 1.disease_symptom
        # 2.symptom_disease
        # 3.disease_cause
        # 4.disease_acompany
        # 5.disease_not_food
        # 6.disease_do_food
        # 7.food_not_disease
        # 8.food_do_disease
        # 9.disease_drug
        # 10.drug_disease
        # 11.disease_check
        # 12.check_disease
        # 13.disease_prevent
        # 14.disease_lasttime
        # 15.disease_cureway
        # 16.disease_cureprob
        # 17.disease_easyget
        # 18.disease_desc

        # 1 疾病症状
        if question_type == "disease_symptom":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"的症状包括：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 2 症状找疾病
        elif question_type == "symptom_disease":
            if 'r3' in query:  # 如果查询语句有'r3' 表明有3个症状
                for an in answer:
                    result1 = {}
                    result2 = {}
                    result3 = {}
                    relation_type = an['rname']
                    start_name1 = an['hname1']
                    start_name2 = an['hname2']
                    start_name3 = an['hname3']
                    end_name = an['tname']
                    result1["source"] = {'name': start_name1}
                    result1['type'] = relation_type
                    result1['target'] = {'name': end_name}
                    answer_list.append(result1)  # 给答案的所有三元组集合 进行知识图谱可视化
                    result2["source"] = {'name': start_name2}
                    result2['type'] = relation_type
                    result2['target'] = {'name': end_name}
                    answer_list.append(result2)  # 给答案的所有三元组集合 进行知识图谱可视化
                    result3["source"] = {'name': start_name3}
                    result3['type'] = relation_type
                    result3['target'] = {'name': end_name}
                    answer_list.append(result3)
                    answer_name.append(end_name)  # 给答案列表
                answer_dict['answer'] = answer_name
                answer_dict['list'] = answer_list
                desc = [i for i in answer_name]
                start_desc = start_name1 + '、' + start_name2 + '、' + start_name3
                answer_txt = '有"{0}"这些症状可能患上的疾病有：{1}'.format(start_desc, '、'.join(list(set(desc))))
                answer_dict['answer_txt'] = answer_txt
            elif 'r2' in query:  # 如果查询语句有's2' 表明有两个症状
                for an in answer:
                    result1 = {}
                    result2 = {}
                    relation_type = an['rname']
                    start_name1 = an['hname1']
                    start_name2 = an['hname2']
                    end_name = an['tname']
                    result1["source"] = {'name': start_name1}
                    result1['type'] = relation_type
                    result1['target'] = {'name': end_name}
                    answer_list.append(result1)  # 给答案的所有三元组集合 进行知识图谱可视化
                    result2["source"] = {'name': start_name2}
                    result2['type'] = relation_type
                    result2['target'] = {'name': end_name}
                    answer_list.append(result2)  # 给答案的所有三元组集合 进行知识图谱可视化
                    answer_name.append(end_name)  # 给答案列表
                answer_dict['answer'] = answer_name
                answer_dict['list'] = answer_list
                desc = [i for i in answer_name]
                start_desc = start_name1 + '、' + start_name2
                answer_txt = '有"{0}"这些症状可能患上的疾病有：{1}'.format(start_desc, '、'.join(list(set(desc))))
                answer_dict['answer_txt'] = answer_txt
            else:  # 1个症状  模糊SBERT或者精确匹配的
                for an in answer:
                    result = {}
                    relation_type = an['rname']
                    start_name = an['hname']
                    end_name = an['tname']
                    result["source"] = {'name': start_name}
                    result['type'] = relation_type
                    result['target'] = {'name': end_name}
                    answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                    answer_name.append(end_name)  # 给答案列表
                answer_dict['answer'] = answer_name
                answer_dict['list'] = answer_list
                desc = [i for i in answer_name]
                start_desc = start_name
                answer_txt = '有"{0}"症状可能患上的疾病有：{1}'.format(start_desc, '、'.join(desc))
                answer_dict['answer_txt'] = answer_txt
        # 3 病因
        elif question_type == "disease_cause":
            for an in answer:
                result = {}
                relation_type = '病因'
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name[:20] + "..."}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"可能的成因有：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 4 并发症
        elif question_type == "disease_acompany":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"的并发症包括：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        #  5 疾病宜吃食物
        elif question_type == "disease_do_food":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"宜食的食物包括有：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 6 疾病忌吃食物
        elif question_type == "disease_not_food":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"忌食的食物包括有：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 7 食物对什么疾病有好处
        elif question_type == "food_do_disease":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(start_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '患有"{0}"的人建议多试试{1}'.format('、'.join(list(set(desc))), end_name)
            answer_dict['answer_txt'] = answer_txt
        # 8 食物对哪些疾病不好
        elif question_type == "food_not_disease":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(start_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '患有"{0}"的人最好不要吃{1}'.format('、'.join(list(set(desc))), end_name)
            answer_dict['answer_txt'] = answer_txt
        # 9 疾病推荐药物
        elif question_type == "disease_drug":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"通常的使用的药品包括：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 10 药物治疗疾病
        elif question_type == "drug_disease":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(start_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"主治的疾病有{1},可以试试'.format(end_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 11 疾病检查
        elif question_type == "disease_check":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"一般可以通过以下方式检查出来：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 12 疾病检查
        elif question_type == "check_disease":
            for an in answer:
                result = {}
                relation_type = an['rname']
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(start_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '一般可以通过"{0}"检查出来的疾病有{1}'.format(end_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 13 预防措施
        elif question_type == "disease_prevent":
            for an in answer:
                result = {}
                relation_type = '预防措施'
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name[:20] + '...'}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"的预防措施包括：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 14 治疗周期
        elif question_type == "disease_lasttime":
            for an in answer:
                result = {}
                relation_type = '治疗周期'
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name[:20] + '...'}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"治疗可能持续的周期为：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 15 治疗方式
        elif question_type == "disease_cureway":
            for an in answer:
                result = {}
                relation_type = '治疗方式'
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': ' '.join(end_name)}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"可以尝试如下治疗：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 16 治愈概率
        elif question_type == "disease_cureprob":
            for an in answer:
                result = {}
                relation_type = '治愈概率'
                start_name = an['hname']
                end_name = an['tname']
                result["source"] = {'name': start_name}
                result['type'] = relation_type
                result['target'] = {'name': end_name[:20] + '...'}
                answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
                answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            answer_txt = '"{0}"治愈的概率为（仅供参考）：{1}'.format(start_name, end_name)
            answer_dict['answer_txt'] = answer_txt
        # 17 易感人群
        elif question_type == "disease_easyget":
            for an in answer:
                result = {}
            relation_type = '易感人群'
            start_name = an['hname']
            end_name = an['tname']
            result["source"] = {'name': start_name}
            result['type'] = relation_type
            result['target'] = {'name': end_name[:20] + '...'}
            answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
            answer_name.append(end_name)  # 给答案列表
            answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}"的易感人群包括：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        # 18 描述
        elif question_type == "disease_desc":
            for an in answer:
                result = {}
            relation_type = '简介'
            start_name = an['hname']
            end_name = an['tname']
            result["source"] = {'name': start_name}
            result['type'] = relation_type
            result['target'] = {'name': end_name[:20] + '...'}
            answer_list.append(result)  # 给答案的所有三元组集合 进行知识图谱可视化
            answer_name.append(end_name)  # 给答案列表
            # answer_dict['answer'] = answer_name
            answer_dict['list'] = answer_list
            desc = [i for i in answer_name]
            answer_txt = '"{0}",熟悉一下：{1}'.format(start_name, '、'.join(list(set(desc))))
            answer_dict['answer_txt'] = answer_txt
        else:
            answer_dict['answer'] = [answer]
            answer_dict['list'] = []

        return answer_dict
