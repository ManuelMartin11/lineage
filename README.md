![alt text](docs/logo.png)

>Track your Machine Learning experiments! But easy!

## <b>Usage</b>

It's really simple to use and **non-invasive** to your existing code.
```
# Set up experiment metadata
from lineage import Experiment
exp = Experiment(
    new_set=True,
    experiment_name="Random Forest for Text Classification",
    experiment_description="Use Random Forest Algorithm for Financial Text Classification",
    model_version="0.0.1",
    data_version="0.0.1"
)

# Train your model as ussually
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, Y = make_classification(4000, 20, n_classes=2)
DEPTH = 100
clf = RandomForestClassifier(depth=DEPTH)
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.33)
clf.fit(Xtrain, Ytrain)
Ypred = clf.predict(Xtest)
clf_report = classification_report(Ytest, Ypred)

# Register more lineage parameters
exp.hyperparameters = {"depth": DEPTH}
rln = exp.draft_release_note()
exp.register(model=clf, data=(X,Y), exploration="eda.ipynb", releasenotes=rln, results=clf_report)
```

Sample of a release note (`releasenotes.md`):

# Experiment Release Note
02/08/20 13:23

### Experiment Name
>Random Forest for Text Classification

### Experiment Description
>Use Random Forest Algorithm for Financial Text Classification

### Model Version
>0.0.1

### Code Commit
>938fe15be7528c41cf45a03e66dd7b246c85205b

### Code Branch
>develop

### Data Version
>0.0.1

### Hyperparameters
> depth = 100

<br></br>
<br></br>
After executing the code before, you will see a new `.lineage` directory with the following structure:
```
├── .lineage
│    ├── experiment_set_1
│    │    ├── experiment_1
│    │    │    ├── data
│    │    │    │   └── data.joblib
│    │    │    ├── exploration
│    │    │    │   └── notebook.ipynb
│    │    │    ├── model
│    │    │    │   └── model.joblib
│    │    │    ├── releasenotes
│    │    │    │   └── releasenotes.md
│    │    │    └── results
│    │    │        └── results.pickle
```

As you progress on your experiments or experiments sets you will have a registry like the following:

```
├── .lineage
│    ├── experiment_set_1
│    │    ├── experiment_1
│    │    ├── experiment_2
│    │    └──experiment_3
│    ├── experiment_set_2
│    │    ├── experiment_1
│    │    └──experiment_2
```

By using this formal structure, you will be able to compare experiments within sets and select the model that better fits your problem.