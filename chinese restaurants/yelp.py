#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import json
import csv
from pprint import pprint
from nltk import word_tokenize
import  operator
import string

ifname = r'C:\Users\chengkai\Downloads\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_business.json'
ofname = 'c_restaurants.csv'

freq = {}

with open(ofname, 'w', newline='', encoding='utf-8') as output:
    fieldnames = ['name', 'city', 'state']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    with open(ifname) as input:
        for line in input:
            business = json.loads(line)
            cat = business['categories']
            if ('Chinese' in cat) and ('Restaurants' in cat):
                name = business['name']
                name = name.replace('Hong Kong', 'HongKong')
                
                if 'Panda Express' in name or 'P.F. Chang' in name or 'P F Chang' in name or 'Pei Wei' in name: continue

                state = business['state']
                if state == 'QC' or state == 'ON' or state == 'BW' or state == 'EDH': continue
                
                city = business['city']
                writer.writerow({'name': name, 'city': city, 'state': state})

                tokens = word_tokenize(name)

                if (tokens[-4:] == ['Chinese', '&', 'Thai', 'Restaurant']
                or tokens[-4:] == ['Chinese', '&', 'Japanese', 'Buffet']
                or tokens[-4:] == ['Chinese', 'and', 'Mexican', 'Food']
                or tokens[-4:] == ['Chinese', '&', 'Sushi', 'Restaurant']
                or tokens[-4:] == ['Chinese', 'Food', 'and', 'Minimart']):
                    tokens = tokens[:-4]
                elif (tokens[-3:] == ['Chinese', 'Food', 'Restaurant']
                or tokens[-3:] == ['Chinese', 'Cuisine', 'Restaurant']
                or tokens[-3:] == ['Chinese', 'Gourmet', 'Buffet']
                or tokens[-3:] == ['Restaurant', '&', 'Lounge']):
                    tokens = tokens[:-3]  
                elif (tokens[-2:] == ['Chinese', 'Restaurant']
                or tokens[-2:] == ['Chinese', 'Restruant']
                or tokens[-2:] == ['Chinese', 'Resturant']
                or tokens[-2:] == ['Chinese', 'Buffet']
                or tokens[-2:] == ['Chinese', 'Buffett']
                or tokens[-2:] == ['Chinese', 'Cafe']
                or tokens[-2:] == ['Chinese', 'Bistro']
                or tokens[-2:] == ['Chinese', 'Cuisine']
                or tokens[-2:] == ['Chinese', 'Cusine']
                or tokens[-2:] == ['Chinese', 'Gourmet']
                or tokens[-2:] == ['Chinese', 'Food']
                or tokens[-2:] == ['Chinese', 'Takeout']
                or tokens[-2:] == ['Chinese', 'Kitchen']
                or tokens[-2:] == ['Chinese', 'Dining']
                or tokens[-2:] == ['Chinese', 'Express']
                or tokens[-2:] == ['Chinese', 'Ex']
                or tokens[-2:] == ['Chinese', 'Delivery']
                or tokens[-2:] == ['Chinese', 'Fusion']
                or tokens[-2:] == ['Chinese', 'Grill']):
                    tokens = tokens[:-2]
                elif (tokens[-1:] == ['Restaurant']
                or tokens[-1:] == ['Buffet']
                or tokens[-1:] == ['Cafe']
                or tokens[-1:] == ['Bistro']
                or tokens[-1:] == ['Cuisine']
                or tokens[-1:] == ['Chinese']):
                    tokens = tokens[:-1]

                for token in set(tokens):
                    if token not in freq:
                        freq[token] = 1
                    else:
                        freq[token] += 1

   
with open('freq.csv', 'w', newline='', encoding='utf-8') as ffile:
    fieldnames = ['term', 'frequency']
    writer = csv.DictWriter(ffile, fieldnames=fieldnames)
    writer.writeheader()
    sorted_freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    for (key, value) in sorted_freq:
        writer.writerow({'term': key, 'frequency': value})

with open('chinese.json', 'w', newline='', encoding='utf-8') as outfile:
    allcounts = []
    for key, val in freq.items():
        if val <= 5: continue
        wordcount = {}
        wordcount['name'] = key
        wordcount['size'] = val
        allcounts.append(wordcount)
    jobject ={}
    jobject["name"] = "meaningless"
    jobject["children"] = allcounts
    
    json.dump(jobject, outfile)

