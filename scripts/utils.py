import json


def get_all_categories():
    all_data = {}
    with open('../data/combined_cleaned_data.json', encoding="utf8") as f:
        all_data = json.load(f)

    flavor = set()
    medical = set()
    aroma = set()
    negative = set()
    positive = set()

    for datum in all_data:
        flavor = flavor.union(set(datum['flavor_descriptors']))
        medical = medical.union(set(datum['medical']))
        aroma = aroma.union(set(datum['aroma']))
        negative = negative.union(set(datum['negative_effects']))
        positive = positive.union(set(datum['positive']))


    output = {
        'flavor': list(flavor),
        'aroma': list(aroma),
        'medical': list(medical),
        'negative': list(negative),
        'positive': list(positive)
    }

    with open('../data/categories.json', 'w') as outfile:
        json.dump(output, outfile)

def reverse_categories():
    categories = {}
    with open('../data/categories.json', encoding="utf8") as f:
        categories = json.load(f)

    inverse_dict = {}
    for category in categories:
        category_lst = categories[category]
        for term in category_lst:
            if term in inverse_dict:
                inverse_dict[term].append(category)
            else:
                inverse_dict[term] = [category]

    with open('../data/inverse_categories.json', 'w') as outfile:
        json.dump(inverse_dict, outfile)

def generate_strainname_to_vector_dict():
    all_data = {}
    with open('../data/combined_cleaned_data.json', encoding="utf8") as f:
        all_data = json.load(f)

    vector_dict = {}
    for datum in all_data:
        if datum['name'] == 'Cherry Skunk':
            print(datum['vector'])
        vector_dict[datum['name']] = datum


    with open('../data/strain_to_vector.json', 'w') as outfile:
        json.dump(vector_dict, outfile)


def keys_to_category_and_index():
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

def lda_keywords():
    lda = {}
    with open('../data/lda.json', encoding="utf8") as f:
        lda = json.load(f)

    output = []
    for key in lda:
        output = output + list(lda[key].keys())

    with open('../data/lda_keys.json', 'w') as f:
        json.dump(output, f)

if __name__ == "__main__":
    # get_all_categories()
    # reverse_categories()
    generate_strainname_to_vector_dict()
    # keys_to_category_and_index()
    # lda_keywords()
