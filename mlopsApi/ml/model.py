from typing import Mapping, List, Any
import json
import os
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

class Model():

    def __init__(self, storage_path: str, model_file_name: str = ''):
        if model_file_name == '':
            config_path = os.path.join(storage_path, 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as config_file:
                    config: Mapping[str, Any] = json.load(config_file)
                    model_file_name = config.get('model')
        model_path = os.path.join(storage_path, model_file_name)
        with open(model_path, 'rb') as model_file:
            self.clf: LogisticRegression = pickle.load(model_file)
    

    def predict(self, X:List[List[float]]) -> List[int]:
        return self.clf.predict(X).tolist()
