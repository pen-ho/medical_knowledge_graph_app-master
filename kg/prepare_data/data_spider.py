#!/usr/bin/env python3
# coding: utf-8
# File: data_spider.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3


import urllib.request
import urllib.parse
from lxml import etree
import pymongo
import re

'''基于司法网的犯罪案件采集'''


class CrimeSpider:
    def __init__(self):
        # self.conn = pymongo.MongoClient() # 默认 "mongodb://localhost:27017/"
        # self.db = self.conn['medical']
        # self.col = self.db['data']
        pass

    '''根据url，请求html'''

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk')
        return html

    '''url解析'''
    # def url_parser(self, content):
    #     selector = etree.HTML(content)
    #     urls = ['http://www.anliguan.com' + i for i in  selector.xpath('//h2[@class="item-title"]/a/@href')]
    #     return urls

    '''测试'''

    # hzp改 20210812
    def spider_main(self):
        """
        从疾病库jib把症状文本爬取下来。用于一些疾病症状页面没有维护好带超链接症状的情况
        生成疾病-症状描述文本 的数据文件
        """
        result_dict = {}
        file_out = open('../data/disease_symptomtxt.tsv', 'a', encoding='utf-8')
        # file_out.write('disease_name' + "\t" + 'symptom_txt' + "\n")
        # 原来爬虫的网页是从(1,11000) 分5次爬下来 1-2000，2001-4000，4001-6000，6001-8000，8001-11000
        # for page in range(1, 2000):
        # for page in range(2001, 4000):
        # for page in range(4001, 6000):
        # for page in range(6001, 8000):
        for page in range(8001, 11000):
            print(page)
            try:
                basic_url = 'http://jib.xywy.com/il_sii/gaishu/%s.htm' % page
                # cause_url = 'http://jib.xywy.com/il_sii/cause/%s.htm'%page
                # prevent_url = 'http://jib.xywy.com/il_sii/prevent/%s.htm'%page
                symptom_url = 'http://jib.xywy.com/il_sii/symptom/%s.htm' % page
                # inspect_url = 'http://jib.xywy.com/il_sii/inspect/%s.htm'%page
                # treat_url = 'http://jib.xywy.com/il_sii/treat/%s.htm'%page
                # food_url = 'http://jib.xywy.com/il_sii/food/%s.htm'%page
                # drug_url = 'http://jib.xywy.com/il_sii/drug/%s.htm'%page
                data = {}
                # data['url'] = basic_url
                data['basic_info'] = self.basicinfo_spider(basic_url)
                # data['cause_info'] =  self.common_spider(cause_url)
                # data['prevent_info'] =  self.common_spider(prevent_url)
                data['symptom_info'] = self.symptom_spider(symptom_url)
                # data['inspect_info'] = self.inspect_spider(inspect_url)
                # data['treat_info'] = self.treat_spider(treat_url)
                # data['food_info'] = self.food_spider(food_url)
                # data['drug_info'] = self.drug_spider(drug_url)
                # print(page, basic_url)
                # self.col.insert(data)
                disease_name = data['basic_info']['name']
                # print('疾病名称：', disease_name)
                symptom_txt = ''.join(data['symptom_info'][1])  ## 0是带链接的症状，1是症状描述
                # print('疾病病症：', len(symptom_text), symptom_text)
                # result_dict[disease_name] = symptom_text
                if disease_name == '' and symptom_txt == '':
                    continue
                file_out.write(disease_name + "\t" + symptom_txt + "\n")

            except Exception as e:
                print(e, page)
        return

    '''基本信息解析'''

    def basicinfo_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        title = selector.xpath('//title/text()')[0]
        category = selector.xpath('//div[@class="wrap mt10 nav-bar"]/a/text()')
        desc = selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')
        ps = selector.xpath('//div[@class="mt20 articl-know"]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            infobox.append(info)
        basic_data = {}
        basic_data['category'] = category
        basic_data['name'] = title.split('的简介')[0]
        basic_data['desc'] = desc
        basic_data['attributes'] = infobox
        return basic_data

    '''treat_infobox治疗解析'''

    def treat_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//div[starts-with(@class,"mt20 articl-know")]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            infobox.append(info)
        return infobox

    '''treat_infobox治疗解析'''

    def drug_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        drugs = [i.replace('\n', '').replace('\t', '').replace(' ', '') for i in selector.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()')]
        return drugs

    '''food治疗解析'''

    def food_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        divs = selector.xpath('//div[@class="diet-img clearfix mt20"]')
        try:
            food_data = {}
            food_data['good'] = divs[0].xpath('./div/p/text()')
            food_data['bad'] = divs[1].xpath('./div/p/text()')
            food_data['recommand'] = divs[2].xpath('./div/p/text()')
        except:
            return {}

        return food_data

    '''症状信息解析'''

    def symptom_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        symptoms = selector.xpath('//a[@class="gre" ]/text()') # 理解这个是在做什么？a表示a标签<a></a> 链接的意思，gre是标签下网页设计者命名的一个业务类class，text表示要的就是文本。
        ps = selector.xpath('//p')  # 网页中的段落元素<p></p>
        detail = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            detail.append(info)
        symptoms_data = {}
        symptoms_data['symptoms'] = symptoms
        symptoms_data['symptoms_detail'] = detail  # 症状描述
        print(symptoms,detail)
        return symptoms, detail

    '''检查信息解析'''

    def inspect_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        inspects = selector.xpath('//li[@class="check-item"]/a/@href')
        return inspects

    '''通用解析模块'''

    def common_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            if info:
                infobox.append(info)
        return '\n'.join(infobox)

    '''检查项抓取模块'''

    def inspect_crawl(self):
        for page in range(1, 3685):
            try:
                url = 'http://jck.xywy.com/jc_%s.html' % page
                html = self.get_html(url)
                data = {}
                data['url'] = url
                data['html'] = html
                self.db['jc'].insert(data)
                print(url)
            except Exception as e:
                print(e)


handler = CrimeSpider()
# 测试爬虫脚本 20210812
handler.spider_main() # 生成疾病--症状描述文本 disease_symptomtxt.tsv


def spider_symptom_name_for_aligning():
    """
    寻医问药网有疾病库，有症状库。爬取症状库所有症状名字。
    """
    def get_html(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk')
        return html

    def symptom_spider(url):
        html = get_html(url)
        selector = etree.HTML(html)
        #<div class="jb-name fYaHei gre">咳嗽</div>
        symptoms_name = selector.xpath('//div[@class="jb-name fYaHei gre"]/text()')[0]
        # print(symptoms_name)
        return symptoms_name

    def spider_main():
        """
        从疾病库jib把症状文本爬取下来symptom_name.tsv。用于一些疾病症状页面没有维护好带超链接症状的情况
        """
        file_out = open('../data/output/symptom_name.tsv', 'w', encoding='utf-8') # 'a'-追加  'w'-从新写
        # file_out.write('disease_name' + "\t" + 'symptom_txt' + "\n")
        # 页码最大 6911
        symptom_name_list = []
        for page in range(1, 6911):
            print(page)
            try:
                symptom_url = 'http://zzk.xywy.com/%s_gaishu.html' % page
                symptom_name = symptom_spider(symptom_url)
                # print(symptom_name)
                # symptom_name_list.append((page,symptom_name))

                if symptom_name == '':
                    continue
                file_out.write(str(page) + "\t" + symptom_name + "\n")

            except Exception as e:
                print(e, page)

        # print(symptom_name_list)
        return

    spider_main()
    return

spider_symptom_name_for_aligning()  #爬取所有症状名，作为症状库文件 symptom_name.tsv



# def create_medical_add_symptomtxt(result_dict):
#     """
#     hzp 20210812
#     创建一个追加了疾病具体症状文本的json文件，在原来的文件medical.json基础上
#     # result_dict：输入字典{'disease':'symptomtxt'}
#     """
#     # import pandas as pd
#     # result = pd.read_json('../data/medical.json')
#     # print(result[:1]) ValueError: Trailing data
#     import json
#
#     file_out = open('../data/medical_addsymptomtext.json', 'w', encoding='utf-8')
#     count = 0
#     for data in open('../data/medical.json'):
#         # if count > 10:
#         #     break
#         count += 1
#         print(count)
#         data_json = json.loads(data)  # json转字典
#         print(data_json['name'])
#         disease_name = data_json['name']
#         if disease_name in result_dict.keys():
#             symptomtxt = result_dict[disease_name]
#             data_json['symptomtxt'] = symptomtxt
#         # print(data_json)
#         file_out.write(json.dumps(data_json, ensure_ascii=False) + '\n')  # 不加参数ensure_ascii会有乱码
#
#     file_out.close()

# create_medical_add_symptomtxt(result_dict)

# handler.inspect_crawl()
