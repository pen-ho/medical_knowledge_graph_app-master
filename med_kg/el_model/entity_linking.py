#!/usr/bin/env python3
# coding: utf-8
# Author  : penho
# File    : entity_linking.py
# Date    : 2021-11-12
import pickle
import torch
from sentence_transformers import SentenceTransformer, util
import os
import csv
import time
import codecs


def entity_linking(inp_question, inp_question_type):
    """
    输入提及词mention,返回目标的kg实体 hzp
    用sentence-bert做语义相似度匹配
    然后结合mention 和 predict_entity的overlab重叠词，最长那个作为最终的预测kg实体。
    :return: {'藿香正气水': ['drug']}
    """
    if inp_question_type == 'symptom':
        with open('med_kg/el_model/embedding/symptom_embeddings.pkl', "rb") as fIn:
            stored_data = pickle.loads(fIn.read())
            stored_sentences = stored_data['sentences']
            stored_embeddings = stored_data['embeddings']
    elif inp_question_type == 'disease':
        with open('med_kg/el_model/embedding/disease_embeddings.pkl', "rb") as fIn:
            stored_data = pickle.loads(fIn.read())
            stored_sentences = stored_data['sentences']
            stored_embeddings = stored_data['embeddings']
    elif inp_question_type == 'drug' or inp_question_type == 'producer':
        with open('med_kg/el_model/embedding/drug_embeddings.pkl', "rb") as fIn:
            stored_data = pickle.loads(fIn.read())
            stored_sentences = stored_data['sentences']
            stored_embeddings = stored_data['embeddings']
    else:
        overlab_top_1 = '没有识别出预测提及词的类型'
        print('overlab_top_1',overlab_top_1)
        stored_embeddings = ""

    model_name = 'quora-distilbert-multilingual'
    model = SentenceTransformer(model_name)
    start_time = time.time()
    if inp_question != "":
        question_embedding = model.encode(inp_question, convert_to_tensor=True)
    else:
        question_embedding = ""
    if stored_embeddings != "" and question_embedding != "":
        hits = util.semantic_search(question_embedding, stored_embeddings, top_k=20)
    else:
        overlab_top_1 = '没有识别到mention'
        return overlab_top_1
    end_time = time.time()
    hits = hits[0]  # Get the hits for the first query
    dic = {}
    t_c_list = []
    result = {}
    print("Input question:", inp_question)
    for c in inp_question:
        t_c_list.append(c)
    t_c_list = list(set(t_c_list))
    print("Results (after {:.3f} seconds):".format(end_time - start_time))
    for hit in hits[0:20]:
        print("\t{:.3f}\t{}".format(hit['score'], stored_sentences[hit['corpus_id']]))
        txt = stored_sentences[hit['corpus_id']]
        cnt = 0
        for c in t_c_list:
            if txt.find(c) != -1:
                cnt += 1
        # print(cnt, txt)
        dic[txt] = cnt
    # print(dic)
    dic_sorted = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
    print(float(dic_sorted[0][1]), len(inp_question) / 2.0)
    if float(dic_sorted[0][1]) >= len(inp_question) / 2.0:  # inp_question 比如眼睛干
        overlab_top_1 = dic_sorted[0][0]
    else:
        overlab_top_1 = 'KG没有对应实体'
    # print(dic_sorted[0][0])
    result[overlab_top_1] = [inp_question_type]
    return result

# 测试
# print(entity_linking("眼睛干","symptom"))
# print(entity_linking("眼干涩","symptom"))
# print(entity_linking("眼睛干涩","symptom"))
# print(entity_linking("屁股痕痒","symptom"))
# print(entity_linking("喷嚏","symptom"))
# print(entity_linking("藿香正气液","drug"))
# print(entity_linking("鼻黏膜肿胀","symptom"))
