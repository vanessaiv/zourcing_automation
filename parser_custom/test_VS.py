import os
os.chdir('C:\\Users\\Lenovo\\Google Drive (vanessa.cruz@quantumworks.io)\\@zourcing\\parser_custom')
from utils import *

cvs = ['1107 (Jose Luis Rodriguez Hernandez)\Cvs 26 marzo\CVAndreaMonserratMartinezMurillo.pdf',
        '1512(Flor de María Amado Ruiz)\ABRAAM BONILLA.pdf', '1211 (Marisol Rojas)\\4 Marzo\Angelica LM CV2020.pdf',
        '1431 (Roberto Puon)\CVs 19 marzo\CV Alducin Garcia Marco Antonio 2020.pdf', '1438 (Edith Pantaleon Gutierrez)\CV Juan Antonio.pdf',
        '1089 (Luz Vistraín)\Daniel_Pedraza.pdf', '1089 (Luz Vistraín)\Carlos Alberto Torres Martinez Embebidos.pdf', '1089 (Luz Vistraín)\Delivery Lead Mauricio Godinez.pdf',
        '1089 (Luz Vistraín)\Technical Lead  Oscar Valencia.pdf', '1511\CV VICTOR GARCIA.docx', '1438 (Edith Pantaleon Gutierrez)\CVVMSR.docx',
        '1348 (Karla Muciño)\Gerentes Admon y Finanzas\CVGeorginaOrtegaOsorio.docx', '1305 (Daniela Uribe)\Curriculum Jocelyn.docx',
        '1089 (Luz Vistraín)\Carlos Alberto Torres Martinez Embebidos.docx', '1089 (Luz Vistraín)\\6 de Abril\SAP ABAP Arturo Castillo.pdf',
        '1511/CV Alberto Cardenas.pdf']

cv_path = '../CVS/'

###############################################################################
# Extract text
pdf = 7  # Buenos: 5, 6; Malos: 1, 11, 12

# from pdf
text = extract_text_from_pdf(cv_path+cvs[pdf])
# from word
text = extract_text_from_doc(cv_path+cvs[pdf])
# in main:
os.path.splitext(cv_path+cvs[pdf])
text = extract_text(cv_path+cvs[pdf], os.path.splitext(cv_path+cvs[pdf])[1])
text
###############################################################################
# Extract entities:
#  - text split not good
#  - change RESUME_SECTIONS
extract_entity_sections(text)
###############################################################################
# Mail allways good
extract_email(text)
###############################################################################
# Name
# - check NAME_PATTERN and add two apellidos
# - se queda con el primer match (?????)
import spacy

nlp = spacy.load("es_core_news_md")
doc = nlp(text)
[ ent for ent in doc.ents if ent.label_ == 'PER' ]

extract_name(cvs[pdf])

###############################################################################
# Telephone
# - check limit of 10 digits
# - adding a '+' (??????)
# - is not finding all numbers
extract_mobile_number(text)
###############################################################################
# Skills
# - check if noun_chunks are correct
# - change __file__ for cwd
# - make a new skills.csv
# - su buena pasadita
#nlp = es_core_news_md.load()
nlp_text = nlp(text)
noun_chunks = list(nlp_text.noun_chunks)
extract_skills(nlp_text, noun_chunks)
###############################################################################
# Education
# - input is list of sentences, not nlp_text
# - check STOPWORDS
# - check EDUCATION
# - check YEAR
sentences = [sent.string.strip() for sent in nlp_text.sents]
extract_education(sentences)
###############################################################################
# Experience
# - MUCHO OJO!! NO SABEMOS NADA
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
extract_experience(text)
###############################################################################
# Extract competencies
# - depends on experience list!
# - check COMPETENCIES
extract_competencies(text, experience_list)

###############################################################################


def names(file_path):
    name = ntpath.basename(file_path)
    name = unidecode.unidecode(name)

    abr = ['CV', 'pdf', 'docx']

    for a in abr:
        name = re.sub(a, '', name)

    name = re.sub(r'([^a-zA-Z ]+?)', '', name)

    for i, char in enumerate(name):
        if char.isupper() and len(name.split()) == 1:
            c = ' '+char
            name = re.sub(char, c, name)
    name = name.strip()
    return name


[names(path) for path in cvs]
names(cvs[5])
extract_name(cvs[5])


def extract_mobile_number(text):
    '''
    Helper function to extract mobile number from text

    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    '''
    # Found this complicated regex on : https://zapier.com/blog/extract-links-email-phone-regex/
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{5})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    phone_ = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][2-8][1-9]|[0-9][0-9][0-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{3})\s*([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    _phone = re.findall(re.compile(r'\d{7,16}'), text)

    if len(_phone) >= 2:
        return _phone
    elif (len(phone) == len(phone_) == len(_phone) == 0):
        return None
    else:
        phone = max([phone, phone_], key=len)
        number = ''.join(phone[0])
        if _phone:
            return(max([_phone[0], number]))
        else:
            return number

extract_mobile_number(text)
prueba = [extract_text(cv_path+cvs[j], os.path.splitext(cv_path+cvs[j])[1]) for j in range(len(cvs))]
[extract_mobile_number(prueba[i]) for i in range(len(prueba))]

[re.findall(re.compile(r'\d{6,16}'), prueba[i]) for i in range(len(prueba))]
###################################################################################

edu = {}
# Extract education degree
for index, text in enumerate(sentences):
    for tex in text.split():
        tex = re.sub(r'[?|$|.|!|,]', r'', tex)
        if tex not in cs.STOPWORDS:
            edu[tex] = text + sentences[index]

edu
# Extract year
education = []
for key in edu.keys():
    year = re.search(re.compile(cs.YEAR), edu[key])
    if year:
        education.append((key, ''.join(year.group(0))))
    else:
        education.append(key)
print(education)

from entities_education import entities as Entities
Entities
Entities = [' '.join(re.findall(r'\w+', Entities[i].lower(), flags = re.UNICODE)) for i in range(len(Entities))]
sentence = ' '.join(re.findall(r'\w+', sentences[-17].lower(), flags = re.UNICODE))

educacion = []
sentences = [' '.join(sentences[i].replace('\n', '').replace('\uf0b7', '').strip().split()) for i in range(len(sentences))]
sentences = [' '.join(re.findall(r'\w+', sentences[i].lower(), flags = re.UNICODE)) for i in range(len(sentences))]
sentences = [re.sub(r'\W+', ' ', entity) for entity in sentences]
sentences

from spacy import displacy
from collections import Counter
nlp = spacy.load('es_core_news_sm')

chunk = [nlp(sentences[i]) for i in range(len(sentences))]
for i in range(len(chunk)):
    chunk[i] = [(X.text, X.label_) for X in chunk[i].ents if X.label_ == 'ORG']

chunkE = [item[0] for sublist in chunk for item in sublist if sublist]
chunkE
#text = nlp(sentences[19])
#print([(X.text, X.label_) for X in text.ents])

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

for entity in sentences:
    for ent in Entities:
        ratio = fuzz.partial_ratio(entity, ent)
        if ratio > 70:
            print(entity, ent, ratio)
