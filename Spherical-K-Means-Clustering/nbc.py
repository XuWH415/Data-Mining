import copy
import sys
import string
import random
import statistics
import math

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

def checkcolumn(col):
    if col == 5 or col == 7:
        return (col - 1)
    else:
        print("ERROR: wrong column number!\n")
        sys.exit()

def preprocess(dataset, col, printtop, key_term):
    ### review: a list of text of reviews, lower-cased, punctuation removed
    review = []
    for i in range(len(dataset)):
        review.append(dataset[i][7].lower())
        for c in string.punctuation:
            review[i] = str(review[i]).replace(c,"")
    
    ### Check if the dataset is the training data or the testing data
    if len(key_term) == 0:
        ### d: a dictionary that counts frequency of every unique word
        from collections import defaultdict
        d = defaultdict(int)
        for text in review:
            for word in text.split():
                d[word] += 1
        d = sorted(d.items(), key=lambda item: item[1], reverse=True)
        
        ### key_term: a list of key term ranked from 200 to 2200 in d
        key_term = []
        for i in range(200, 2200):
            key_term.append(copy.deepcopy(d[i][0]))
            
        ### top: whether to print top 10 words from key_term
        if printtop == 1:
            for i in range(10):
                print("WORD", i + 1, ":", key_term[i])
    
    ### new_dataset: a list of new generated attributes using the form as required
    new_dataset = []
    k = 0
    for text in review:
        temp = []
        for i in range(len(key_term)):
            if key_term[i] in text:
                temp.append(1)
            else:
                temp.append(0)
        if col == 4:
            if int(dataset[k][4]) > 0:
                temp.append(1)
            else:
                temp.append(0)
        if col == 6:
            if int(dataset[k][6]) == 5:
                temp.append(1)
            else:
                temp.append(0)
        new_dataset.append(copy.deepcopy(temp))
        k += 1
    
    return new_dataset, key_term
    
def dividedata(dataset, k):
    random.shuffle(dataset)
    trainset = dataset[:k]
    testset = dataset[k:]
            
    return trainset, testset

def nbclassifier(trainset):
    classcol = len(trainset[0]) - 1
    positive_label = 0
    for i in range(len(trainset)):
        if trainset[i][classcol] == 1:
            positive_label += 1
    negative_label = len(trainset) - positive_label
    
    from collections import defaultdict
    model = defaultdict(int)
    for i in range(classcol):
        for line in trainset:
            if line[i] == 0 and line[classcol] == 0:
                model[0, 2 * i] += 1
            elif line[i] == 0 and line[classcol] == 1:
                model[1, 2 * i] += 1
            elif line[i] == 1 and line[classcol] == 0:
                model[0, 2 * i + 1] += 1
            else:
                model[1, 2 * i + 1] += 1
    
    return model, positive_label, negative_label

def testmodel(model, p_label, n_label, testset):
    classcol = len(testset[0]) - 1
    theta = 0
    error_count = 0
    for line in testset:
        theta_0 = math.log(float(n_label) / (p_label + n_label))
        theta_1 = math.log(float(p_label) / (p_label + n_label))
        for i in range(classcol):	# With Laplace smoothing
            theta_0 = theta_0 + math.log(float((model[0, 2 * i + int(line[i])] + 1)) / (model[0, 2 * i] + model[0, 2 * i + 1] + 2))
            theta_1 = theta_1 + math.log(float((model[1, 2 * i + int(line[i])] + 1)) / (model[1, 2 * i] + model[1, 2 * i + 1] + 2))
        if theta_0 >= theta_1:
            theta = 0
        else:
            theta = 1
        if theta != line[classcol]:
            error_count += 1
    
    return float(error_count) / len(testset)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        dataset = readfile(sys.argv[1])
        try:
            col = int(sys.argv[2])
        except ValueError:
            print("ERROR: argument 3 should be integer.")
            sys.exit(0)
        col = checkcolumn(col)
        new_dataset, key_term = preprocess(dataset, col, 0, [])
        zero_one_loss_10 = []
        zero_one_loss_50 = []
        zero_one_loss_90 = []
        print("10%:")
        for i in range(10):
            trainset, testset = dividedata(new_dataset, 500)
            positive_label = 0
            for i in range(len(trainset)):
                if trainset[i][2000] == 1:
                    positive_label += 1
            negative_label = len(trainset) - positive_label
            error_count = 0
            if positive_label >= negative_label:
                for line in testset:
                    if line[2000] != 1:
                        error_count += 1
            else:
                for line in testset:
                    if line[2000] != 0:
                        error_count += 1
            zero_one_loss = float(error_count) / len(testset)
            print("The 0-1 loss on test set is:", zero_one_loss)
            zero_one_loss_10.append(copy.deepcopy(zero_one_loss))
        print("50%:")
        for i in range(10):
            trainset, testset = dividedata(new_dataset, 2500)
            positive_label = 0
            for i in range(len(trainset)):
                if trainset[i][2000] == 1:
                    positive_label += 1
            negative_label = len(trainset) - positive_label
            error_count = 0
            if positive_label >= negative_label:
                for line in testset:
                    if line[2000] != 1:
                        error_count += 1
            else:
                for line in testset:
                    if line[2000] != 0:
                        error_count += 1
            zero_one_loss = float(error_count) / len(testset)
            print("The 0-1 loss on test set is:", zero_one_loss)
            zero_one_loss_50.append(copy.deepcopy(zero_one_loss))
        print("90%:")
        for i in range(10):
            trainset, testset = dividedata(new_dataset, 4500)
            positive_label = 0
            for i in range(len(trainset)):
                if trainset[i][2000] == 1:
                    positive_label += 1
            negative_label = len(trainset) - positive_label
            error_count = 0
            if positive_label >= negative_label:
                for line in testset:
                    if line[2000] != 1:
                        error_count += 1
            else:
                for line in testset:
                    if line[2000] != 0:
                        error_count += 1
            zero_one_loss = float(error_count) / len(testset)
            print("The 0-1 loss on test set is:", zero_one_loss)
            zero_one_loss_90.append(copy.deepcopy(zero_one_loss))
        print("10% training, 90% testing:")
        print("Mean:", statistics.mean(zero_one_loss_10), "Stdev:", statistics.stdev(zero_one_loss_10))
        print("50% training, 50% testing:")
        print("Mean:", statistics.mean(zero_one_loss_50), "Stdev:", statistics.stdev(zero_one_loss_50))
        print("90% training, 10% testing:")
        print("Mean:", statistics.mean(zero_one_loss_90), "Stdev:", statistics.stdev(zero_one_loss_90))
        
    elif len(sys.argv) == 4:
        dataset = readfile(sys.argv[1])
        try:
            col = int(sys.argv[2])
            printTop = int(sys.argv[3])
        except ValueError:
            print("ERROR: argument 3 & 4 should be integer.")
            sys.exit(0)
        col = checkcolumn(col)
        new_dataset, key_term = preprocess(dataset, col, printTop, [])
        zero_one_loss_10 = []
        zero_one_loss_50 = []
        zero_one_loss_90 = []
        print("10%:")
        for i in range(10):
            trainset, testset = dividedata(new_dataset, 500)
            model, positive_label, negative_label = nbclassifier(trainset)
            zero_one_loss = testmodel(model, positive_label, negative_label, testset)
            zero_one_loss_10.append(copy.deepcopy(zero_one_loss))
            print("The 0-1 loss on test set is:", zero_one_loss)        
        print("50%:")
        for i in range(10):
            trainset, testset = dividedata(new_dataset, 2500)
            model, positive_label, negative_label = nbclassifier(trainset)
            zero_one_loss = testmodel(model, positive_label, negative_label, testset)
            zero_one_loss_50.append(copy.deepcopy(zero_one_loss))
            print("The 0-1 loss on test set is:", zero_one_loss)
        print("90%:")
        for i in range(10):
            trainset, testset = dividedata(new_dataset, 4500)
            model, positive_label, negative_label = nbclassifier(trainset)
            zero_one_loss = testmodel(model, positive_label, negative_label, testset)
            zero_one_loss_90.append(copy.deepcopy(zero_one_loss))
            print("The 0-1 loss on test set is:", zero_one_loss)
        print("10% training, 90% testing:")
        print("Mean:", statistics.mean(zero_one_loss_10), "Stdev:", statistics.stdev(zero_one_loss_10))
        print("50% training, 50% testing:")
        print("Mean:", statistics.mean(zero_one_loss_50), "Stdev:", statistics.stdev(zero_one_loss_50))
        print("90% training, 10% testing:")
        print("Mean:", statistics.mean(zero_one_loss_90), "Stdev:", statistics.stdev(zero_one_loss_90))
            
    elif len(sys.argv) == 5:
        trainset = readfile(sys.argv[1])
        testset = readfile(sys.argv[2])
        try:
            col = int(sys.argv[3])
            printTop = int(sys.argv[4])
        except ValueError:
            print("ERROR: argument 4 & 5 should be integer.")
            sys.exit(0)
        col = checkcolumn(col)
        new_trainset, key_term = preprocess(trainset, col, printTop, [])
        model, positive_label, negative_label = nbclassifier(new_trainset)
        new_testset, key_term = preprocess(testset, col, 0, key_term)
        zero_one_loss = testmodel(model, positive_label, negative_label, new_testset)
        print("The 0-1 loss on test set is:", zero_one_loss)
        
    else:
        print("ERROR: wrong arguments, check readme to see how to set arguments.")
        sys.exit(0)
		