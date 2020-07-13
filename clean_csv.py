#### List of Names ####
import pandas as pd
import re
import unidecode
import spacy
nlp = spacy.load("es_core_news_md")

_data = pd.read_csv(cv_path+'candidates1.csv')
data = _data[['Full Name','Skill Set']]

names = data.iloc[:,0].str.lower().tolist()
names = [ unidecode.unidecode(n) for n in names ]
names = list(set([token.text for token in nlp(' '.join(names)) if not token.is_stop and len(token)>2 ]))

pd.DataFrame(names).to_csv('names.csv',header=False,index=False)

def clean_contents(t):
    return " ".join(re.findall(r'[a-zA-Z\u00C0-\u00FF]{1,}', t, re.UNICODE))
skills = data.iloc[:,1].str.lower().tolist()
skills = [ clean_contents(s) for s in skills if type(s) == str ]
skills = list(set([token.text for token in nlp(' '.join(skills)) if not token.is_stop and token.pos_ == 'PROPN']))


sk = list(pd.read_csv('./parser_custom/skills.csv').columns)

pd.DataFrame(sk + skills).to_csv('skills.csv',header=False,index=False)
