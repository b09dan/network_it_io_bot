# -*- coding: utf-8 -*-
import re
import sqlite3
from db_functions_class import DbFunctions

# one class for all rules and checks
class Rules:

    #how many words from black list
    @staticmethod
    def regexp_check(message_text):
        match_points = 0
        message_text = message_text.lower()
        blacklist_list = [ 'активн',  'ответствен', 'партнер', 'удалённо', 'работ', 'обуч',  'писат', 'личн', 'сообщен', 'крипт']
        for word in blacklist_list:
            match_points += message_text.count(word)
        
        return match_points
        
    #check against mix of languages
    @staticmethod
    def languages_mix(message_text):
        russian_alphabet = re.compile(r'^[а-яёА-ЯЁ]+$')
        english_alphabet = re.compile(r'^[a-zA-Z]+$')
        pattern = r'[^А-яЁёA-Za-z\s]'
        text = re.sub(pattern, '', message_text)
        cleaned_text = re.sub(r'\n', '', text)

        mixed_words_count = 0
        for word in cleaned_text.split(' '):
            if len(word) > 4 and russian_alphabet.match(word) is None and english_alphabet.match(word) is None:
                print(word + str(len(word)))
                mixed_words_count += 1
                if mixed_words_count > 1:
                    return True #two mixed words enough for decision
        return False
   

    #work with message: make spam decision. False = not spam
    @staticmethod
    def message_check(config_values, message_text, user_id, chat_id, reply_id):
        
        if DbFunctions.is_human(config_values, user_id):
            return False

        if DbFunctions.duplicate_messages(config_values, user_id, message_text):
            return True
        
        #spam points (needs to be adjusted)
        spam_probability = 0
        
        #check language mix
        if Rules.languages_mix(message_text):
            spam_probability += 1

        #check regexp
        spam_probability += 10 *  Rules.regexp_check(message_text)
        
        if spam_probability > 0:
            print(spam_probability)
            if spam_probability > 1000:
                print(message_text)
        

        return False











