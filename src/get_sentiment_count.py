import argparse
from pathlib import Path
import os
import json
import re
import math
parentdir = Path(__file__).parents[1]


def read_json(jsonfile):
    with open(jsonfile, "r") as jfile:
        jsonfile = json.load(jfile)
        return jsonfile['data']


def count(data, topics):

    for tweet in data:

        if tweet['topic'] in topics:
            topics[tweet['topic']][tweet['sentiment']]+=1

    return topics

def change_keys(dic):
    tops = {1:"vaccination", 2:"variants", 3:"safety measures", 4:"economy", 5:"symptoms", 6:"news", 7:"other"}
    sents = {1:"positive", 2:"negative", 3:"neutral"}
    x=dict((tops[key], value) for (key,value) in dic.items())

    for k in x:
        x[k]=dict((sents[key], value) for (key,value) in x[k].items())

    return x
    
def dic_to_json(output, dic):
    with open(output, 'w') as f:
        json.dump(dic,f,indent=4)

    
def total(topics):
    tot_sent = {'positive':0, 'negative':0, 'neutral':0}
    for top in topics:
        for sent in topics[top]:
            tot_sent[sent]+=topics[top][sent]

    return tot_sent





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-j', '--input2')
    parser.add_argument('-k', '--input3')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    
    topics={1:{1:0,2:0,3:0}, 2:{1:0,2:0,3:0}, 3:{1:0,2:0,3:0}, 4:{1:0,2:0,3:0}, 1:{1:0,2:0,3:0}, 5:{1:0,2:0,3:0}, 6:{1:0,2:0,3:0},7:{1:0,2:0,3:0}}


    data1=read_json(args.input)
    count(data1,topics)
    data2=read_json(args.input2)
    count(data2,topics)
    data3=read_json(args.input3)
    count(data3,topics)

    dic= change_keys(topics)
    tot = total(dic)
    dic['total']=tot
    dic_to_json(args.output, dic)




if __name__ == '__main__':
    main()
