from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import sys
import os
sys.path.insert(0, "..")

from manager import LineageManager

lm = LineageManager()
lm.new_experiment()

X, Y = make_classification(400, 20, n_classes=2)

clf = RandomForestClassifier()
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.33)

clf.fit(Xtrain, Ytrain)
Ypred = clf.predict(Xtest)
clf_report = classification_report(Ytest, Ypred)

lm.register_experiment_factors(data=(X, Y),
                               exploration="notebook.ipynb",
                               model=clf,
                               results=clf_report,
                               releasenotes="##Version\nv0.0.1")
