import os
import numpy as np
from collections import Counter
from sklearn import svm
from sklearn.metrics import accuracy_score

import pickle as cPickle
import gzip

def load(file_name):
    # load the model
    stream = gzip.open(file_name, "rb")
    model = cPickle.load(stream)
    stream.close()
    return model


def save(file_name, model):
    # save the model
    stream = gzip.open(file_name, "wb")
    cPickle.dump(model, stream)
    stream.close()


def make_Dictionary(root_dir):
    all_words = []
    emails = [os.path.join(root_dir,f) for f in os.listdir(root_dir)]
    for mail in emails:
        with open(mail) as m:
            for line in m:
                words = line.split()
                all_words += words
    dictionary = Counter(all_words)
    list_to_remove = list(dictionary)

    for item in list_to_remove:
        if item.isalpha() == False:
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(3000)

    return dictionary



def extract_features(mail_dir):
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),3000))
    train_labels = np.zeros(len(files))
    count = 0;
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        train_labels[docID] = 0;
        filepathTokens = fil.split('/')
        lastToken = filepathTokens[len(filepathTokens) - 1]
        if lastToken.__contains__("spmsg"):
            train_labels[docID] = 1;
            count = count + 1
        docID = docID + 1
    return features_matrix, train_labels



TRAIN_DIR = 'E://CodingProjects//SPAMSVM//train-mails'
TEST_DIR = 'E://CodingProjects//SPAMSVM//Newspam'

dictionary = make_Dictionary(TRAIN_DIR)

print("reading and processing emails from file.")

# features_matrix, train_labels = extract_features(TRAIN_DIR)
test_feature_matrix, test_labels = extract_features(TEST_DIR)
print(test_feature_matrix, 'testing')
features_matrix = load("E://CodingProjects//SPAMSVM//code//temp//features_matrix.txt")
train_labels = load("E://CodingProjects//SPAMSVM//code//temp//train_labels.txt")
# test_feature_matrix = load("E://CodingProjects//SPAMSVM//code//temp//test_feature_matrix.txt")
# test_labels = load("E://CodingProjects//SPAMSVM//code//temp//test_labels.txt")

# features_matrix = features_matrix[:len(features_matrix)//10]
# train_labels = train_labels[:len(train_labels)//10]

save("E://CodingProjects//SPAMSVM//code//temp//features_matrix.txt", features_matrix)
save("E://CodingProjects//SPAMSVM//code//temp//train_labels.txt", train_labels)
save("E://CodingProjects//SPAMSVM//code//temp//test_feature_matrix.txt", test_feature_matrix)
save("E://CodingProjects//SPAMSVM//code//temp//test_labels.txt", test_labels)

model = svm.SVC(kernel="rbf", C = 1)
print("Training model.")
#train model
model.fit(features_matrix, train_labels)

predicted_labels = model.predict(test_feature_matrix)

for i in range(len(predicted_labels)):
    if predicted_labels[i] == 1:
        print([i], 'yes it is spam')
    elif predicted_labels[i] == 0:
        print([i], "Not Spam")
    else: print([i], 'Unable to detect')

# print("FINISHED classifying. accuracy score : ")
# print(accuracy_score(test_labels, predicted_labels))
