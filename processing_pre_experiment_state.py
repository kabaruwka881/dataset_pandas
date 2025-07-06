from common_func import *
import json, sys, os

def pre_processing_pre_experiment(df, filename, path):
    delete_empty_columns(df)
    df = fix_data(df)
    if not os.path.exists(f'json/pre_experiment/{filename}_columns.json') or os.path.getsize(f'json/pre_experiment/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл json/pre_experiment/{filename}_columns.json содержит данные. Загрузка столбцов...')
        with open(f'json/pre_experiment/{filename}_columns.json', 'r', encoding='utf-8') as file:
            column_mapping = json.load(file)
            df.rename(columns=column_mapping, inplace=True)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')

    if not os.path.exists(f'json/pre_experiment/{filename}_opinion.json') or os.path.getsize(f'json/pre_experiment/{filename}_columns.json') == 0:
        get_short_user_description(df, filename)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл json/pre_experiment/{filename}_opinion.json содержит данные. Загрузка ячеек...')
        with open(f'json/pre_experiment/{filename}_opinion.json', 'r', encoding='utf-8') as file:
            column = df.columns[2]
            opinion_mapping = json.load(file)
            for index, row in df.iterrows():
                text = str(row[column])
                df.at[index, column] = opinion_mapping[text]
            print(f'[ГОТОВО] Ответ: ячейки с мнениями участников переименованы из {filename}_opinion')
    return df

def get_short_user_description(df, filename):
    column = df.columns[2]
    new_answers = {}
    prompt = get_prompt('pre_experiment')[0]
    for index, row in df.iterrows():
        text = str(row[column])
        ans = get_chat_answer_llama(prompt + text)
        new_answers[text] = ans
        print(f'[ПОЛУЧЕНО] Ответ: {new_answers[text]}')
        df.at[index, column] = ans
    with open(f'json/pre_experiment/{filename}_opinion.json', 'w') as file:
        json.dump(new_answers, file, ensure_ascii=False, indent=4)
    return df