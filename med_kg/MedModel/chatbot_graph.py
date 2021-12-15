#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是医药智能助理。你的问题无法精确回复，可以从以下链接http://so.xywy.com/进一步了解，或反馈人工客服。祝您身体健康。'
        # 得到问句的提及实体和问句的意图 {'args': {'气短': ['symptom'], '烦热': ['symptom']}, 'question_types': ['symptom_disease']}
        res_classify = self.classifier.classify(sent)
        if not res_classify: # 问句的意图类型 和 领域词 都找不到，直接给出无法回答的提示
            return answer
        res_sql = self.parser.parser_main(res_classify,sent) # 根据提及实体和问句意图得到查询的sql
        print(res_sql)
        final_answers = self.searcher.search_main(res_sql)  # 执行sql得到答案
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小助手:', answer)

