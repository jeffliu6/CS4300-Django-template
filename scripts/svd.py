from sklearn.feature_extraction.text import TfidfVectorizer
import json
# from scipy.sparse.linalg import svds
from constants import additional_stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import numpy as np


def find_dims():
    input_data = {}
    with open('../data/combined_cleaned_data.json') as f:
        input_data = json.load(f)

    # combine description and reviews
    documents = []
    for input in input_data:
        text = input['description']
        reviews = input['reviews']
        for review in reviews:
            text += review
        documents.append(text)

    #turn text into matrix
    stop_words = ENGLISH_STOP_WORDS.union(additional_stopwords)
    vectorizer = TfidfVectorizer(stop_words = stop_words, max_df = .90, min_df = 200)
    my_matrix = vectorizer.fit_transform(documents)

    keys_vector = []
    with open('../data/keys_vector.json') as f:
        keys_vector = json.load(f)

    cond_vectors = []
    for input in input_data:
        cond_vector = strain_to_vector(input, keys_vector)
        cond_vectors.append(cond_vector)
    final_matrix = np.array([np.array(xi) for xi in cond_vectors])
    average_matrix = list(np.mean(final_matrix, axis=0))

    # add vector to every strain
    i = 0
    for data in input_data:
        data['vector'] = list(final_matrix[i,:])
        i += 1

    with open('../data/combined_cleaned_data.json', 'w') as f:
        json.dump(input_data, f)

    with open('../data/averages.json', 'w') as f:
        json.dump(average_matrix, f)


def strain_to_vector(input, keys_vector):
    vector_list = input['positive'] + input['negative_effects'] + \
        input['medical'] + input['aroma'] + input['flavor_descriptors']
    cond_vector = []
    for key in keys_vector:
        if key in vector_list:
            cond_vector.append(1)
        else:
            cond_vector.append(0)
    cond_vector.append(float(input['rating'])/5)
    return cond_vector


def gather_keys():
    '''
        find all keys so we can use them to generate a vector of binaries
    '''
    input_data = {}
    with open('../data/combined_cleaned_data.json') as f:
        input_data = json.load(f)

    # combine description and reviews
    positive = set()
    negative = set()
    medical = set()
    aroma = set()
    flavor = set()
    #'positive', 'medical', 'aroma', 'flavor_descriptors',  'negative_effects'

    for input in input_data:
        for pos in input['positive']:
            positive.add(pos)
        for neg in input['negative_effects']:
            negative.add(neg)
        for med in input['medical']:
            medical.add(med)
        for aro in input['aroma']:
            aroma.add(aro)
        for flav in input['flavor_descriptors']:
            flavor.add(flav)

    union_set = list(positive.union(negative).union(medical).union(aroma).union(flavor))
    with open('../data/keys_vector.json', 'w') as f:
        json.dump(union_set, f)



if __name__ == "__main__":
    # gather_keys()
    find_dims()
