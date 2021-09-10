from typing import Any, Mapping
import datetime
import json
import os
import pickle
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import check_random_state

date_format = '%Y-%m-%d %H:%M:%S'

def train(storage_path: str, min_datetime: str, max_datetime: str):
  csv_path = os.path.join(storage_path, 'data.csv')
  raw_df = pd.read_csv(csv_path)

  df = raw_df[(raw_df['datetime'] <= max_datetime) & (raw_df['datetime'] >= min_datetime)]

  data_count = df.shape[0]
  train_data_count = int(0.7 * data_count)
  test_data_count = int(0.3 * data_count)

  X = df.loc[:, 'pixel1':'pixel784'].to_numpy()
  y = df.loc[:, ['class']].to_numpy().ravel()

  random_state = check_random_state(0)
  permutation = random_state.permutation(X.shape[0])
  X = X[permutation]
  y = y[permutation]
  X = X.reshape((X.shape[0], -1))

  X_train, X_test, y_train, y_test = train_test_split(
      X, y, train_size=train_data_count, test_size=test_data_count)

  scaler = StandardScaler()
  X_train = scaler.fit_transform(X_train)
  X_test = scaler.transform(X_test)

  # Turn up tolerance for faster convergence
  clf = LogisticRegression(
      C=50. / train_data_count, penalty='l1', solver='saga', tol=0.1
  )
  clf.fit(X_train, y_train)
  sparsity = np.mean(clf.coef_ == 0) * 100
  score = clf.score(X_test, y_test)

  # print('Best C % .4f' % clf.C_)
  print("Sparsity with L1 penalty: %.2f%%" % sparsity)
  print("Test score with L1 penalty: %.4f" % score)

  # save model
  model_file_name = f'model-{datetime.datetime.now()}.pkl'
  model_path = os.path.join(storage_path, model_file_name)
  with open(model_path, 'wb') as model_file:
    pickle.dump(clf, model_file)
  os.chmod(model_path, 0o777)
  print("Save model to %s" % model_file_name)

  # read config
  config_path = os.path.join(storage_path, 'config.json')
  config: Mapping[str, Any] = {}
  if os.path.exists(config_path):
    with open(config_path, 'r') as config_file:
      try:
        config = json.load(config_file)
      except:
        print('Invalid JSON, proceed with default values')
  config.setdefault('sparsity', sparsity)
  config.setdefault('score', score)
  config.setdefault('model', model_file_name)
  config.setdefault('last_updated', datetime.datetime.now().strftime(date_format))

  # get old model
  old_model_path = os.path.join(storage_path, config['model'])
  with open(old_model_path, 'rb') as model_file:
    old_clf = pickle.load(model_file)

  # update config if new model is better than old model
  old_score = old_clf.score(X_test, y_test)
  if score >= old_score:
    config['model'] = model_file_name
    config['score'] = score
    config['last_updated'] = datetime.datetime.now().strftime(date_format)
    with open(config_path, 'w') as config_file:
      json.dump(config, config_file)
    os.chmod(config_path, 0o777)


if __name__ == '__main__':
  storage_path = os.path.abspath(os.getenv('MLOPS_MODEL_TRAINER_STORAGE', './storage'))
  min_datetime = os.getenv('MLOPS_MODEL_TRAINER_MIN_DATETIME', '2021-09-09 09:09:09')
  max_datetime = os.getenv('MLOPS_MODEL_TRAINER_MAX_DATETIME', '')
  if max_datetime == '':
    max_datetime = datetime.datetime.now().strftime(date_format)
  train(storage_path, min_datetime, max_datetime)