from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
from numpy import array, dot
from numpy.linalg import norm
from random import shuffle
from django.conf import settings
import pybase64


import sys
sys.path.append('../../scripts')
import scripts.database_connection as db
from .forms import SearchForm

positive_effects_key = 'positive'
negative_effects_key = 'negative_effects'
medical_effects_key = 'medical'
aromas_key = 'aroma'
flavors_key = 'flavor_descriptors'
keywords_key = 'keywords'
MAX_THC = 34.0
MIN_THC = 1.0
MEAN_THC = 19.092282784673504

@csrf_exempt
def login(request):
    return render_url(request, 'login.html')

@csrf_exempt
def failed_authentication(request):
    return render_url(request, 'failed_authentication.html')

@csrf_exempt
def create_account(request):
    return render_url(request, 'create_account.html')

@csrf_exempt
def logout(request):
    try:
        del request.session['user_id']
        del request.session['email']
    except:
        pass
    response = redirect('/login')
    return response

@csrf_exempt
def home(request):
    return render_url(request, 'home.html')

@csrf_exempt
def similar_search(request):
    return render_url(request, 'search_similar.html')

@csrf_exempt
def custom_search(request):
    return render_url(request, 'search_custom.html')

def render_url(request, url):
    if is_session_set(request):
        context = convert_request_to_context(request)
        return render_to_response(url, context=context)
    else:
        return render_to_response(url)

def is_session_set(request):
    return request.session.has_key('user_id')

def convert_request_to_context(request):
    user_id = request.session['user_id']
    liked_strains = find_liked_strains(user_id)
    disliked_strains = find_disliked_strains(user_id)
    context = {'user_id': user_id,
        'email': request.session['email'],
        'liked_strains': liked_strains,
        'disliked_strains': disliked_strains}
    return context

def find_liked_strains(user_id):
    return get_strains_of_preference(user_id, 1)

def find_disliked_strains(user_id):
    return get_strains_of_preference(user_id, -1)

def get_strains_of_preference(user_id, is_liked):
    strains_of_preference_query = create_strain_preference_query(user_id, is_liked)
    raw_strain_results = db.execute_select_statement(strains_of_preference_query)
    if raw_strain_results != []:
        strain_results = [result[0] for result in raw_strain_results]
        return strain_results
    else:
        return []

def create_strain_preference_query(user_id, is_liked):
    query = "SELECT DISTINCT(strain_name) FROM user_feedback INNER JOIN strains \
        ON strains.id = user_feedback.strain_id \
        WHERE user_id={user_id} AND \
            user_feedback.user_feedback = {is_liked}".format(user_id=user_id, is_liked=is_liked)
    return query

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
def perform_signin(request):
    signin_info = convert_to_dictionary(request)
    user_data = find_user_data(signin_info)
    is_user_in_db = is_user_existent(user_data)
    if is_user_in_db:
        create_session(user_data, request)
    return HttpResponse(json.dumps(is_user_in_db))

def convert_to_dictionary(request):
    request_keys = request.POST.keys()
    request_as_json = list(request_keys)[0]
    return (json.loads(request_as_json))

def find_user_data(signin_info):
    email = signin_info['email']
    hashed_password = hash_password(signin_info['password'])
    query_to_find_user = create_query_to_find_user(email, hashed_password)
    return db.execute_select_statement(query_to_find_user)

def create_query_to_find_user(email, hashed_password):
    query = "SELECT * FROM users WHERE email = '{email}' \
            AND password='{hashed_password}' LIMIT 1".format(email=email, hashed_password=hashed_password)
    return query

def create_session(user_data, request):
    user_record = user_data[0]
    request.session['user_id'] = user_record[0]
    request.session['email'] = user_record[1]

def is_user_existent(user_data):
    return len(user_data) > 0

def unhash_password(hashed_password):
    hashed_password_as_bytes = hashed_password.encode('utf-8')
    unhashed_password_as_bytes = pybase64.b64decode(hashed_password_as_bytes, altchars='_:', validate=True)
    unhashed_password = unhashed_password_as_bytes.decode('utf-8')
    return unhashed_password

@csrf_exempt
def enter_user(request):
    signin_info = convert_to_dictionary(request)
    insert_user_to_db(signin_info)
    return render_to_response('home.html')

def insert_user_to_db(signin_info):
    email = signin_info['email']
    hashed_password = hash_password(signin_info['password'])
    insert_new_user_query = create_query_for_new_user(email, hashed_password)
    db.execute_insert_statement(insert_new_user_query)
    return render_to_response('home.html')

def hash_password(password):
    password_as_bytes = password.encode('utf-8')
    hashed_password = (pybase64.b64encode(password_as_bytes, altchars='_:'))
    hashed_password_as_string = hashed_password.decode('utf-8')
    return hashed_password_as_string

def create_query_for_new_user(email, hashed_password):
    return ("INSERT INTO users (email, password) \
        VALUES ('{email}', '{password}')".format(email=email, password=hashed_password))

def search_vector_to_obj(strain_vector):
    keys_vector = []
    with open('./data/keys_vector.json', encoding="utf8") as f:
        keys_vector = json.loads(f.read())

    inverse_categories_dict = {}
    with open('./data/inverse_categories.json', encoding="utf8") as f:
        inverse_categories_dict = json.loads(f.read())


    total_dict = {}
    total_dict['positive'] = []
    total_dict['negative'] = []
    total_dict['medical'] = []
    total_dict['aroma'] = []
    total_dict['flavor'] = []
    total_dict['keywords'] = []
    total_dict['strength'] = []
    for index in range(len(strain_vector)):
        if strain_vector[index] == 1:
            curr_val = keys_vector[index]
            category_lst = inverse_categories_dict[curr_val]
            for cat in category_lst:
                total_dict[cat] = (total_dict[cat]) + [curr_val]


    total_dict['flavor_descriptors'] = total_dict['flavor']
    total_dict['negative_effects'] = total_dict['negative']
    del total_dict['flavor']
    del total_dict['negative']
    return total_dict

@csrf_exempt
def similar_results(request):
    keys_vector = {}
    with open('./data/keys_vector.json', encoding="utf8") as f:
        keys_vector = json.loads(f.read())

    current_strain_request = (get_request_data(request))
    current_strain_name = current_strain_request['strain']

    # get strain from db
    search_strain_vector = get_strain_obj(current_strain_name)

    #getting the correct strain data
    if search_strain_vector == None:
        return HttpResponse(json.dumps([]))


    search_obj = search_vector_to_obj(search_strain_vector)


    search_strain, relv_search = get_rel_search(search_strain_vector)

    search_strain_names = find_relevant_strains(search_obj)

    search_vectors = names_to_vectors(search_strain_names)

    strain_ranks = rank_strains(search_vectors, search_strain, relv_search, None, None, keys_vector, request)

    return HttpResponse(json.dumps(strain_ranks[1:]))


def get_request_data(request):
    l = (dict(request.POST)).keys()
    k = {}
    for i in l:
        k = i
    return json.loads(k)


def parse_search(data):
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

    lda_keys = {}
    with open('./data/lda_keys.json', encoding="utf8") as f:
        lda_keys = json.load(f)
    keyword_lst = data.get("keywords")
    if keyword_lst == None:
        keyword_lst = []
    valid_key_lst = []
    for keyword in keyword_lst:
        if keyword in lda_keys:
            valid_key_lst.append(keyword.lower().strip())

    strength = data.get('strength')
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
        'keywords': valid_key_lst,
        'strength': strength
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
    if max(dom_topic_weights) == 0:
        return None

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


def calculate_strength_diff(search_strength, curr_strain):
    curr_thc = 0
    if 'percentages' in curr_strain and 'THC' in curr_strain['percentages']:
            curr_thc = curr_strain['percentages']['THC']
    else:
        curr_thc = str(MEAN_THC)
    curr = curr_thc.split("%")
    curr_thc = (curr[0])
    scaled_search_strength = float(search_strength) / MAX_THC
    scaled_curr_strength = float(curr_thc) / MAX_THC
    divsor = scaled_search_strength
    if scaled_search_strength == 0:
        divsor = 1
    compare =  1 - ((abs(scaled_search_strength-scaled_curr_strength)/ divsor))

    return compare


def rank_strains(search_vectors, search_strain, relv_search, dom_topic, search_strength, keys_vector, request):
    scoring = []
    if is_session_set(request):
        user_id = request.session['user_id']
        liked_strains = find_liked_strains(user_id)
        disliked_strains = find_disliked_strains(user_id)
    else:
        liked_strains = []
        disliked_strains = []

    for i in range(len(search_vectors)):
        curr_strain = search_vectors[i]
        curr_vector = curr_strain['vector']
        score_categories_breakdown_lst = []
        curr_array = []
        for relv_item in relv_search:
            relv_index = relv_item[0]
            curr_value = curr_vector[relv_index]

            # for the score breakdown, what words are relevant
            if relv_index < len(keys_vector):
                score_categories_breakdown_lst.append(keys_vector[relv_index])
            curr_array.append(curr_value)

        #the four pieces of the score
        categories_weight = 1 - settings.RATING_WEIGHT
        total_weight = settings.RATING_WEIGHT

        #rating score always exists
        rating = float(curr_strain['rating'])/5
        rating_score = settings.RATING_WEIGHT * rating

        keywords_score = settings.DOM_TOPIC_WEIGHT * (1 if (dom_topic is not None and curr_strain['dominant_topic'] == int(dom_topic)) else 0)
        if keywords_score > 0:
            categories_weight -= settings.DOM_TOPIC_WEIGHT
            total_weight += settings.DOM_TOPIC_WEIGHT

        strength_score = 0
        if search_strength is not None:
            strength_score_diff = calculate_strength_diff(search_strength, curr_strain)
            strength_score = settings.STRENGTH_WEIGHT * strength_score_diff
            categories_weight -= settings.STRENGTH_WEIGHT
            total_weight += settings.STRENGTH_WEIGHT

        cos_sim = 0 if len(curr_array) < 1 else cosine_sim(array(search_strain), array(curr_array))

        if cos_sim > 0:
            categories_score = categories_weight * cos_sim
            total_weight = 1
        else:
            categories_score = 0

        score = 100*(rating_score + keywords_score + strength_score + categories_score) / total_weight

        liked = False
        disliked = False
        if curr_strain['name'] in liked_strains:
            liked = True
        if curr_strain['name'] in disliked_strains:
            disliked = True

        score_breakdown = calculate_score_breakdown(curr_strain['name'], score, \
            score_categories_breakdown_lst, 100*rating_score, \
            100*categories_score, 100*keywords_score, 100*strength_score, liked, disliked)

        scoring.append((score, curr_strain, score_breakdown))

    return sorted(scoring, key=lambda tup: tup[0], reverse=True)


def calculate_score_breakdown(name, score, \
    score_categories_breakdown_lst, rating_score, \
    categories_score, keywords_score, strength_score, liked, disliked):
    '''
        return score object
        {
            'rating': .3,
            'strength': .2,
            'keywords': .2,
            'flavors': {
                'cherry': .15,
                'sage': .15
            }

        }
    '''
    change = 0
    if liked:
        change = (1-score)**settings.LIKE_WEIGHT
    elif disliked:
        change = -1  * score**settings.LIKE_WEIGHT
    score = score + change

    score_breakdown = {}
    score_breakdown['rating'] = rating_score#/score
    score_breakdown['keywords'] = 0 if (keywords_score is None or keywords_score == 0) else keywords_score#/score
    score_breakdown['strength'] = 0 if strength_score == 0 else strength_score#/score
    score_breakdown['social'] = change#/score

    inverse_categories= {}
    with open('./data/inverse_categories.json', encoding="utf8") as f:
        inverse_categories = json.loads(f.read())


    per_word_score = 0 if len(score_categories_breakdown_lst)==0 else categories_score/len(score_categories_breakdown_lst)#/score


    for word in score_categories_breakdown_lst:
        categories = inverse_categories[word]
        for category in categories:
            if category not in score_breakdown:
                category_obj = {}
                category_obj[word] = per_word_score/len(categories)
                score_breakdown[category] = category_obj
            else:
                score_breakdown[category][word] = per_word_score/len(categories)

    return score_breakdown


@csrf_exempt
def custom_results(request):
    # data = {}
    # with open('./data/combined_cleaned_data.json', encoding="utf8") as f:
    #     data = json.loads(f.read())
    keys_vector = []
    with open('./data/keys_vector.json') as f:
        keys_vector = json.load(f)

    # set up request data
    user_request = get_request_data(request)

    # get strain and determine valid search
    search_obj = parse_search(user_request)

    #if no inputs or gibberish inputs in keywords only
    if search_obj is None:
        return HttpResponse(json.dumps([]))

    # turn object into vector so we can use cosine similarity
    search_strain_vector = search_to_vector(search_obj, keys_vector)

    # get list of strains from SQL database
    strain_names = find_relevant_strains(search_obj)

    #finding the relevant dimensions to run cosine sim on
    search_strain, relv_search = get_rel_search(search_strain_vector)

    #get dominant topic
    dom_topic = get_dom_topic(search_obj)
    search_vectors = names_to_vectors(strain_names)
    strength = search_obj['strength']
    strain_ranks = rank_strains(search_vectors, search_strain, relv_search, dom_topic, strength, keys_vector, request)

    return HttpResponse(json.dumps(strain_ranks))


def names_to_vectors(strain_names):
    vectors = {}
    with open('./data/strain_to_vector.json', encoding="utf8") as f:
        vectors = json.load(f)

    output = []
    for name in strain_names:
        try:
            vector = vectors[name]
            output.append(vector)
        except KeyError:
            continue
    return output




def search_to_vector(input, keys_vector):
    vector_list_1 = input['positive'] + input['negative_effects'] + \
        input['medical'] + input['aroma'] + input['flavor_descriptors']
    vector_list = [x.lower() for x in vector_list_1]
    cond_vector = [1 if key in vector_list else 0 for key in keys_vector]
    return array(cond_vector)

def get_strain_obj(name):
    name = name.replace('\'','\'\'')
    query_strain_name = "SELECT *\
        FROM strain_vectors \
        WHERE strain_name = '{strain}'".format(strain = name)
    raw_vector = db.execute_select_statement(query_strain_name)
    if raw_vector == []:
        return None
    else:
        real_vector = raw_vector[0][2:]
        return real_vector

def find_relevant_strains(search_keys):
    #create copy without keywords
    new_search_keys = {}
    for key in search_keys:
        if key != 'keywords':
            new_search_keys[key] = search_keys[key]
    query_for_strain_names = create_db_query_for_strain_names(search_keys)
    raw_strain_names_results = db.execute_select_statement(query_for_strain_names)
    strain_names = [record[0] for record in raw_strain_names_results]
    return strain_names


def create_db_query_for_strain_names(search_keys):
    keys_for_db, negative_keys_for_db = get_db_keys(search_keys)

    # if we have keys and no negative keys, all 3 cases
    if len(keys_for_db) > 0:
        if len(negative_keys_for_db) > 0:
            query_for_strain_names = "SELECT strain_name, 6 - {negative_sum_all_db_keys} + {sum_all_db_keys} as strain_score \
                FROM strain_vectors \
                WHERE {sum_all_db_keys} > 0 \
                OR {negative_sum_all_db_keys} = 0 \
                ORDER BY strain_score DESC \
                LIMIT 50".format(sum_all_db_keys = " + ".join(keys_for_db), negative_sum_all_db_keys = " - ".join(negative_keys_for_db))
        else:
            query_for_strain_names = "SELECT strain_name, {sum_all_db_keys} as strain_score \
                FROM strain_vectors \
                WHERE {sum_all_db_keys} > 0 \
                ORDER BY strain_score DESC \
                LIMIT 50".format(sum_all_db_keys = " + ".join(keys_for_db))
    else:
        if len(negative_keys_for_db) > 0:
            query_for_strain_names = "SELECT strain_name, 6 - {negative_sum_all_db_keys} as strain_score \
                FROM strain_vectors \
                WHERE {negative_sum_all_db_keys} = 0 \
                ORDER BY strain_score DESC \
                LIMIT 50".format(negative_sum_all_db_keys = " + ".join(negative_keys_for_db))
        else:
            query_for_strain_names = "SELECT strain_name, rating \
                FROM strains \
                ORDER BY rating DESC \
                LIMIT 50"
    return query_for_strain_names

def get_db_keys(search_keys):
    all_keys = concatenate_all_keys_from(search_keys)
    negative_keys = search_keys['negative_effects']

    keys_for_db = []
    for key in all_keys:
        formatted_key = format_key_to_db_key(key)
        keys_for_db.append(formatted_key)

    negative_keys_for_db = []
    for key in negative_keys:
        formatted_key = format_key_to_db_key(key)
        negative_keys_for_db.append(formatted_key)

    return keys_for_db, negative_keys_for_db

def concatenate_all_keys_from(search_keys):
    key_categories = [positive_effects_key, medical_effects_key, aromas_key, flavors_key]
    keys_concatenated = []
    for key_category in key_categories:
        keys_concatenated += search_keys[key_category]

    return keys_concatenated

def format_key_to_db_key(key):
    key = key.replace("'", "")
    key = key.replace("/", "_")
    return "is_" + key.replace(" ", "_")

@csrf_exempt
def provide_strain_feedback(request):
    user_feedback = convert_to_dictionary(request)
    if is_session_set(request):
        user_id = request.session['user_id']
        strain_name = user_feedback['strain']
        user_feedback_score = user_feedback['input']

        strain_id = get_strain_id_given(strain_name)
        insert_user_feedback_query = create_user_feedback_query(user_id, strain_id, user_feedback_score)
        db.execute_insert_statement(insert_user_feedback_query)

        delete_older_feedback_query = create_delete_older_feedback_query(user_id, strain_id, user_feedback_score)
        db.execute_insert_statement(delete_older_feedback_query)

    return render_url(request, 'search_custom.html')

def get_strain_id_given(strain_name):
    get_id_query = 'SELECT id FROM strain_vectors WHERE strain_name = \
        "{strain_name}"'.format(strain_name = strain_name)

    strain_id_results = db.execute_select_statement(get_id_query)
    strain_id = strain_id_results[0][0]
    return strain_id

def create_user_feedback_query(user_id, strain_id, user_feedback_score):
    insert_user_feedback_query = "INSERT INTO user_feedback (user_id, strain_id, user_feedback) VALUES ({user_id}, {strain_id}, {user_feedback_score})".format(user_id=user_id, strain_id=strain_id, user_feedback_score=user_feedback_score)
    return insert_user_feedback_query

def create_delete_older_feedback_query(user_id, strain_id, user_feedback_score):
    user_feedback_score = user_feedback_score * -1
    delete_older_feedback_query = "DELETE FROM user_feedback WHERE \
        user_id={user_id} AND strain_id={strain_id} \
            AND user_feedback={user_feedback_score}".format(user_id=user_id, strain_id=strain_id, user_feedback_score=user_feedback_score)
    return delete_older_feedback_query
