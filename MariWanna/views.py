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
    results = []
    return HttpResponse(json.dumps(results))


def get_request_data(request):
    l = (dict(request.POST)).keys()
    k = {}
    for i in l:
        k = i
    return json.loads(k)


def get_strain(data, keys_vector):
    '''
        determine what search terms are valid and
        set up the strain object
    '''
    medical_lst = data.get("medicalEffects")
    if medical_lst == None:
        medical_lst = []
    desired_lst = data.get("desiredEffects")

    if desired_lst == None:
        desired_lst = []
    undesired_lst = data.get("undesiredEffects")
    if undesired_lst == None:
        desired_lst = []
    flavors_lst = data.get("flavors")
    if flavors_lst == None:
        flavors_lst = []
    aromas_lst = data.get("aromas")
    if aromas_lst == None:
        aromas_lst = []
    keyword_lst = data.get("keyword")
    if keyword_lst == None:
        keyword_lst = []

    # state = data.get('state')
    # city = data.get('city')
    # strength = data.get('strength')

    #determine avlid keys
    valid_key_lst = []
    for keyword in keyword_lst:
        if keyword in keys_vector:
            valid_key_lst.append(keyword.lower().strip())

    return {
        'positive': desired_lst,
        'negative_effects': undesired_lst,
        'medical': medical_lst,
        'aroma': aromas_lst,
        'flavor_descriptors': flavors_lst,
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


@csrf_exempt
def custom_results(request):
    RATING_WEIGHT = 1/4
    DOM_TOPIC_WEIGHT = 1/8
    REMAINING_WEIGHT = 1 - RATING_WEIGHT - DOM_TOPIC_WEIGHT

    data = {}
    with open('./data/combined_cleaned_data.json', encoding="utf8") as f:
        data = json.loads(f.read())
    keys_vector = []
    with open('./data/keys_vector.json') as f:
        keys_vector = json.load(f)

    # set up request data
    q = get_request_data(request)

    # get strain and determine valid search
    strain = get_strain(q, keys_vector)
    search_strain_vector = strain_to_vector(strain, keys_vector)

    #finding the relevant dimensions to run cosine sim on
    search_strain, relv_search = get_rel_search(search_strain_vector)

    #get dominant topic
    dom_topic = get_dom_topic(strain)

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
            DOM_TOPIC_WEIGHT * (1 if curr_strain['dominant_topic'] == int(dom_topic) else 0) + \
            REMAINING_WEIGHT * cos_sim
        scoring.append((score, curr_strain))

    sorted_strains = sorted(scoring, key=lambda tup: tup[0], reverse=True)
    top_ten = sorted_strains[:9]
    data = top_ten
    return HttpResponse(json.dumps(data))


def strain_to_vector(input, keys_vector):
    vector_list_1 = input['positive'] + input['negative_effects'] + \
        input['medical'] + input['aroma'] + input['flavor_descriptors']
    vector_list = [x.lower() for x in vector_list_1]

    cond_vector = [1 if key in vector_list else 0 for key in keys_vector]
    cond_vector.append(1) #always include rating
    return array(cond_vector)
