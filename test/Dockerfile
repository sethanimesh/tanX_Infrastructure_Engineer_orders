FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the entire context into the container
COPY . /app

RUN mkdir -p /app/test && touch /app/test/__init__.py

RUN pip install pandas numpy

CMD ["python", "-m", "unittest", "discover", "-s", "test", "-p", "*.py"]