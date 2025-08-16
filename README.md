
# US Visa Approval Prediction

This project aims to predict the approval of US visa applications using machine learning techniques. The dataset used for this project is sourced from Kaggle and contains various features related to visa applications. 

## Problem Statement

Given certain features of a visa application, the goal is to predict whether the application will be approved or not. This is a binary classification problem where the target variable is `approved` (1 for approved, 0 for not approved).

## Solution Scope

This can be used in real life by visa processing agencies to automate the initial screening of applications, thereby improving efficiency and reducing manual workload. Also US visa applicants can use this model to get an idea of their chances of approval based on historical data, so that they could improve their applications accordingly.

## Solution Proposal

We will build a machine learning model using the following steps:
1. **Load the dataset**: Import the necessary libraries and load the dataset.   
2. **Data Preprocessing**: Clean the data, handle missing values, and encode categorical variables.
3. **Exploratory Data Analysis (EDA)**: Analyze the data to understand the distribution of features and their relationship with the target variable.
4. **Feature Engineering**: Create new features if necessary, and select the most relevant features for the model.
5. **Model Building**: Split the data into training and testing sets, and build a machine learning model using algorithms like Logistic Regression, Decision Trees, or Random Forest, etc.
6. **Hyperparameter Tuning**: Optimize the model's performance by tuning hyperparameters using techniques like Grid Search or Random Search.
7. **Model Evaluation**: Evaluate the model's performance using metrics like accuracy, precision, recall, and F1-score.

---

## Data Ingestion

We have implemented the first step of the MLOps pipeline: **Data Ingestion**. 

- Reads data from CSV files, serving as the initial data source.

- Performs a stratified train-test split to ensure balanced representation across classes.

- Organizes and saves artifacts, such as processed datasets, in a structured directory.

- Generates a `DataIngestionArtifact` that includes metadata and file paths for traceability.

#### Data Ingestion Flow

```
[Data Ingestion Config]
   |-- Data Ingestion Dir
   |-- Feature Store File Path
   |-- Training File Path
   |-- Testing File Path
   |-- Train-Test Split Ratio
   |-- Collection Name
	   |
	   v
[Initiate Data Ingestion] ---> (MongoDB)
	   |
	   v
[Export Data to Feature Store] ---> [usvisa.csv] ---> [Feature Store] ---> [Ingested]
	   |
	   v
[Split Data as Train and Test]
	   |
	   +--> [Data Ingestion Artifact] ---> [artifact folder]
	   +--> [train.csv]
	   +--> [test.csv]
```

#### Steps Completed

- Configured data ingestion parameters (directories, file paths, split ratio, collection name).
- Connected to MongoDB and exported the data to a local feature store as `usvisa.csv`.
- Split the data into training and testing sets based on the configured ratio.
- Saved the ingested artifacts (train/test CSVs) in the designated artifact folder for downstream tasks.

---

## Data Validation

We have implemented the second step of the MLOps pipeline: **Data Validation**.

- Ensures the integrity and quality of ingested data before it proceeds to further pipeline stages.

- Validates schema (column names, data types, missing values).

- Detects data drift between training and testing sets using the Evidently library.

- Saves validation reports and artifacts for traceability and monitoring.

#### Data Validation Flow

```
[Data Validation Config]
   |-- Schema File (schema.yaml)
   |-- Report File Path
   |-- Report Page Path
        |
        v
[Initiate Data Validation]
        |
        v
[Validate Dataset Schema]
   |-- Check Column Names
   |-- Check Data Types
   |-- Check Missing Values
        |
        v
[Detect Data Drift] ---> (Evidently Library)
        |
        v
[Generate Validation Reports]
   |-- JSON Report (report.json)
   |-- HTML Report (report.html)
        |
        v
[Data Validation Artifact] ---> [artifact folder]
```

#### Steps Completed

- Configured data validation parameters (schema file, report paths).
- Validated schema consistency of ingested train and test datasets.
- Used Evidently to detect and report data drift.
- Generated and saved both JSON and HTML validation reports.
- Stored the DataValidationArtifact in the artifact folder for downstream consumption.

---

## Setup Instructions

1. Clone the repository:
	```bash
	git clone <https://github.com/BenGJ10/US-Visa-Approval-Prediction.git>
	cd US-Visa-Approval-Prediction
	```
2. Create and activate a virtual environment:
	```bash
	python -m venv venv
	source venv/bin/activate
	```
3. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
4. Set up environment variables (e.g., `MONGO_DB_URL`).

5. To run the pipeline:
	```bash
	python main.py
	```

---

**MORE MODULES ON THE WAY...**


