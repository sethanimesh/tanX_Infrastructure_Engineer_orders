# tanX.fi Orders Project

## Overview

This project processes order data, calculates various metrics such as monthly revenue, product revenue, and customer revenue, and includes unit tests to validate the data processing logic. The project is Dockerized with separate services for the task processing and testing.

## Project Structure

/my_app
  /task
    Dockerfile
    task_script.py
    orders.csv
  /test
    Dockerfile
    test_script.py
docker-compose.yml


## Setup Instructions

1. **Clone the Repository**
   git clone https://github.com/sethanimesh/tanX_Infrastructure_Engineer_orders.git

2. **Ensure Docker and Docker Compose are Installed**
  
## Running the Task Service
The task service processes the order data, performs data cleaning, and calculates various metrics.


**Navigate to the Project Directory:**

 ```
  cd /path/to/tanX_Infrastructure_Engineer_orders
  Build and Run the Task Service:
```

```
docker-compose up --build task
```

### Check the Output:

The processed data and metrics will be displayed in the console.

The cleaned data will be saved as orders_rearranged.csv in the /task directory.


### Running the Tests
The test service runs unit tests to validate the data processing logic.

Build and Run the Test Service:
```
docker-compose up --build test
```

### Check the Output:
The test results will be displayed in the console.

## File Details

### task/task.py

This script:

Loads the dataset (orders.csv).
Cleans and processes the data.
Calculates monthly revenue, product revenue, and customer revenue.
Saves the cleaned data to orders_rearranged.csv.


### test/test.py

This script contains unit tests that:

Validate the conversion of order dates.
Check the calculation of total revenue.
Verify the extraction of month and year from order dates.
Confirm the calculation of monthly,
product, and customer revenue.

## Contact

For any questions, please contact [sethanimesh@hotmail.com].
