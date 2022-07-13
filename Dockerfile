FROM python:3.9

COPY . .

EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait

RUN chmod +x /wait
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

CMD /wait && python3 main.py

#docker system prune -a --volumes