import os, sys, random, codecs
import pickle, datetime, logging

import memory_profiler, line_profiler

import lzma, json
from pathlib import Path
import xml.etree.cElementTree as ET
import pandas as pd
import numpy as np

class CaseWrangler():

    def extractCases(self, file):
        #Set path to locate files
        compressed_file = os.path.join(file)

        cases = []
        #Decompress the file line by line
        with lzma.open(compressed_file) as infile:
            for line in infile:
                #decode the file into a convenient format
                record = json.loads(str(line, 'utf-8'))
                cases.append(record)

        print("Number of Cases: {}".format(len(cases)))
        # cases_law = open('cases_law.pkl', 'wb')
        # pickle.dump(cases, cases_law)

        return cases

    def wrangleCases(self, cases):
        parsed_files = []

        # Parsing files to extract used variables
        for case in cases:
            feat_dict = {}
            header = True
            feat_dict["court"] = case['court']['name']
            feat_dict["jurisdiction"] = case['jurisdiction']['name_long']
            feat_dict["name"] = case['jurisdiction']['name']
            feat_dict["citation"] = [citation for citation in case['citations'] if citation['type'] == 'official'][0]['cite']
            feat_dict["name"] = case['name_abbreviation']
            feat_dict["date"] = case['decision_date']
            for elem in ET.fromstring(case['casebody']['data']):
                opinions = []
                if elem.tag.split("}")[1] == "opinion":
                    op = {}
                    text = []
                    op["type"] = elem.attrib["type"]
                    op["author"] = ""
                    for opinion_element in elem.getchildren():
                        if opinion_element.tag.split("}")[1] == 'author':
                            op["author"] = opinion_element.text.replace(u'\xad', '')
                        else:
                            text.append(opinion_element.text.replace(u'\xad', ''))
                    op["text"] = " ".join(text)
                    opinions.append(op)
            feat_dict["opinions"] = opinions

            parsed_files.append(feat_dict)

        raw_df = pd.DataFrame(parsed_files)
        df = raw_df[raw_df['court'].isin(raw_df['court'].value_counts()[:4].index.tolist())]
        df = df[df['court'].isin(df['court'].value_counts()[:4].index.tolist())]

        array_opinions = []

        #Loop through case dataframe and flatten opinions
        for _, row in df.iterrows():
            for opinion in row['opinions']:
                temp = {}
                keys = list(row.keys())
                keys.remove('opinions')
                for key in keys:
                    temp[key] = row[key]
                keys = list(opinion.keys())
                for key in keys:
                    temp[key] = opinion[key]
                array_opinions.append(temp)

        df = pd.DataFrame(array_opinions)
        # df_law = open('df_law.pkl', 'wb')
        # pickle.dump(df, df_law)

        return df
