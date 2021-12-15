#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
import ahocorasick
from util.nlp_ner import el
from ner_model.predict_ner import predict_med_ner


class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.department_path = os.path.join(cur_dir, 'dict/department.txt')  # 科室
        self.check_path = os.path.join(cur_dir, 'dict/check.txt')  # 检查项目
        self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')  # 药品
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')  # 食物
        self.producer_path = os.path.join(cur_dir, 'dict/producer.txt')  # 在售药品
        self.symptom_path = os.path.join(cur_dir, 'dict/symptom.txt')  # 症状 重新创建过这个文件
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')
        # 加载特征词
        self.disease_wds = [i.strip() for i in open(self.disease_path) if i.strip()]
        self.department_wds = [i.strip() for i in open(self.department_path) if i.strip()]
        self.check_wds = [i.strip() for i in open(self.check_path) if i.strip()]
        self.drug_wds = [i.strip() for i in open(self.drug_path) if i.strip()]
        self.food_wds = [i.strip() for i in open(self.food_path) if i.strip()]
        self.producer_wds = [i.strip() for i in open(self.producer_path) if i.strip()]
        self.symptom_wds = [i.strip() for i in open(self.symptom_path) if i.strip()]

        # 将上面各个文件中的关键字加入到领域词典
        self.region_words = set(self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.producer_wds + self.symptom_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path) if i.strip()]

        # 构造领域actree
        # 包括所有医疗领域关键词：科室、疾病、药品、在售药品、食物、症状、科室 放入ac算法树中(作为领域词) 如果问句没有一个词在领域词中，则直接返回无法回答。
        self.region_tree = self.build_actree(list(self.region_words))

        # 构建词典（词：词类型）
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.disease_qwds = ['什么病', '什么回事', '什么问题', '什么毛病', '什么疾病', '毛病', '疾病', '问题']
        self.cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成', '病因']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片', '吃什么药']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医', '治愈概率', '治愈率']
        self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '容易', '染上', '得上']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']
        # 20210811 将某个疾病的患者的注意事项列出，
        # disease_desc, disease_cureway, disease_lasttime 是什么，怎么治疗，治疗多久
        # disease_drug 吃什么药
        # disease_do_food, disease_not_food,  吃了食物 不吃什么食物
        # disease_acompany 注意可能出现的并发症
        self.sicknotice_qwds = ['注意', '关注', '留心', '小心', '留意', '照顾']

        print('model init finished ......')

        return

    def entity_linking(self, sent, args):
        """
        args：medical_dict领域词典，有可能识别出多个或者一个症状。
        目前逻辑：
            ner模型只是出一个提及词及它的类型，
            而基于词典的ac算法可以匹配出一个或者多个词以及它们的类型，
            因此对于一个词的情况，结合ner和词典的结果，取长度长的。
            对于多个词的情况，直接用基于词典的ac算法模型。
        """
        output_text = predict_med_ner(sent)  # bert预测结果
        bert_ner_text = ""
        bert_ner_text_type = ""
        segment_text = ""
        segment_text_type = ""
        if output_text != "无识别出mention":
            bert_ner_text = output_text.split(':')[0].split('、')
            bert_ner_text_type = output_text.split(':')[1]
        print(bert_ner_text, args.keys())
        # assert(len(bert_ner_text) == len(args.keys())),'bert识别出来的领域词数 不等于 基于词典分词得到的领域词数'
        if len(args.keys()) != 0:
            # print('args', args)
            segment_text = [k for k in args.keys()]
            segment_text_type = [k for k in args.values()][0]
        print('segment_text', segment_text, 'segment_text_type', segment_text_type)
        print('bert_ner_text', bert_ner_text, 'bert_ner_text_type', bert_ner_text_type)

        if len(bert_ner_text) == 0 and len(segment_text) == 0:
            print('md无识别出mention')
        el_result_dit = dict()
        if len(bert_ner_text) <= len(segment_text):
            # 对于 鼻黏膜肿胀 和 肿胀 这种情况：
            if len(bert_ner_text) == len(segment_text):
                for item_a, item_b in zip(bert_ner_text, segment_text):
                    if len(item_a) > len(item_b):  # 取长度长那个,比如 鼻黏膜肿胀
                        el_result = el(item_a, bert_ner_text_type)
                        el_result_dit[list(el_result.keys())[0]] = list(el_result.values())[0]
                    else:
                        el_result_dit[item_b] = segment_text_type
            else:
                el_result_dit = args
        elif len(bert_ner_text) > len(segment_text):
            el_result = dict()
            for bert_ner_item in bert_ner_text:
                el_result = el(bert_ner_item, bert_ner_text_type)  # 返回是dict {'鼻塞': ['symptom']}
                el_result_dit[list(el_result.keys())[0]] = list(el_result.values())[0]
        # print('el_result_dit', el_result_dit)  # 返回完成实体链接的(症状/疾病/等)列表
        return el_result_dit

    '''分类主函数'''

    def classify(self, question):
        data = {}

        medical_dict = self.check_medical(question)  # 检查领域词典   {'藿香正气水': ['drug']}

        # 这里就要完成entity linking
        el_result = self.entity_linking(question, medical_dict)  # {'藿香正气水': ['drug']}

        data['args'] = el_result  # {'args': {'藿香正气水': ['drug']}}

        # print('func_classify_data', data)
        # 收集问句当中所涉及到的实体类型 ['symptom','disease',...]
        types = []  # 记录涉及领域词的类型，是疾病还是症状还是药品，等实体类型。
        print('res_el-entity', el_result)
        for type_ in el_result.values():
            types += type_

        question_types = []

        # 检查各类提问词，用提问词人工映射到问题意图
        # 症状 _qwds表示提问词。问句中包含提问词如"症状" 且 问句包含疾病类型的关键词如"湿疹" ，则映射到问句意图为 问疾病的症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):  # ('disease' in types)表示问题文本的词涉及疾病这个类型
            question_type = 'disease_symptom'
            question_types.append(question_type)

        # 原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)
        # 并发症
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)

        # 推荐食品
        if self.check_words(self.food_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)

        # 已知食物找疾病
        if self.check_words(self.food_qwds + self.cure_qwds, question) and 'food' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)

        # 推荐药品
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.check_words(self.cure_qwds, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.check_words(self.check_qwds, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)

        # 已知检查项目查相应疾病
        if self.check_words(self.check_qwds + self.cure_qwds, question) and 'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)

        # 症状防御
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        # 疾病医疗周期
        if self.check_words(self.lasttime_qwds, question) and 'disease' in types:
            question_type = 'disease_lasttime'
            question_types.append(question_type)

        # 疾病治疗方式
        if self.check_words(self.cureway_qwds, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)

        # 疾病治愈可能性
        if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)

        # 疾病易感染人群
        if self.check_words(self.easyget_qwds, question) and 'disease' in types:
            question_type = 'disease_easyget'
            question_types.append(question_type)

        # 20210811
        if self.check_words(self.sicknotice_qwds, question) and 'disease' in types:
            question_types = ['disease_desc', 'disease_cureway', 'disease_lasttime', 'disease_drug', 'disease_do_food', 'disease_not_food', 'disease_acompany']
            # disease_desc, disease_cureway, disease_lasttime 是什么，怎么治疗，治疗多久
            # disease_drug 吃什么药
            # disease_do_food, disease_not_food,  吃了食物 不吃什么食物
            # disease_acompany

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 20210909
        # 已知症状寻找可能疾病  第一种情况：有疾病提问词 和 症状领域词，or 第二种情况:只有疾病提问词（比如 什么毛病）
        if question_types == [] and (
                (self.check_words(self.disease_qwds, question) and ('symptom' in types))
                or
                (self.check_words(self.cureway_qwds, question) and ('symptom' in types))  # 有时候提问者 会把 有什么症状怎么办？  比如 食欲不振怎么办？
                or
                self.check_words(self.disease_qwds, question)  # 模糊描述症状  XXXX是什么毛病？
        ):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 将多个分类结果进行合并处理，组装成一个字典
        # hzp 211023 对于任何问题，只能对应一个问题类型。
        if len(question_types) > 0:
            data['question_types'] = [question_types[0]]
        else:
            data['question_types'] = []

        return data

    '''构造词对应的类型'''

    def build_wdtype_dict(self):
        wd_dict = dict()  # 构建{词：类型} 字典
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
        return wd_dict

    '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''

    def check_medical(self, question):
        region_wds = []  # 放问句提及的所有关键词
        for i in self.region_tree.iter(question):  # 返回的格式是(text_end_index,(insertion index,original string))
            wd = i[1][1]  # 提取ac树中的关键词
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:  # 如果字符串存在包含，则将短的作为停用词。比如"睾丸胀痛"包含"胀痛"，则忽略"胀痛"
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]  # 返回不在停用词列表但在领域词中的词
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}  # 得到不在停用词但在领域词的字典

        return final_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
