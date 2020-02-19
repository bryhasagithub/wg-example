FROM python:2.7
COPY . /app

WORKDIR /app

RUN pip install -r dependencies.txt

ENTRYPOINT ["python"]

CMD ["main.py"]