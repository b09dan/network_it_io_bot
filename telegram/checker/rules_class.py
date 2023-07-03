# -*- coding: utf-8 -*-
import re
import sqlite3
from db_functions_class import DbFunctions

# one class for all rules and checks
class Rules:

#
#                           Message check
# 

    #work with message: make spam decision. False = not spam----------------------------
    @staticmethod
    def message_check(config_values, message_text, user_id, chat_id, reply_id):
        print("Message check starting.")

        if DbFunctions.is_human(config_values, user_id):
            print("This is human. Stop message check.")
            return False

        if DbFunctions.duplicate_messages(config_values, user_id, message_text):
            print("This is duplicated message. Stop message check.")
            return True
        
        #spam points (needs to be adjusted)
        spam_probability = 0
        
        #check language mix
        #these combintation of checks work perfect. if they al true - 100% spam
        if Rules.languages_mix(message_text):
            spam_probability += 1
            #emotions - heavy function
            if Rules.check_emotions(message_text):
                print("too many emotions")
            if Rules.count_newlines(message_text):
                print("too many newlines")          


        #check regexp
        spam_probability += 10 *  Rules.regexp_check(message_text)
        if spam_probability > 0:
            #emotions - heavy function
            if Rules.check_emotions(message_text):
                print("too many emotions") 
            if Rules.count_newlines(message_text):
                print("too many newlines") 
            if Rules.count_eclamation_marks(message_text):
                print("too many eclamation marks") 

        if spam_probability > 0:
            print(spam_probability)
            if spam_probability > 20:
                #print(spam_probability)
                print(message_text)
        
        print("Message check done.")
        return False

#
#                           Main functions
# 
    #how many words from black list
    @staticmethod
    def regexp_check(message_text):
        match_points = 0
        message_text = message_text.lower()
        cleaned_text = ''.join(c for c in message_text if c.isalnum() or c.isspace())
        word_count = len(cleaned_text.split())

        blacklist_list = ['00$', 'активн',  'ответствен', 'партн', 'удалён', 'работ', 'обуч',  'писат', 'личн', 'сообщен', 'крипт', 'предлаг',
                        'залив', 'профит', 'свобод', 'сотрудничеств', 'мотивац', 'депозит', 'трейдин']
        if word_count > 5:
            for word in blacklist_list:
                match_points += message_text.count(word)
        
        return round(10*match_points/(word_count + 1))

    #check against mix of languages
    @staticmethod
    def languages_mix(message_text):
        russian_alphabet = re.compile(r'^[а-яёА-ЯЁ]+$')
        english_alphabet = re.compile(r'^[a-zA-Z]+$')
        pattern = r'[^А-яЁёA-Za-z\s]'
        text = re.sub(pattern, '', message_text)
        cleaned_text = re.sub(r'\n', ' ', text)

        mixed_words_count = 0
        for word in cleaned_text.split(' '):
            if len(word) > 4 and russian_alphabet.match(word) is None and english_alphabet.match(word) is None:
                #print(word + str(len(word)))
                mixed_words_count += 1
                if mixed_words_count > 1:
                    return True #two mixed words enough for decision
        return False
   



#
#                           additional checks
# 
    #too many newlines? use this only as additional check
    def count_newlines(message_text):
        count = message_text.count("\n")
        if count > 4: 
            return True
        return False

    #too many eclamation marks? use this only as additional check
    def count_eclamation_marks(message_text):
        count = message_text.count("!")
        if count > 4: 
            return True
        return False

    
    #too many emotions? use this only as additional check or optimize it first
    def check_emotions(message_text):
        #make message shorter
        message_short = message_text[:300]

        emotion_ranges = [
            (0x1F601, 0x1F64F),
            (0x2702, 0x27B0),
            (0x1F680, 0x1F6C0),
            (0x24C2, 0x1F251),
            (0x1F600, 0x1F636),
            (0x1F681, 0x1F6C5)
        ]
        count = 0
        for start, end in emotion_ranges:
            for codepoint in range(start, end + 1):
                emotion = chr(codepoint)
                if emotion in message_short:
                    count += 1
        if count > 2:
            return True
        return False


#
#   functions to test or for analyse
#
    #not tested
    def find_unicode_emotions(message_text):
        pattern = r"[\U0001F000-\U0001F9FF]+" 

        emotions = re.findall(pattern, message_text[:300])
        return len(emotions)


    #check agains greek alphabet. for future use?
    @staticmethod
    def is_greek_letters(message_text):
        greek_alphabet = re.compile(r'[α-ωΑ-Ω]')
        greek_letters = re.findall(greek_alphabet, message_text)
        count = len(greek_letters)
        if count > 2: 
            return True
        return False






