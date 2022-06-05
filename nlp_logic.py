from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords as sw
import pymorphy2
import re
import translators as ts
from langdetect import detect
from nltk.stem import SnowballStemmer

russian_stopwords = sw.words("russian")
morph = pymorphy2.MorphAnalyzer()
snowball = SnowballStemmer(language="russian")

vacancy_stop_words = ['ведущий', 'главный', 'младший', 'эксперт', 'стажер', 'старший',
                      'middle', 'junior', 'senior', 'стажёр', 'эксперт', 'expert',
                      'помощник', 'главный', 'начальник', 'мастер', 'отдела',
                      'trainee', 'тимлид', 'lead']

ru_to_en_dict = {'разработчик': 'developer',
                 'программист': 'developer',
                 'менеджер': 'manager',
                 'рекрутер': 'recruiter',
                 'аналитик': 'analyst',
                 'исследователь': 'analyst',
                 'эйчар': 'humanresource',
                 'продуктовый': 'product',
                 'руководитель': 'manager',
                 'банковый': 'banking',
                 'банковский': 'banking',
                 'банк': 'banking',
                 'мэнеджер': 'manager',
                 'директор': 'manager',
                 'управляющий': 'manager',
                 'hr': 'humanresource',
                 'c++': 'plusplus',
                 'маркетолог': 'marketing',
                 'pr': 'publicrelations',
                 'стратегический': 'strategy',
                 'qa': 'qualityassurance',
                 'тестировщик': 'qualityassurance'}


class userInput:
    def __init__(self, user_input: str, *args, **kwargs):
        self.initial_input: str = user_input
        self.text: str = user_input
        self.tokens: list = []
        self.process_input()

    def process_input(self):
        # Удалить знаки пунктуации и числа
        tokenizer = RegexpTokenizer(r'\w+')
        self.tokens = tokenizer.tokenize(self.text)

        for pos, token in enumerate(self.tokens):
            # Если токен в ручном словаре - перевод по хэшу
            if token in ru_to_en_dict:
                self.tokens[pos] = ru_to_en_dict[token]

            # Если токен на русском и его нет в ручном словаре - стеммить и переводить
            elif detect(token) == 'ru':
                new_token = snowball.stem(token)
                self.tokens[pos] = ts.google(new_token, from_language='ru', to_language='en').lower()

        self.text = ' '.join(self.tokens)


