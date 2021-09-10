import pandas as pd
from sklearn.datasets import fetch_openml

df_x, df_y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=True)

df = df_x.join(df_y)

df_1 = df[df['class'] == '1'].sample(1000)
df_2 = df[df['class'] == '2'].sample(1000)

df_12 = pd.concat([df_1, df_2], ignore_index=True)

print(df_1.shape, df_2.shape, df_12.shape)

df_12.to_csv('all.csv', index = False)
df = pd.read_csv('all.csv')
print(df.shape)