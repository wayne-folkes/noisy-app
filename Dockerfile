FROM python

ADD requirements.txt .
ADD src/ /
RUN pip install -r requirements.txt --quiet
ENTRYPOINT [ "/app.py" ]