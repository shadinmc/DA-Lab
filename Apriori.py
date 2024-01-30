def load_data(file_path):
    transactions = []
    with open(file_path, 'r') as file:
        next(file)  
        for line in file:
            tid, items = line.strip().split(',')
            transaction = items.split()
            transactions.append((tid, transaction))
    return transactions
def get_unique_items(data):
    unique_items = set()
    for transaction in data:
        for item in transaction:
            unique_items.add(frozenset([item]))
    return unique_items
def support_count(data, itemset):
    count = 0
    for transaction in data:
        if itemset.issubset(transaction):
            count += 1
    return count

def generate_candidate_itemsets(prev_itemsets, k):
    candidates = set()
    for item1 in prev_itemsets:
        for item2 in prev_itemsets:
            union = item1.union(item2)
            if len(union) == k:
                candidates.add(union)
    return candidates
def apriori(data, min_support, min_confidence):
    unique_items = get_unique_items(data)
    frequent_itemsets = []
    k = 1
    while True:
        if k == 1:
            candidate_itemsets = unique_items
        else:
            candidate_itemsets = generate_candidate_itemsets(prev_itemsets, k)
        prev_itemsets = candidate_itemsets.copy()
        frequent_itemsets_k = []
        for itemset in candidate_itemsets:
            support = support_count(data, itemset)
            if support >= min_support:
                frequent_itemsets_k.append(itemset)
        if not frequent_itemsets_k:
            break
        frequent_itemsets.extend(frequent_itemsets_k)
        k += 1
    rules = []
    for itemset in frequent_itemsets:
        for item in itemset:
            antecedent = frozenset([item])
            consequent = itemset - antecedent
            confidence = support_count(data, itemset) / support_count(data, antecedent)
            if confidence >= min_confidence:
                rules.append((antecedent, consequent, confidence))
    return frequent_itemsets, rules
def main() :
    file_path = "apriori.csv"  
    min_support = 2
    min_confidence = 0.7 
    data = load_data(file_path)
    transactions = [transaction for _, transaction in data]  
    frequent_itemsets, rules = apriori(transactions, min_support, min_confidence)
    print(transactions)
    print("Frequent Itemsets:")
    print(frequent_itemsets[-1])
    print("\nAssociation Rules:")
    for rule in rules:
        antecedent, consequent, confidence = rule
        print(f"{antecedent} => {consequent} (Confidence: {confidence:.2f})")
main()
