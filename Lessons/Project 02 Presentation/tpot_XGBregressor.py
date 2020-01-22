import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from xgboost import XGBRegressor

# NOTE: Make sure that the class is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1).values
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'].values, random_state=8675309)

# Average CV score on the training set was:0.4261794002742591
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=XGBRegressor(learning_rate=0.01, max_depth=7, min_child_weight=8, n_estimators=100, nthread=1, objective="reg:squarederror", reg_alpha=4, reg_lambda=2, subsample=0.15000000000000002)),
    XGBRegressor(learning_rate=0.1, max_depth=1, min_child_weight=5, n_estimators=100, nthread=1, objective="reg:squarederror", reg_alpha=2, reg_lambda=2, subsample=0.15000000000000002)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
