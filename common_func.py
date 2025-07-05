import pandas as pd
import json
from new_api import get_chat_answer_llama

promt_columns = "Напиши в 1-3 словах на английском (пробелы нельзя только нижнее подчеркивание, с маленькой буквы) название для переменной программирования на основе текста (пиши только ответ). Предложение: "


def delete_empty_columns(df):
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

def to_make_columns(df, path):
    new_columns = {}
    for column in df.columns:
        new_column_name = get_chat_answer_llama(promt_columns + str(column))
        print(f'[ПОЛУЧЕНО] Ответ: {new_column_name} для столбца: {column}')
        new_columns[column] = new_column_name
    df.columns = [new_columns[col] for col in df.columns]
    with open(path, 'w', encoding='utf-8') as file:
       json.dump(new_columns, file, ensure_ascii=False, indent=4)
    return df

def fix_data(df):
    if 'Время создания' in df.columns:
        df['Время создания'] = pd.to_datetime(df['Время создания'], errors='coerce')
        df['Время создания'] = df['Время создания'].apply(date_processing)
    return df

def date_processing(date_obj):
    return date_obj.isoformat(sep='T', timespec='auto')

def approximate_assessment(assessment):
    if not isinstance(assessment, str):
        return assessment
    if assessment[0].isdigit() and assessment.count('-') == 1 and assessment[2] == '-':
        assessment = assessment.replace('-', ' ').split()[0]
    return assessment



