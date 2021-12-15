# -*- coding: utf-8 -*-
import sys

sys.path.append("../../")

from django.shortcuts import render
from ner_model.predict_ner import predict_med_ner

# from util.pre_load import segment
from util.pre_load import classifier
from util.nlp_ner import el


# 分词+词性+实体识别
def ner_post(request):
    ctx = {}
    if request.POST:
        # 获取输入文本
        input_text = request.POST['user_text']

        # input_text = input_text[:300]
        # # 移除空格
        # input_text = input_text.strip()
        # # 分词
        # word_nature = segment.seg(input_text)
        #
        # text = ""
        # # 实体识别
        # ner_list = get_ner(word_nature)
        # # 遍历输出
        # for pair in ner_list:
        #     if pair[1] == 0:
        #         text += pair[0]
        #         continue
        #     # text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_ner_info(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
        #     if pair[1] == 'nr':  # 人物
        #         text += "<a style='color:blue'   data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_ner_info(
        #             pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
        #     elif pair[1] == 'ns':  # 地名
        #         text += "<a style='color:red'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_ner_info(
        #             pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
        #     elif pair[1] == 'nt':  # 机构
        #         text += "<a style='color:orange'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_ner_info(
        #             pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
        #     elif pair[1] == 'nm':  # 电影名
        #         text += "<a style='color:yellow'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_ner_info(
        #             pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
        #     else:  # 演员名
        #         text += "<a style='color:green'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_ner_info(
        #             pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
        #
        # ctx['rlt'] = text
        # '''
        # 分词及词性
        # 设置显示格式
        # '''
        # # 获取词和词性
        # seg_word = list(term.word + " <strong><small>[" + str(term.nature) + "]</small></strong> " for term in word_nature)
        # seg_word = ''.join(seg_word)
        # ctx['seg_word'] = seg_word

        # hzp  用训练好的ner模型预测 20211112
        input_text = input_text[:512]
        input_text = input_text.strip()

        # 基于领域词典分词 ac算法做匹配，这里还没有用最大逆向匹配哈。需要用一下。todo
        # output_text_segment = classifier.classify(input_text)
        medical_dict = classifier.check_medical(input_text)
        # 基于自建数据上精调好的 BERT+CRF 模型
        output_text = predict_med_ner(input_text)
        bert_ner_text = ""
        bert_ner_text_type = ""
        segment_text = ""
        segment_text_type = ""
        if output_text != "无识别出mention":
            bert_ner_text = output_text.split(':')[0]
            bert_ner_text_type = output_text.split(':')[1]
        if len(medical_dict.keys()) != 0:
            segment_text = str([k for k in medical_dict.keys()][0])
            segment_text_type = str([k for k in medical_dict.values()][0][0])
        print(segment_text, segment_text_type, bert_ner_text, bert_ner_text_type)
        if bert_ner_text == "" and segment_text == "":
            ctx['el_result'] = '无识别出mention'
        if len(bert_ner_text) > len(segment_text) or segment_text == 'KG没有对应实体':
            final_text = bert_ner_text
            final_text_type = bert_ner_text_type
        else:
            final_text = segment_text
            final_text_type = segment_text_type
        print(final_text, final_text_type)
        ctx['self_trained_ner'] = 'BERT-CRF预测：' + '{' + str(output_text) + '}' + '，词典分词最大匹配：' + str(segment_text) + '，取较长作为提及词：{' + final_text + ':' + final_text_type + '}'
        print(ctx)

        # 实体链接结果
        el_result = el(final_text, final_text_type)
        print(el_result)
        ctx['el_result'] = str(el_result.keys())
        print(ctx)
    return render(request, "index.html", ctx)

# def test_ner_view():
#     sent_list = ["眼干是什么毛病？", "眼睛干是什么毛病？", "眼干涩是什么毛病？", "屁股痕痒是什么毛病？",
#                  "999皮炎平可以治疗什么疾病？",
#                  "力度伸可以治疗什么疾病？"]
#     ctx = {}
#     for input_text in sent_list:
#         output_text_segment = classifier.classify(input_text)
#         output_text = predict_med_ner(input_text)
#         final_text = ""
#         final_text_type = ""
#         bert_ner_text = ""
#         segment_text = ""
#         if output_text != "无识别出实体":
#             bert_ner_text = output_text.split(':')[0]
#             bert_ner_text_type = output_text.split(':')[1]
#         if len(output_text_segment['args'].keys()) != 0:
#             segment_text = str([k for k in output_text_segment['args'].keys()][0])
#             segment_text_type = str([k for k in output_text_segment['args'].values()][0][0])
#         if len(bert_ner_text) > len(segment_text):
#             final_text = bert_ner_text
#             final_text_type = bert_ner_text_type
#         else:
#             final_text = segment_text
#             final_text_type = segment_text_type
#         print(final_text, final_text_type)
#         ctx['self_trained_ner'] = 'BERT-CRF预测：' + '{' + str(output_text) + '}' + '，词典分词最大匹配：' + str(output_text_segment['args']) + '，取较长作为提及词：{' + final_text + ':' + final_text_type + '}'
#         print(ctx)

# test_ner_view()

# dic = {'皮炎': ['disease', 'symptom']}
# dic_1 = {}
# print([i for i in dic.values()])
# print([k for k in dic.keys()][0])
# if len(dic_1.keys()) != 0:
#     print(1)
