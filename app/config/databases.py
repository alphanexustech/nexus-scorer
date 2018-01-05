from app import app
from flask_pymongo import PyMongo

app.config['AFFECTCORPUS_DBNAME'] = 'affect-corpus'
affect_corpus = PyMongo(app, config_prefix='AFFECTCORPUS')

app.config['AFFECTSYNOPSIS_DBNAME'] = 'affect-synopsis'
affect_synopsis = PyMongo(app, config_prefix='AFFECTSYNOPSIS')

'''
Emotion Sets
'''

'''
The first 83 included from the emotionml
'''
emotion_ml = ['acceptance', 'admiration', 'affection', 'amusement', 'anger', 'anticipation', 'anxiety', 'appreciation', 'arousal', 'arrogance', 'awe', 'blame', 'boredom', 'calmness', 'compassion', 'compromise', 'concern', 'confidence', 'confusion', 'contempt', 'contentment', 'curiosity', 'denial', 'depression', 'desire', 'despair', 'disappointment', 'disgust', 'dissonance', 'distress', 'dread', 'ecstasy', 'edginess', 'embarrassment', 'enjoyment', 'enthusiasm', 'envy', 'eroticism',
'excitement', 'exuberance', 'fear', 'grace', 'gratification', 'gratitude', 'grief', 'happiness', 'harmony', 'hate', 'hope', 'humility', 'indifference', 'interest', 'irritation', 'jealousy', 'joy', 'love', 'lunacy', 'lust', 'mania', 'melancholy', 'pain', 'panic', 'patience', 'perturbation', 'pity', 'pleasure', 'pride', 'rage', 'relief', 'remorse', 'reproach', 'resentment', 'resignation', 'sadness', 'satisfaction', 'shame', 'shock', 'stress', 'surprise', 'triumph', 'trust', 'wonder', 'worry']

'''
uses the entire synopsis of emotions in the corpora
'''
all_emotions = ['abandonment', 'abhorrence', 'abomination', 'absorption', 'abstinence', 'acceptance', 'admiration', 'adoration', 'affection', 'affectionateness', 'affliction', 'aggravation', 'aggressiveness', 'agony', 'alarm', 'alienation', 'aliveness', 'aloofness', 'alteration', 'amazement', 'ambiance', 'amusement', 'anger', 'angst', 'anguish', 'animation', 'anticipation', 'antipathy', 'anxiety', 'apathy', 'appraisal', 'appreciation', 'arousal', 'arrogance', 'assimilation', 'astonishment', 'attraction', 'audaciousness', 'aversion', 'avoidance', 'awareness', 'awe', 'awfulness', 'awkwardness', 'badness', 'bashfulness', 'belief', 'bewilderment', 'bitterness', 'blame', 'blessedness', 'boldness', 'boredom', 'bravery', 'brightness', 'calmness', 'capableness', 'cautiousness', 'certainty', 'chastity', 'cheerfulness', 'cleverness', 'closeness', 'cloudiness', 'coercion', 'coldness', 'compassion', 'composure', 'compromise', 'compulsion', 'concern', 'confidence', 'conformity', 'confusion', 'consciousness', 'consideration', 'consonance', 'contempt', 'content', 'contentment', 'contrariness', 'courage', 'courageousness', 'covetousness', 'criticalness', 'crossness', 'curiosity', 'darkness', 'decency', 'defeat', 'defiance', 'delight', 'denial', 'depression', 'desire', 'desolation', 'despair', 'despicableness', 'determination', 'devastation', 'devotion', 'diffidence', 'diligence', 'dimension', 'disappointment', 'disbelief', 'disdain', 'disgrace', 'disgust', 'disillusionment', 'dislike', 'dismay', 'disorientation', 'disrespect', 'dissonance', 'distance', 'distress', 'distrust', 'disturbance', 'dominance', 'doubt', 'doubtfulness', 'dread', 'dullness', 'eagerness', 'earnestness', 'easiness', 'ecstasy', 'edginess', 'ego', 'elation', 'embarrassment', 'empathy', 'emptiness', 'encouragement', 'endurance', 'engagement', 'engrossment', 'enjoyment', 'enlightenment', 'enragement', 'enthusiasm', 'envy', 'eroticism', 'euphoria', 'exasperation', 'excitation', 'excitement', 'exhaustion', 'exploitation', 'exuberance', 'familiarity', 'fascination', 'fate', 'fatigue', 'fear', 'festivity', 'flatness', 'fondness', 'foolishness', 'forgiveness', 'fortune', 'freedom', 'fright', 'friskiness', 'frustration', 'fulfillment', 'furiousness', 'fury', 'gallantry', 'gayness', 'glee', 'gloominess', 'gluttony', 'goodness', 'grace', 'gratification', 'gratitude', 'greatness', 'greed', 'grief', 'guilt', 'happiness', 'hardiness', 'harmony', 'hate', 'helplessness', 'hesitance', 'hesitancy', 'honor', 'hope', 'hopefulness', 'horror', 'hostility', 'hotness', 'humbleness', 'humiliation', 'humility', 'hurt', 'ignorance', 'importance', 'impulse', 'impulsiveness', 'inadequacy', 'inadequateness', 'incapableness', 'indifference', 'inducement', 'indulgence', 'infatuation', 'infection', 'inferiority', 'inflammation', 'infuriation', 'innocence', 'inquisitiveness', 'insecurity', 'insignificance', 'inspiration', 'insult', 'intensity', 'intentness', 'interest', 'intimacy', 'intrigue', 'invulnerability', 'irritation', 'isolation', 'jealousy', 'joy', 'jubilance', 'keenness', 'kindness', 'liberality', 'liberation', 'lifelessness', 'liveliness', 'lividness', 'loathing', 'loneliness', 'loss', 'lousiness', 'love', 'luck', 'luckiness', 'lunacy', 'lust', 'mania', 'melancholy', 'merriness', 'misery', 'modesty', 'motivation', 'mournfulness', 'negation', 'negativeness', 'neglect', 'nervousness', 'neutrality', 'nonchalance', 'nostalgia', 'numbness', 'obsession', 'offensiveness', 'openness', 'optimism', 'outrage', 'pain', 'panic', 'paralysis', 'passion', 'passionateness', 'patience', 'peacefulness', 'permanence', 'perplexity', 'persuasion', 'perturbation', 'pessimism', 'petrification', 'pity', 'playfulness', 'pleasantness', 'pleasure', 'positiveness', 'potency', 'power', 'powerfulness', 'powerlessness', 'preoccupation', 'pride', 'provocation', 'quietness', 'quirkiness', 'rage', 'reassurance', 'rebellion', 'rebelliousness', 'reception', 'receptiveness', 'reenforcement', 'regret', 'reinforcement', 'rejection', 'relaxation', 'reliability', 'relief', 'reluctance', 'remorse', 'reproach', 'resentment', 'reservation', 'resignation', 'resistance', 'respect', 'restlessness', 'revulsion', 'ridicule', 'sadness', 'safety', 'saltiness', 'sarcasm', 'satisfaction', 'scorn', 'sensitivity', 'serenity', 'seriousness', 'shakiness', 'shame', 'shock', 'shyness', 'skepticism', 'sloth', 'snoopiness', 'sobriety', 'sourness', 'spirit', 'spiritedness', 'spite', 'stolidity', 'straightness', 'strength', 'stress', 'stubbornness', 'stupidity', 'submission', 'subversion', 'sulkiness', 'sulky', 'sullenness', 'sunniness', 'sureness', 'surprise', 'suspicion', 'sweetness', 'sympathy', 'tearfulness', 'tenaciousness', 'tenacity', 'tenderness', 'tenseness', 'terribleness', 'terror', 'thoughtfulness', 'threat', 'thrill', 'tolerance', 'tragedy', 'triumph', 'trust', 'uncertainty', 'understanding', 'uneasiness', 'unhappiness', 'unification', 'uniqueness', 'unity', 'unpleasantness', 'unpredictability', 'uselessness', 'valence', 'validation', 'vanity', 'veneration', 'vengefulness', 'victimization', 'vigor', 'vileness', 'vulnerability', 'warmness', 'weariness', 'withdrawal', 'withdrawnness', 'woe', 'woefulness', 'wonder', 'wonderfulness', 'worry', 'worthlessness', 'wrath']

'''
included from paul ekman, conforms to emotionml
'''
big_6 = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']

'''
everday categories included from the emotion_ml section
'''
everday_categories = ['affection', 'anxiety', 'amusement', 'anger', 'boredom', 'confidence', 'satisfaction', 'disappointment', 'excitement', 'joy', 'curiosity', 'love', 'pride', 'calmness', 'sadness', 'harmony', 'worry']

'''
OCC (Ortony, Clore and Collins) categories included from the emotion_ml section
'''
occ_categories = ['admiration', 'anger', 'disappointment', 'distress', 'fear', 'dread' , 'triumph', 'gratification', 'gratitude', 'appreciation', 'hate' , 'hope', 'joy', 'love', 'pity' , 'pride', 'relief', 'remorse', 'reproach', 'resentment', 'satisfaction', 'embarrassment']

'''
FSRE (ontaine, Scherer, Roesch and Ellsworth) categories included from emotion_ml section
'''
fsre_categories = ['anger', 'anxiety', 'pain', 'compassion', 'contempt', 'contentment', 'despair', 'disappointment', 'disgust', 'fear', 'guilt', 'happiness', 'hate', 'interest', 'irritation', 'jealousy', 'joy', 'love', 'pleasure', 'pride', 'sadness', 'shame', 'stress', 'surprise']

'''
Nico Frijda's proposal of action tendencies included from the emotion_ml section
'''
frijda_categories = ['anger', 'arrogance', 'desire', 'disgust', 'enjoyment', 'fear', 'humility', 'indifference', 'interest', 'resignation', 'shock', 'surprise']

'''
Dimensions included from the emotion_ml section
'''
dimensions = ['pleasure', 'arousal', 'dominance', 'valence', 'potency', 'unpredictability', 'intensity']

'''
Emotion Sets
'''

emotion_sets = {
    "emotion_ml": emotion_ml,
    "all_emotions": all_emotions,
    "big_6": big_6,
    "everday_categories": everday_categories,
    "occ_categories": occ_categories,
    "fsre_categories": fsre_categories,
    "frijda_categories": frijda_categories,
    "dimensions": dimensions,
}

def get_e_set(emotion_set):
    return emotion_sets[emotion_set]
