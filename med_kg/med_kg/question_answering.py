# -*- coding:utf-8 -*-
import torch
import torch.nn.functional as F
from django.shortcuts import render
from util.pre_load import neo4jconn, classifier, parser
# from util.pre_load import segment


# , model_dict, name_dict, category_dict

# model, words, classes, index_classes = model_dict
# model.eval()

# actor_name_dict, movie_name_dict = name_dict[0], name_dict[1]


def question_answering(request):
    """
    qa的主入口函数，在urls.py中定义 hzp
    :param request:
    :return:
    """
    context = {'ctx': ''}
    if (request.GET):
        question = request.GET['question']
        # question = question[:300]
        # 移除空格
        question = question.strip()
        question = question.lower()

        word_nature = segment.seg(question)
        print('word_nature:{}'.format(word_nature))
        classfication_num = chatbot_response(word_nature)  # 模型意图识别模型是基于CBOW的分类 问题意图一共有16个 intent_classification/classification_data/question_classification.txt
        print('类别：{}'.format(classfication_num))
        # 实体识别

        # 返回格式：答案和关系图{‘answer':[], 'result':[]}
        if classfication_num == 0:
            word = ''
            for term in word_nature:
                if str(term.nature) == 'nm':
                    word = movie_name_dict[term.word]
                    ret_dict = neo4jconn.movie_rate(word)
                    break
            if word == '':
                ret_dict = []
        elif classfication_num == 1:
            word = ''
            for term in word_nature:
                if str(term.nature) == 'nm':
                    word = movie_name_dict[term.word]
                    ret_dict = neo4jconn.movie_showtime(word)
                    print('test-', ret_dict)
                    break
            if word == '':
                ret_dict = []

        elif classfication_num == 2:
            word = ''
            for term in word_nature:
                if str(term.nature) == 'nm':
                    word = movie_name_dict[term.word]
                    ret_dict = neo4jconn.movie_category(word)
                    break
            if word == '':
                ret_dict = []

        elif classfication_num == 3:
            ret_dict = {}

        elif classfication_num == 4:
            word = ''
            for term in word_nature:
                if str(term.nature) == 'nm':
                    word = movie_name_dict[term.word]
                    ret_dict = neo4jconn.movie_actors(word)
                    print('test-', ret_dict)
                    break
            if word == '':
                ret_dict = []

        elif classfication_num == 5:
            ret_dict = {}

        elif classfication_num == 6:
            name = ''
            category = ''
            for term in word_nature:
                if str(term.nature) == 'nnt':
                    name = actor_name_dict[term.word]
                elif str(term.nature) == 'ng':
                    if term.word in category_dict.keys():
                        category = category_dict[term.word]
                    else:
                        category = term.word
                if (name != '') and (category != ''):
                    break
            if (name != '') and (category != ''):
                ret_dict = neo4jconn.actor_category_movie(name, category)
            else:
                ret_dict = []

        elif classfication_num == 7:
            word = ''
            for term in word_nature:
                if str(term.nature) == 'nnt':
                    word = actor_name_dict[term.word]
                    ret_dict = neo4jconn.actor_movie(word)
                    break
            if word == '':
                ret_dict = []

        elif classfication_num == 8:
            name = ''
            rate = ''
            for term in word_nature:
                if str(term.nature) == 'nnt':
                    name = actor_name_dict[term.word]
                elif str(term.nature) == 'm':
                    rate = term.word
                if (name != '') and (rate != ''):
                    break
            if (name != '') and (rate != ''):
                ret_dict = neo4jconn.actor_gt_rate_movie(name, rate)
            else:
                ret_dict = []

        elif classfication_num == 9:
            name = ''
            rate = ''
            for term in word_nature:
                if str(term.nature) == 'nnt':
                    name = actor_name_dict[term.word]
                elif str(term.nature) == 'm':
                    rate = term.word
                if (name != '') and (rate != ''):
                    break
            if (name != '') and (rate != ''):
                ret_dict = neo4jconn.actor_lt_rate_movie(name, rate)
            else:
                ret_dict = []

        elif classfication_num == 10:
            word = ''
            for term in word_nature:
                if str(term.nature) == 'nnt':
                    word = actor_name_dict[term.word]
                    ret_dict = neo4jconn.actor_movie_category(word)
                    break
            if word == '':
                ret_dict = []

        elif classfication_num == 11:
            name1 = ''
            name2 = ''
            for term in word_nature:
                if str(term.nature) == 'nnt':
                    if name1 == '':
                        name1 = actor_name_dict[term.word]
                    else:
                        name2 = actor_name_dict[term.word]
                if (name1 != '') and (name2 != ''):
                    break
            if (name1 != '') and (name2 != ''):
                ret_dict = neo4jconn.actor_actor_movie(name1, name2)
            else:
                ret_dict = []

        elif classfication_num == 12:
            word = ''
            for term in word_nature:
                if str(term.nature) == 'nnt':
                    word = actor_name_dict[term.word]
                    ret_dict = neo4jconn.actor_movie_count(word)
                    break
            if word == '':
                ret_dict = []

        elif classfication_num == 13:
            ret_dict = {}

        elif classfication_num == 14:
            word = ''
            for term in word_nature:
                if str(term.nature) == 'm':
                    word = term.word
                    ret_dict = neo4jconn.gt_rate_movie(word)
                    break
            if word == '':
                ret_dict = []

        elif classfication_num == 15:
            rate = ''
            category = ''
            for term in word_nature:
                if str(term.nature) == 'm':
                    rate = term.word
                elif str(term.nature) == 'ng':
                    if term.word in category_dict.keys():
                        category = category_dict[term.word]
                    else:
                        category = term.word

                if (rate != '') and (category != ''):
                    break
            if (rate != '') and (category != ''):
                ret_dict = neo4jconn.gt_rate_category_movie(rate, category)
            else:
                ret_dict = []

        if (len(ret_dict) != 0):
            return render(request, 'question_answering.html', {'ret': ret_dict})

        return render(request, 'question_answering.html', {'ctx': '暂未找到答案'})

    return render(request, 'question_answering.html', context)


# 分词，需要将电影名，演员名和评分数字转为nm，nnt，ng
def _sentence_segment(word_nature):
    sentence_words = []
    for term in word_nature:
        if str(term.nature) == 'nnt':
            sentence_words.append('nnt')
        elif str(term.nature) == 'nm':
            sentence_words.append('nm')
        elif str(term.nature) == 'ng':
            sentence_words.append('ng')
        elif str(term.nature) == 'm':
            sentence_words.append('x')
        else:
            sentence_words.append(term.word)
    return sentence_words


def _bow(word_nature, show_detail=True):
    sentence_words = _sentence_segment(word_nature)
    # 词袋
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1  # 词在词典中
            if show_detail:
                print("found in bag:{}".format(w))
    return [bag]


def _predict_class(word_nature):
    sentence_bag = _bow(word_nature, False)
    with torch.no_grad():
        outputs = model(torch.FloatTensor(sentence_bag))
    # print('outputs:{}'.format(outputs))
    predicted_prob, predicted_index = torch.max(F.softmax(outputs, 1), 1)  # 预测最大类别的概率与索引
    # print('softmax_prob:{}'.format(predicted_prob))
    # print('softmax_index:{}'.format(predicted_index))
    results = []
    # results.append({'intent': index_classes[predicted_index.detach().numpy()[0]], 'prob': predicted_prob.detach().numpy()[0]})
    results.append({'intent': predicted_index.detach().numpy()[0], 'prob': predicted_prob.detach().numpy()[0]})
    # print('result:{}'.format(results))
    return results


def _get_response(predict_result):
    tag = predict_result[0]['intent']
    return tag


# 和intent_classification/pytorch/feedforward_network/predict.ipynb 中的方法一致，就是输入问题，给模型进行预测的过程 hzp
def chatbot_response(word_nature):
    predict_result = _predict_class(word_nature)
    print(predict_result)
    res = _get_response(predict_result)
    print(res)
    return res


# 下面是引入 med基于提问词和sbert的问答系统 hzp
def question_answering_med(request):
    """
    qa的主入口函数，在urls.py中定义 hzp
    :param request:
    :return:
    """
    context = {'ctx': ''}
    if (request.GET):
        question = request.GET['question']
        # question = question[:300]
        # 移除空格
        question = question.strip()
        question = question.lower()

        ret_dict = []
        # 主函数 （用分类器对问题意图分类，解析器对意图转SQL）
        ret_dict = neo4jconn.gt_med_answer(question,classifier,parser)

        if (len(ret_dict) != 0):
            return render(request, 'question_answering.html', {'ret': ret_dict}) # 回调函数

        return render(request, 'question_answering.html', {'ctx': '暂未找到答案'})

    return render(request, 'question_answering.html', context)
