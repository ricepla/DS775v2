import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.kernel_approximation import RBFSampler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.svm import LinearSVR
from tpot.builtins import StackingEstimator

# NOTE: Make sure that the class is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1).values
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'].values, random_state=8675309)

# Average CV score on the training set was:0.47300070588253096
exported_pipeline = make_pipeline(
    RBFSampler(gamma=0.4),
    StackingEstimator(estimator=LinearSVR(C=10.0, dual=True, epsilon=1.0, loss="squared_epsilon_insensitive", tol=0.0001)),
    ExtraTreesRegressor(bootstrap=False, max_features=0.9000000000000001, min_samples_leaf=12, min_samples_split=20, n_estimators=100)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
