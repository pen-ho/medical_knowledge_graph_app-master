# coding:utf-8
from sentence_transformers import SentenceTransformer, util
import os
import csv
import time
import torch
import pickle


# if not torch.cuda.is_available():
#     print("Warning: No GPU detected. Processing will be slow. Please add a GPU to this notebook")

class SBert:
    def __init__(self):
        self.model_name = 'quora-distilbert-multilingual'
        self.model = SentenceTransformer(self.model_name)
        self.corpus_sentences = set()
        self.corpus_embeddings = []

    def store_embedding(self):
        dataset_path = "./data/output/symptom_for_matching.txt"
        max_corpus_size = 100000
        # Get all unique sentences from the file

        with open(dataset_path, encoding='utf8') as fIn:
            for row in fIn:
                self.corpus_sentences.add(row.strip())  # 把疾病名称和疾病症状拼接起来
                if len(self.corpus_sentences) >= max_corpus_size:
                    break
            # for row in reader:
            #     corpus_sentences.add(row['symptom']) # 只用疾病症状
            #     if len(corpus_sentences) >= max_corpus_size:
            #         break
        self.corpus_sentences = list(self.corpus_sentences)
        print("Encode the corpus. This might take a while")
        self.corpus_embeddings = self.model.encode(self.corpus_sentences, show_progress_bar=True, convert_to_tensor=True)  # 导出？下次直接导入？
        ###############################
        print("Corpus loaded with {} sentences / embeddings".format(len(self.corpus_sentences)))
        # Store sentences & embeddings on disc
        with open('symptom_embedding/embeddings.pkl', "wb") as fOut:
            pickle.dump({'sentences': self.corpus_sentences, 'embeddings': self.corpus_embeddings}, fOut, protocol=pickle.HIGHEST_PROTOCOL)

    def load_embedding(self):
        # Load sentences & embeddings from disc
        with open('/Users/penho/Documents/GDUT/PythonProject/medical_knowledge_graph_app-master/med_kg/MedModel/symptom_embedding/embeddings.pkl', "rb") as fIn:
            stored_data = pickle.load(fIn)
            self.corpus_sentences = stored_data['sentences']
            self.corpus_embeddings = stored_data['embeddings']

    def search(self, inp_question):
        start_time = time.time()
        question_embedding = self.model.encode(inp_question, convert_to_tensor=True)
        hits = util.semantic_search(question_embedding, self.corpus_embeddings)
        end_time = time.time()
        print('test-hits',hits)
        hits = hits[0]  # Get the hits for the first query

        # print("Input question:", inp_question)
        # print("Results (after {:.3f} seconds):".format(end_time - start_time))
        top_1_symptom = self.corpus_sentences[hits[0]['corpus_id']][:-6]
        print('找到了语义最相似的症状：' + top_1_symptom)
        return top_1_symptom
        # for hit in hits[0:5]:
        #     print("\t{:.3f}\t{}".format(hit['score'], self.corpus_sentences[hit['corpus_id']]))


if __name__ == '__main__':
    # SBert存储与导出嵌入 https://www.sbert.net/examples/applications/computing-embeddings/README.html#storing-loading-embeddings

    # 存储
    # model = SBert()
    # model.store_embedding()

    # 导出
    model = SBert()
    model.load_embedding()
    while 1:
        question = input('用户:')  # eg.皮肤痕痒，红肿是什么毛病？ 嘴唇旁边干裂是什么毛病？眼睛干涩是什么毛病？
        top1_symptom=model.search(question)

    # 语义匹配例子：
    # 用户: 皮肤痕痒，红肿是什么毛病？
    # 找到了语义最相似的症状：皮肤弥漫性红肿
    #
    # 用户: 眼睛干涩是什么毛病？
    # 找到了语义最相似的症状：眼干
    #
    # 用户: 嘴唇旁边干裂是什么毛病？
    # 找到了语义最相似的症状：唇干裂
