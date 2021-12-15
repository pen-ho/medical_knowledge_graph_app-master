#!/usr/bin/env python3
# coding: utf-8
# Author  : penho
# File    : build_self_data.py
# Date    : 2021-10-29

# baseline,使用这个api进行实体识别。https://zstp.pcl.ac.cn:8002/medicalner
import codecs
import json
import random


def buil_total():
    """
    用于硬匹配无法命中时，就用sbert语义模糊匹配
    """
    with codecs.open("question_type.tsv", "r", "utf-8") as f:
        question_type = []
        for line in f:
            if line.strip() != "":
                tmp = line.strip().replace('?', '？').lower()
                if '#' not in tmp:
                    question_type.append(tmp)
        print(len(question_type), question_type)
    with codecs.open("../../dict/disease.txt", "r", "utf-8") as f2:
        disease = []
        for line in f2:
            if line.strip() != "":
                tmp = line.strip().lower()
                disease.append(tmp)
        print('disease', len(disease), disease[:10])
    with codecs.open("../../dict/check.txt", "r", "utf-8") as f2:
        check = []
        for line in f2:
            if line.strip() != "":
                tmp = line.strip().lower()
                check.append(tmp)
        print('check', len(check), check[:10])
    with codecs.open("../../dict/drug.txt", "r", "utf-8") as f2:
        drug = []
        for line in f2:
            if line.strip() != "":
                tmp = line.strip().lower()
                drug.append(tmp)
        print('drug', len(drug), drug[:10])
    with codecs.open("../../dict/food.txt", "r", "utf-8") as f2:
        food = []
        for line in f2:
            if line.strip() != "":
                tmp = line.strip().lower()
                food.append(tmp)
        print('food', len(food), food[:10])
    with codecs.open("../../dict/symptom.txt", "r", "utf-8") as f2:
        symptom = []
        for line in f2:
            if line.strip() != "":
                tmp = line.strip().lower()
                symptom.append(tmp)
        print('symptom', len(symptom), symptom[:10])

    dataset = []
    cnt = 0
    file_out = open('total.json', 'w', encoding='utf-8')
    disease_type = []
    food_type = []
    symptom_type = []
    drug_type = []
    check_type = []
    for i in question_type:
        cnt += 1
        if '[disease]' in i:
            disease_type.append(i)
        elif '[food]' in i:
            food_type.append(i)
        elif '[symptom]' in i:
            symptom_type.append(i)
        elif '[drug]' in i:
            drug_type.append(i)
        elif '[check]' in i:
            check_type.append(i)
    assert len(question_type) == len(disease_type) + len(drug_type) + len(food_type) + len(check_type) + len(symptom_type)

    cnt = int(len(disease) / len(disease_type)) + 1
    print(len(disease), len(drug_type), cnt)
    cnt2 = int(len(symptom) / len(symptom_type)) + 1
    print(len(food), len(food_type), cnt2)
    cnt3 = int(len(drug) / len(drug_type)) + 1
    print(len(drug), len(drug_type), cnt3)
    cnt4 = int(len(check) / len(check_type)) + 1
    print(len(symptom), len(symptom_type), cnt4)
    cnt5 = int(len(food) / len(food_type)) + 1
    print(len(check), len(check_type), cnt5)
    c = 0
    for i in disease_type:  # 4个
        b = cnt * c
        e = cnt * (c + 1)
        for j in disease[b:e]:
            data_json = dict()
            o = i.replace('[disease]', j)
            data_json['text'] = o
            dic1 = dict()
            dic2 = dict()
            start = o.index(j)
            end = start + len(j)-1
            idx = list()
            idx.append(start)
            idx.append(end)
            dic2[j] = [idx]
            dic1['disease'] = dic2
            data_json['label'] = dic1
            file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')
        c += 1
    c = 0
    for i in symptom_type:  # 4个
        b = cnt2 * c
        e = cnt2 * (c + 1)
        for j in symptom[b:e]:
            data_json = dict()
            o = i.replace('[symptom]', j)
            data_json['text'] = o
            dic1 = dict()
            dic2 = dict()
            start = o.index(j)
            end = start + len(j)-1
            idx = list()
            idx.append(start)
            idx.append(end)
            dic2[j] = [idx]
            dic1['symptom'] = dic2
            data_json['label'] = dic1
            file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')
        c += 1

    c = 0
    for i in drug_type:  # 4个
        b = cnt3 * c
        e = cnt3 * (c + 1)
        for j in drug[b:e]:
            data_json = dict()
            o = i.replace('[drug]', j)
            data_json['text'] = o
            dic1 = dict()
            dic2 = dict()
            start = o.index(j)
            end = start + len(j)-1
            idx = list()
            idx.append(start)
            idx.append(end)
            dic2[j] = [idx]
            dic1['drug'] = dic2
            data_json['label'] = dic1
            file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')
        c += 1

    c = 0
    for i in check_type:  # 4个
        b = cnt4 * c
        e = cnt4 * (c + 1)
        for j in check[b:e]:
            data_json = dict()
            o = i.replace('[check]', j)
            data_json['text'] = o
            dic1 = dict()
            dic2 = dict()
            start = o.index(j)
            end = start + len(j)-1
            idx = list()
            idx.append(start)
            idx.append(end)
            dic2[j] = [idx]
            dic1['check'] = dic2
            data_json['label'] = dic1
            file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')
        c += 1

    c = 0
    for i in food_type:  # 4个
        b = cnt5 * c
        e = cnt5 * (c + 1)
        for j in food[b:e]:
            data_json = dict()
            o = i.replace('[food]', j)
            data_json['text'] = o
            dic1 = dict()
            dic2 = dict()
            start = o.index(j)
            end = start + len(j)-1
            idx = list()
            idx.append(start)
            idx.append(end)
            dic2[j] = [idx]
            dic1['food'] = dic2
            data_json['label'] = dic1
            file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')
        c += 1
    file_out.close()


def buil_split_dataset():
    with codecs.open("total.json", "r", "utf-8") as f2:
        json = []
        for line in f2:
            if line.strip() != "":
                tmp = line.strip()
                json.append(tmp)
        random.shuffle(json) # 打乱列表
        l = len(json)
        cut = int(l * 0.8)
        cut2 = int(l * 0.9)
        train = json[:cut]
        valid = json[cut:cut2]
        test = json[cut2:]
        assert len(train) + len(test) + len(valid) == l
    with codecs.open("train.json", "w") as f3:
        for item in train:
            f3.write(item + "\n")
    with codecs.open("valid.json", "w") as f3:
        for item in valid:
            f3.write(item + "\n")
    with codecs.open("test.json", "w") as f3:
        for item in test:
            f3.write(item + "\n")


# buil_total()

# 打算然后按 80：10：10分配数据。


# str = '妊娠合并梅毒这个病的简介有吗？'
# j = '妊娠合并梅毒'
# dic = dict()
# start = str.index(j)
# end = start + len(j)-1
# idx = list()
# idx.append(start)
# idx.append(end)
# print(idx)
# dic[j] = idx
# print(dic)

buil_split_dataset()
