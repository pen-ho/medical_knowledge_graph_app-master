#!/usr/bin/env python3
# coding: utf-8
# Author  : penho
# File    : predict_ner.py
# Date    : 2021-11-01

import sys

sys.path.append("")
from ner_model.models.transformers import BertConfig
from ner_model.models.bert_for_ner import BertCrfForNer
from ner_model.processors.utils_ner import CNerTokenizer, get_entities
import torch
from ner_model.processors.ner_seq import ner_processors as processors



def predict_med_ner(sentence):
    MODEL_CLASSES = {
        'bert': (BertConfig, BertCrfForNer, CNerTokenizer)}
    config_class, model_class, tokenizer_class = MODEL_CLASSES['bert']

    config = config_class.from_pretrained('med_kg/ner_model/outputs/1101medselfner-finetune/bert')
    tokenizer = tokenizer_class.from_pretrained('med_kg/ner_model/outputs/1101medselfner-finetune/bert')
    model = model_class.from_pretrained('med_kg/ner_model/outputs/1101medselfner-finetune/bert', config=config)
    # model.to(args.device)
    max_seq_length = 512
    # input_ids = tokenizer.encode("屁股痕痒是什么毛病？", add_special_tokens=True, max_length=512)  # Batch size 1
    input_ids = tokenizer.encode(sentence, add_special_tokens=True, max_length=512)
    # print(input_ids)
    padding_length = max_seq_length - len(input_ids)
    input_mask = [1] * len(input_ids)
    input_ids += [0] * padding_length
    input_mask += [0] * padding_length
    segment_ids = [0] * len(input_ids)

    input_ids = torch.tensor(input_ids).unsqueeze(0)
    input_mask = torch.tensor(input_mask).unsqueeze(0)
    input_lens = torch.tensor([1])
    # print(input_ids,input_mask,input_lens)

    inputs = {"input_ids": input_ids, "attention_mask": input_mask, "labels": None, 'input_lens': input_lens}

    outputs = model(input_ids)
    # print(outputs)

    logits = outputs[0]
    tags = model.crf.decode(logits, inputs['attention_mask'])
    tags = tags.squeeze(0).cpu().numpy().tolist()
    preds = tags[0][1:-1]  # [CLS]XXXX[SEP]

    processor = processors['medselfner']()
    label_list = processor.get_labels()
    id2label = {i: label for i, label in enumerate(label_list)}
    label_entities = get_entities(preds, id2label, 'bios')
    # print(label_entities)
    if len(label_entities) != 0:
        b = label_entities[0][1]
        e = label_entities[0][2]
        output = sentence[b:e + 1] + ':' + label_entities[0][0]
    else:
        output = '无识别出mention'
    return output

# 这三个实体训练数据都无，但是模型泛化能力强可以识别出来。hzp
predict_med_ner('大腿痕痒是什么毛病？')
predict_med_ner('胆红素偏高怎么治疗？')
predict_med_ner('999皮炎平可以治疗什么疾病？')
