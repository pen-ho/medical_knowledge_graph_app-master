# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer, util
from el_model.entity_linking import entity_linking
import os
import csv
import time
import torch
import pickle
import codecs

'''
人名:nr
地名:ns
机构名:nt

'''


# 获取实体信息
def get_ner_info(nature):
    if nature == 'nr':
        return 'nr'
    if nature == 'ns':
        return 'ns'
    if nature == 'nt':
        return 'nt'
    if nature == 'nm':
        return 'nm'
    if nature == 'nnt':
        return 'nnt'


def get_detail_ner_info(nature):
    if nature == 'nr':
        return '人物'
    if nature == 'ns':
        return '地名'
    if nature == 'nt':
        return '机构'
    if nature == 'nm':
        return '电影名'
    if nature == 'nnt':
        return '演员名'


def get_ner(word_nature):
    ner_list = []
    for term in word_nature:
        word = term.word
        pos = str(term.nature)
        if pos.startswith('nr'):
            ner_list.append([word, 'nr'])
        elif pos.startswith('ns'):
            ner_list.append([word, 'ns'])
        elif pos.startswith('nt'):
            ner_list.append([word, 'nt'])
        elif pos.startswith('nm'):
            ner_list.append([word, 'nm'])
        elif pos.startswith('nnt'):
            ner_list.append([word, 'nnt'])
        else:
            ner_list.append([word, 0])
    return ner_list


def el(inp_question,inp_question_type):
    """
    输入提及词mention,返回目标的kg实体 hzp
    用sentence-bert做语义相似度匹配
    然后结合mention 和 predict_entity的overlab，最长那个作为最终的预测kg实体。
    :return: {'藿香正气水': ['drug']}
    """
    el_result = entity_linking(inp_question, inp_question_type)
    return el_result
