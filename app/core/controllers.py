from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from flask import jsonify
import requests, operator, math

from bson.json_util import loads, dumps

from config import databases

affect_corpus = databases.affect_corpus
affect_synopsis = databases.affect_synopsis

'''
Statistic Functions
'''

def display_affect_word_similarities(include_word=None, truncated=None, upper_bound=None, lower_bound=None):

    cursor = affect_synopsis.db['affect-word-frequency'].find({})

    final_stats = []
    stats = []
    if include_word == "3":
        for doc in cursor:
            stats.append({
                'emotion-count': doc['emotion-count'],
                'word': doc['word'],
            })
    elif include_word == "2":
        for doc in cursor:
            stats.append(doc['word'])
    elif include_word == "1":
        for doc in cursor:
            stats.append({
                'emotion-count': doc['emotion-count'],
                'word': doc['word'],
            })
    elif include_word == "0":
        for doc in cursor:
            stats.append(doc['emotion-count'])


    if include_word != "2":
        sorted_stats = sorted(stats, key=lambda x: x['emotion-count'], reverse=True)
    else:
        sorted_stats = sorted(stats, key=lambda x: x['emotion-count'])

    j = 0
    trunc_stats = []
    if truncated == "1":
        for stat in sorted_stats:
            if (j % 160 == 0):
                trunc_stats.append(stat)
            j =+ j + 1

    if truncated == "1":
        final_stats = trunc_stats
    elif truncated == "0":
        final_stats = sorted_stats
    else:
        final_stats = sorted_stats

    # There is a little overlap between ranges due to to rounding...
    if upper_bound != None and lower_bound != None:
        upper_bound_percent_to_number = int(math.ceil(len(final_stats) * int(upper_bound) / 100))
        lower_bound_percent_to_number = int(math.ceil(len(final_stats) * int(lower_bound) / 100))
        final_stats = final_stats[(upper_bound_percent_to_number):(len(final_stats)-lower_bound_percent_to_number)]
    elif upper_bound != None:
        upper_bound_percent_to_number = int(math.ceil(len(final_stats) * int(upper_bound) / 100))
        final_stats = final_stats[0:(upper_bound_percent_to_number)]
    elif lower_bound != None:
        lower_bound_percent_to_number = int(math.ceil(len(final_stats) * int(lower_bound) / 100))
        final_stats = final_stats[(len(final_stats)-lower_bound_percent_to_number):len(final_stats)]


    affect_word_list = []
    if include_word == "3":
        for stat in final_stats:
            affect_word_list.append(stat['word'])

        final_stats = affect_word_list

    return final_stats

'''
Metrics Functions
'''

# IDEA Incorporate overlapping orders in some way
def calculate_r_score(is_in_order_1, is_in_order_2, is_in_order_3):
    ## Score of the affect, based on weights in the order
    r_affect_score = (
        ((is_in_order_1 * 0.7) + (is_in_order_2 * 0.2) + (is_in_order_3 * 0.1))/3
    )
    return r_affect_score

# IDEA Incorporate overlapping orders in some way
def calculate_normalized_r_score(normalized_order_1, normalized_order_2, normalized_order_3):
    ## Score of the affect, based on weights in the order
    normalized_r_score = (
        ((normalized_order_1 * 0.7) + (normalized_order_2 * 0.2) + (normalized_order_3 * 0.1))/3
    )
    return normalized_r_score

def calculate_r_density_score(r_affect_score, length_words_no_stop):
    ## But this one is based on density
    r_affect_density_score = r_affect_score/length_words_no_stop * 100
    return r_affect_density_score

'''
Primary Functions
'''

'''
Find the 'stop words' that are very common in each affect corpus
'''
def find_emotion_stop_words(upper_bound=None, lower_bound=None):

    result = []
    ub = display_affect_word_similarities(include_word="3", upper_bound=upper_bound)
    lb = display_affect_word_similarities(include_word="3", lower_bound=lower_bound)
    result = ub + lb

    return list(set(result))

'''
Business logic below

1. Take an emotion
2. Do something with it ---- this the 'process_emotion' method
3. Return results
4. Repeat for all emotions in a set ---- this is the 'process_emotion_set' method
'''

'''
doc > <string>
lang > <string>
emotion > <string>
flags <dict>:
    {
        naturalFlag > <string> (number)
        stemmerFlag > <string> (number)
        lemmaFlag > <string> (number)
    }
emotion_stop_words > (list of <strings>)
word_lists_no_emotion_stop <dict>:
    {
        list_of_words > (list of <strings>)
        stemmed_list > (list of <strings>)
        lemmatized_list > (list of <strings>)
    }
order > <string>
==
Finds the metadata for an order, used and combined with other similar objects to
find metadata for and emotion, see: process emotion
RETURNS:
{
        "order_length": <number>,
        "natural_list_of_order": <list>,
        "stemmer_list_of_order": <list>,
        "lemma_list_of_order": <list>,
        "is_in_order": <number>, # Count of the number of times a word is in the order
        "order_fdist": <list of [<list>,<number>]>,
        "natural_order_fdist": <list of [<list>,<number>]>,
        "stemmer_order_fdist": <list of [<list>,<number>]>,
        "lemma_order_fdist": <list of [<list>,<number>]>,
        "normalized_order": <number>, # A score
}
'''
def process_order(doc, lang, emotion, flags, emotion_stop_words, word_lists_no_emotion_stop, order):

    processed_order = {
        "status": "success",
        "order": order,
    }

    # Select the corpora, get the length of the corpora
    order_corpora = None
    order_corpora_length = 0
    if order == 'order-1' or order == 'order-2' or order == 'order-3' :
        order_corpora = affect_synopsis.db['lingustic-affects'].find_one({'word': emotion})[order]
    else:
        order_corpora = affect_synopsis.db['lingustic-affects-order-similarities'].find_one({'word': emotion})[order]

    order_corpora_length = len(order_corpora)

    # More of the metadata for the order
    natural_list_of_order = list()
    stemmer_list_of_order = list()
    lemma_list_of_order = list()
    is_in_order = 0

    if flags['naturalFlag'] == '1':
        for word in word_lists_no_emotion_stop['list_of_words']:
            if word in order_corpora:
                is_in_order+=1
                natural_list_of_order.append(word)
    if flags['stemmerFlag'] == '1':
        for stem_word in word_lists_no_emotion_stop['stemmed_list']:
            if stem_word in order_corpora:
                is_in_order+=1
                stemmer_list_of_order.append(stem_word)
    if flags['lemmaFlag'] == '1':
        for lemma_word in word_lists_no_emotion_stop['lemmatized_list']:
            if lemma_word in order_corpora:
                is_in_order+=1
                lemma_list_of_order.append(lemma_word)


    # Calculate Frequency Dist
    pre_natural_order_fdist = dict(FreqDist(pos_tag(natural_list_of_order)))
    pre_stemmer_order_fdist = dict(FreqDist(pos_tag(stemmer_list_of_order)))
    pre_lemma_order_fdist = dict(FreqDist(pos_tag(lemma_list_of_order)))
    natural_order_fdist = sorted(pre_natural_order_fdist.items(), key=lambda x: (x[1],x[0]))
    stemmer_order_fdist = sorted(pre_stemmer_order_fdist.items(), key=lambda x: (x[1],x[0]))
    lemma_order_fdist = sorted(pre_lemma_order_fdist.items(), key=lambda x: (x[1],x[0]))

    # Calculate Normalized Order
    normalized_order = 0
    try:
        normalized_order = float(is_in_order)/order_corpora_length * 100
    except Exception as e:
        pass

    processed_order['order_length'] = order_corpora_length
    processed_order['natural_list_of_order'] = natural_list_of_order
    processed_order['stemmer_list_of_order'] = stemmer_list_of_order
    processed_order['lemma_list_of_order'] = lemma_list_of_order
    processed_order['is_in_order'] = is_in_order
    processed_order['natural_order_fdist'] = natural_order_fdist
    processed_order['stemmer_order_fdist'] = stemmer_order_fdist
    processed_order['lemma_order_fdist'] = lemma_order_fdist
    processed_order['normalized_order'] = normalized_order

    return processed_order

def process_emotion(doc, lang, emotion, natural, stemmer, lemma, emotion_stop_words):

    flags = {}
    flags['naturalFlag'] = natural
    flags['stemmerFlag'] = stemmer
    flags['lemmaFlag'] = lemma

    valid_orders = ['order-1', 'order-2', 'order-3', 'order_1_and_2', 'order_1_and_3', 'order_2_and_3', 'all_orders']

    processed_doc_metadata = {
        "status": "success",
        "emotion": emotion,
    }

    # Stop Words
    stop_words = stopwords.words(lang)

    '''
    Remove emotion stop words and then return the words lists
    '''
    # IDEA: There is a more efficient way to do this
    pre_list_of_words = [i.lower() for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]
    pre_stemmed_list = []
    pre_lemmatized_list = []

    # IDEA: Handle language that isn't supported by stemmer!
    stemmer = SnowballStemmer(lang) # This is the stemmer
    lemma = WordNetLemmatizer() # This is the lemma
    for word in pre_list_of_words:
        pre_stemmed_list.append(lemma.lemmatize(word))
        pre_lemmatized_list.append(stemmer.stem(word))

    # Create a dictionary of the three lists without emotion based stop words
    word_lists_no_emotion_stop = {
        'list_of_words': [i for i in pre_list_of_words if i not in emotion_stop_words],
        'stemmed_list': [],
        'lemmatized_list': [],
    }
    # Remove emotion_stop_words only for these if the flag is set to true
    if flags['stemmerFlag'] == '1':
        word_lists_no_emotion_stop['stemmed_list'] = [i for i in pre_stemmed_list if i not in emotion_stop_words]
    if flags['lemmaFlag'] == '1':
        word_lists_no_emotion_stop['lemmatized_list'] = [i for i in pre_lemmatized_list if i not in emotion_stop_words]

    for order in valid_orders:
        order_result = process_order(doc, lang, emotion, flags, emotion_stop_words, word_lists_no_emotion_stop, order)
        if order_result['status'] == 'success':
            processed_doc_metadata[order] = order_result

    # IDEA: This needs to be moved
    list_of_words_no_stop = [i for i in wordpunct_tokenize(doc) if i.lower()]
    length_words_no_stop = len(list_of_words_no_stop)

    # Find some scores for each order
    is_in_order_1 = processed_doc_metadata['order-1']['is_in_order']
    is_in_order_2 = processed_doc_metadata['order-2']['is_in_order']
    is_in_order_3 = processed_doc_metadata['order-3']['is_in_order']
    normalized_order_1 = processed_doc_metadata['order-1']['normalized_order']
    normalized_order_2 = processed_doc_metadata['order-2']['normalized_order']
    normalized_order_3 = processed_doc_metadata['order-3']['normalized_order']

    r_affect_score = calculate_r_score(is_in_order_1, is_in_order_2, is_in_order_3)
    normalized_r_score = calculate_normalized_r_score(normalized_order_1, normalized_order_2, normalized_order_3)
    r_affect_density_score = calculate_r_density_score(r_affect_score, length_words_no_stop)

    processed_doc_metadata['r_affect_score'] = r_affect_score
    processed_doc_metadata['normalized_r_score'] = normalized_r_score
    processed_doc_metadata['r_affect_density_score'] = r_affect_density_score
    processed_doc_metadata['length_words_no_stop'] = length_words_no_stop

    return processed_doc_metadata

# IDEA: Error Handling needed!
def process_emotion_set(doc, lang, emotion_set, natural, stemmer, lemma, emotion_stop_words):

    processed_doc_list_metadata = []
    emotion_sets = ['emotion_ml', 'all_emotions', 'big_6',
    'everday_categories', 'occ_categories', 'fsre_categories', 'dimensions']

    e_set = None
    # pick emotion_set
    if emotion_set in emotion_sets:
        e_set = databases.get_e_set(emotion_set)
    else:
        e_set = []

    # IDEA: Better error handling here would be nice!
    for emotion in e_set:
        processed_doc_list_metadata.append(process_emotion(doc, lang, emotion, natural, stemmer, lemma, emotion_stop_words))

    return processed_doc_list_metadata
