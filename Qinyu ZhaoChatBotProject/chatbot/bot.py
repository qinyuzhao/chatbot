from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from requests_html import HTMLSession
import random
import time

def remove_stop_word(words):
    '''
    remove stop words from a list of words
    :param words: a list of words (list)
    :return: a list of words without stopwords (list)
    '''
    return [w for w in words if w not in stopwords.words('english')]


def tokenize(sentence):
    '''
    remove punctuations and tokenize the sentence
    :param sentence: a sentence (str)
    :return: tokenized sentence (list)
    '''
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(sentence)


def preprocessing(sentence):
    '''
    preprocess the sentence input to a series of words
    :param sentence: sentence input (str)
    :return: words (list)
    '''
    sentence = sentence.lower()  # get lower str
    words = tokenize(sentence)
    return remove_stop_word(words)

class ChatBot:
    '''
    The chat bot class
    '''

    name = ""

    say_hello = [
        "Hello!",
        "Hello",
        "Hi",
        "Hi!",
        "Good morning!"
    ]

    answer_hello = [
        "Hello ^_^",
        "Hi ^_^"
    ]

    sentences = [
        "What a nice day today!",
        "wow ~",
        "^_^",
        "A boring day.. =_=",
        "AI will rule the world!",
        "meow~meow~meow~",
        "What's that?"
    ]

    say_bye = [
        'Goodbye!',
        'Bye!'
    ]

    def __init__(self, name):
        '''
        init function
        :param name: the bot's name
        '''
        self.name = name
        self.sentences.extend([self.name + " is a smart robot!",
                               "No one can stop " + self.name + " form ruling the world",
                               "Do you like " + self.name + "?",
                               "I'm " + self.name + " ~~~~~~"])

    last_sentence = ""  # The bot can remember what you just said to him.

    def say(self, sentence):
        '''
        Return the sentence
        :param sentence: str
        :return: str
        '''
        print (self.name + " says:", sentence)
        return sentence

    def ask_stackoverflow(self, key_words):
        '''
        Search answer from Stack Overflow
        :param key_words: list of key words (list of str)
        :return: answer from Stack Overflow (str)
        '''
        htmlsess = HTMLSession()  # instantiate the class HTMLSession
        querry = "+".join(key_words)  # organize the question
        url_question = "https://stackoverflow.com/search?q=" + querry  # make link of stackoverflow
        content_question = htmlsess.get(url_question)  # get html content
        url_answer = "https://stackoverflow.com/" + \
                     content_question.html.xpath("//div[@class='result-link']/h3/a/@href")[0]
        content_answer = htmlsess.get(url_answer)
        answer = content_answer.html.xpath("//div[@id='answers']")[0].xpath("//div[@class='post-text']")[0].text
        return answer

    def answer_python_question(self, question):
        '''
        Answer a python question
        :param question: a sentence describe the question (str)
        :return: answer from Stack Overflow (str)
        '''
        key_words = preprocessing(question)
        answer = self.ask_stackoverflow(key_words)
        return answer

    def is_question(self, sentence):
        '''
        Is the sentence a question?
        :param sentence: str
        :return: boolean
        '''
        if "?" in sentence:
            return True
        else:
            return False

    def is_python_question(self, sentence):
        '''
        Is the sentence a python question?
        :param sentence:
        :return:
        '''
        if "python" in sentence.lower():
            return True
        else:
            return False

    def is_quit(self, sentence):
        '''
        Is a quit command?
        :param sentence: str
        :return: boolean
        '''
        if "quit" in sentence.lower():
            return True
        else:
            return False

    def random_choice(self, sentences):
        '''
        Choose a sentence from a list of sentences randomly.
        :param sentences: list of sentences (list of str)
        :return: sentence choice (str)
        '''
        return random.choice(sentences)

    def answer(self, sentence):
        '''
        Say a sentence.
        :param sentence: sentence the chatbot got (str)
        :return: a sentence (str)
        '''
        if sentence in self.say_hello and self.last_sentence not in self.say_hello:
            self.last_sentence = sentence
            return self.random_choice(self.say_hello)
        if self.is_python_question(sentence):
            self.last_sentence = sentence
            return self.answer_python_question(sentence)
        if self.is_question(sentence):
            self.last_sentence = sentence
            return "Sorry, I can't answer this question.  T.T"
        if "sorry" in sentence.lower():
            self.last_sentence = sentence
            return "That's OK."
        self.last_sentence = sentence
        return self.random_choice(self.sentences)

    def chat(self):
        '''
        Start a chat!
        :return: None
        '''
        print ("Hi, I'm a chat bot.")  # start sentence
        while (True):
            sentence = input("You:")
            if self.is_quit(sentence):
                self.say(self.random_choice(self.say_bye))
                break
            else:
                self.say(self.answer(sentence))

def two_bots(round):
    '''
    Let two bots chat with each other
    :param round: number of round the bots talk
    :return: None
    '''
    bot0 = ChatBot("bot0")
    bot1 = ChatBot("bot1")

    counter = 0
    sentence = "Hello!"
    time.sleep(1)
    bot0.say(sentence)
    while(counter < round):
        sentence = bot1.say(bot1.answer(sentence))
        time.sleep(1)
        sentence = bot0.say(bot0.answer(sentence))
        time.sleep(1)
        counter += 1
    bot1.say(bot1.random_choice(bot1.say_bye))
    time.sleep(1)
    bot0.say(bot0.random_choice(bot0.say_bye))
    time.sleep(1)


