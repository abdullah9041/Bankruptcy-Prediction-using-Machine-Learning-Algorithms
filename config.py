# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kI5TmD5oo2zxqbrai_-SEfyua6ZR5Yk5
"""

# Configuration parameters for bankruptcy prediction

# Path to the dataset files (Excel format)
INACTIVE_DATASET_PATH = 'path/to/inactive_{year}.xlsx'
ACTIVE_DATASET_PATH = 'path/to/active_{year}.xlsx'

# List of financial ratios used for analysis
FINANCIAL_RATIOS = ['ratio_1', 'ratio_2', 'ratio_3', '...']

# Number of samples to extract from each dataset
NUM_SAMPLES = 500

# Machine learning algorithms to be used
ML_ALGORITHMS = ['Baseline', 'Logistic Regression', 'Random Forest', 'k-NN Classifier', 'Linear SVM', 'Neural Networks']

# Hyperparameters for models
BASELINE_PARAMETERS = {
    'strategy': 'most_frequent',
    'random_state': 42
}

LOGISTIC_REGRESSION_PARAMETERS = {
    'max_iter': 1900
}

RANDOM_FOREST_PARAMETERS = {
    'n_estimators': 100,
    'max_depth': None,
    'random_state': 42
}

KNN_PARAMETERS = {
    'n_neighbors': 5,
    'weights': 'uniform'
}

LINEAR_SVM_PARAMETERS = {
    'C': 10,         # Adjusted based on your hyperparameter tuning
    'max_iter': 1000 # Adjusted based on your hyperparameter tuning
    # Add more parameters based on your hyperparameter tuning
}

NEURAL_NETWORK_PARAMETERS = {
    'hidden_layer_sizes': (20, 10),
    'activation': 'relu',
    'solver': 'adam',
    'batch_size': 32,
    'epochs': 200
}