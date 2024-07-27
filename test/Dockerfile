FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install packages
RUN pip install pandas numpy unittest

# Run test.py
CMD ["python", "-m", "unittest", "test.py"]
