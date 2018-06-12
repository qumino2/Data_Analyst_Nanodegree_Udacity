#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.grid_search import GridSearchCV



### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
# You will need to use more features

target_label = ['poi']
email_feature_list = [
    'from_messages',
    'from_poi_to_this_person',
    'from_this_person_to_poi',
    'shared_receipt_with_poi',
    'to_messages',
    ]

financial_features_list = [
    'salary',
    'deferral_payments',
    'total_payments',
    'loan_advances',
    'bonus',
    'restricted_stock_deferred',
    'deferred_income',
    'total_stock_value',
    'expenses',
    'exercised_stock_options',
    'other',
    'long_term_incentive',
    'restricted_stock',
    'director_fees',
    ]

features_list = target_label + financial_features_list + email_feature_list
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers
def remove_outlier(dict_object, keys):
    for key in keys:
        dict_object.pop(key, 0)

outliers = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
remove_outlier(data_dict, outliers)

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

### add new features to dataset
def computeFraction(poi_messages, all_messages):
    fraction = 0.
    if poi_messages == "NaN" or all_messages == "NaN":
        return fraction
    else:
        fraction = float(poi_messages)/all_messages
        return fraction

for name in my_dataset:
    data_point = my_dataset[name]
    from_poi_to_this_person = data_point["from_poi_to_this_person"]
    to_messages = data_point["to_messages"]
    fraction_from_poi = computeFraction(from_poi_to_this_person, to_messages)
    data_point["fraction_from_poi"] = fraction_from_poi

    from_this_person_to_poi = data_point["from_this_person_to_poi"]
    from_messages = data_point["from_messages"]
    fraction_to_poi = computeFraction(from_this_person_to_poi, from_messages)
    data_point["fraction_to_poi"] = fraction_to_poi

###update the features_list
my_feature_list = features_list + ['fraction_from_poi', 'fraction_to_poi']

###get K-best features
# num_features = 10
#
# def get_k_best(data_dict, features_list, k):
#     """ runs scikit-learn's SelectKBest feature selection
#         returns dict where keys=features, values=scores
#     """
#     data = featureFormat(data_dict, features_list)
#     labels, features = targetFeatureSplit(data)
#
#     k_best = SelectKBest(k=k)
#     k_best.fit(features, labels)
#     scores = k_best.scores_
#     unsorted_pairs = zip(features_list[1:], scores)
#     sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
#     k_best_features = dict(sorted_pairs[:k])
#     print "{0} best features: {1}\n".format(k, k_best_features.keys())
#     return k_best_features
#
#
# best_features = get_k_best(my_dataset, my_feature_list, num_features)
#
# my_feature_list = target_label + best_features.keys()
#
# ###print features
# print "{0} selected features: {1}\n".format(len(my_feature_list) - 1, my_feature_list[1:])

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, my_feature_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

print "Chosen features:", my_feature_list

# Scale features
scaler = MinMaxScaler()
features = scaler.fit_transform(features)


# K-best features
k_best = SelectKBest(k=5)
k_best.fit(features, labels)

k_best_results = zip(my_feature_list[1:], k_best.scores_)
k_best_results = sorted(k_best_results, key=lambda x: x[1], reverse=True)
print "K-best features:", k_best_results



### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
# from sklearn.naive_bayes import GaussianNB
# clf = GaussianNB()

from sklearn import tree
clf = tree.DecisionTreeClassifier(max_features=None, max_leaf_nodes=None,
        min_impurity_decrease=0.0, min_impurity_split=None,
        min_samples_leaf=1, min_samples_split=4,
        min_weight_fraction_leaf=0.0, presort=False, random_state=None,
        splitter='random')

# from sklearn.neighbors import KNeighborsClassifier
# clf = KNeighborsClassifier(algorithm='auto', leaf_size=5, metric='minkowski', \
#             metric_params=None, n_neighbors=10, p=3, weights='distance')


#tune the parameters for decision tress classifier
from sklearn import grid_search
parameters = {'min_samples_split': [2,4,6,8,10],
              'max_depth':[None, 2,4,6,8,10],
              'splitter': ('best', 'random')
             }
clf_optimize = grid_search.GridSearchCV(tree.DecisionTreeClassifier(), parameters).fit(features, labels)

print 'Best estimator:'
print clf_optimize.best_estimator_

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

test_classifier(clf, my_dataset, my_feature_list)

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.



dump_classifier_and_data(clf, my_dataset, features_list)
