#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from MedModel.sbert import SBert
from ner_model.predict_ner import predict_med_ner
from util.nlp_ner import el


class QuestionPaser:
    '''构建实体节点'''
    '''
    将args字典如：{'气短': ['symptom'], '烦热': ['symptom']}
    变为entity_dict字典：{'symptom': ['气短', '烦热']}
    '''

    # def entity_linking(self, sent, args):
    #     """
    #
    #     :param sent:
    #     :param args:
    #     :return: {'entity':['type']} eg {'藿香正气水': ['drug']}
    #     """
    #     output_text = predict_med_ner(sent)  # bert预测结果
    #     bert_ner_text = ""
    #     bert_ner_text_type = ""
    #     segment_text = ""
    #     segment_text_type = ""
    #     if output_text != "无识别出mention":
    #         bert_ner_text = output_text.split(':')[0]
    #         bert_ner_text_type = output_text.split(':')[1]
    #     if len(args.keys()) != 0:
    #         segment_text = str([k for k in args.keys()][0])
    #         segment_text_type = str([k for k in args.values()][0][0])
    #     print(segment_text, segment_text_type, bert_ner_text, bert_ner_text_type)
    #     if bert_ner_text == "" and segment_text == "":
    #         print('md无识别出mention')
    #     if len(bert_ner_text) > len(segment_text):
    #         final_text = bert_ner_text
    #         final_text_type = bert_ner_text_type
    #     else:
    #         final_text = segment_text
    #         final_text_type = segment_text_type
    #     el_result = el(final_text, final_text_type)
    #     return el_result.keys()

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():  # 参数args是一个字典，比如：{'气短': ['symptom'], '烦热': ['symptom']}
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]  # 刚开始，entity_dict是空
                else:
                    entity_dict[type].append(arg)  # 之后，追加到endtity_dict中

        return entity_dict

    '''解析主函数'''

    def parser_main(self, res_classify, sent):
        args = res_classify['args']  # 问题提及的实体，用文本字符string:实体类型 包成一个字典
        print('test---fun:parser_main,para--args', args)
        entity_dict = self.build_entitydict(args)  # {'symptom': ['气短', '烦热']}
        question_types = res_classify['question_types']  # 问题意图，是一个列表
        sqls = []
        if list(args.keys())[0] == "KG没有对应实体":  # 20211115
            return sqls  # 返回空sql
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                # hzp 改 用实体链接的结果 pass
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)
                # sql = self.sql_transfer(question_type, [self.entity_linking(sent, args)], sent)
            elif question_type == 'symptom_disease':
                # hzp 改 用实体链接的结果 pass
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'), sent)
                # sql = self.sql_transfer(question_type, [self.entity_linking(sent, args)], sent)

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'disease_acompany':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'food_not_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'), sent)

            elif question_type == 'food_do_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'), sent)

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'), sent)

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'), sent)

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'disease_lasttime':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'disease_cureprob':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'disease_easyget':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), sent)

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    '''https://neo4j.com/docs/cypher-manual/current/clauses/match/'''

    def sql_transfer(self, question_type, entities, sent):
        if not (entities or question_type == 'symptom_disease'):
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name as hname, m.cause as tname".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name as hname, m.prevent as tname".format(i) for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'disease_lasttime':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name as hname, m.cure_lasttime as tname".format(i) for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'disease_cureprob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name as hname, m.cured_prob as tname".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name as hname, m.cure_way as tname".format(i) for i in entities]

        # 查询疾病的易发人群
        elif question_type == 'disease_easyget':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name as hname, m.easy_get as tname".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name as hname, m.desc as tname".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        # 20210823 修改为支持取症状交集返回答案
        elif question_type == 'symptom_disease':
            # 列表表达式
            '''
            比如entities是:['气短','烦热']
            sql得到:["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '气短' return m.name, r.name, n.name", 
            "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '烦热' return m.name, r.name, n.name"]
            '''
            if not entities:
                cnt = 0
            else:
                cnt = len(entities)
            if cnt == 0:
                # 用训练好的sbert去做相似度匹配（语义上的模糊匹配而非字面上的精确匹配）20210824
                model = SBert()
                model.load_embedding()
                top1_symptom = model.search(sent)
                sql = ["match (d:Disease)-[r:has_symptom]-(s1:Symptom) where s1.name='{0}'  return DISTINCT r.name as rname,d.name as tname,s1.name as hname".format(top1_symptom)]
            elif cnt == 1:
                i = entities[0]
                sql = ["match (d:Disease)-[r:has_symptom]-(s1:Symptom) where s1.name='{0}'  return DISTINCT r.name as rname,d.name as tname,s1.name as hname".format(i)]
            elif cnt == 2:
                i = entities[0]
                j = entities[1]
                sql = [
                    "match (d:Disease)-[r1:has_symptom]-(s1:Symptom),(d:Disease)-[r2:has_symptom]-(s2:Symptom) where s1.name='{0}' and  s2.name='{1}'  return DISTINCT r1.name as rname, d.name as tname,s1.name as hname1,s2.name as hname2".format(
                        i, j)]
            elif cnt == 3:
                i = entities[0]
                j = entities[1]
                k = entities[2]
                sql = [
                    "match (d:Disease)-[r1:has_symptom]-(s1:Symptom),(d:Disease)-[r2:has_symptom]-(s2:Symptom),(d:Disease)-[r3:has_symptom]-(s3:Symptom) where s1.name='{0}' and  s2.name='{1}' and  s3.name='{2}'  return DISTINCT r1.name as rname, d.name as tname,s1.name as hname1,s2.name as hname2, s3.name as hname3".format(
                        i, j, k)]
            elif cnt == 4:
                i = entities[0]
                j = entities[1]
                k = entities[2]
                l = entities[3]
                sql = [
                    "match (d:Disease)-[r:has_symptom]-(s1:Symptom),(d:Disease)-[:has_symptom]-(s2:Symptom),(d:Disease)-[:has_symptom]-(s3:Symptom),(d:Disease)-[:has_symptom]-(s4:Symptom) where s1.name='{0}' and  s2.name='{1}' and  s3.name='{2}' and  s4.name='{3}'  return DISTINCT d.name,s1.name,s2.name,s3.name,s4.name".format(
                        i, j, k, l)]
            else:
                # 最多支持到5个症状的描述
                entities = entities[0:5]
                i = entities[0]
                j = entities[1]
                k = entities[2]
                l = entities[3]
                m = entities[4]
                sql = [
                    "match (d:Disease)-[r:has_symptom]-(s1:Symptom),(d:Disease)-[:has_symptom]-(s2:Symptom),(d:Disease)-[:has_symptom]-(s3:Symptom),(d:Disease)-[:has_symptom]-(s4:Symptom),(d:Disease)-[:has_symptom]-(s5:Symptom) where s1.name='{0}' and  s2.name='{1}' and  s3.name='{2}' and  s4.name='{3}' and  s5.name='{4}'  return DISTINCT d.name,s1.name,s2.name,s3.name,s4.name,s5.name".format(
                        i, j, k, l, m)]

        # # 查询症状会导致哪些疾病  20210811
        # elif question_type == 'symptoms_disease':
        #     if len(entities) == 2:
        #         i = entities[0]
        #         j = entities[1]
        #         sql = ["MATCH p = (n1)<-[r1:has_symptom]-(m)-[r2:has_symptom]->(n2) where n1.name = '{0}' and n2.name = '{1}' return m.name,n1.name,n2.name".format(i, j)]

        # 查询疾病的并发症
        elif question_type == 'disease_acompany':
            sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]
            sql = sql1

        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]
            # sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1

        # 已知忌口查疾病
        elif question_type == 'food_not_disease':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]

        # 已知推荐查疾病
        elif question_type == 'food_do_disease':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]
            # sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            # sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]
            sql = sql2

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            # sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name as hname , r.name as rname, n.name as tname ".format(i) for i in entities]
            sql = sql2
        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name as hname, r.name as rname, n.name as tname".format(i) for i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
