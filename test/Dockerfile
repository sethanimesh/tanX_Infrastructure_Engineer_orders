FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install pandas numpy unittest

CMD ["python", "-m", "unittest", "discover", "-s", "test", "-p", "*.py"]