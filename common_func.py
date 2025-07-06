import pandas as pd
import json
from new_api import get_chat_answer_llama

def get_prompt(field):
    with open('ai_access/promts.json', 'r', encoding='utf-8') as file:
        prompts = json.load(file)
    return prompts[field]['prompts']

def delete_empty_columns(df):
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

def to_make_columns(df, path):
    new_columns = {}
    prompt = get_prompt('common_functions')[0]
    for column in df.columns:
        new_column_name = get_chat_answer_llama(prompt + str(column))
        print(f'[ПОЛУЧЕНО] Ответ: {new_column_name} для столбца: {column}')
        new_columns[column] = new_column_name
    df.columns = [new_columns[col] for col in df.columns]
    with open(path, 'w', encoding='utf-8') as file:
       json.dump(new_columns, file, ensure_ascii=False, indent=4)
    return df

def fix_data(df):
    column = df.columns[1]
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df[column] = df[column].apply(date_processing)
    return df

def date_processing(date_obj):
    return date_obj.isoformat(sep='T', timespec='auto')

def approximate_assessment(assessment):
    if not isinstance(assessment, str):
        return assessment
    if assessment[0].isdigit() and assessment.count('-') == 1 and assessment[2] == '-':
        assessment = assessment.replace('-', ' ').split()[0]
    return assessment

