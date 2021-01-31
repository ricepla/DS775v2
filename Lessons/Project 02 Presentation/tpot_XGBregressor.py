import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=8675309)

# Average CV score on the training set was: 0.43616934248780376
exported_pipeline = XGBRegressor(learning_rate=0.05, max_depth=7, min_child_weight=17, n_estimators=100, nthread=1, objective="reg:squarederror", reg_alpha=5.0, reg_lambda=4.75, subsample=0.3)
# Fix random state in exported estimator
if hasattr(exported_pipeline, 'random_state'):
    setattr(exported_pipeline, 'random_state', 8675309)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
