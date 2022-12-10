from django.shortcuts import render, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from googlesearch import search
from bs4 import BeautifulSoup
import nltk
import string
import random
import requests

data = ""


def find_data(query):
    global data
    for j in search(query, tld='co.in', num=10, stop=10, pause=3):
        res = requests.get(j)
        contents = res.text

        soup = BeautifulSoup(contents, "html.parser")

        paragraph = soup.find_all(name="p")
        # print(soup.p)

        for each in paragraph:
            # print(each.getText())
            data += each.getText()
        print(data)


def utility_func():
    raw_doc = data
    raw_doc = raw_doc.lower()
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    sentence_tokens = nltk.sent_tokenize(raw_doc)
    word_tokens = nltk.word_tokenize(raw_doc)
    return sentence_tokens, word_tokens


def lem_tokens(tokens):
    lemmer = nltk.stem.WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]


def lemmatizer(text):
    remove_punc_dict = dict((ord(punct), None) for punct in string.punctuation)
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punc_dict)))


def greet(sentence):
    greet_inputs = ('hello', 'hi', 'hey')
    greet_outputs = ('hi', 'hey', 'Hey there')
    for word in sentence.split():
        if word.lower == 'wassup':
            return 'M good! You say!';
        if word.lower in greet_inputs and word.lower != 'wassup':
            return random.choice(greet_outputs)


def response(user_response, sentence_tokens):
    robo1_response = ''
    tf_idf_vec = TfidfVectorizer(tokenizer=lemmatizer, stop_words='english')
    tfidf = tf_idf_vec.fit_transform(sentence_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo1_response = robo1_response + 'I am Sorry. Unable to understand you!'
        return robo1_response
    else:
        robo1_response = robo1_response + sentence_tokens[idx]
        return robo1_response


def home(request):
    if request.method == 'POST':
        topic = request.POST.get('topic').lower()
        find_data(topic)
        return redirect('bot')

    return render(request,'home.html')


def bot_page(request):
    bot_text = 'Hello there! I am a learning Bot. Start typing your text after greeting to talk to me. To exit type ' \
               'bye! '
    if request.method == 'POST':
        u_text = request.POST.get('u_text').lower()
        user_response = u_text
        user_response = user_response.lower()
        if user_response != 'bye':
            if user_response == 'thank you' or user_response == 'thanks':
                bot_text = 'You are Welcome..'
            else:
                if greet(user_response) is not None:
                    bot_text = greet(user_response)
                else:
                    sentence_tokens, word_tokens = utility_func()
                    sentence_tokens.append(user_response)
                    bot_text = response(user_response, sentence_tokens)
                    sentence_tokens.remove(user_response)
        else:
            bot_text = 'Goodbye!'

    return render(request, 'bot.html', {'bot_text': bot_text})
