import csv
import pandas as pd
import spacy

# From https://spacy.io/
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

data_file = 'ontology.csv'

dataframe = pd.read_csv(data_file,sep=',')

