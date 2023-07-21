import pandas as pd

##### Data frame 호출 #####
def df_open():
    df = pd.read_csv('./data/df_json.csv', encoding = 'UTF-8')  # csv파일 경로는 각자 환경에 따라 맞춰주면 됨
    return df

df_json = df_open()


##### 열 삭제 #####
def col_delete():
    df_json.drop(['Unnamed: 0', 'id', 'size', 'drug_S', 'width', 'height', 'mark_code_front', 'mark_code_back', 'line_front',
                  'line_back', 'mark_code_front_anal', 'mark_code_back_anal', 'mark_code_front_img', 'mark_code_back_img',
                  'color_class2', 'file_name', 'dl_company_en', 'di_company_mf', 'di_company_mf_en', 'img_regist_ts',
                  'change_date', 'back_color', 'light_color', 'camera_la', 'camera_lo', 'print_back'],
                  axis = 1, inplace = True)
    return df_json

df_json = col_delete()


##### fillna #####
# 0으로 채우기
def fill_zero():
    df_json['leng_long'].fillna(0, inplace = True)
    df_json['leng_short'].fillna(0, inplace = True)
    df_json['thick'].fillna(0, inplace = True)
    return df_json

df_json = fill_zero()

# unknown으로 채우기
def fill_unknown():
    df_json.fillna('unknown', inplace = True)
    return df_json

df_json = fill_unknown()
# print(df_json.isna().sum())  # checking


##### csv로 저장하기 #####
# df_json.to_csv('./data/df_na_processing.csv', encoding = 'UTF-8', index = False)