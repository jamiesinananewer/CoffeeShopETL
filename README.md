# La-Vida-Mocha
ETL Pipeline for Coffee Shop

DOCKER COMMANDS:
    GET POSTGRES ON DOCKER:
    docker pull postgres
    
    INSIDE THE DOCKER FOLDER TERMINAL:
        START THE DOCKER:
        docker-compose up

        CHECK DOCKER CONFIG DETAILS IN TERMINAL:
        docker config

        Ctrl+C to stop the docker

# AWS Lambda Function for Redshift ETL

This repository contains an AWS Lambda function that performs Extract, Transform, Load (ETL) operations for order data. The Lambda function reads a CSV file from an S3 bucket, processes the data, and loads it into an Amazon Redshift database. It also maintains a unique order number across executions by storing and updating the order number in the S3 bucket.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Testing](#testing)
- [License](#license)

## Overview

This AWS Lambda function is designed to:
1. **Extract** order data from a CSV file stored in an S3 bucket.
2. **Transform** the data by cleaning it and splitting it into relevant tables.
3. **Load** the transformed data into Amazon Redshift tables.
4. **Update** the order number in the S3 bucket to ensure unique order numbers for future operations.

## Features

- Extracts CSV data from S3 and parses it into a list of dictionaries.
- Transforms data to fit Redshift schema requirements.
- Loads data into `orders`, `items`, and `order_item_junction` tables in Redshift.
- Maintains a unique order number across Lambda invocations by storing the last used number in S3.

## Prerequisites

To use this Lambda function, you will need:
- An AWS account with permissions to access S3, Lambda, and Redshift.
- An Amazon Redshift cluster with the necessary database and schema created.
- AWS CLI configured with necessary permissions.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/generation-de-nat1/La-Vida-Mocha.git

Imported libaries
https://docs.python.org/3/library/re.html

