#!/usr/bin/env python3
# coding: utf-8
# Author  : penho
# File    : test_neo4j_models.py
# Date    : 2021-09-16
from util.pre_load import neo4jconn, classifier, parser


def test():
    # ans = neo4jconn.gt_med_answer(question="百日咳有什么症状？")
    # ans = neo4jconn.gt_med_answer(question="经常鼻塞、打喷嚏是什么毛病？")
    # ans = neo4jconn.gt_med_answer(question="出现口苦、口干、口渴是什么毛病？")
    # ans = neo4jconn.gt_med_answer(question="甲状腺结节需要做什么检查？")
    # ans = neo4jconn.gt_med_answer("小儿感冒了，有什么食物推荐吗？", classifier, parser)
    # ans = neo4jconn.gt_med_answer("糖尿病会有什么并发症？", classifier, parser)
    # ans = neo4jconn.gt_med_answer("糖尿病有什么需要忌吃的？", classifier, parser)
    # ans = neo4jconn.gt_med_answer("眼睛干涩是什么毛病？", classifier, parser)
    # ans = neo4jconn.gt_med_answer("感冒灵颗粒可以治疗什么疾病？", classifier, parser)

    # disease_cause pass
    # ans = neo4jconn.gt_med_answer("感冒的原因是什么？", classifier, parser)
    # ans = neo4jconn.gt_med_answer("为什么有的人会失眠？", classifier, parser)

    # disease_acompany
    # ans = neo4jconn.gt_med_answer("失眠的并发症有哪些？", classifier, parser)

    # disease_prevent

    # print(ans)

    # 高血压要怎么治？
    # ans = neo4jconn.gt_med_answer("哪些人不能吃芒果？", classifier, parser)

    # 食欲不振怎么办？ syptom_disease  disease_crue
    ans = neo4jconn.gt_med_answer("糖尿病能治好吗？", classifier, parser)

    # 食欲不振怎么办？ syptom_disease  disease_crue
    ans = neo4jconn.gt_med_answer("皮肤痒是什么毛病？", classifier, parser)

    print(ans)


if __name__ == '__main__':
    test()
