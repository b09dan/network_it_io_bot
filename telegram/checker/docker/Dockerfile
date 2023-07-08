FROM python:alpine


RUN adduser -D telegram

RUN pip3 install requests \
    && mkdir -p /anf_checker/database \
    && chown -R telegram /anf_checker 

COPY ./tmp/* /anf_checker/

WORKDIR /anf_checker

USER telegram

CMD python3 checker.py
   

LABEL title="Antispam bot anf_checker." 
