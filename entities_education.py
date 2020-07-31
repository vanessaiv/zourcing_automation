import requests
import urllib
import time
from bs4 import BeautifulSoup
from pandas import DataFrame as df
import unidecode
import re

page = requests.get('http://sistemas.anuies.mx/perl/directorios/reprec1.pl')
page
page.encoding = 'latin1'
soup = BeautifulSoup(page.text, 'html.parser')

data = soup.find_all('b')
entities = [data[i].text for i in range(len(data)) if '\n' in data[i].text]
entities = [' '.join(entities[i].replace('\n', '').replace('\r', '').replace(',', '').strip().split()) for i in range(len(entities))]

#check
entities = [re.sub(r'\W+', ' ', entity) for entity in entities]
entities.append("Colegio de Estudios Científicos y Tecnológicos del Estado de México Plantel Ixtapaluca")

#[strip_accents(entities[i]) for i in range(len(entities))]
#df(entities[1:]).to_csv('entities.csv',encoding='utf8', index=False, header=None)
