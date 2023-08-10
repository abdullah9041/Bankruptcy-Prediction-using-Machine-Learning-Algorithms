# -*- coding: utf-8 -*-
"""Dissertation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dmch69K_0FHmcFBWwuSWUrOzxZ7yIT3l

# Data Cleaning and pre-processing
"""

#importing the necessary libraries
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from scipy import stats
from sklearn import linear_model
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support, classification_report
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import cross_val_predict
from sklearn.svm import LinearSVC
from sklearn import tree
from sklearn import ensemble
from sklearn import neural_network
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.dummy import DummyClassifier
import time
from sklearn.impute import KNNImputer

#INACTIVE COMPANIES
def inactive_clean_data():
    df=pd.read_excel(f"inactive_{year}.xlsx")
    df = df.drop('Company name', axis=1)
    df = df.replace(0, np.nan)
    df=df.loc[~(df == 'n.s.').sum(axis=1).astype(bool)]
    df=df.loc[~(df == 'n.a.').sum(axis=1).astype(bool)]
    df['Bankrupt']=1
    nan = np.nan
    imputer = KNNImputer(n_neighbors=5)
    df = pd.DataFrame(imputer.fit_transform(df),columns = df.columns)
    df=df.sample(n=500,random_state=1)
    return df

#ACTIVE COMPANIES
def active_clean_data():
    df=pd.read_excel(f"active_{year}.xlsx")
    df = df.drop('Company name', axis=1)
    df = df.replace(0, np.nan)
    df=df.loc[~(df == 'n.s.').sum(axis=1).astype(bool)]
    df=df.loc[~(df == 'n.a.').sum(axis=1).astype(bool)]
    df['Bankrupt']=0
    nan = np.nan
    imputer = KNNImputer(n_neighbors=5)
    df = pd.DataFrame(imputer.fit_transform(df),columns = df.columns)
    df=df.sample(n=500,random_state=1)
    return df

year='2017'
inactive_2017=inactive_clean_data()
active_2017=active_clean_data()
total_2017=active_2017.append(inactive_2017)

year='2018'
inactive_2018=inactive_clean_data()
active_2018=active_clean_data()
total_2018=active_2018.append(inactive_2018)

year='2019'
inactive_2019=inactive_clean_data()
active_2019=active_clean_data()
total_2019=active_2019.append(inactive_2019)

year='2020'
inactive_2020=inactive_clean_data()
active_2020=active_clean_data()
total_2020=active_2020.append(inactive_2020)

year='2021'
inactive_2021=inactive_clean_data()
active_2021=active_clean_data()
total_2021=active_2021.append(inactive_2021)

"""# Loading and exploring the data"""

my_dfs=[total_2017,total_2018,total_2019,total_2020,total_2021]

#checking the datatype in file
for df in my_dfs:
  print(df.dtypes)

#checking distribution for all features
for df in my_dfs:
  df.hist(figsize = (40,40))

#correlation matrix to check the relationship of each financial ratio(predictor) with bankruptcy (target)
#Each year separately
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize = (20,20))
sns.heatmap(total_2017.corr(), cmap = "Oranges")

plt.figure(figsize = (20,20))
sns.heatmap(total_2018.corr(), cmap = "Oranges")

plt.figure(figsize = (20,20))
sns.heatmap(total_2019.corr(), cmap = "Oranges")

plt.figure(figsize = (20,20))
sns.heatmap(total_2020.corr(), cmap = "Oranges")

plt.figure(figsize = (20,20))
sns.heatmap(total_2021.corr(), cmap = "Oranges")

#Summary Statistics for each year's dataset
#1 year before bankruptcy i.e. 2021
total_2021.describe()

#2 years before bankruptcy i.e. 2020
total_2020.describe()

#3 years before bankruptcy i.e. 2019
total_2019.describe()

#4 years before bankruptcy i.e. 2018
total_2018.describe()

#5 years before bankruptcy i.e. 2017
total_2017.describe()

#defining the predictor and target variables for each year
#5 years before bankruptcy i.e. 2017
X5 = total_2017.drop(columns = "Bankrupt")
Y5 = total_2017["Bankrupt"]
#4 years before bankruptcy i.e. 2018
X4 = total_2018.drop(columns = "Bankrupt")
Y4 = total_2018["Bankrupt"]
#3 years before bankruptcy i.e. 2019
X3 = total_2019.drop(columns = "Bankrupt")
Y3 = total_2019["Bankrupt"]
#2 years before bankruptcy i.e. 2020
X2 = total_2020.drop(columns = "Bankrupt")
Y2 = total_2020["Bankrupt"]
#1 year before bankruptcy i.e. 2021
X1 = total_2021.drop(columns = "Bankrupt")
Y1 = total_2021["Bankrupt"]

#checking for the class balance for each year
for df in my_dfs:
  print(df['Bankrupt'].value_counts())

#doing a 80-20 split for each year's dataset
from sklearn.model_selection import train_test_split
#1 year before bankruptcy i.e. 2021
X1_train,X1_test,Y1_train,Y1_test = train_test_split(X1,Y1, test_size=0.2, random_state=1,stratify=total_2021["Bankrupt"])
#2 years before bankruptcy i.e. 2020
X2_train,X2_test,Y2_train,Y2_test = train_test_split(X2,Y2, test_size=0.2, random_state=1,stratify=total_2020["Bankrupt"])
#3 years before bankruptcy i.e. 2019
X3_train,X3_test,Y3_train,Y3_test = train_test_split(X3,Y3, test_size=0.2, random_state=1,stratify=total_2019["Bankrupt"])
#4 years before bankruptcy i.e. 2018
X4_train,X4_test,Y4_train,Y4_test = train_test_split(X4,Y4, test_size=0.2, random_state=1,stratify=total_2018["Bankrupt"])
#5 years before bankruptcy i.e. 2017
X5_train,X5_test,Y5_train,Y5_test = train_test_split(X5,Y5, test_size=0.2, random_state=1,stratify=total_2017["Bankrupt"])

#normalize the data since algorithms like NN and KNN do not assume any distribution of data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
#1 year before bankruptcy i.e. 2021
X1_train = scaler.fit_transform(X1_train)
X1_test = scaler.fit_transform(X1_test)
#2 year before bankruptcy i.e. 2020
X2_train = scaler.fit_transform(X2_train)
X2_test = scaler.fit_transform(X2_test)
#3 year before bankruptcy i.e. 2019
X3_train = scaler.fit_transform(X3_train)
X3_test = scaler.fit_transform(X3_test)
#4 year before bankruptcy i.e. 2018
X4_train = scaler.fit_transform(X4_train)
X4_test = scaler.fit_transform(X4_test)
#5 year before bankruptcy i.e. 2017
X5_train = scaler.fit_transform(X5_train)
X5_test = scaler.fit_transform(X5_test)

"""# Baseline Model"""

#BASELINE MODEL using Dummy Classifier for each year
from sklearn.dummy import DummyClassifier
from sklearn.metrics import precision_recall_fscore_support, classification_report
from sklearn import metrics

#1 year before bankruptcy i.e. 2021
baseline1 = DummyClassifier(random_state=42)
baseline1.fit(X1_train, Y1_train)
Y1_hat_baseline=baseline1.predict(X1_test)
p1,r1,f1,s1 = precision_recall_fscore_support(Y1_test,Y1_hat_baseline, average="macro")
print(f"Precision - 1 year before bankruptcy: {p1}")
print(f"Recall - 1 year before bankruptcy: {r1}")
print(f"F-score - 1 year before bankruptcy: {f1}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y1_test,Y1_hat_baseline))

#2 year before bankruptcy i.e. 2020
baseline2 = DummyClassifier(random_state=42)
baseline2.fit(X2_train, Y2_train)
Y2_hat_baseline=baseline2.predict(X2_test)
p2,r2,f2,s2 = precision_recall_fscore_support(Y2_test,Y2_hat_baseline, average="macro")
print(f"Precision - 2 year before bankruptcy: {p2}")
print(f"Recall - 2 year before bankruptcy: {r2}")
print(f"F-score - 2 year before bankruptcy: {f2}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y2_test,Y2_hat_baseline))

#3 year before bankruptcy i.e. 2019
baseline3 = DummyClassifier(random_state=42)
baseline3.fit(X3_train, Y3_train)
Y3_hat_baseline=baseline3.predict(X3_test)
p3,r3,f3,s3 = precision_recall_fscore_support(Y3_test,Y3_hat_baseline, average="macro")
print(f"Precision - 3 year before bankruptcy: {p3}")
print(f"Recall - 3 year before bankruptcy: {r3}")
print(f"F-score - 3 year before bankruptcy: {f3}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y3_test,Y3_hat_baseline))

#4 year before bankruptcy i.e. 2018
baseline4 = DummyClassifier(random_state=42)
baseline4.fit(X4_train, Y4_train)
Y4_hat_baseline=baseline4.predict(X4_test)
p4,r4,f4,s4 = precision_recall_fscore_support(Y4_test,Y4_hat_baseline, average="macro")
print(f"Precision - 4 year before bankruptcy: {p4}")
print(f"Recall - 4 year before bankruptcy: {r4}")
print(f"F-score - 4 year before bankruptcy: {f4}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y4_test,Y4_hat_baseline))

#5 year before bankruptcy i.e. 2017
baseline5 = DummyClassifier(random_state=42)
baseline5.fit(X5_train, Y5_train)
Y5_hat_baseline=baseline5.predict(X5_test)
p5,r5,f5,s5 = precision_recall_fscore_support(Y5_test,Y5_hat_baseline, average="macro")
print(f"Precision - 5 year before bankruptcy: {p5}")
print(f"Recall - 5 year before bankruptcy: {r5}")
print(f"F-score - 5 year before bankruptcy: {f5}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y5_test,Y5_hat_baseline))

"""# Logistic Regression"""

#1 year before bankruptcy i.e. 2021
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
lg1 = linear_model

lg1 = linear_model.LogisticRegression(max_iter=1900)
lg1.fit(X1_train,Y1_train)

# Evaluating model on test data
Y1_hat_lg = lg1.predict(X1_test)

# checking for Recall, Precision and Fscore of Baseline model
p1,r1,f1,s1 = precision_recall_fscore_support(Y1_test,Y1_hat_lg, average="macro")

print(f"Precision - 1 year before bankruptcy: {p1}")
print(f"Recall - 1 year before bankruptcy: {r1}")
print(f"F-score - 1 year before bankruptcy: {f1}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y1_test,Y1_hat_lg))

#Coefficients for the LogReg model
coeff=lg1.coef_
Coefficients = pd.DataFrame(coeff, columns = X1.columns)
Coefficients.head(10)

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(lg1, X1_test, Y1_test,cmap='Oranges',normalize='true')

#2 year before bankruptcy i.e. 2020
from sklearn import linear_model
lg2 = linear_model

lg2 = linear_model.LogisticRegression(max_iter=1900)
lg2.fit(X2_train,Y2_train)

# Evaluating model on test data
Y2_hat_lg = lg2.predict(X2_test)

# checking for Recall, Precision and Fscore of Baseline model
p2,r2,f2,s2 = precision_recall_fscore_support(Y2_test,Y2_hat_lg, average="macro")

print(f"Precision - 2 year before bankruptcy: {p2}")
print(f"Recall - 2 year before bankruptcy: {r2}")
print(f"F-score - 2 year before bankruptcy: {f2}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y2_test,Y2_hat_lg))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(lg2, X2_test, Y2_test,cmap='Oranges',normalize='true')

#3 year before bankruptcy i.e. 2019
from sklearn import linear_model
lg3 = linear_model

lg3 = linear_model.LogisticRegression(max_iter=1900)
lg3.fit(X3_train,Y3_train)

# Evaluating model on test data
Y3_hat_lg = lg3.predict(X3_test)

# checking for Recall, Precision and Fscore of Baseline model
p3,r3,f3,s3 = precision_recall_fscore_support(Y3_test,Y3_hat_lg, average="macro")

print(f"Precision - 3 year before bankruptcy: {p3}")
print(f"Recall - 3 year before bankruptcy: {r3}")
print(f"F-score - 3 year before bankruptcy: {f3}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y3_test,Y3_hat_lg))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(lg3, X3_test, Y3_test,cmap='Oranges',normalize='true')

#4 year before bankruptcy i.e. 2018
from sklearn import linear_model
lg4 = linear_model

lg4 = linear_model.LogisticRegression(max_iter=1900)
lg4.fit(X4_train,Y4_train)

# Evaluating model on test data
Y4_hat_lg = lg4.predict(X4_test)

# checking for Recall, Precision and Fscore of Baseline model
p4,r4,f4,s4 = precision_recall_fscore_support(Y4_test,Y4_hat_lg, average="macro")

print(f"Precision - 4 year before bankruptcy: {p4}")
print(f"Recall - 4 year before bankruptcy: {r4}")
print(f"F-score - 4 year before bankruptcy: {f4}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y4_test,Y4_hat_lg))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(lg4, X4_test, Y4_test,cmap='Oranges',normalize='true')

#5 year before bankruptcy i.e. 2017
from sklearn import linear_model
lg5 = linear_model

lg5 = linear_model.LogisticRegression(max_iter=1900)
lg5.fit(X5_train,Y5_train)

# Evaluating model on test data
Y5_hat_lg = lg5.predict(X5_test)

# checking for Recall, Precision and Fscore of Baseline model
p5,r5,f5,s5 = precision_recall_fscore_support(Y5_test,Y5_hat_lg, average="macro")

print(f"Precision - 5 year before bankruptcy: {p5}")
print(f"Recall - 5 year before bankruptcy: {r5}")
print(f"F-score - 5 year before bankruptcy: {f5}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y5_test,Y5_hat_lg))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(lg5, X5_test, Y5_test,cmap='Oranges',normalize='true')

"""# Random Forest"""

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
#1 year before bankruptcy i.e. 2021
RF1_model=ensemble.RandomForestClassifier(random_state=7)
param_grid1_RF = [{'n_estimators': [10,20,50,100],
               'max_depth': [1,2,5,10,15],
               'bootstrap': [True,False]},]
# Cross-validating for the Fscore for all Hyperparameters
rf_grid_search1 = GridSearchCV(RF1_model, param_grid1_RF , cv=10,
                              scoring='f1_macro',
                              return_train_score=True)
rf_grid_search1.fit(X1_train,Y1_train)
#Finding the best Hyperparameter settings for Random Forest
print(f"Best hyperparamter settings  = {rf_grid_search1.best_estimator_}")
Y1_hat_RF = rf_grid_search1.predict(X1_test)
p1,r1,f1,s1 = precision_recall_fscore_support(Y1_test,Y1_hat_RF, average="macro")
print(f"Precision - 1 year before bankruptcy: {p1}")
print(f"Recall - 1 year before bankruptcy: {r1}")
print(f"F-score - 1 year before bankruptcy: {f1}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y1_test,Y1_hat_RF))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(rf_grid_search1.best_estimator_, X1_test, Y1_test,cmap='Oranges',normalize='true')

#2 years before bankruptcy i.e. 2020
RF2_model=ensemble.RandomForestClassifier(random_state=7)
param_grid2_RF = [{'n_estimators': [10,20,50,100],
               'max_depth': [1,2,5,10,15],
               'bootstrap': [True,False]},]
# Cross-validating for the Fscore for all Hyperparameters
rf_grid_search2 = GridSearchCV(RF2_model, param_grid2_RF , cv=10,
                              scoring='f1_macro',
                              return_train_score=True)
rf_grid_search2.fit(X2_train,Y2_train)
#Finding the best Hyperparameter settings for Random Forest
print(f"Best hyperparamter settings  = {rf_grid_search2.best_estimator_}")
Y2_hat_RF = rf_grid_search2.predict(X2_test)
p2,r2,f2,s2 = precision_recall_fscore_support(Y2_test,Y2_hat_RF, average="macro")
print(f"Precision - 2 year before bankruptcy: {p2}")
print(f"Recall - 2 year before bankruptcy: {r2}")
print(f"F-score - 2 year before bankruptcy: {f2}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y2_test,Y2_hat_RF))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(rf_grid_search2.best_estimator_, X2_test, Y2_test,cmap='Oranges',normalize='true')

#3 years before bankruptcy i.e. 2019
RF3_model=ensemble.RandomForestClassifier(random_state=7)
param_grid3_RF = [{'n_estimators': [10,20,50,100],
               'max_depth': [1,2,5,10,15],
               'bootstrap': [True,False]},]
# Cross-validating for the Fscore for all Hyperparameters
rf_grid_search3 = GridSearchCV(RF3_model, param_grid3_RF , cv=10,
                              scoring='f1_macro',
                              return_train_score=True)
rf_grid_search3.fit(X3_train,Y3_train)
#Finding the best Hyperparameter settings for Random Forest
print(f"Best hyperparamter settings  = {rf_grid_search3.best_estimator_}")
Y3_hat_RF = rf_grid_search3.predict(X3_test)
p3,r3,f3,s3 = precision_recall_fscore_support(Y3_test,Y3_hat_RF, average="macro")
print(f"Precision - 3 year before bankruptcy: {p3}")
print(f"Recall - 3 year before bankruptcy: {r3}")
print(f"F-score - 3 year before bankruptcy: {f3}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y3_test,Y3_hat_RF))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(rf_grid_search3.best_estimator_, X3_test, Y3_test,cmap='Oranges',normalize='true')

#4 years before bankruptcy i.e. 2018
RF4_model=ensemble.RandomForestClassifier(random_state=7)
param_grid4_RF = [{'n_estimators': [10,20,50,100],
               'max_depth': [1,2,5,10,15],
               'bootstrap': [True,False]},]
# Cross-validating for the Fscore for all Hyperparameters
rf_grid_search4 = GridSearchCV(RF4_model, param_grid4_RF , cv=10,
                              scoring='f1_macro',
                              return_train_score=True)
rf_grid_search4.fit(X4_train,Y4_train)
#Finding the best Hyperparameter settings for Random Forest
print(f"Best hyperparamter settings  = {rf_grid_search4.best_estimator_}")
Y4_hat_RF = rf_grid_search4.predict(X4_test)
p4,r4,f4,s4 = precision_recall_fscore_support(Y4_test,Y4_hat_RF, average="macro")
print(f"Precision - 4 year before bankruptcy: {p4}")
print(f"Recall - 4 year before bankruptcy: {r4}")
print(f"F-score - 4 year before bankruptcy: {f4}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y4_test,Y4_hat_RF))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(rf_grid_search4.best_estimator_, X4_test, Y4_test,cmap='Oranges',normalize='true')

#5 years before bankruptcy i.e. 2017
RF5_model=ensemble.RandomForestClassifier(random_state=7)
param_grid5_RF = [{'n_estimators': [10,20,50,100],
               'max_depth': [1,2,5,10,15],
               'bootstrap': [True,False]},]
# Cross-validating for the Fscore for all Hyperparameters
rf_grid_search5 = GridSearchCV(RF5_model, param_grid5_RF , cv=10,
                              scoring='f1_macro',
                              return_train_score=True)
rf_grid_search5.fit(X5_train,Y5_train)
#Finding the best Hyperparameter settings for Random Forest
print(f"Best hyperparamter settings  = {rf_grid_search5.best_estimator_}")
Y_hat_RF5 = rf_grid_search5.predict(X5_test)
p5,r5,f5,s5 = precision_recall_fscore_support(Y5_test,Y_hat_RF5, average="macro")
print(f"Precision - 5 year before bankruptcy: {p5}")
print(f"Recall - 5 year before bankruptcy: {r5}")
print(f"F-score - 5 year before bankruptcy: {f5}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y5_test,Y_hat_RF5))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(rf_grid_search5.best_estimator_, X5_test, Y5_test,cmap='Oranges',normalize='true')

"""# k-NN Classifier"""

#1 year before bankruptcy i.e. 2021
pipeline1 = Pipeline([
        ('k_nn', KNeighborsClassifier())
    ])
param_grid1_knn = [{'k_nn__n_neighbors': [1,3,5,7,9,11,13,15,17],
                'k_nn__weights' : ['uniform','distance']}]
k_nn_grid_search1 = GridSearchCV(pipeline1, param_grid1_knn, cv=10,
                              scoring='f1_macro',
                              return_train_score=True,
                              verbose=1,n_jobs=-1)
k_nn_grid_search1.fit(X1_train,Y1_train)
#Finding the best Hyperparameter settings for k-NN
print(f"Best hyperparamter settings  = {k_nn_grid_search1.best_estimator_}")
Y1_hat_knn = k_nn_grid_search1.predict(X1_test)
p1,r1,f1,s1 = precision_recall_fscore_support(Y1_test,Y1_hat_knn, average="macro")
print(f"Precision - 1 year before bankruptcy: {p1}")
print(f"Recall - 1 year before bankruptcy: {r1}")
print(f"F-score - 1 year before bankruptcy: {f1}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y1_test,Y1_hat_knn))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(k_nn_grid_search1.best_estimator_, X1_test, Y1_test,cmap='Oranges',normalize='true')

#2 years before bankruptcy i.e. 2020
pipeline2 = Pipeline([
        ('k_nn', KNeighborsClassifier())
    ])
param_grid2_knn = [{'k_nn__n_neighbors': [1,3,5,7,9,11,13,15,17],
                'k_nn__weights' : ['uniform','distance']}]
k_nn_grid_search2 = GridSearchCV(pipeline2, param_grid2_knn, cv=10,
                              scoring='f1_macro',
                              return_train_score=True,
                              verbose=1,n_jobs=-1)
k_nn_grid_search2.fit(X2_train,Y2_train)
#Finding the best Hyperparameter settings for k-NN
print(f"Best hyperparamter settings  = {k_nn_grid_search2.best_estimator_}")
Y2_hat_knn = k_nn_grid_search2.predict(X2_test)
p2,r2,f2,s2 = precision_recall_fscore_support(Y2_test,Y2_hat_knn, average="macro")
print(f"Precision - 2 year before bankruptcy: {p2}")
print(f"Recall - 2 year before bankruptcy: {r2}")
print(f"F-score - 2 year before bankruptcy: {f2}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y2_test,Y2_hat_knn))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(k_nn_grid_search2.best_estimator_, X2_test, Y2_test,cmap='Oranges',normalize='true')

#3 year before bankruptcy i.e. 2019
pipeline3 = Pipeline([
        ('k_nn', KNeighborsClassifier())
    ])
param_grid3_knn = [{'k_nn__n_neighbors': [1,3,5,7,9,11,13,15,17],
                'k_nn__weights' : ['uniform','distance']}]
k_nn_grid_search3 = GridSearchCV(pipeline3, param_grid3_knn, cv=10,
                              scoring='f1_macro',
                              return_train_score=True,
                              verbose=1,n_jobs=-1)
k_nn_grid_search3.fit(X3_train,Y3_train)
#Finding the best Hyperparameter settings for k-NN
print(f"Best hyperparamter settings  = {k_nn_grid_search3.best_estimator_}")
Y3_hat_knn = k_nn_grid_search3.predict(X3_test)
p3,r3,f3,s3 = precision_recall_fscore_support(Y3_test,Y3_hat_knn, average="macro")
print(f"Precision - 3 year before bankruptcy: {p3}")
print(f"Recall - 3 year before bankruptcy: {r3}")
print(f"F-score - 3 year before bankruptcy: {f3}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y3_test,Y3_hat_knn))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(k_nn_grid_search3.best_estimator_, X3_test, Y3_test,cmap='Oranges',normalize='true')

#4 year before bankruptcy i.e. 2018
pipeline4 = Pipeline([
        ('k_nn', KNeighborsClassifier())
    ])
param_grid4_knn = [{'k_nn__n_neighbors': [1,3,5,7,9,11,13,15,17],
                'k_nn__weights' : ['uniform','distance']}]
k_nn_grid_search4 = GridSearchCV(pipeline4, param_grid4_knn, cv=10,
                              scoring='f1_macro',
                              return_train_score=True,
                              verbose=1,n_jobs=-1)
k_nn_grid_search4.fit(X4_train,Y4_train)
#Finding the best Hyperparameter settings for k-NN
print(f"Best hyperparamter settings  = {k_nn_grid_search4.best_estimator_}")
Y4_hat_knn = k_nn_grid_search4.predict(X4_test)
p4,r4,f4,s4 = precision_recall_fscore_support(Y4_test,Y4_hat_knn, average="macro")
print(f"Precision - 4 year before bankruptcy: {p4}")
print(f"Recall - 4 year before bankruptcy: {r4}")
print(f"F-score - 4 year before bankruptcy: {f4}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y4_test,Y4_hat_knn))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(k_nn_grid_search4.best_estimator_, X4_test, Y4_test,cmap='Oranges',normalize='true')

#5 year before bankruptcy i.e. 2017
pipeline5 = Pipeline([
        ('k_nn', KNeighborsClassifier())
    ])
param_grid5_knn = [{'k_nn__n_neighbors': [1,3,5,7,9,11,13,15,17],
                'k_nn__weights' : ['uniform','distance']}]
k_nn_grid_search5 = GridSearchCV(pipeline5, param_grid5_knn, cv=10,
                              scoring='f1_macro',
                              return_train_score=True,
                              verbose=1,n_jobs=-1)
k_nn_grid_search5.fit(X5_train,Y5_train)
#Finding the best Hyperparameter settings for k-NN
print(f"Best hyperparamter settings  = {k_nn_grid_search5.best_estimator_}")
Y5_hat_knn = k_nn_grid_search5.predict(X5_test)
p5,r5,f5,s5 = precision_recall_fscore_support(Y5_test,Y5_hat_knn, average="macro")
print(f"Precision - 5 year before bankruptcy: {p5}")
print(f"Recall - 5 year before bankruptcy: {r5}")
print(f"F-score - 5 year before bankruptcy: {f5}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y5_test,Y5_hat_knn))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(k_nn_grid_search5.best_estimator_, X5_test, Y5_test,cmap='Oranges',normalize='true')

"""# Linear SVM"""

#1 year before bankruptcy i.e. 2021
svm1=LinearSVC(random_state=7)

param_grid1_svc = {'C' : [0.1, 1, 10, 100],
                   'max_iter' : [10,50,100,1000,5000,10000]}

svm_grid_search1 = GridSearchCV(svm1, param_grid1_svc, cv=5,
                              scoring='f1_macro',
                              return_train_score=True)
svm_grid_search1.fit(X1_train,Y1_train)
#Finding the best Hyperparameter settings for SVM
print(f"Best hyperparamter settings  = {svm_grid_search1.best_estimator_}")
Y1_hat_svm = svm_grid_search1.predict(X1_test)
p1,r1,f1,s1 = precision_recall_fscore_support(Y1_test,Y1_hat_svm, average="macro")
print(f"Precision - 1 year before bankruptcy: {p1}")
print(f"Recall - 1 year before bankruptcy: {r1}")
print(f"F-score - 1 year before bankruptcy: {f1}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y1_test,Y1_hat_svm))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(svm_grid_search1.best_estimator_, X1_test, Y1_test,cmap='Oranges',normalize='true')

#2 year before bankruptcy i.e. 2020
svm2=LinearSVC(random_state=7)

param_grid2_svc = {'C' : [0.1, 1, 10, 100],
                   'max_iter' : [10,50,100,1000,5000,10000]}

svm_grid_search2 = GridSearchCV(svm2, param_grid2_svc, cv=5,
                              scoring='f1_macro',
                              return_train_score=True)
svm_grid_search2.fit(X2_train,Y2_train)
#Finding the best Hyperparameter settings for SVM
print(f"Best hyperparamter settings  = {svm_grid_search2.best_estimator_}")
Y2_hat_svm = svm_grid_search2.predict(X2_test)
p2,r2,f2,s2 = precision_recall_fscore_support(Y2_test,Y2_hat_svm, average="macro")
print(f"Precision - 2 year before bankruptcy: {p2}")
print(f"Recall - 2 year before bankruptcy: {r2}")
print(f"F-score - 2 year before bankruptcy: {f2}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y2_test,Y2_hat_svm))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(svm_grid_search2.best_estimator_, X2_test, Y2_test,cmap='Oranges',normalize='true')

#3 year before bankruptcy i.e. 2019
svm3=LinearSVC(random_state=7)

param_grid3_svc = {'C' : [0.1, 1, 10, 100],
                   'max_iter' : [10,50,100,1000,5000,10000]}

svm_grid_search3 = GridSearchCV(svm3, param_grid3_svc, cv=5,
                              scoring='f1_macro',
                              return_train_score=True)
svm_grid_search3.fit(X3_train,Y3_train)
#Finding the best Hyperparameter settings for SVM
print(f"Best hyperparamter settings  = {svm_grid_search3.best_estimator_}")
Y3_hat_svm = svm_grid_search3.predict(X3_test)
p3,r3,f3,s3 = precision_recall_fscore_support(Y3_test,Y3_hat_svm, average="macro")
print(f"Precision - 3 year before bankruptcy: {p3}")
print(f"Recall - 3 year before bankruptcy: {r3}")
print(f"F-score - 3 year before bankruptcy: {f3}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y3_test,Y3_hat_svm))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(svm_grid_search3.best_estimator_, X3_test, Y3_test,cmap='Oranges',normalize='true')

#4 year before bankruptcy i.e. 2018
svm4=LinearSVC(random_state=7)

param_grid4_svc = {'C' : [0.1, 1, 10, 100],
                   'max_iter' : [10,50,100,1000,5000,10000]}

svm_grid_search4 = GridSearchCV(svm4, param_grid4_svc, cv=5,
                              scoring='f1_macro',
                              return_train_score=True)
svm_grid_search4.fit(X4_train,Y4_train)
#Finding the best Hyperparameter settings for SVM
print(f"Best hyperparamter settings  = {svm_grid_search4.best_estimator_}")
Y4_hat_svm = svm_grid_search4.predict(X4_test)
p4,r4,f4,s4 = precision_recall_fscore_support(Y4_test,Y4_hat_svm, average="macro")
print(f"Precision - 4 year before bankruptcy: {p4}")
print(f"Recall - 4 year before bankruptcy: {r4}")
print(f"F-score - 4 year before bankruptcy: {f4}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y4_test,Y4_hat_svm))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(svm_grid_search4.best_estimator_, X4_test, Y4_test,cmap='Oranges',normalize='true')

#5 year before bankruptcy i.e. 2017
svm5=LinearSVC(random_state=7)

param_grid5_svc = {'C' : [0.1, 1, 10, 100],
                   'max_iter' : [10,50,100,1000,5000,10000]}

svm_grid_search5 = GridSearchCV(svm5, param_grid5_svc, cv=5,
                              scoring='f1_macro',
                              return_train_score=True)
svm_grid_search5.fit(X5_train,Y5_train)
#Finding the best Hyperparameter settings for SVM
print(f"Best hyperparamter settings  = {svm_grid_search5.best_estimator_}")
Y5_hat_svm = svm_grid_search5.predict(X5_test)
p5,r5,f5,s5 = precision_recall_fscore_support(Y5_test,Y5_hat_svm, average="macro")
print(f"Precision - 5 year before bankruptcy: {p5}")
print(f"Recall - 5 year before bankruptcy: {r5}")
print(f"F-score - 5 year before bankruptcy: {f5}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y5_test,Y5_hat_svm))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(svm_grid_search5.best_estimator_, X5_test, Y5_test,cmap='Oranges',normalize='true')

"""# Neural Network"""

from numpy import unique
import tensorflow as tf
from numpy import argmax
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# classification Multi-layer perceptron model
#1 year before bankruptcy i.e. 2021

# define the keras model
ann1 = Sequential()
ann1.add(Dense(20, activation='relu', kernel_initializer='he_normal'))
ann1.add(Dense(10, activation='relu', kernel_initializer='he_normal'))
ann1.add(Dense(1, activation='sigmoid'))

# compile the keras model
ann1.compile(loss='binary_crossentropy', optimizer='adam')

# fit the keras model on the dataset
ann1.fit(X1_train, Y1_train, epochs=200, batch_size=32, verbose=2)
# evaluate on test set
Y1hat_NN = ann1.predict(X1_test)
Y1hat_NN = argmax(Y1hat_NN, axis=-1).astype('int')

# checking for Recall, Precision and Fscore of
p1,r1,f1,s1 = precision_recall_fscore_support(Y1_test,Y1hat_NN,average="macro")

# Printing the results
print(f"Precision - 1 year before bankruptcy:{p1}")
print(f"Recall - 1 year before bankruptcy: {r1}")
print(f"F-score - 1 year before bankruptcy: {f1}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y1_test,Y1hat_NN))

#2 year before bankruptcy i.e. 2020

# define the keras model
ann2 = Sequential()
ann2.add(Dense(20, activation='relu', kernel_initializer='he_normal'))
ann2.add(Dense(10, activation='relu', kernel_initializer='he_normal'))
ann2.add(Dense(1, activation='sigmoid'))

# compile the keras model
ann2.compile(loss='binary_crossentropy', optimizer='adam')

# fit the keras model on the dataset
ann2.fit(X2_train, Y2_train, epochs=200, batch_size=32, verbose=2)
# evaluate on test set
Y2hat_NN = ann2.predict(X2_test)
Y2hat_NN = argmax(Y2hat_NN, axis=-1).astype('int')

# checking for Recall, Precision and Fscore of
p2,r2,f2,s2 = precision_recall_fscore_support(Y2_test,Y2hat_NN,average="macro")

# Printing the results
print(f"Precision - 2 year before bankruptcy:{p2}")
print(f"Recall - 2 year before bankruptcy: {r2}")
print(f"F-score - 2 year before bankruptcy: {f2}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y2_test,Y2hat_NN))

#3 year before bankruptcy i.e. 2019

# define the keras model
ann3 = Sequential()
ann3.add(Dense(20, activation='relu', kernel_initializer='he_normal'))
ann3.add(Dense(10, activation='relu', kernel_initializer='he_normal'))
ann3.add(Dense(1, activation='sigmoid'))

# compile the keras model
ann3.compile(loss='binary_crossentropy', optimizer='adam')

# fit the keras model on the dataset
ann3.fit(X3_train, Y3_train, epochs=200, batch_size=32, verbose=2)
# evaluate on test set
Y3hat_NN = ann3.predict(X3_test)
Y3hat_NN = argmax(Y3hat_NN, axis=-1).astype('int')
acc = accuracy_score(Y3_test, Y3hat_NN)

# checking for Recall, Precision and Fscore of
p3,r3,f3,s3 = precision_recall_fscore_support(Y3_test,Y3hat_NN,average="macro")

# Printing the results
print(f"Precision - 3 year before bankruptcy:{p3}")
print(f"Recall - 3 year before bankruptcy: {r3}")
print(f"F-score - 3 year before bankruptcy: {f3}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y3_test,Y3hat_NN))

# classification Multi-layer perceptron model
#4 year before bankruptcy i.e. 2018

# define the keras model
ann4 = Sequential()
ann4.add(Dense(20, activation='relu', kernel_initializer='he_normal'))
ann4.add(Dense(10, activation='relu', kernel_initializer='he_normal'))
ann4.add(Dense(1, activation='sigmoid'))

# compile the keras model
ann4.compile(loss='binary_crossentropy', optimizer='adam')

# fit the keras model on the dataset
ann4.fit(X4_train, Y4_train, epochs=200, batch_size=32, verbose=2)
# evaluate on test set
Y4hat_NN = ann4.predict(X4_test)
Y4hat_NN = argmax(Y4hat_NN, axis=-1).astype('int')
acc = accuracy_score(Y4_test, Y4hat_NN)

# checking for Recall, Precision and Fscore of
p4,r4,f4,s4 = precision_recall_fscore_support(Y4_test,Y4hat_NN,average="macro")

# Printing the results
print(f"Precision - 4 year before bankruptcy:{p4}")
print(f"Recall - 4 year before bankruptcy: {r4}")
print(f"F-score - 4 year before bankruptcy: {f4}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y4_test,Y4hat_NN))

#5 years before bankruptcy i.e. 2017

# define the keras model
model = Sequential()
model.add(Dense(20, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(10, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam')

# fit the keras model on the dataset
model.fit(X5_train, Y5_train, epochs=200, batch_size=32, verbose=2)
# evaluate on test set
Y5hat_NN = model.predict(X5_test)
Y5hat_NN = argmax(Y5hat_NN, axis=-1).astype('int')

# checking for Recall, Precision and Fscore of
p5,r5,f5,s5 = precision_recall_fscore_support(Y5_test,Y5hat_NN,average="macro")

# Printing the results
print(f"Precision - 5 year before bankruptcy:{p5}")
print(f"Recall - 5 year before bankruptcy: {r5}")
print(f"F-score - 5 year before bankruptcy: {f5}")
print("Overall classification Accuracy: ", metrics.accuracy_score(Y5_test,Y5hat_NN))