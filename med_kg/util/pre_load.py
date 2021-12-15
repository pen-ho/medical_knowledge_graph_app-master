# -*- coding: utf-8 -*-
# from pyhanlp import HanLP
from Model.neo4j_models import Neo4j_Handle
from MedModel.question_classifier import QuestionClassifier
from MedModel.question_parser import QuestionPaser


import torch
import torch.nn as nn
import pickle
import os


# 初始化模型
def init_model():
    words_path = os.path.join(os.getcwd() + '/util', 'words.pkl')  # getcwd 当前路径的文本
    with open(words_path, 'rb') as f_words:
        words = pickle.load(f_words)

    classes_path = os.path.join(os.getcwd() + '/util', "classes.pkl")
    with open(classes_path, 'rb') as f_classes:
        classes = pickle.load(f_classes)

    classes_index_path = os.path.join(os.getcwd() + '/util', "classes_index.pkl")
    with open(classes_index_path, 'rb') as f_classes_index:
        classes_index = pickle.load(f_classes_index)

    index_classes = dict(zip(classes_index.keys(), classes_index.values()))

    # 定义分类模型
    class classifyModel(nn.Module):

        def __init__(self):
            super(classifyModel, self).__init__()
            self.model = nn.Sequential(
                nn.Linear(len(words), 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, 64),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(64, len(classes)))

        def forward(self, x):
            out = self.model(x)
            return out

    model = classifyModel()
    model_path = os.path.join(os.getcwd() + '/util', "model.h5")  # 模型参数
    # 加载训练好的模型
    model.load_state_dict(torch.load(model_path))
    return model, words, classes, index_classes


# 初始化pyhanlp
# def init_hanlp():
#     # 工具用法
#     # https://github.com/hankcs/HanLP/tree/1.x#8-%E7%94%A8%E6%88%B7%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AF%8D%E5%85%B8
#     segment = HanLP.newSegment().enableNameRecognize(True).enableOrganizationRecognize(True).enablePlaceRecognize(True).enableCustomDictionaryForcing(True)
#     return segment


# 初始化neo4j
def init_neo4j():
    neo4jconn = Neo4j_Handle()
    neo4jconn.connectNeo4j()
    return neo4jconn


# 加载演员名和电影名
def init_name_dict():
    root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    actor_path = os.path.join(root, 'data/custom_dict/演员名dict.txt')
    movie_path = os.path.join(root, 'data/custom_dict/电影名dict.txt')

    actor_name_dict = {}
    movie_name_dict = {}

    with open(actor_path, 'r', encoding='utf-8') as actor_read, open(movie_path, 'r', encoding='utf-8') as movie_read:
        for line in actor_read:
            line = line.strip().split('#')
            actor_name_dict[line[1]] = line[0]
        for line in movie_read:
            line = line.strip().split('#')
            movie_name_dict[line[1]] = line[0]

    return actor_name_dict, movie_name_dict


# 加载电影类型名
def init_category_dict():
    root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    movie_category_path = os.path.join(root, 'data/custom_dict/电影类型dict.txt')

    movie_category = {}

    with open(movie_category_path, 'r', encoding='utf-8') as category_read:
        for line in category_read:
            line = line.strip().split(":")
            movie_category[line[0]] = line[2]
            movie_category[line[1]] = line[2]
    return movie_category


def init_classifier():
    classifier = QuestionClassifier()
    return classifier


def init_parser():
    parser = QuestionPaser()
    return parser


# 初始化
# segment = init_hanlp()

# 初始化
neo4jconn = init_neo4j()

# 初始化 med
classifier = init_classifier()
parser = init_parser()

# hzp 注释
# 初始化演员名和电影名
# name_dict = init_name_dict()
#
# # 初始化分类模型，词典等
# model_dict = init_model()
#
# # 初始化电影类型词典
# category_dict = init_category_dict()
