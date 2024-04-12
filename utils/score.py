import pandas as pd
import numpy as np

def calc_score(df,weight):
    df = df.mul(weight,axis=1)
    df = df.sum(axis=1)
    perfect_score = round((np.array(weight)*17).sum(),2)
    df = (df/perfect_score)*100
    return df

if __name__ == '__main__':
    personal = pd.read_csv('data\preprocessed\personal_health_middle_classification_rank.csv',index_col='시도')
    external = pd.read_csv('data\preprocessed\external_factor_middle_classification_rank.csv',index_col='시도')
    personal_weight = [0.2279,0.0597,0.0658,0.0402,0.0658,0.0022,0.0172,0.0059,0.0263,0.1253,0.1253,0.1013,0.0177,0.0012,0.0435]
    external_weight = [0.25,0.0949,0.0316,0.0025,0.2426,0.0528,0.1368,0.014,0.0024,0.0583,0.0467,0.0352,0.0267,0.0049,0.0006]
    print(calc_score(personal,personal_weight))