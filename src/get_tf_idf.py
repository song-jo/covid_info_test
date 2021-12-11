import argparse
from pathlib import Path
import os
import json
import re
import math
parentdir = Path(__file__).parents[1]
"""
USAGE: python3 get_tf_idf.py -i ../data/tweetsday*.json -o outputfile

Computes 10 highest tf-idf words for each topic for one jsonfile

TODO: do it for all jsonfile together

"""



def read_json(jsonfile):
    with open(jsonfile, "r") as jfile:
        jsonfile = json.load(jfile)
        return jsonfile['data']


def getstopwords(file):
    stopset = set([])
    with open(file, 'r') as stopwords:
        for line in stopwords:
            if line[0]!='#':
                stopset.add(line.strip())
    return stopset 

def compute_word_count(tweetlist, wdict, stopwords):
    topiclist = ["vaccination", "variants", "safety measures", "economy", "symptoms", "news", "other"]
    rx = '[' + re.escape('()[],-.?!:;#&')+ ']'
    for tweet in tweetlist:
        topic = topiclist[tweet['topic']-1]
        curdict = wdict[topic]
        newtext = re.sub(rx, " ", tweet['text'])
        newtext = newtext.strip()
        newtext = newtext.split(' ')
        for word in newtext:
            if word.isalpha() and (word.lower() not in stopwords):
                word = word.lower()
                if word not in curdict:
                    curdict[word] = 1
                else:
                    curdict[word]+=1

def write_to_output(wdict, out):
    with open(out, 'w') as o:
        json.dump(wdict, o, indent=4)

def remove_non_freq(worddict):
    
    for topic in worddict:
        newworddict = {}
        for word in worddict[topic]:
            totalcount = 0
            for t in worddict:
                if word in worddict[t]:
                    totalcount +=worddict[t][word]
            if totalcount >=5:
                newworddict[word] = worddict[topic][word]
            
        worddict[topic] = newworddict

def compute_tf_idf(word, word_dict, topic):
    tf = word_dict[topic][word]
    word_count = 0
    for topic in word_dict:
        if word in word_dict[topic]:
            word_count +=1
    idf = math.log(len(word_dict)/word_count)
    return tf*idf

def compute_stat(wordcounts):
    stat_dict = {"vaccination":[], "variants":[], "safety measures":[], "economy":[], "symptoms":[], "news":[], "other":[]}

    for topic in wordcounts:
        for word in wordcounts[topic]:
            stat_dict[topic].append([word, compute_tf_idf(word, wordcounts, topic)])
    return stat_dict

def sortandkeepn(stat_dict, n):
    for topic in stat_dict:
        stat_dict[topic].sort(key = lambda x: x[1], reverse = True)
        stat_dict[topic] = stat_dict[topic][:n]
        #stat_dict[pony] = [x[0] for x in stat_dict[pony]]
    return stat_dict
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-j', '--input2')
    parser.add_argument('-k', '--input3')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    
    
    topics = {"vaccination":{}, "variants":{}, "safety measures":{}, "economy":{}, "symptoms":{}, "news":{}, "other":{}}
    stopwords = getstopwords(os.path.join(parentdir, 'data', 'stopwords.txt'))
    compute_word_count(read_json(args.input), topics, stopwords)
    compute_word_count(read_json(args.input2), topics, stopwords)
    compute_word_count(read_json(args.input3), topics, stopwords)
    
    remove_non_freq(topics)
    stats = compute_stat(topics)
    sortandkeepn(stats, 10)
    
    write_to_output(stats, args.output)
    
    




if __name__ == '__main__':
    main()
