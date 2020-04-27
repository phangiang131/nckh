from collections import defaultdict
import re

from flair.models import SequenceTagger
from flair.data import Sentence

def load_model(modelpath):
    return SequenceTagger.load(modelpath)

def get_tag_dic(sentence):
    res = defaultdict(list)
    for entity in sentence.get_spans('ner'):
        en_dict = entity.to_dict()
        res[en_dict['type']].append(en_dict['text'])
    return res 

def get_tag_sentence(model,query):
    sentence = Sentence(query)
    model.predict(sentence)
    return sentence

def get_entity_by_tag(query, tag='target'):
    model = load_model('./service/model/final-model.pt')
    tag_sentence = get_tag_sentence(model, query)
    print(tag_sentence.to_tagged_string())
    display_dict = to_display(tag_sentence)
    tag_dic = get_tag_dic(tag_sentence)
    return display_dict, tag_dic

def to_display(sentence):
    dct = {}
    i = 0
    cur_tag = ''
    phrase = []
    tokens = sentence.to_tagged_string().split()
    while i < len(tokens)-1:
        if '<' in tokens[i+1]:
            if cur_tag == '':
                cur_tag = tokens[i+1]
                phrase += [tokens[i]]
            elif cur_tag == tokens[i+1]:
                phrase += [tokens[i]]
            elif cur_tag != tokens[i+1]:
                dct[' '.join(phrase)] = cur_tag
                cur_tag = tokens[i+1]
                phrase = [tokens[i]]
            i += 1
        else:
            if cur_tag != '':
                dct[' '.join(phrase)] = cur_tag
                phrase = []
                cur_tag = ''
            dct[tokens[i]] = ''
        i += 1

    if i == len(tokens)-1 and '<' not in tokens[i]:
        dct[tokens[i]] = ''
    
    if cur_tag != '':
        dct[' '.join(phrase)] = cur_tag 

    return dct