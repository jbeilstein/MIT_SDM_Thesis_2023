# Used with CUDA 12.2.2

# pip install cupy-cuda11x
# pip install -U 'spacy[cuda-autodetect]'
# pip install pdfminer
# pip install pdfquery
# pip install pdfminer.six
# pip install tabula-py

# py -m spacy download en_core_web_sm
# py -m spacy download en_core_web_lg
# py -m spacy init fill-config ./base_config.cfg ./config.cfg
# py -m spacy init fill-config ./tagger_parser_ud/configs/default.cfg ./config.cfg
# py -m spacy project clone pipelines/tagger_parser_ud

import csv
#import numpy
import math
import pandas as pd
import pdfminer
import pdfquery
#import spacy
#import tabula
#import tensorflow

from csv import writer
from pathlib import Path
from pdfminer.high_level import extract_pages
# from pdfminer.high_level import extract_text
# from pdfminer.layout import LAParams
# from pdfminer.converter import PDFPageAggregator
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from pdfminer.layout import LTTextBoxHorizontal
# from spacy import displacy
# from spacy.lang.en import English
# from spacy.pipeline import EntityRuler
# from spacy.matcher import Matcher
from typing import Iterable, Any

#########
# This section of code is adapted from code written by Yusuke Shinyama on 12 Sep 2021 on Stack Overflow.  Written 2013.  Last Accessed 4 Oct 2023.
# https://pdfminer-docs.readthedocs.io/programming.html

# This section of code is adapted from code written by Stack Overflow User Pieter on 12 Sep 2021 on Stack Overflow.  Written 12 Sep, 2021.  Last Accessed 4 Oct 2023.
# https://stackoverflow.com/questions/22898145/how-to-extract-text-and-text-coordinates-from-a-pdf-file

from pdfminer.converter import PDFResourceManager
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
#from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

data_entry = ['','','','','','','','','','','','','','','','']
data_file = 'data.csv'

with open(data_file, 'a', newline='') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close()   

source_document = open('requirement_document2.pdf', 'rb')
#Create resource manager
rsrcmgr = PDFResourceManager()
# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
id_num = 0
for page in PDFPage.get_pages(source_document):
    page_id = page.pageid
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    for element in layout:
        class_name = element.__class__.__name__
        coords0 = 0
        coords1 = 0
        coords2 = 0
        coords3 = 0
        logical_shall = 'false'
        logical_should = 'false'
        parent_of = ''
        sibling_of = ''
        child_of = ''
        reference_internal = ''
        reference_external = ''
        association_with = ''
                
        if hasattr(element, 'bbox'):
            coords0 = element.bbox[0]
            coords1 = element.bbox[1]
            coords2 = element.bbox[2]
            coords3 = element.bbox[3]
            
        if hasattr(element, 'get_text'):
            text = element.get_text().strip()

            if "shall" in text or "must" in text:
                logical_shall = 'true'
            if "should" in text:
                logical_should = 'true'
            if text == 'C1':
                text = 'C1'
        else:
            text = ''
        

        if len(text) > 0:
            if class_name != 'LTChar' and class_name != 'LTAnno' and class_name != 'LTLine':
            # if class_name != 'LTChar' and class_name != 'LTAnno' and class_name != 'LTLine' and class_name != 'LTTextLineHorizontal':

                data_entry = [id_num, page_id, class_name, coords0, coords1, coords2, coords3, logical_shall, logical_should, parent_of, sibling_of, child_of, reference_internal, reference_external, association_with, text]
                
                with open(data_file, 'a', encoding="utf-8", newline='') as object:
                    write_object = writer(object)
                    write_object.writerow(data_entry)
                    object.close() 
                                       
                id_num = id_num + 1
                
        # if instanceof(element, LTTextBoxHorizontal):
            # print(element.get_text())


                        

                        
    # with open(data_file,'r') as object:
    #     data = csv.reader(object)
    #     for current_row in data:
    #         if current_row[0] != '' and current_row[0] != 'id_num':
    #             x=1
                    
                
# dataframe_original = tabula.read_pdf('requirement_document.pdf', pages='all')
# dataframe_original = extract_text('requirement_document.pdf')

#########
# This section of code is based upon code written by Stack Overflow User Pieter on 12 Sep 2021 on Stack Overflow.  Written 12 Sep, 2021.  Last Accessed 4 Oct 2023.
# https://stackoverflow.com/questions/22898145/how-to-extract-text-and-text-coordinates-from-a-pdf-file
# def show_ltitem_hierarchy(o: Any, depth=0):
#     """Show location and text of LTItem and all its descendants"""
#     if depth == 0:
#         print('element                        x1  y1  x2  y2   text')
#         print('------------------------------ --- --- --- ---- -----')

#     text = f'{get_optional_text(o)}'
#     if len(text) > 0:
#         print(
#             f'{get_indented_name(o, depth):<30.20s} '
#             f'{get_optional_bbox(o)} '
#             f'{get_optional_text(o)}'
#         )

#     if isinstance(o, Iterable):
#         for i in o:
#             if i.__class__.__name__ != 'LTChar' and i.__class__.__name__ != 'LTAnno' and i.__class__.__name__ != 'LTLine' and i.__class__.__name__ != 'LTTextLineHorizontal':
#                 show_ltitem_hierarchy(i, depth=depth + 1)

# def get_indented_name(o: Any, depth: int) -> str:
#     return '  ' * depth + o.__class__.__name__

# def get_optional_bbox(o: Any) -> str:
#     if hasattr(o, 'bbox'):
#         return ''.join(f'{i:<4.0f}' for i in o.bbox)
#     return ''

# def get_optional_text(o: Any) -> str:
#     if hasattr(o, 'get_text'):
#         return o.get_text().strip()
#     return ''

# path_source_document = Path('requirement_document.pdf')

# pages_source_document = extract_pages(path_source_document)
# show_ltitem_hierarchy(pages_source_document)


# #read the source document and write to XML
# source_document = pdfquery.PDFQuery('requirement_document.pdf')
# source_document.load()
# source_document.tree.write('requirement_document.xml', pretty_print = True, encoding="utf-8")



# df0 = dataframe_original[0]
# df1 = dataframe_original[1]
# df2 = dataframe_original[2]
# df3 = dataframe_original[3]

# From https://spacy.io/
# Load English tokenizer, tagger, parser and NER

#######

# nlp = spacy.load("en_core_web_sm")

# # Process whole documents
# text = ("I want to design a car.  The car will be really fast.  It will allow four passengers to sit comfortable.  It will have sixteen cupholders.  There will be a margarita maker as well.")
# doc = nlp(text)

# # Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# # Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)
    

# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop)
    
# doc = nlp("This is a sentence.  Hello, my name is Billy Bob Thornton, I work for NASA")
# # options = {"compact": True, "bg": "#09a3d5",
#         #    "color": "white", "font": "Source Sans Pro"}
# # displacy.serve(doc, style="dep", options=options)

# # Results can be seen via pasting "http://localhost:5000/" in your browswer

# # print(spacy.displacy.render(doc, style="ent", page="true"))

# for ent in doc.ents:
#     print(ent.text, ent.label_)
    
# print(doc.ents)
    
    
# nlp_test = spacy.blank("en")   
# doc_test = nlp("this is a test, this is only a test")

# for token in doc_test:
#     # print(token)
#     token_text = token.text
#     token_pos = token.pos_
#     token_dep = token.dep_
#     # This is for formatting only
#     print(f"{token_text:<12}{token_pos:<10}{token_dep:<10}")
#     if token.text == ",":
#         next_token = doc_test[token.i + 1]
#         if next_token.text != ",":
#             print("hey look i found a comma followed by",next_token.text)
            
# for ent in doc_test.ents:
#     # Print the entity text and its label
#     print(ent.text, ent.label)
                     
# # Initialize the matcher with the shared vocab
# matcher = Matcher(nlp.vocab)

# # Add the pattern to the matcher
# pattern = [{"TEXT": "iPhone"}, {"TEXT": "X"}]
# matcher.add("IPHONE_PATTERN", [pattern])

# # Process some text
# doc = nlp("Upcoming iPhone X release date leaked")

# # Call the matcher on the doc
# matches = matcher(doc)    
# print(matches)        

# # Iterate over the matches
# for match_id, start, end in matches:
#     # Get the matched span
#     matched_span = doc[start:end]
#     print(matched_span.text)
    
# pattern = [
#     {"IS_DIGIT": True},
#     {"LOWER": "fifa"},
#     {"LOWER": "world"},
#     {"LOWER": "cup"},
#     {"IS_PUNCT": True}
# ]   
# matcher.add("FIFA_PATTERN", [pattern])    
# doc = nlp("2018 FIFA World Cup: France won!")
# matches = matcher(doc)    
# print(matches)      
# # Iterate over the matches
# for match_id, start, end in matches:
#     # Get the matched span
#     matched_span = doc[start:end]
#     print(matched_span.text)
    
# pattern = [
#     {"LEMMA": "love", "POS": "VERB"},
#     {"POS": "NOUN"}
# ]    
# matcher.add("PET_PATTERN", [pattern])
# doc = nlp("I loved dogs but now I love cats more.")
# matches = matcher(doc)    
# print(matches)      
# # Iterate over the matches
# for match_id, start, end in matches:
#     # Get the matched span
#     matched_span = doc[start:end]
#     print(matched_span.text)
    
# pattern = [
#     {"LEMMA": "buy"},
#     {"POS": "DET", "OP": "?"},  # optional: match 0 or 1 times
#     {"POS": "NOUN"}
# ]    
# matcher.add("PET_PATTERN", [pattern])
# doc = nlp("I bought a smartphone. Now I'm buying apps.")
# matches = matcher(doc)    
# print(matches)      
# # Iterate over the matches
# for match_id, start, end in matches:
#     # Get the matched span
#     matched_span = doc[start:end]
#     print(matched_span.text)



# doc = nlp("Upcoming iPhone X release date leaked as Apple reveals pre-orders")

# # Initialize the Matcher with the shared vocabulary
# matcher = Matcher(nlp.vocab)

# # Create a pattern matching two tokens: "iPhone" and "X"
# pattern = [{"TEXT": "iPhone"}, {"TEXT": "X"}]

# # Add the pattern to the matcher
# matcher.add("IPHONE_X_PATTERN", [pattern])

# # Use the matcher on the doc
# matches = matcher(doc)
# print("Matches:", [doc[start:end].text for match_id, start, end in matches])


    
# # # This is an auto-generated partial config. To use it with 'spacy train'
# # # you can run spacy init fill-config to auto-fill all default settings:
# # # python -m spacy init fill-config ./base_config.cfg ./config.cfg
# # [paths]
# # train = null
# # dev = null
# # vectors = "en_core_web_lg"
# # [system]
# # gpu_allocator = null

# # [nlp]
# # lang = "en"
# # pipeline = ["tok2vec","ner","spancat","textcat","tagger","morphologizer","trainable_lemmatizer","parser"]
# # batch_size = 1000

# # [components]

# # [components.tok2vec]
# # factory = "tok2vec"

# # [components.tok2vec.model]
# # @architectures = "spacy.Tok2Vec.v2"

# # [components.tok2vec.model.embed]
# # @architectures = "spacy.MultiHashEmbed.v2"
# # width = ${components.tok2vec.model.encode.width}
# # attrs = ["NORM", "PREFIX", "SUFFIX", "SHAPE"]
# # rows = [5000, 1000, 2500, 2500]
# # include_static_vectors = true

# # [components.tok2vec.model.encode]
# # @architectures = "spacy.MaxoutWindowEncoder.v2"
# # width = 256
# # depth = 8
# # window_size = 1
# # maxout_pieces = 3

# # [components.morphologizer]
# # factory = "morphologizer"
# # label_smoothing = 0.05

# # [components.morphologizer.model]
# # @architectures = "spacy.Tagger.v2"
# # nO = null

# # [components.morphologizer.model.tok2vec]
# # @architectures = "spacy.Tok2VecListener.v1"
# # width = ${components.tok2vec.model.encode.width}

# # [components.tagger]
# # factory = "tagger"
# # label_smoothing = 0.05

# # [components.tagger.model]
# # @architectures = "spacy.Tagger.v2"
# # nO = null

# # [components.tagger.model.tok2vec]
# # @architectures = "spacy.Tok2VecListener.v1"
# # width = ${components.tok2vec.model.encode.width}

# # [components.parser]
# # factory = "parser"

# # [components.parser.model]
# # @architectures = "spacy.TransitionBasedParser.v2"
# # state_type = "parser"
# # extra_state_tokens = false
# # hidden_width = 128
# # maxout_pieces = 3
# # use_upper = true
# # nO = null

# # [components.parser.model.tok2vec]
# # @architectures = "spacy.Tok2VecListener.v1"
# # width = ${components.tok2vec.model.encode.width}

# # [components.ner]
# # factory = "ner"

# # [components.ner.model]
# # @architectures = "spacy.TransitionBasedParser.v2"
# # state_type = "ner"
# # extra_state_tokens = false
# # hidden_width = 64
# # maxout_pieces = 2
# # use_upper = true
# # nO = null

# # [components.ner.model.tok2vec]
# # @architectures = "spacy.Tok2VecListener.v1"
# # width = ${components.tok2vec.model.encode.width}

# # [components.spancat]
# # factory = "spancat"
# # max_positive = null
# # scorer = {"@scorers":"spacy.spancat_scorer.v1"}
# # spans_key = "sc"
# # threshold = 0.5

# # [components.spancat.model]
# # @architectures = "spacy.SpanCategorizer.v1"

# # [components.spancat.model.reducer]
# # @layers = "spacy.mean_max_reducer.v1"
# # hidden_size = 128

# # [components.spancat.model.scorer]
# # @layers = "spacy.LinearLogistic.v1"
# # nO = null
# # nI = null

# # [components.spancat.model.tok2vec]
# # @architectures = "spacy.Tok2VecListener.v1"
# # width = ${components.tok2vec.model.encode.width}

# # [components.spancat.suggester]
# # @misc = "spacy.ngram_suggester.v1"
# # sizes = [1,2,3]

# # [components.trainable_lemmatizer]
# # factory = "trainable_lemmatizer"
# # backoff = "orth"
# # min_tree_freq = 3
# # overwrite = false
# # scorer = {"@scorers":"spacy.lemmatizer_scorer.v1"}
# # top_k = 1

# # [components.trainable_lemmatizer.model]
# # @architectures = "spacy.Tagger.v2"
# # nO = null
# # normalize = false

# # [components.trainable_lemmatizer.model.tok2vec]
# # @architectures = "spacy.Tok2VecListener.v1"
# # width = ${components.tok2vec.model.encode.width}

# # [components.textcat]
# # factory = "textcat"

# # [components.textcat.model]
# # @architectures = "spacy.TextCatEnsemble.v2"
# # nO = null

# # [components.textcat.model.tok2vec]
# # @architectures = "spacy.Tok2VecListener.v1"
# # width = ${components.tok2vec.model.encode.width}

# # [components.textcat.model.linear_model]
# # @architectures = "spacy.TextCatBOW.v2"
# # exclusive_classes = true
# # ngram_size = 1
# # no_output_layer = false

# # [corpora]

# # [corpora.train]
# # @readers = "spacy.Corpus.v1"
# # path = ${paths.train}
# # max_length = 0

# # [corpora.dev]
# # @readers = "spacy.Corpus.v1"
# # path = ${paths.dev}
# # max_length = 0

# # [training]
# # dev_corpus = "corpora.dev"
# # train_corpus = "corpora.train"

# # [training.optimizer]
# # @optimizers = "Adam.v1"

# # [training.batcher]
# # @batchers = "spacy.batch_by_words.v1"
# # discard_oversize = false
# # tolerance = 0.2

# # [training.batcher.size]
# # @schedules = "compounding.v1"
# # start = 100
# # stop = 1000
# # compound = 1.001

# # [initialize]
# vectors = ${paths.vectors}