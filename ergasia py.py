import pandas as pd #like in lab codes
import numpy as np #like in lab codes
df = pd.read_csv('Groceries_dataset.csv') #to read the csv file and df for dataframe to be able to work with it
# create something like a dictionary to be able to store basket items for each costumer without beraking th program
baskets_dict = {} #empty dictionary


# scan the dataframe row by row in a single loop 38,766 rows instead of 1.45  billion rows (38.766^2) by doing double loop
for index, row in df.iterrows():
    #getting all the information from csv file 
    member_id = row['Member_number']
    date = row['Date']
    item = row['itemDescription']
    
    # create a key for dictionary by member id and date
    key = (member_id, date)
    
    if key not in baskets_dict:
        # if isnt there make a new list for that key
        baskets_dict[key] = []
        
    # if its there just store it
    baskets_dict[key].append(item)

#when its finished the csv file converts all of them into sets

transactions = [set(items) for items in baskets_dict.values()]
#transactions cuz its easier to work with that and easy to remember it

print(f"Created{len(transactions)}distinct baskets")

#now i need to know all items that sold to the costumers
items_list=[]
for basket in transactions:
    for item in basket:
        items_list.append(item)

store_items = sorted(set(items_list))
#sorted list of all items sold th th estore 
print(f"Store has {len(store_items)}distinct items")

#custom code for apriori algorithm, i guess?
#user input for minimum support and confidence as asked in the ergasia 

min_support = float(input("Enter minimum support (as a decimal, eg. 0.01 for 1%)"))
min_confidence = float(input("Enter minimum confidence (as a decimal, eg. 0.5 for 50%)"))

#for k = 1 first apriori algorithm step, praying to code will run
item_counts = {}
for basket in transactions:
    for item in basket:
        if item not in item_counts:
            item_counts[item]= 0
        item_counts[item] +=1

L1= {}#empty table to store k = 1 items and their support values, as wanted in ergasia
rejected_count = 0
for item, count in item_counts.items():
    support = count/len(transactions)

    if support>=min_support:
        L1[frozenset([item])] = support
#frozenset to avoid duplicated sets like {milk, bread} and {bread, milk} being counted as different sets
    else:
        rejected_count +=1 #rejeted items as wanted in ergasia

print(f"\nResults for k = 1")
print(f"Total Candidate items tested: {len(item_counts)}")
print(f"Surviving Frequent 1-itemsets (L1): {len(L1)}")
print(f"Items rejected: {rejected_count}")

#printing them as its wanted to be there
l1_items = list(L1.keys())

candidate_2 = set()#trying to merge them to be able to continue for k = 2 then its starts apriori algorithm and pd.merge() was hader

n = len(l1_items)
for i in range(n):
    for j in range(i + 1, n):
        pair  = l1_items[i].union(l1_items[j])

        candidate_2.add(pair)
print(f"\ntotal items in the candidate 2-itemsets are: {len(candidate_2)}")
