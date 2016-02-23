import copy
import string
import math
from collections import defaultdict
from itertools import combinations
from scipy.stats import chisquare
 
def readfile(filename):
    import csv
    with open(filename) as f:
        reader = csv.reader(f)
        row = []
        i = 0
        for line in reader:
            if (i != 0):
                row.append(line)
            i = i + 1
             
        return row
 
def preprocess(dataset):
    ### review: a list of text of reviews, lower-cased, punctuation removed
    review = []
    for i in range(len(dataset)):
        review.append(dataset[i][7].lower())
        for c in string.punctuation:
            review[i] = str(review[i]).replace(c,"")
        review[i] = review[i].split()
    
#     print("*** Top 10 key term ***")
    ### d: a dictionary that counts frequency of every unique word
    d = defaultdict(int)
    for text in review:
        for word in text:
            d[word] += 1
    d = sorted(d.items(), key=lambda item: item[1], reverse=True)
       
    ### key_term: a list of key term ranked from 100 to 2100 in d
    key_term = []
    for i in range(100, 2100):
        key_term.append(d[i][0])
          
    ### print top 10 words from key_term
#     for i in range(10):
#         print("WORD", i + 1, ":", key_term[i])
#     print("***********************")
    
    new_dataset = []
    k = 0
    for text in review:
        temp = []
        for i in range(len(key_term)):
            if key_term[i] in text:
                temp.append(1)
            else:
                temp.append(0)
        if int(dataset[k][6]) == 5:
            temp.append(1)
            temp.append(0)
        else:
            temp.append(0)
            temp.append(1)
        new_dataset.append(temp)
        k += 1
        
    return new_dataset, key_term

def generateItemset(itemsets, support, binary_data):
    new_itemsets = []
    new_freq = []
    num_sets = len(itemsets)    #    Number of item sets
    len_set = len(itemsets[0])  #    Length per item set
    counted_support = 0
    
    for i in range(num_sets):
        for j in range(i + 1, num_sets):
            temp = set()
            temp = temp.union(itemsets[i])
            temp = temp.union(itemsets[j])
            
            if len(temp) == (len_set + 1):  #    Check if the size of set is 1 larger than old set
                if temp not in new_itemsets:   #    Check if already exist in 
                    count = 0
                    temp2 = list(combinations(temp, len_set))
                    if len_set == 1:
                        count = len(temp2)
                    else:
                        for k in temp2: #    Check if all subset is in itemset
                            if set(k) in itemsets:
                                count += 1
                            else:
                                break
                    if count == len(temp2): 
                        counted_support += 1
                        count = 0
                        for k in range(len(binary_data)):
                            c = 0
                            for it in temp:
                                if binary_data[k][it] == 1:
                                    c += 1
                                else:
                                    break
                            if c == (len_set + 1):
                                count += 1
                        if count >= (support * len(binary_data)):
                            new_itemsets.append(temp)
                            new_freq.append(count)
            else:
                temp.clear()
                
    print("Number of itemsets whose support are counted: {0}".format(counted_support))
                
    return new_itemsets, new_freq

def generateRule(itemsets, itmsets_freq, dependentsets, depsets_freq, confidence):
    rule = []
    for i in range(len(itemsets)):
        for item in itemsets[i]:
            consequent = set()
            consequent.add(item)
            antecedent = itemsets[i].difference(consequent)
            j = dependentsets.index(antecedent)
            
            confd = float(itmsets_freq[i]) / depsets_freq[j]
            if confd >= confidence:
                t = []
                t.append(antecedent)
                t.append(consequent)
                t.append(confd)
                rule.append(t)
    return rule

def calChiSquare(ante_freq, consq_freq, rule_freq, n):
    c_t = [[rule_freq, ante_freq - rule_freq], [consq_freq - rule_freq, n + rule_freq - ante_freq - consq_freq]]
    e_t = [[float(ante_freq * consq_freq) / n, float(ante_freq * (n - consq_freq)) / n], [float((n - ante_freq) * consq_freq) / n, float((n - ante_freq) * (n - consq_freq)) / n]]
#     print(c_t)
    return chisquare(f_obs = c_t, f_exp = e_t, axis = None, ddof = 2)

def generateChiRule(itemsets, itmsets_freq, antesets, antes_freq, consqsets, consqs_freq, size, alpha):
    rule = []
    for i in range(len(itemsets)):
        for item in itemsets[i]:
            consequent = set()
            consequent.add(item)
            antecedent = itemsets[i].difference(consequent)
            j = antesets.index(antecedent)
            k = consqsets.index(consequent)
            
            sig = calChiSquare(antes_freq[j], consqs_freq[k], itmsets_freq[i], size)[1]
            if sig <= alpha:
                t = []
                t.append(antecedent)
                t.append(consequent)
                t.append(sig)
                rule.append(t)
    return rule


def generateChiRule_corrected(itemsets, itmsets_freq, antesets, antes_freq, consqsets, consqs_freq, size, alpha, n):
    rule = []
    for i in range(len(itemsets)):
        for item in itemsets[i]:
            consequent = set()
            consequent.add(item)
            antecedent = itemsets[i].difference(consequent)
            j = antesets.index(antecedent)
            k = consqsets.index(consequent)
            
            sig = calChiSquare(antes_freq[j], consqs_freq[k], itmsets_freq[i], size)[1]
            p = (1 - (1 - alpha)**(1.0 / n))
            if sig <= p:
                t = []
                t.append(antecedent)
                t.append(consequent)
                t.append(sig)
                rule.append(t)
    return rule

def printRule(rule, keyterm, label, L2, L2_freq, L3, L3_freq):
    import sys
    print("Association Rule:")
    print("Antecedent\t\tConsequent\t\t{0}\t\tSupport".format(label))
    for r in rule:
        a = r[0]
        c = r[1]
        f = r[2]
        s = a.union(c)
        if len(a) == 2:
            ind = L3.index(s)
            if (len(keyterm[list(a)[0]]) + len(keyterm[list(a)[1]])) > 11:
                sys.stdout.write('{'+ keyterm[list(a)[0]] + ', ' + keyterm[list(a)[1]] +"}\t{" + keyterm[list(c)[0]] + "}\t\t" + str(f))
                if len(str(f)) > 15:
                    sys.stdout.write("\t")
                else:
                    sys.stdout.write("\t\t")
                sys.stdout.write(str(float(L3_freq[ind]) / 5000))
                print()
            else:
                sys.stdout.write('{'+ keyterm[list(a)[0]] + ', ' + keyterm[list(a)[1]] +"}\t\t{" + keyterm[list(c)[0]] + "}\t\t" + str(f))
                if len(str(f)) > 15:
                    sys.stdout.write("\t")
                else:
                    sys.stdout.write("\t\t")
                sys.stdout.write(str(float(L3_freq[ind]) / 5000))
                print()
        elif len(a) == 1:
            ind = L2.index(s)
            if len(keyterm[list(a)[0]]) > 5:
                sys.stdout.write('{'+keyterm[list(a)[0]]+'}' + "\t\t" + '{' + keyterm[list(c)[0]] + '}' + "\t\t" + str(f))
                if len(str(f)) > 15:
                    sys.stdout.write("\t")
                else:
                    sys.stdout.write("\t\t")
                sys.stdout.write(str(float(L2_freq[ind]) / 5000))
                print()
            else:
                sys.stdout.write('{'+keyterm[list(a)[0]]+'}' + "\t\t\t" + '{' + keyterm[list(c)[0]] + '}' + "\t\t" + str(f))
                if len(str(f)) > 15:
                    sys.stdout.write("\t")
                else:
                    sys.stdout.write("\t\t")
                sys.stdout.write(str(float(L2_freq[ind]) / 5000))
                print()
        else:
            print("ERROR!!!")
        


print(100 * '-')
data = readfile("stars_data.csv")
binary_data, keyterm = preprocess(data)
keyterm.append("isPositive")
keyterm.append("isNegative")
n_col = len(binary_data[0])
n_row = len(binary_data)
support = 0.03
confidence = 0.25
alpha = 0.05
         
L1 = []
L1_freq = []
for c in range(n_col):
    freq = 0
    for r in range(n_row):
        if binary_data[r][c] == 1:
            freq += 1
    if freq >= (support * n_row):
        temp = set()
        temp.add(c)
        L1.append(temp)
        L1_freq.append(freq)
                   
print("L1 has {0} itemsets\n".format(len(L1)))
# print(L1)
# print(L1_freq)
# print()
       
L2, L2_freq = generateItemset(L1, support, binary_data)
print("L2 has {0} itemsets\n".format(len(L2)))
# print(L2)
# print(L2_freq)
# print()
       
L3, L3_freq = generateItemset(L2, support, binary_data)
print("L3 has {0} itemsets\n".format(len(L3)))
# print(L3)
# print(L3_freq)
# print()
   
   
print("\nGenerating rules based on confidence ......")
L2_rule = generateRule(L2, L2_freq, L1, L1_freq, confidence)
print("{0} rules are generated from L2".format(len(L2_rule))) 
L3_rule = generateRule(L3, L3_freq, L2, L2_freq, confidence)
print("{0} rules are generated from L3".format(len(L3_rule)))
rule = copy.deepcopy(L2_rule)
for r in L3_rule:
    rule.append(r)
top_rule = sorted(rule, key=lambda x:x[2], reverse = True)[:30]
# printRule(top_rule, keyterm, "Confidence", L2, L2_freq, L3, L3_freq)
   
print("\nGenerating rules based on chi-square ......")
L2_chi_rule = generateChiRule(L2, L2_freq, L1, L1_freq, L1, L1_freq, n_row, alpha)
print("{0} rules are generated from L2".format(len(L2_chi_rule)))
L3_chi_rule = generateChiRule(L3, L3_freq, L2, L2_freq, L1, L1_freq, n_row, alpha)
print("{0} rules are generated from L3".format(len(L3_chi_rule)))
chi_rule = copy.deepcopy(L2_chi_rule)
for r in L3_chi_rule:
    chi_rule.append(r)
top_chi_rule = sorted(chi_rule, key=lambda x:x[2], reverse = False)[:30]
# printRule(top_chi_rule, keyterm, "Significant", L2, L2_freq, L3, L3_freq)

print("\nGenerating rules based on corrected chi-square ......")
n = 2 * len(L2) + 3 * len(L3)
L2_correct_rule = generateChiRule_corrected(L2, L2_freq, L1, L1_freq, L1, L1_freq, n_row, alpha, n)
print("{0} rules are generated from L2".format(len(L2_correct_rule)))
L3_correct_rule = generateChiRule_corrected(L3, L3_freq, L2, L2_freq, L1, L1_freq, n_row, alpha, n)
print("{0} rules are generated from L3".format(len(L3_correct_rule)))
correct_rule = copy.deepcopy(L2_correct_rule)
for r in L3_correct_rule:
    correct_rule.append(r)
top_correct_rule = sorted(correct_rule, key=lambda x:x[2], reverse = False)[:30]
# printRule(top_correct_rule, keyterm, "Significant", L2, L2_freq, L3, L3_freq)

print("-" * 100)