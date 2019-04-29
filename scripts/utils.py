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


if __name__ == "__main__":
    # get_all_categories()
    reverse_categories()
