import pandas as pd
import numpy as np
df = pd.read_csv('jundata.csv')
def preprocessing(df):
    df['di_edi_code'] = df['di_edi_code'].astype(str)  # str이랑 섞여있는것들 str타입으로 변경 
    # ,구분자 처리 
    df['dl_name'] = df['dl_name'].str.replace(',', ' ') 
    df['dl_name_en'] = df['dl_name_en'].str.replace(',', ' ')
    df['print_front'] = df['print_front'].str.replace(',', ' ')
    df['dl_custom_shape'] = df['dl_custom_shape'].str.replace(',', '|')
    df['di_class_no'] = df['di_class_no'].str.replace(',', '|')
    df['di_edi_code'] = df['di_edi_code'].str.replace(',', '|')
    df['color_class1'] = df['color_class1'].str.replace(',', '|')
    df['form_code_name'] = df['form_code_name'].str.replace(',', '|')
    # .구분자 처리
    df['di_class_no'] = df['di_class_no'].str.replace('.', '|')
    df['dl_material'] = df['dl_material'].str.replace('.', '|')
    df['dl_material_en'] = df['dl_material_en'].str.replace('.', '|')
    df['dl_name'] = df['dl_name'].str.replace(',', '|')
    df['dl_name_en'] = df['dl_name_en'].str.replace(',', '|')
    # 공백처리 
    df['di_edi_code'] = df['di_edi_code'].astype(str).replace(r'\.0$', '', regex=True)
    df['leng_short'] = df['leng_short'].replace(r'\s', '', regex=True)
    df['leng_long'] = df['leng_long'].replace(r'\s', '', regex=True)
    df['thick'] = df['thick'].replace(r'\s', '', regex=True)
    # name 분리 
    df['dl_name_korean'] = df['dl_name'].str.extract(r'([가-힣]+)', expand=False)
    df['dl_name_nonkorean'] = df['dl_name'].str.extract(r'([^가-힣]+)', expand=False)
    # chart 삭제
    df.drop('chart',axis=1,inplace=True)
    df['dl_name_nonkorean'] = df['dl_name_nonkorean'].fillna('unknown')
    # df.to_csv('data_ho.csv')
    return df
preprocessing(df)