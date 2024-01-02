from itertools import chain, combinations

class Aprio:

    def __init__(self, dataset, min_support, min_confidence):
        self.transactions = self.list_from_dataframe(dataset)
        self.item_sets = self.generate_item_sets()
        self.min_support = min_support
        self.min_confidence = min_confidence
        pass

    """
        input: transactions in form of a dataframe
        output: a 2-D list of transactions [[item1, item2...], [item1, item3...]]
    """
    def list_from_dataframe(self, dataset):
        list_ = []
        for index in range(dataset.shape[0]):
            row = dataset.iloc[index].dropna()
            list_.append(list(row.values))
        return list_
    
    """
        needed data: 2-D list of transactions
        output: a list of all items in all transactions 
    """
    def generate_item_sets(self):
        return [frozenset([item]) for transaction in self.transactions for item in transaction]
    

    """
        removes items that does not verify the minimum support condition
    """
    def prune_min_supp(self, candidate_counts):
        return {itemset for itemset, count in candidate_counts.items() if count >= self.min_support}
        

    def prune_subsets(self,candidates, prev_frequent_itemsets):
        pruned_candidates = set()
        for candidate in candidates:
            is_valid = True
            subsets = combinations(candidate, len(candidate) - 1)
            for subset in subsets:
                if frozenset(subset) not in prev_frequent_itemsets:
                    is_valid = False
                    break
            if is_valid:
                pruned_candidates.add(candidate)
        return pruned_candidates


    def generate_next_candidates_set(prev_candidates, k):
        candidates = set()
        for itemset1 in prev_candidates:
            for itemset2 in prev_candidates:
                union_set = itemset1.union(itemset2)
                if len(union_set) == k:
                    candidates.add(union_set)
        return candidates


    """
        needed data: 2-D list of transactions
        output: list of union(F_k), frequent items in eatch iteration 
    """
    def get_frequent_itemsets(self):
        itemsets = self.item_sets.copy()
        frequent_itemsets = []
        
        k = 2

        while itemsets:

            candidate_counts = {}
            for transaction in self.transactions:
                for candidate in itemsets:
                    if candidate.issubset(transaction):
                        candidate_counts[candidate] = candidate_counts.get(candidate, 0) + 1
            
            # Prune candidates that do not meet the minimum support
            frequent_itemsets_k = self.prune_min_supp(candidate_counts)
            
            # Generate candidates for the next iteration
            candidates_k = self.generate_next_candidates_set(frequent_itemsets_k, k)
            
            # Prune candidates using the Apriori property
            
            
            frequent_itemsets.extend(frequent_itemsets_k)
            itemsets = candidates_k
            k += 1
        
        return frequent_itemsets