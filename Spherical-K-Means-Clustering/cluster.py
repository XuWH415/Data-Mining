import copy
import string
import math
import statistics
import random
from collections import defaultdict
from sklearn.cluster import KMeans
from sphericalKMeans import SphericalKMeans
# import sphericalKMeans as SKM
import nbc as nbc

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

def preprocess(dataset, key_term):
    ### review: a list of text of reviews, lower-cased, punctuation removed
    review = []
    class_labels = []
    for i in range(len(dataset)):
        review.append(dataset[i][7].lower())
        for c in string.punctuation:
            review[i] = str(review[i]).replace(c,"")
		review[i] = review[i].split()
        if int(dataset[i][6]) == 5:
            class_labels.append(1)
        else:
            class_labels.append(0)
         
    ### Check if the dataset is the training data or the testing data
    if len(key_term) == 0:
        print("*** Top 10 key term ***")
        ### d: a dictionary that counts frequency of every unique word
        d = defaultdict(int)
        for text in review:
            for word in text:
                d[word] += 1
        d = sorted(d.items(), key=lambda item: item[1], reverse=True)
         
        ### key_term: a list of key term ranked from 200 to 2200 in d
        key_term = []
        for i in range(200, 2200):
            key_term.append(copy.deepcopy(d[i][0]))
             
        ### print top 10 words from key_term
        for i in range(10):
            print("WORD", i + 1, ":", key_term[i])
        
        print("***********************")
     
    ### W_P, W_NP: two matrixes of dimension 2000 * 2500
    W_P = []
    W_NP = []
    for i in range(2000):
        k = 0
        temp_p = []
        temp_np = []
        for text in review:
            if int(dataset[k][6]) == 5:
                temp_p.append(text.count(key_term[i]))
            else:
                temp_np.append(text.count(key_term[i]))
            k = k + 1
#         if i < 10:
#             print(temp_p[:50])
#             print(temp_np[:50])
        W_P.append(temp_p)
        W_NP.append(temp_np)
    print("Dimension of W_P: {0} * {1}\nDimension of W_NP: {2} * {3}".format(len(W_P), len(W_P[0]), len(W_NP), len(W_NP[0])))
    
    return W_P, W_NP, key_term, review, class_labels

def generateTopic(estimator, data, num_cluster, key_term): ### Generate topics using estimator on data
    estimator.fit(data)
    print("Score directly from estimator: {0}".format(estimator.inertia_))
    
    topic = []
    for i in range(max(estimator.labels_) + 1):
        temp = []
        for j, k in enumerate(estimator.labels_):
            if k == i:
                temp.append(key_term[j])
        topic.append(temp)
    
    return topic 
    
def binaryTopic(positive_topic, negative_topic, review, class_labels):
    binary_topic = []
    len_review = len(review)
    len_positive = len(positive_topic)
    len_negative = len(negative_topic)
    
    for i in range(len_review):
        temp = [0] * (len_positive + len_negative)
        for j in range(len_positive):
            for word in positive_topic[j]:
                if word in review[i]:
                    temp[j] = 1
                    break
        for j in range(len_negative):
            for word in negative_topic[j]:
                if word in review[i]:
                    temp[j + len_positive] = 1
                    break
        temp.append(class_labels[i])
        binary_topic.append(temp)
                
    return binary_topic

def crossValidation(dataset, k):
    tss = [0.04, 0.1, 0.2, 0.4, 0.8]
    new_dataset = copy.deepcopy(dataset)
    random.shuffle(new_dataset)
    for portion in tss:
        zero_one_loss = [0] * k
        for i in range(k):
            testset = [x for j, x in enumerate(new_dataset) if j % k == i]
            restset = [x for j, x in enumerate(new_dataset) if j % k != i]
            trainset = random.sample(restset, int(len(restset) * portion))
            model, positive_label, negative_label = nbc.nbclassifier(trainset)
            zero_one_loss[i] = nbc.testmodel(model, positive_label, negative_label, testset)
        print("tss: {0}, 0/1 Loss mean: {1}, 0/1 Loss sterr: {2}".format(portion, statistics.mean(zero_one_loss), statistics.stdev(zero_one_loss) / math.sqrt(k)))



print(100 * '-')
#===============================================================================
# Part 0: readfile
#===============================================================================
print("PART 0: readfile")
dataset = readfile("stars_data.csv")
print()
 
#===============================================================================
# Part 1: choose proper k
#===============================================================================
print("PART 1: choose proper k")
W_P, W_NP, key_term, review, class_labels = preprocess(dataset, [])
cluster_size = [10, 20, 50, 100, 200]
    
print()
# for c_size in cluster_size:
#     positive_topic = generateTopic(KMeans(init = 'k-means++', n_clusters = c_size, max_iter = 100, n_init = 10), W_P, c_size, key_term)
#     negative_topic = generateTopic(KMeans(init = 'k-means++', n_clusters = c_size, max_iter = 100, n_init = 10), W_NP, c_size, key_term)
print("K-Means (k = 50):")
positive_topic = generateTopic(KMeans(init = 'k-means++', n_clusters = 50, max_iter = 100, n_init = 50), W_P, 50, key_term)
negative_topic = generateTopic(KMeans(init = 'k-means++', n_clusters = 50, max_iter = 100, n_init = 50), W_NP, 50, key_term)
# print("Positive topics:\n{0}".format(positive_topic))
# print("Negative topics:\n{0}".format(negative_topic))
    
# exit()
print()
# for c_size in cluster_size:
#     positive_s_topic = generateTopic(SphericalKMeans(n_clusters = c_size, max_iter = 100, n_init = 10), W_P, c_size, key_term)
#     negative_s_topic = generateTopic(SphericalKMeans(n_clusters = c_size, max_iter = 100, n_init = 10), W_NP, c_size, key_term)
print("Spherical K-Means (k = 50):")
positive_s_topic = generateTopic(SphericalKMeans(n_clusters = 50, max_iter = 100, n_init = 50), W_P, 50, key_term)
negative_s_topic = generateTopic(SphericalKMeans(n_clusters = 50, max_iter = 100, n_init = 50), W_NP, 50, key_term)
# print("Positive topics:\n{0}".format(positive_s_topic))
# print("Negative topics:\n{0}".format(negative_s_topic))
print()
# exit()
 
#===============================================================================
# Part 2: compare K-Means with Spherical K-Means
#===============================================================================
print("PART 2: compare K-Means with Spherical K-Means")
binary_topic = binaryTopic(positive_topic, negative_topic, review, class_labels)
binary_s_topic = binaryTopic(positive_s_topic, negative_s_topic, review, class_labels)
print("K-Means:")
crossValidation(binary_topic, 10)
print("Spherical K-Means:")
crossValidation(binary_s_topic, 10)
print()
# exit()

#===============================================================================
# Part 3: compare plain feature with topic feature
#===============================================================================
print("PART 3: compare plain feature with topic feature")
nbc_dataset, key_term = nbc.preprocess(dataset, 6, 0, key_term)
print("Plain feature:")
crossValidation(nbc_dataset, 10)
print("Topic feature:")
crossValidation(binary_s_topic, 10)
print()
# exit()
 
#===============================================================================
# Part 4: assess number of features
#===============================================================================
print("PART 4: assess number of features")
new_key_term = copy.deepcopy(key_term)
random.shuffle(new_key_term)
nbc_new_dataset, new_key_term = nbc.preprocess(dataset, 6, 0, new_key_term[:100])
print("Selected plain feature:")
crossValidation(nbc_new_dataset, 10)
print("Topic feature:")
crossValidation(binary_s_topic, 10)
print("Combination of plain feature and topic feature:")
combined_dataset = copy.deepcopy(nbc_new_dataset)
for i in range(len(combined_dataset)):
    combined_dataset[i].pop()
    combined_dataset[i].extend(binary_s_topic[i])
crossValidation(combined_dataset, 10)