# 기능별로 분리
# 데이터프레임에서 특정 
def count_commas(df,string): 
    count_dict = {}
    for column in df.columns:
        count = df[column].astype(str).str.count('string')
        count_dict[column] = count.sum()   # dict value값 -> 개수 
    return count_dict

# 특정 구분자값 변경
def replace_string(df, column, old_value, new_value):
    df[column] = df[column].str.replace(old_value, new_value)
    return df

# 한글 , 한글x 분리  
def separate_korean_nonkorean(df, column):
    df[column + '_korean'] = df[column].str.extract(r'([가-힣]+)', expand=False)
    df[column + '_nonkorean'] = df[column].str.extract(r'([^가-힣]+)', expand=False)

    
