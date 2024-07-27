FROM python:3.9

#working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install pandas numpy

# Run task_script.py
CMD ["python", "task.py"]