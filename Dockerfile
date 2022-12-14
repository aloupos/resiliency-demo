from alpine:latest
RUN apk add --no-cache py3-pip \
    && pip3 install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt


ENTRYPOINT ["python3"]
CMD ["transaction_service.py"]
#CMD ["test.py"]
EXPOSE 5000
