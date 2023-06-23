import re

# one class for all rules and checks
class Rules:

    #check against duplicate messages
    @staticmethod
    def duplicate_messages(user, message):
        #check hash and compare to previous 
        return True

    #all regexp checks with the summ of matched regexps
    @staticmethod
    def regexp_check(message):
        return match_points
        
    #check against mix of languages
    @staticmethod
    def languages_mix(message):
        russian_alphabet = re.compile(r'^[а-яёА-ЯЁ]+$')
        english_alphabet = re.compile(r'^[a-zA-Z]+$')
        for word in message.split(' '):
            if len(word) > 5 and russian_alphabet.match(word) is None and english_alphabet.match(word) is None:
                return True #may be we need only one word, may be not
        return False
   


