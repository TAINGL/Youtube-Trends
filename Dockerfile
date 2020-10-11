FROM python:3.7

COPY . /app

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

EXPOSE 5000 

ENTRYPOINT ["python"]
CMD ["app.py"]