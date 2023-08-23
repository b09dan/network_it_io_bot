FROM python:alpine


RUN adduser -D telegram

RUN pip3 install requests \
    && mkdir -p /anf_checker/database \
    && chown -R telegram /anf_checker


USER telegram

RUN mkdir -p /anf_checker/database
COPY logging.cfg /anf_checker/logging.cfg
COPY config_checker.cfg /anf_checker/config_checker.cfg

COPY checker.py /anf_checker/checker.py
COPY db_functions_class.py /anf_checker/db_functions_class.py
COPY rules_class.py /anf_checker/rules_class.py
COPY spam_processing_class.py /anf_checker/spam_processing_class.py
COPY training_class.py /anf_checker/training_class.py

WORKDIR /anf_checker

ENTRYPOINT python3 checker.py

LABEL title="Antispam bot anf_checker." 
