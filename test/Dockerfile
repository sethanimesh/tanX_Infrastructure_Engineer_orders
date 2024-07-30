FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the entire context into the container
COPY . /app

# Ensure that the 'test' directory exists and is recognized as a Python package
RUN mkdir -p /app/test && touch /app/test/__init__.py

# Install necessary Python packages
RUN pip install pandas numpy

# Run the unit tests using unittest's discovery mode
CMD ["python", "-m", "unittest", "discover", "-s", "test", "-p", "*.py"]