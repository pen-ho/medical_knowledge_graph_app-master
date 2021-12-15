# coding:utf-8

import ahocorasick
import pandas as pd
import os, json


# 测试 从症状文本中抽取指定症状列表项 20210820
# AC算法介绍参考：https://zhuanlan.zhihu.com/p/65424670

def extract_symptom_from_symptontxt():
    # create an Automaton:
    A = ahocorasick.Automaton()

    # 拿到所有症状名
    df_all_symptom = pd.read_csv('./data/output/symptom_name.tsv', names=["id", "symptom_name"], sep='\t', encoding='utf_8')
    i = 0
    for i, r in df_all_symptom.iterrows():
        # if i < 10:
        #     i += 1
        # print(i + 1)
        idx = r['id']
        key = r['symptom_name']
        print(idx, key)
        A.add_word(key, (idx, key))

    # Now convert the trie to an Aho-Corasick automaton to enable Aho-Corasick search:
    A.make_automaton()

    # 遍历每个疾病症状
    df_disease = pd.read_csv('./data/disease_symptomtxt.tsv', names=["disease", "symptomtxt"], sep='\t', encoding='utf_8')
    file_out = open('./data/output/disease_symptom_ac.tsv', 'w', encoding='utf-8')  # 'a'-追加  'w'-从新写
    for j, r in df_disease.iterrows():
        # if j < 20:
        j += 1
        print(j)
        # 遍历行取出药名+适应症
        disease_name = r['disease']
        sentence = r['symptomtxt']
        print(sentence)

        # disease_name = '百日咳'
        # sentence = '根据接触史及典型的痉咳期表现，如无典型痉咳者可结合典型血象改变，' \
        #        '均可作出临床诊断，病原学诊断有赖于细菌培养和特异的血清学检查，对各年龄组不明原因的持续性咳嗽，' \
        #        '特别有痉咳症状者，均需考虑本病的可能，作进一步的检测。潜伏期3～21天，平均7～10天，典型临床经过分3期。' \
        #        '1、卡他期或称痉咳前期：起病时有咳嗽，打喷嚏，流涕，流泪，有低热或中度发热，类似感冒症状，' \
        #        '3～4天后症状消失，热退，但咳嗽逐渐加重，尤以夜间为重，此期传染性最强，可持续7～10天，若及时治疗，能有效地控制本病的发展。' \
        #        '2、痉咳期：卡他期未能控制，患者出现阵发性痉挛性咳嗽，其特点是频繁不间断的短咳10余声，如呼气状态，最后深长呼气，此时由于咳嗽而造成胸腔内负压，' \
        #        '加之吸气时，声带仍处于紧张状态，空气气流快速地通过狭窄的声门而发出一种鸡鸣样高音调的吸气声，接着又是一连串阵咳。如此反复发作，一次比一次加剧，直至咳出大量黏稠痰液和呕吐胃内容物而止，痉咳发作前有诱因，发作时常有喉痒，胸闷等不适预兆。' \
        #        '患儿预感痉咳来临时，表现恐惧，痉咳发作时表情是痛苦的。痉咳时由于胸腔内压力增加，上腔静脉回流受阻，颈静脉怒张，眼睑及颜面充血水肿，口唇发绀，眼结膜充血。如毛细血管破裂可引起球结膜下出血及鼻出血，有的患者舌向齿外伸，' \
        #        '与门齿摩擦，常见有舌系带溃疡，有的患者因阵咳，腹压增高使大小便失禁及出现疝症。此期如无并发症发生，一般持续2～6周，也有长达2个月或以上。婴幼儿和新生儿百日咳症状比较特殊，无典型痉咳，由于声门较小可因声带痉挛和黏稠分泌物的堵塞而发生呼吸暂停。' \
        #        '因缺氧而出现发绀，甚至于抽搐，亦可因窒息而死亡。成人或年长儿童，百日咳症状轻，而且不典型，主要表现为干咳，无阵发性痉咳，白细胞和淋巴细胞增加不明显，大多被误诊为支气管炎或上呼吸道感染。3、恢复期：阵发性痉咳次数逐渐减少至消失，持续2～3周好转痊愈，' \
        #        '若有并发肺炎，肺不张等常迁延不愈，可长达数周之久。支气管肺炎是常见的并发症，多发生在痉咳期，还可并发百日咳脑病，患者意识障碍，惊厥，但脑脊液无变化。'

        # for end_index, (insert_order, original_value) in A.iter(sentence): # iter方法返回从文本中识别关键字的尾索引
        #     start_index = end_index - len(original_value) + 1  # 通过尾索引-关键词长度+1 得到头索引
        #     print((start_index, end_index, (insert_order, original_value))) # 输出关键词所在文本的位置（头索引、尾索引）
        #     assert sentence[start_index:start_index + len(original_value)] == original_value

        print('-------')
        extract_symptom = set()
        for k in A.iter(sentence):
            # if not k:
            #     continue
            extract_symptom.add(k[1][1])  # 集合去重

        print(extract_symptom)

        # 写出结果
        if len(extract_symptom) == 0:
            continue
        file_out.write(disease_name + "\t" + str(extract_symptom) + "\n")


# 重新生成 disease_symptom 的知识图谱 20210820
def rebuild_medkg_disease_symptom():
    """
    把上面对齐的症状更新到data/medical.json文件中，新文件叫data/medical_rebuild.json
    然后调用build_medicalgraph.py
    """

    def update_medical_json():
        """
        把上面对齐的症状更新到data/medical.json文件中，新文件叫data/medical_rebuild.json
        """
        import json

        df_all_symptom = pd.read_csv('./data/output/disease_symptom_ac.tsv', names=["disease", "symptom"], sep='\t', encoding='utf_8')
        # i = 0
        res_dict = {}
        for i, r in df_all_symptom.iterrows():
            # if i < 10:
            #     i += 1
            # print(i + 1)
            d = r['disease']
            s = r['symptom']
            res_dict[d] = s
        print(len(res_dict))

        file_out = open('./data/medical_rebuild.json', 'w', encoding='utf-8')
        count = 0
        no_count = 0
        do_count = 0
        for data in open('./data/medical.json'):
            # if count > 10:
            #     break
            count += 1

            data_json = json.loads(data)  # json转字典
            # print(data_json['name'])
            disease_name = data_json['name']
            # 读d_s_ac.tsv 疾病 和 症状list,把症状list更新到原来json的症状list
            # 用disease_name找到tsv对应的症状list
            if disease_name in res_dict.keys():
                new_symptom = res_dict[disease_name][1:-1].replace("'", "").replace(" ", "").split(",")
                data_json['symptom'] = new_symptom
                print(data_json)
                do_count += 1
                file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')  # 不加参数ensure_ascii会有乱码
            else:
                print('记录' + str(count) + ':' + data_json['name'] + ' 没被更新')
                no_count += 1
                # file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')
        print('一共处理' + str(count) + '条疾病记录')
        print('一共处理' + str(do_count) + '条疾病记录（对齐症状库）被写入')
        print('一共处理' + str(no_count) + '条疾病记录（未对齐症状库）没被写入')

        pass

    update_medical_json()

    # 执行build_medicalgraph.py  把 medical.json 更替为 medical_rebuild.json
    pass


def create_medical_add_symptomtxt(result_dict):
    """
    hzp 20210812
    创建一个追加了疾病具体症状文本的json文件，在原来的文件medical.json基础上
    # result_dict：输入字典{'disease':'symptomtxt'}
    """
    # import pandas as pd
    # result = pd.read_json('../data/medical.json')
    # print(result[:1]) ValueError: Trailing data
    import json

    # 拿到所有症状名

    file_out = open('../data/medical_addsymptomtext.json', 'w', encoding='utf-8')
    count = 0
    for data in open('../data/medical.json'):
        # if count > 10:
        #     break
        count += 1
        print(count)
        data_json = json.loads(data)  # json转字典
        print(data_json['name'])
        disease_name = data_json['name']
        if disease_name in result_dict.keys():
            symptom = result_dict[disease_name]
            data_json['symptomtxt'] = symptomtxt
        # print(data_json)
        file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')  # 不加参数ensure_ascii会有乱码

    file_out.close()


# create_medical_add_symptomtxt(result_dict)

def write_to_symptom_dict():
    """
    把新抽取的所有症状写入到领域词典，在用户输入问题时用于发现领域词
    """
    import codecs
    i = 0
    symptom_set = set()
    with codecs.open("data/output/disease_symptom_ac.tsv", "r", "utf-8") as f:
        for line in f:
            try:
                if line.strip() != "":
                    symptom_list = []
                    tmp = line.strip().split("\t")
                    symptom_list = tmp[1][1:-1].replace("'", "").split(",")
                    for item in symptom_list:
                        symptom_set.add(item.strip())
                    i += 1
            except IndexError:
                print(i)
        print(len(symptom_set))

    with codecs.open("dict/symptom.txt", "w") as f2:
        symptom_list = list(symptom_set)
        for item in symptom_list:
            f2.write(item + "\n")


# def matching_model_data_process():
#     """
#     用于硬匹配无法命中时，就用sbert语义模糊匹配
#     """
#     import codecs
#     with codecs.open("dict/symptom.txt", "r", "utf-8") as f:
#         symptom_list = []
#         for line in f:
#             if line.strip() != "":
#                 tmp = line.strip()
#                 symptom_list.append(tmp)
#         print(len(symptom_list))
#     with codecs.open("data/output/symptom_for_matching.txt", "w") as f2:
#         for item in symptom_list:
#             f2.write(item + "是什么毛病？" + "\n")


def test_pkuseg_medicine_and_synonyms():
    """
    hzp
    用了分词工具 和 近义词工具，由于词典太少很多词没有，所有效果一般。比如想找到痕痒近义词"瘙痒"，但是痕痒是OOV因此没找到，返回[]
    所以把提问转成近义词再去搜索KB的想法就没用。
    """
    # https://github.com/lancopku/pkuseg-python
    import pkuseg
    seg = pkuseg.pkuseg(model_name='medicine')  # 程序会自动下载所对应的细领域模型
    text = seg.cut('皮肤瘙痒，红肿是什么毛病？')  # 进行分词
    # ['皮肤', '痕痒', '，', '红肿', '是', '什么', '毛病', '？']
    print(text)

    import synonyms
    print("瘙痒: ", synonyms.nearby("瘙痒"))
    print("红肿: ", synonyms.nearby("红肿"))
    keywords = synonyms.keywords(
        "甲亢的临床表现包括甲状腺肿大、性情急躁、容易激动、失眠、两手颤动、怕热、多汗、皮肤潮湿，食欲亢进但却消瘦、体重减轻、心悸、脉快有力(脉率常在每分钟100次以上，休息及睡眠时仍快)、脉压增大(主要由于收缩压升高)、内分泌紊乱(如月经失调)以及无力、易疲劳、出现肢体近端肌萎缩等。其中脉率增快及脉压增大尤为重要，常可作为判断病情程度和治疗效果的重要标志。1、临床症状甲亢可发生于任何年龄，大多数年龄在20～40岁，一般女性比男性发病率高，约为4∶1，但是地方性甲状腺肿流行区，则女性稍多于男性，约为4∶3。青年女性常可出现青春期甲亢，症状较轻，有的人未经治疗，而在青春期过后也可自愈。老年病人较年轻者更易见“隐匿性”或“淡漠型”甲亢，其神经过敏和情绪症状较轻，突眼发生率也较少，甲亢时多系统受累，临床表现多变，20～40岁中青年发病较常见，但近年来老年甲亢不断增多，起病较慢，多有精神创伤史和家族史，发病后病程迁延，数年不愈，复发率高，并可发生多种并发症。")
    print(keywords)


def test_dict():
    dict = {'d.name': '月经病', 's1.name': '口干', 's2.name': '口苦'}
    value1 = dict.get('s1.name', '')
    value2 = dict.get('s2.name', '')
    value3 = dict.get('s3.name', '')
    value4 = dict.get('s4.name', '')
    value5 = dict.get('s5.name', '')
    s = {value1, value2, value3, value4, value5}
    s.remove('')
    desc = ','.join(s)
    print(s)
    print(desc)




def read_nodes():
    """
    读最原始的json文件
    """
    cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
    data_path = os.path.join(cur_dir, 'data/medical_rebuild.json')
    # 共７类节点 每类内部节点不重复
    drugs = []  # 药品
    foods = []  # 食物
    checks = []  # 检查
    departments = []  # 科室
    producers = []  # 药品大类
    diseases = []  # 疾病
    symptoms = []  # 症状

    disease_infos = []  # 疾病信息

    # 构建节点实体关系
    rels_department = []  # 科室－科室关系
    rels_noteat = []  # 疾病－忌吃食物关系
    rels_doeat = []  # 疾病－宜吃食物关系
    rels_recommandeat = []  # 疾病－推荐吃食物关系
    rels_commonddrug = []  # 疾病－通用药品关系
    rels_recommanddrug = []  # 疾病－热门药品关系
    rels_check = []  # 疾病－检查关系
    rels_drug_producer = []  # 厂商－药物关系

    rels_symptom = []  # 疾病症状关系
    rels_acompany = []  # 疾病并发关系
    rels_category = []  # 疾病与科室之间的关系

    count = 0
    for data in open(data_path):
        disease_dict = {}
        count += 1
        print(count)
        data_json = json.loads(data)
        disease = data_json['name']
        disease_dict['name'] = disease
        diseases.append(disease)
        disease_dict['desc'] = ''
        disease_dict['prevent'] = ''
        disease_dict['cause'] = ''
        disease_dict['easy_get'] = ''
        disease_dict['cure_department'] = ''
        disease_dict['cure_way'] = ''
        disease_dict['cure_lasttime'] = ''
        disease_dict['symptom'] = ''
        disease_dict['cured_prob'] = ''

        if 'symptom' in data_json:
            symptoms += data_json['symptom']
            for symptom in data_json['symptom']:
                rels_symptom.append([disease, symptom])

        if 'acompany' in data_json:
            for acompany in data_json['acompany']:
                rels_acompany.append([disease, acompany])

        if 'desc' in data_json:
            disease_dict['desc'] = data_json['desc']

        if 'prevent' in data_json:
            disease_dict['prevent'] = data_json['prevent']

        if 'cause' in data_json:
            disease_dict['cause'] = data_json['cause']

        if 'get_prob' in data_json:
            disease_dict['get_prob'] = data_json['get_prob']

        if 'easy_get' in data_json:
            disease_dict['easy_get'] = data_json['easy_get']

        if 'cure_department' in data_json:
            cure_department = data_json['cure_department']
            if len(cure_department) == 1:
                rels_category.append([disease, cure_department[0]])
            if len(cure_department) == 2:
                big = cure_department[0]
                small = cure_department[1]
                rels_department.append([small, big])
                rels_category.append([disease, small])

            disease_dict['cure_department'] = cure_department
            departments += cure_department

        if 'cure_way' in data_json:
            disease_dict['cure_way'] = data_json['cure_way']

        if 'cure_lasttime' in data_json:
            disease_dict['cure_lasttime'] = data_json['cure_lasttime']

        if 'cured_prob' in data_json:
            disease_dict['cured_prob'] = data_json['cured_prob']

        if 'common_drug' in data_json:
            common_drug = data_json['common_drug']
            for drug in common_drug:
                rels_commonddrug.append([disease, drug])
            drugs += common_drug

        if 'recommand_drug' in data_json:
            recommand_drug = data_json['recommand_drug']
            drugs += recommand_drug
            for drug in recommand_drug:
                rels_recommanddrug.append([disease, drug])

        if 'not_eat' in data_json:
            not_eat = data_json['not_eat']
            for _not in not_eat:
                rels_noteat.append([disease, _not])

            foods += not_eat
            do_eat = data_json['do_eat']
            for _do in do_eat:
                rels_doeat.append([disease, _do])

            foods += do_eat
            recommand_eat = data_json['recommand_eat']

            for _recommand in recommand_eat:
                rels_recommandeat.append([disease, _recommand])
            foods += recommand_eat

        if 'check' in data_json:
            check = data_json['check']
            for _check in check:
                rels_check.append([disease, _check])
            checks += check
        if 'drug_detail' in data_json:
            drug_detail = data_json['drug_detail']
            producer = [i.split('(')[0] for i in drug_detail]
            rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
            producers += producer
        disease_infos.append(disease_dict)
    return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases), disease_infos, \
           rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, \
           rels_symptom, rels_acompany, rels_category


if __name__ == '__main__':
    # 从症状文本中抽取指定症状列表项
    # 8803个疾病症状文本 有 8446个疾病有对齐的症状
    # extract_symptom_from_symptontxt()
    # rebuild_medkg_disease_symptom()

    # write_to_symptom_dict()

    # test_pkuseg_medicine_and_synonyms()

    # matching_model_data_process()

    # test_dict()

    Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = read_nodes()

    # 只要 Diseases Drugs Symptoms
    # 只要 rels_symptom rels_commonddrug

    dict_out = dict()
    item_list = []
    symptom_list = []
    disease_list = []
    drug_list = []
    # for i in rels_symptom:  # 99492
    for i in rels_symptom[:1000]:
        dict_item = dict()
        source = i[0]
        target = i[1]
        dict_item['relation'] = "症状"
        dict_item['source'] = source
        dict_item['target'] = target
        disease_list.append(source)
        symptom_list.append(target)
        dict_item['value'] = int(3)  # 线宽
        item_list.append(dict_item)

    disease_set = set(disease_list)
    symptom_set = set(symptom_list)

    for i in rels_commonddrug:  # 14104
        dict_item = dict()
        source = i[0]
        target = i[1]
        if source in disease_set: # 药物对齐疾病
            dict_item['relation'] = "常用药"
            dict_item['source'] = source
            dict_item['target'] = target
            disease_list.append(source)
            drug_list.append(target)
            dict_item['value'] = int(3)  # 线宽
            item_list.append(dict_item)

    drug_set = set(drug_list)

    dict_out['links'] = item_list
    print(dict_out)  # 写出json 的links

    # dict_nodes = dict()
    item_list = []
    for j in disease_set:  # 8442
        dict_item = dict()
        dict_item['class'] = "疾病"
        dict_item['group'] = 0
        dict_item['id'] = j
        dict_item['size'] = 10  # 节点大小
        item_list.append(dict_item)

    for j in symptom_set:
        dict_item = dict()
        dict_item['class'] = "症状"
        dict_item['group'] = 1
        dict_item['id'] = j
        dict_item['size'] = 8  # 节点大小
        item_list.append(dict_item)

    for j in drug_set:
        dict_item = dict()
        dict_item['class'] = "药品"
        dict_item['group'] = 2
        dict_item['id'] = j
        dict_item['size'] = 12  # 节点大小
        item_list.append(dict_item)

    dict_out['nodes'] = item_list
    print(dict_out)  # 写出json 的links

    # 把 dict_out 以json写出即可。
    json_str = json.dumps(dict_out, ensure_ascii=False)
    with open('data/output/vizdata_med_kg_1000.json', 'w') as json_file:
        json_file.write(json_str)

    pass
