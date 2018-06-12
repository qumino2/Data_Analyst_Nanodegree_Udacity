# Project Report - Identify Fraud from Enron Email 

##### 1. Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?

The goal of this porject is build machine learning algorithm to identify Enron Employees who may have committed fraud based on Enron financial and email dataset which is open to public. By using machine learning techniques, we can extract and identify useful features, build algorithms to identify person of interest in Enron company. We can also use some metrics, e.g., accuracy, time to evaluate the performance of the algorithms we use. 



There are 146 data points in the Enron dataset in total and there are 21 features available for each person (1 labeled feature, 14 financial features, 6 email features). There are 35 POIs in total and 18 POIs in the dataset. 



However, the dataset is not complete with quite a portion of values missing in each feature, as shown in the table below.

| Feature                   | the numbe of NaN |
| ------------------------- | ---------------- |
| Loan advances             | 142              |
| Director fees             | 129              |
| Restricted stock deferred | 128              |
| Deferred payment          | 107              |
| Deferred income           | 97               |
| Long term incentive       | 80               |
| Bonus                     | 64               |
| Emails sent also to POI   | 60               |
| Emails sent               | 60               |
| Emails received           | 60               |
| Emails from POI           | 60               |
| Emails to POI             | 60               |
| Other                     | 53               |
| Expenses                  | 51               |
| Salary                    | 51               |
| Excersised stock option   | 44               |
| Restricted stock          | 36               |
| Email address             | 35               |
| Total payment             | 21               |
| Total stock value         | 20               |

From the exploratory data analysis, 3 entries need to be removed:

+ `TOTAl`: Obviously, this is an outlier for summing up each financial data.
+ `THE TRAVEL AGENCY IN THE PARK`: This entry does represent an individual person's information.
+ `LOCKHART EUGENE E`: This entry contained only NaN data.



##### 2. What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it.

We have an intuition that persons of interest might have stronger email connection between each other than the general population, therefore new features `ratio_from_poi` and`ratio_to_poi` (messages from/to the POI divided by to/from messages from the person) were added. 

I have used SelectKBest to conduct the feature selection, the selected top 5 best (k=5) features are as shown below:

**K-best features: [('exercised_stock_options', 24.815079733218194), ('total_stock_value', 24.182898678566872), ('bonus', 20.792252047181538), ('salary', 18.289684043404513), ('fraction_to_poi', 16.40971254803579)]**

Scaling has been done by using MinMax scaling, since the unit and range of the features are different.

##### 3. What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  

Three classifiers have been tested, namely, GaussianNB, Decision Tree, and K Nearest Neighbors. Please see the results below:

**KNeighborsClassifier:**

    Accuracy: 0.86380	Precision: 0.23457	Recall: 0.00950	F1: 0.01826	F2: 0.01176
    Total predictions: 15000	True positives:   19	False positives:   62	False negatives: 1981	True negatives: 12938
**DecisionTreeClassifier:**

    Accuracy: 0.82287	Precision: 0.31740	Recall: 0.28550	F1: 0.30061	F2: 0.29136
    Total predictions: 15000	True positives:  571	False positives: 1228	False negatives: 1429	True negatives: 11772
**GaussianNB(priors=None):**

	Accuracy: 0.73900	Precision: 0.22604	Recall: 0.39500	F1: 0.28753	F2: 0.34363
	Total predictions: 15000	True positives:  790	False positives: 2705	False negatives: 1210	True negatives: 10295


By comparing the results, we found DecisionTreeClassifier performed better across a set of different metrics, like accuracy, precision, and recall. Therefore, we decided to use DecisionTreeClassifier to identify the POI.



##### 4. What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? What parameters did you tune? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier). 

Tuning an algorithm is a process in which one optimize the parameters that impact the model in order to enable the algorithm to perform the best. If you don't do this well, you might not be able to release the real power of the model and the results can be biased. 

There are quite a few parameters in DecisionTreeClassifier need to be tuned. GridsearchCV in sklearn is used to choose the parameters to maximize the cross-validation score, which will evaluate different combination of algorithm parameters specified in a grid.

Parameters to be tuned in Decision tress classifier:

```python
parameters = {'min_samples_split': [2,4,6,8,10],
              'max_depth':[None, 2,4,6,8,10],
              'splitter': ('best', 'random')
             }
```

The results of optimized parameters:

```python
        max_features=None, max_leaf_nodes=None,
        min_impurity_decrease=0.0, min_impurity_split=None,
        min_samples_leaf=1, min_samples_split=4,
        min_weight_fraction_leaf=0.0, presort=False, random_state=None,
        splitter='random')
```


##### 5. What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis? 

Validation consists of a set of techniques to make sure our model based on training dataset can generalize with the test dataset as well. A classic mistake is over-fitting, which your model perform very well in the training dataset but has significantly lower performance in the test dataset. Due to the size of the dataset is quite small, we use stratified shuffle split validation which provided by Udacity in tester.py file.

##### 6. Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. 



**Recall:** the number of True Positives divided by the number of True Positives and the number of False Negatives, which tells us the ratio of all the real POIs the model can predict.

**Precision:** the number of True Positives divided by the number of True Positives and False Positives, which tells us the ratio of all predicted POIs are truely POIs.

| DecisionTreeClassifier | Precision | Recall  |
| ---------------------- | --------- | ------- |
|                        | 0.31740   | 0.28550 |





##### References:

https://stackoverflow.com/questions/22903267/what-is-tuning-in-machine-learning

http://scikit-learn.org/stable/tutorial/statistical_inference/model_selection.html

https://github.com/lyvinhhung/Udacity-Data-Analyst-Nanodegree/tree/master/p5%20-%20Identify%20Fraud%20from%20Enron%20Email

