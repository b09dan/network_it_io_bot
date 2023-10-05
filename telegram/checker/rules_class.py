# -*- coding: utf-8 -*-
import re
import sqlite3
import unicodedata
from db_functions_class import DbFunctions


# one class for all rules and checks
class Rules:
    #
    #                           Message check
    #

    # work with message: make spam decision. False = not spam----------------------------
    @staticmethod
    def message_check(config_values, message_text, user_id, chat_id, reply_id, message_id):
        logger = config_values["logger"]

        logger.info("Message_id=%s. Start message check.  Chat_id=%s", message_id, chat_id)
        is_mixed = False

        if DbFunctions.is_human(config_values, user_id):
            logger.info("Message_id=%s. This is human (not spam). Stop message check.", message_id)
            return False

        if DbFunctions.duplicate_messages(config_values, user_id, message_text):
            logger.info("Message_id=%s. This is duplicated (spam) message. Stop message check.", message_id)
            return True

        # spam points (needs to be adjusted)
        spam_probability = 0
        # check regexp
        spam_probability += 10 * Rules.regexp_check(message_text)
        logger.info("Message_id=%s. Spam probability = %d.", message_id, spam_probability)
        # check language mix
        is_mixed = Rules.languages_mix(message_text, message_id, logger)
        # extended alphabet
        is_extended_alphabet = Rules.contains_modified_letters(message_text, message_id, logger)

        # additional checks
        add_checks_sum = (
            int(Rules.count_unicode_characters(message_text, message_id, logger))
            + int(Rules.count_newlines(message_text, message_id, logger))
            + int(Rules.count_eclamation_marks(message_text, message_id, logger))
        )

        if ((is_mixed or spam_probability > 0) and add_checks_sum > 1) or add_checks_sum == 3 or is_extended_alphabet:
            logger.info("Message_id=%s. Message check done: SPAM (advanced rules).", message_id)
            return True

        logger.info("Message_id=%s. Message check done.  Chat_id=%s", message_id, chat_id)

        return False

    #
    #                           Main functions
    #
    # how many words from black list
    @staticmethod
    def regexp_check(message_text):
        match_points = 0
        message_text = message_text.lower()
        cleaned_text = "".join(c for c in message_text if c.isalnum() or c.isspace())
        word_count = len(cleaned_text.split())

        blacklist_list = [
            "00$",
            "00 $",
            "00€",
            "00 €",
            "активн",
            "ответствен",
            "партн",
            "удалён",
            "работ",
            "обуч",
            "писат",
            "личн",
            "сообщен",
            "крипт",
            "предлаг",
            "залив",
            "профит",
            "свобод",
            "сотрудничеств",
            "мотивац",
            "депозит",
            "трейдин",
            "пиши",
            "temи.com",
            "бирж",
            "судьб",
            "crypt",
            "оbуч",
            "bесплат",
            "арбит",
            "трейд",
            "треид",
            "возможности"
            "бинанс",
            "скам",
            "CRY5TO",
            "💲",
            "лс",
            "партнер",
            "актuвн",
            "пuсат",
            "лuчн",
            "крuпт",
            "залuв",
            "профuт",
            "сотруднuчеств",
            "мотuвац",
            "депозuт",
            "трейдuн",
            "пuшu",
            "temu.com",
            "бuрж",
            "арбuт",
            "треuд",
            "возможностu"
            "бuнанс",
        ]
        if word_count > 5:
            for word in blacklist_list:
                match_points += message_text.count(word)

        return round(10 * match_points / (word_count + 1))

    # check against mix of languages
    @staticmethod
    def languages_mix(message_text, message_id, logger):
        russian_alphabet = re.compile(r"^[а-яёА-ЯЁ]+$")
        english_alphabet = re.compile(r"^[a-zA-Z]+$")
        pattern = r"[^А-яЁёA-Za-z\s]"
        text = re.sub(pattern, "", message_text)
        cleaned_text = re.sub(r"\n", " ", text)

        mixed_words_count = 0
        for word in cleaned_text.split(" "):
            if len(word) > 4 and russian_alphabet.match(word) is None and english_alphabet.match(word) is None:
                mixed_words_count += 1
                if mixed_words_count > 1:
                    logger.info("Message_id=%s. Mixed languages.", message_id)
                    return True  # two mixed words enough for decision
        return False

    # detect modified alphabet
    def contains_modified_letters(message_text, message_id, logger):
        # extended unicodes for russian and latin
        modified_russian_alphabet = range(0x1D04, 0x1D2B)
        modified_latin_alphabet = range(0x1D00, 0x1D7F)
        count = 0

        for char in message_text[:100]:
            if ord(char) in modified_russian_alphabet or ord(char) in modified_latin_alphabet:
                count += 1

        if count > 3:
            logger.info("Message_id=%s. Extended alphabet detected.", message_id)
            return True

        return False

    #
    #                           additional checks
    #
    # too many newlines? use this only as additional check
    def count_newlines(message_text, message_id, logger):
        count = message_text.count("\n")
        if count > 3:
            logger.info("Message_id=%s. Too many newlines: %d", message_id, count)
            return True

        return False

    # too many eclamation marks? use this only as additional check
    def count_eclamation_marks(message_text, message_id, logger):
        count = message_text.count("!")
        if count > 4:
            logger.info("Message_id=%s. Too many eclamation marks: %d", message_id, count)
            return True
        return False

    # count emotions (not exactly but close to needed)
    def count_unicode_characters(message_text, message_id, logger):
        count = 0
        for char in message_text:
            if unicodedata.category(char)[0] == "C":
                count += 1
        if count > 3:
            logger.info("Message_id=%s. Too many Unicode: %d", message_id, count)
            return True

        return False

    #
    #   functions to test or for analyse
    #

    # check agains greek alphabet. for future use?
    @staticmethod
    def is_greek_letters(message_text, message_id):
        greek_alphabet = re.compile(r"[α-ωΑ-Ω]")
        greek_letters = re.findall(greek_alphabet, message_text)
        count = len(greek_letters)
        if count > 2:
            return True
        return False
