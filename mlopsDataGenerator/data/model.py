import pandas as pd
import os
from sklearn.datasets import fetch_openml
from typing import Mapping, Optional, List, Tuple, Any
from pydantic import BaseModel

class GeneratorParam(BaseModel):
    datetime: Optional[str] = '2021-09-09 09:09:09'
    count_per_label: Optional[int] = 50
    labels: Optional[List[str]] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

class GeneratorResponse(BaseModel):
    datetime: str
    count_per_label: int
    labels: List[str]
    shape: Tuple[int, int]


class Generator():

    def __init__(self, storage_path: str):
        df_x, df_y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=True)
        self.df: pd.DataFrame = df_x.join(df_y)
        self.storage_path: str = storage_path
    
    def _get_labeled_df(self, label: str, count: int, datetime_str: str) -> pd.DataFrame:
        labeled_df = self.df[self.df['class'] == label].sample(count) 
        labeled_df['datetime'] = datetime_str
        return labeled_df
    

    def generate(self, param = GeneratorParam) -> GeneratorResponse:
        datetime_str = param.datetime
        labels = param.labels
        count_per_label = param.count_per_label
        additional_df_list = [
            self._get_labeled_df(label, count_per_label, datetime_str)
            for label in labels
        ]
        csv_path = os.path.join(self.storage_path, 'data.csv')
        old_df = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame([])
        new_df = pd.concat([old_df, *additional_df_list], ignore_index=True)
        new_df.to_csv(csv_path, index = False)
        return GeneratorResponse(
            datetime = datetime_str,
            count_per_label = count_per_label,
            labels = labels,
            shape = new_df.shape
        )
