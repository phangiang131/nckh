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

def get_entity_by_tag(query, models, tag='target'):
    # target_model = load_model('./service/model/final-model-target.pt')
    # non_target_model = load_model('./service/model/final-model-non-target.pt')

    tag_sentence = get_tag_sentence(models["target_model"], query)
    non_tag_sentence = get_tag_sentence(models["non_target_model"], query)

    tag_display = to_display(tag_sentence)
    non_tag_display = to_display(non_tag_sentence)

    tag_display, non_tag_display = combine(tag_display, non_tag_display)

    tag_dic = get_tag_dic(tag_sentence)

    return {"tag_display": tag_display, "non_tag_display": non_tag_display}, tag_dic

def to_display(sentence):
    dct = []
    i = 0
    cur_tag = ''
    phrase = []
    tokens = sentence.to_tagged_string().split()
    # tokens = sentence.split()
    while i < len(tokens)-1:
        if '<' in tokens[i+1]:
            if cur_tag == '':
                cur_tag = tokens[i+1]
                phrase += [tokens[i]]
            elif cur_tag == tokens[i+1]:
                phrase += [tokens[i]]
            elif cur_tag != tokens[i+1]:
                dct.append([' '.join(phrase), cur_tag])
                cur_tag = tokens[i+1]
                phrase = [tokens[i]]
            i += 1
        else:
            if cur_tag != '':
                dct.append([' '.join(phrase), cur_tag])
                phrase = []
                cur_tag = ''
            dct.append([tokens[i], ''])
        i += 1

    if i == len(tokens)-1 and '<' not in tokens[i]:
        dct.append([tokens[i], ''])
    
    if cur_tag != '':
        dct.append([' '.join(phrase), cur_tag]) 

    return dct

def combine(tag, non_tag):
    new_non_tag = [nt for nt in non_tag if nt[1]!='']
    return tag, new_non_tag

if __name__ == '__main__':
    tag = 'laptop <target> dell <target> chính <target> hãng <target> giá <price> rẻ <price> rẻ <price> dell <target> 200'
    non_tag = 'laptop dell <brand> chính hãng giá <price> rẻ <price> rẻ <price> dell <brand> 200'
    # tag = to_display(tag)
    # non_tag = to_display(non_tag)
    # tag, non_tag = combine(tag, non_tag)
    print(combine(tag, non_tag))