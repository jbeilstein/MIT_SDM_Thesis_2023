# Used with CUDA 12.2.2

# pip install cupy-cuda11x
# pip install -U 'spacy[cuda-autodetect]'
# pip install networkx
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

data_entry = ['','','','','','','','','','','','','','','','','','','','']
data_file = 'data.csv'

with open(data_file, 'a', newline='') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close()   

source_document = open('requirement_document1.pdf', 'rb')
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
                
            if hasattr(element, 'fontname'):
                font_type = element.fontname
            
            if hasattr(element, 'size'):
                font_size = element.size
                
                x=4
        else:
            text = ''

        if len(text) > 0:
            if class_name != 'LTChar' and class_name != 'LTAnno' and class_name != 'LTLine':
            # if class_name != 'LTChar' and class_name != 'LTAnno' and class_name != 'LTLine' and class_name != 'LTTextLineHorizontal':
                categorized = ''
                itemized = ''
                relational = ''
                referenced = ''                
                
                data_entry = [id_num, page_id, class_name, coords0, coords1, coords2, coords3, logical_shall, logical_should, parent_of, sibling_of, child_of, reference_internal, reference_external, association_with, text]
                
                with open(data_file, 'a', encoding="utf-8", newline='') as object:
                    write_object = writer(object)
                    write_object.writerow(data_entry)
                    object.close() 
                                       
                id_num = id_num + 1