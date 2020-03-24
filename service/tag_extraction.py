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

def get_entity_by_tag(query,tag='target'):
    model = load_model('./service/model/final-model.pt')
    tag_sentence = get_tag_sentence(model,query)
    tag_dic = get_tag_dic(tag_sentence)
    return tag_dic[tag]


