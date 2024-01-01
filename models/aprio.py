"""
    this the implementation of the apriori Algorithm
"""

"""
    pseudo code
"""

"""
    L[1] = {frequent 1-itemsets};
    for (k=2; L[k-1] != 0; k ++) do begin
        // perform self-joining
        C[k] = getUnion(L[k-1])
        // remove pruned supersets
        C[k] = pruning(C[k])
        // get itemsets that satisfy minSup
        L[k] = getAboveMinSup(C[k], minSup)
    end
    Answer = Lk (union) 
"""

from utils import *
from collections import Counter, defaultdict

def aprio(dataset, minSup, minConf):
    
    C1ItemSet = get_items(dataset)
    
    globalFreqItemSet = dict()
    
    globalItemSetWithSup = defaultdict(int)

    item_counts = Counter(dataset.values.flatten().astype(str))

    L1ItemSet = above_min_supp(C1ItemSet, item_counts, minSup, globalItemSetWithSup)

    currentLSet = L1ItemSet

    k = 2

    # Calculating frequent item set
    while(currentLSet):
        
        globalFreqItemSet[k-1] = currentLSet
        
        candidateSet = union(currentLSet, k)
        # Perform subset testing and remove pruned supersets
        candidateSet = prun(candidateSet, currentLSet, k-1)
        # Scanning itemSet for counting support
        currentLSet = above_min_supp(candidateSet, item_counts, minSup, globalItemSetWithSup)
        k += 1


    #rules = associationRule(globalFreqItemSet, globalItemSetWithSup, minConf)
    #rules.sort(key=lambda x: x[2])

    return globalFreqItemSet#, rules

