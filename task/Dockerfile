FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip setuptools

RUN pip install pandas==1.3.3 numpy==1.21.2

RUN mkdir -p /app/task && touch /app/task/__init__.py

CMD ["python", "-m", "task.__main__"]