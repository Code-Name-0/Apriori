from itertools import combinations

class Aprio:

    def __init__(self, dataset, min_support, min_confidence):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.transactions = self.list_from_dataframe(dataset)
        self.item_sets = self.generate_item_sets()
        self.frequent_items = self.get_frequent_itemsets()
        self.items_count = self.get_items_count()
        self.rules = self.generate_rules(self.frequent_items, self.min_confidence)
        
    def get_items_count(self):
        print("====> getting items' count")

        items_count = {}
        for transaction in self.transactions:

            for itemset in self.frequent_items:

                if itemset.issubset(transaction):
                    items_count[itemset] = items_count.get(itemset, 0) + 1

        return items_count

    """
        input: transactions in form of a dataframe
        output: a 2-D list of transactions [[item1, item2...], [item1, item3...]]
    """
    def list_from_dataframe(self, dataset):
        print("====> getting list of transactions")

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
        print("====> generating item sets")

        return [frozenset([item]) for transaction in self.transactions for item in transaction]
    
    """
        removes items that does not verify the minimum support condition
    """
    def prune_min_supp(self, candidate_counts):
        print("====> pruning min support")

        return {itemset for itemset, count in candidate_counts.items() if count  >= self.min_support}
   
    """
        removes items that does not occure in the previous frequent itemset
    """ 
    def prune_subsets(self,candidates, prev_frequent_itemsets):
        print("====> pruning")

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

    def generate_next_candidates_set(self, prev_candidates, k):
        print("====> generating next condidates")

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
        print("====> getting frequent items")

        itemsets = self.item_sets.copy()
        frequent_itemsets = []
        k = 2

        while itemsets:

            candidate_counts = {}
            for transaction in self.transactions:

                for candidate in itemsets:

                    if candidate.issubset(transaction):
                        candidate_counts[candidate] = candidate_counts.get(candidate, 0) + 1
            
            frequent_itemsets_k = self.prune_min_supp(candidate_counts)
            
            candidates_k = self.generate_next_candidates_set(frequent_itemsets_k, k)
            
            candidates_k = self.prune_subsets(candidates_k, frequent_itemsets_k)
            
            frequent_itemsets.extend(frequent_itemsets_k)

            itemsets = candidates_k
            
            k += 1
        
        return frequent_itemsets

    def calculate_confidence(self, itemset, antecedent):
        return float("%.4f" % (self.items_count[itemset] / self.items_count[antecedent])) 

    def calculate_lift(self, confidence, consequent):
        return float("%.4f" % (confidence / self.calculate_support(consequent)))

    def calculate_support(self, itemset):
        return float("%.4f" %(self.items_count[itemset] / len(self.transactions)))

    def generate_rules(self, frequent_itemsets, min_confidence):
        print("====> generating rules")

        rules = []
        for itemset in frequent_itemsets:

            if len(itemset) > 1:

                itemset_list = list(itemset)
                for i in range(1, len(itemset)):

                    antecedent = frozenset(itemset_list[:i])
                    consequent = frozenset(itemset_list[i:])
                    confidence = self.calculate_confidence(itemset, antecedent)
                    lift = self.calculate_lift(confidence, consequent)
                    if confidence >= min_confidence:
                        if len(list(antecedent)) > 0 and len(list(consequent)) > 0:
                            rules.append({"antecedent": list(antecedent), "consequent": list(consequent), "confidence": confidence, "lift": lift})
        
        return rules
    