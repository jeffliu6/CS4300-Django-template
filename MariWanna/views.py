from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
from numpy import array, dot
from numpy.linalg import norm
from random import shuffle
from django.conf import settings


import sys
sys.path.append('../../scripts')
import scripts.database_connection as db
from .forms import SearchForm

@csrf_exempt
def home(request):
    return render_to_response('home.html')

@csrf_exempt
def similar_search(request):
    return render_to_response('search_similar.html')

@csrf_exempt
def custom_search(request):
    return render_to_response('search_custom.html')

def cosine_sim(a, b):
    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    if norma == 0:
        norma = 1
    if normb == 0:
        normb = 1
    cos = dot / (norma * normb)
    return cos

@csrf_exempt
def similar_results(request):
    RATING_WEIGHT = 1/4
    REMAINING_WEIGHT = 1 - RATING_WEIGHT

    current_strain_request = (get_request_data(request))
    current_strain_name = current_strain_request['strain']
    # Get Data (Change later?)
    data = {}
    with open('./data/combined_cleaned_data.json', encoding="utf8") as f:
        data = json.loads(f.read())

    #getting the correct strain data
    current_strain_data = []
    for strain in data:
        if current_strain_name in strain["name"] or current_strain_name in strain["name"]:
            current_strain_data = strain
            break
    if current_strain_data == []:
        return HttpResponse(json.dumps(current_strain_data))

    search_strain, relv_search = get_rel_search(current_strain_data['vector'])

    scoring = []
    for i in range(len(data)):
        curr_strain = data[i]
        curr_array = []
        for relv_item in relv_search:
            relv_index = relv_item[0]
            curr_value = (curr_strain['vector'])[relv_index]
            curr_array.append(curr_value)
        cos_sim = cosine_sim(array(search_strain), array(curr_array))
        rating = float(curr_strain['rating'])/5
        score = RATING_WEIGHT * (cos_sim*rating) + \
            REMAINING_WEIGHT * cos_sim
        scoring.append((score, curr_strain))

    sorted_strains = sorted(scoring, key=lambda tup: tup[0], reverse=True)
    top_ten = sorted_strains[1:10]
    data = top_ten

    keys = {}
    with open('./data/keys_vector.json', encoding="utf8") as f:
        keys = json.loads(f.read())

    for sim_tup in top_ten:
        sim_score = sim_tup[0]
        sim_strain = sim_tup[1]

        matched_values = []
        matched_vector =[]
        for index in range(len(sim_strain['vector'])):
            matched_vector.append((sim_strain['vector'])[index] + (current_strain_data['vector'])[index])

        matched_vector = matched_vector[:-1]




        for index in range(len(matched_vector)):
            if matched_vector[index] > 1:
                matched_factor = keys[index]
                matched_values.append(matched_factor)
        print(matched_values)







    return HttpResponse(json.dumps(data))


def get_request_data(request):
    l = (dict(request.POST)).keys()
    k = {}
    for i in l:
        k = i
    return json.loads(k)


def parse_search(data, keys_vector):
    '''
        determine what search terms are valid and
        set up the strain object
    '''
    categories = {}
    with open('./data/categories.json', encoding="utf8") as f:
        categories = json.load(f)

    draft_medical_lst = data.get("medicalEffects")
    medical_lst = []
    for term in draft_medical_lst:
        if term in categories['medical']:
            medical_lst.append(term)
    draft_positive_lst = data.get("desiredEffects")
    positive_lst = []
    for term in draft_positive_lst:
        if term in categories['positive']:
            positive_lst.append(term)
    draft_negative_lst = data.get("undesiredEffects")
    negative_lst = []
    for term in draft_negative_lst:
        if term in categories['negative']:
            negative_lst.append(term)
    draft_aroma_lst = data.get("aromas")
    aroma_lst = []
    for term in draft_aroma_lst:
        if term in categories['aroma']:
            aroma_lst.append(term)
    draft_flavor_lst = data.get("flavors")
    flavor_lst = []
    for term in draft_flavor_lst:
        if term in categories['flavor']:
            flavor_lst.append(term)

    keyword_lst = data.get("keyword")
    if keyword_lst == None:
        keyword_lst = []
    valid_key_lst = []
    for keyword in keyword_lst:
        if keyword in keys_vector:
            valid_key_lst.append(keyword.lower().strip())

    # state = data.get('state')
    # city = data.get('city')
    # strength = data.get('strength')

    #if input is just gibberish return None
    if len(positive_lst) + len(negative_lst) + len(medical_lst) + \
        len(aroma_lst) + len(flavor_lst) + len(valid_key_lst) == 0:
        return None

    return {
        'positive': positive_lst,
        'negative_effects': negative_lst,
        'medical': medical_lst,
        'aroma': aroma_lst,
        'flavor_descriptors': flavor_lst,
        'keywords': valid_key_lst
    }


def get_dom_topic(strain):
    dom_topics = []
    with open('./data/lda.json') as f:
        dom_topics = json.load(f)
    # find dominant topic
    dom_topic_weights = [0] * len(dom_topics)
    for keyword in strain['keywords']:
        for topic in dom_topics:
            current_topic_lst = dom_topics[topic]
            if keyword in current_topic_lst:
                dom_topic_weights[int(topic)] += current_topic_lst[keyword]
    # choose a maximum with random tiebreaker
    shuffle(dom_topic_weights)
    return max(range(len(dom_topic_weights)), key=lambda i: dom_topic_weights[i])


def get_rel_search(search_strain_vector):
    relv_search = []
    search_strain = []
    for index in range(len(search_strain_vector)):
        is_val = search_strain_vector[index]
        if is_val == 1:
            search_strain.append(1)
            relv_search.append((index, search_strain_vector[index]))
    return search_strain, relv_search


def rank_strains(data, search_strain, relv_search, dom_topic):
    scoring = []
    for i in range(len(data)):
        curr_strain = data[i]
        curr_array = []
        for relv_item in relv_search:
            relv_index = relv_item[0]
            curr_value = (curr_strain['vector'])[relv_index]
            curr_array.append(curr_value)
        cos_sim = cosine_sim(array(search_strain), array(curr_array))
        rating = float(curr_strain['rating'])/5
        score = settings.RATING_WEIGHT * (cos_sim*rating) + \
            settings.DOM_TOPIC_WEIGHT * (1 if curr_strain['dominant_topic'] == int(dom_topic) else 0) + \
            settings.REMAINING_WEIGHT * cos_sim
        scoring.append((score, curr_strain))

    sorted_strains = sorted(scoring, key=lambda tup: tup[0], reverse=True)

    #return top 10
    return sorted_strains[:9]



@csrf_exempt
def custom_results(request):
    data = {}
    with open('./data/combined_cleaned_data.json', encoding="utf8") as f:
        data = json.loads(f.read())
    keys_vector = []
    with open('./data/keys_vector.json') as f:
        keys_vector = json.load(f)

    # set up request data
    user_request = get_request_data(request)

    # get strain and determine valid search
    search_obj = parse_search(user_request, keys_vector)

    #if no inputs or gibberish inputs in keywords only
    if search_obj is None:
        return HttpResponse(json.dumps([]))

    # turn object into vector so we can use cosine similarity
    search_strain_vector = search_to_vector(search_obj, keys_vector)

    # get list of strains from SQL database
    # data = get_stuff_from_fred()

    #finding the relevant dimensions to run cosine sim on
    search_strain, relv_search = get_rel_search(search_strain_vector)

    #get dominant topic
    dom_topic = get_dom_topic(search_obj)

    output = rank_strains(data, search_strain, relv_search, dom_topic)

    return HttpResponse(json.dumps(output))


def search_to_vector(input, keys_vector):
    vector_list_1 = input['positive'] + input['negative_effects'] + \
        input['medical'] + input['aroma'] + input['flavor_descriptors']
    vector_list = [x.lower() for x in vector_list_1]

    cond_vector = [1 if key in vector_list else 0 for key in keys_vector]
    cond_vector.append(1) #always include rating
    return array(cond_vector)
