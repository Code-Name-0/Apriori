from itertools import *
import json



def union(items, length):
    return set([i.union(j) for i in items for j in items if len(i.union(j)) == length])


def prun(candidateSet, prevFreqSet, length):
    tempCandidateSet = candidateSet.copy()
    for item in candidateSet:
        subsets = combinations(item, length)
        for subset in subsets:
            if(frozenset(subset) not in prevFreqSet):
                tempCandidateSet.remove(item)
                break
    return tempCandidateSet

def above_min_supp(itemSet, item_counts, minSup, globalItemSetWithSup):
    freqItemSet = set()
    
    for item in itemSet:
        if item in item_counts:
            
            globalItemSetWithSup[item] += item_counts[item]
            support = float(item_counts[item] / len(item_counts) * 100) 
            if(support >= minSup):
                freqItemSet.add(frozenset((item,)))

    return freqItemSet

def get_items(dataset):
    items = set()

    for row_index in range(dataset.shape[0]):
        row = dataset.iloc[row_index].dropna()
        for item in row:
            str_item = str(item)
            if str_item.endswith('.0'):
                str_item = str_item[:-2]
            items.add(str_item)

    return items






