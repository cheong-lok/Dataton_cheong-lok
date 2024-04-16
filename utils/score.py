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
    personal_weight = [0.2629,0.069,0.076,0.0462,0.076,0.0026,0.0198,0.0069,0.0263,0.1253,0.1253,0.1013,0.0177,0.0012,0.0435]
    external_weight = [0.25,0.0949,0.0316,0.0025,0.2426,0.0528,0.1368,0.014,0.0024,0.0583,0.0467,0.0352,0.0267,0.0049,0.0006]
    personal_weight_pca = [0.254,0.301,0.419,0.392,0.485,0.253,0.435,0.169,0.444,0.392,0.42,0.003,0.349,0.431,0.407]
    external_weight_pca = [0.261,0.293,0.308,0.288,0.329,0.332,0.36,0.117,0.075,0.107,0.25,0.137,0.307,0.315,0.123]
    df_1 = calc_score(personal,personal_weight)
    df_2 = calc_score(external,external_weight)
    df = pd.concat([df_1,df_2],axis=1)
    df.columns = ['개인건강 점수','외부환경요인 점수']
    df['총점'] = (df['개인건강 점수'] + df['외부환경요인 점수'])/2
    df['최종순위'] = df['총점'].rank()
    df = df.astype({'최종순위': 'int32'})
    df = df[['최종순위','총점','개인건강 점수','외부환경요인 점수']]
    df.to_csv('./지역별 건강순위 AHP')
    print(df)