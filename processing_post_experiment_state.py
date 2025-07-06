import os, os.path, sys
from common_func import *
from new_api import get_chat_answer_llama


def get_short_user_description(df, column, filename):
    new_answers = {}
    prompt = get_prompt('post_experiment')[0]
    for index, row in df.iterrows():
        text = str(row[column])
        request_message = prompt + text
        new_answers[text] = get_chat_answer_llama(request_message)
        df.at[index, column] = new_answers[text]
        print(f'[ПОЛУЧЕНО] Ответ: {new_answers[text]}')

    with open(f'json/post_experiment/{filename}_{column}.json', 'w', encoding='utf-8') as file:
        json.dump(new_answers, file, ensure_ascii=False, indent=4)
    return df

def pre_processing_post_experiment(df, filename, path):
    delete_empty_columns(df)
    df.astype(str).fillna('Нет информации')
    df = fix_data(df)
    for column in df.columns:
        df[column] = df[column].apply(approximate_assessment)
    if not os.path.exists(f'json/post_experiment/{filename}_columns.json') or os.path.getsize(f'json/post_experiment/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл json/post_experiment/{filename}_columns.json содержит данные. Загрузка столбцов...')
        with open(f'json/post_experiment/{filename}_columns.json', 'r', encoding='utf-8') as file:
            column_mapping = json.load(file)
            df.rename(columns=column_mapping, inplace=True)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')

    columns = df.iloc[:, 41:45].columns
    for i, column in enumerate(columns):
        if not os.path.exists(f'json/post_experiment/{filename}_{column}.json') or os.path.getsize(f'json/post_experiment/{filename}_{column}.json') == 0:
            df = get_short_user_description(df, column, filename)
        else:
            with open(f'json/post_experiment/{filename}_{column}.json', 'r', encoding='utf-8') as file:
                content = json.load(file)
                if not content:
                    df = get_short_user_description(df, column, filename)
                else:
                    print(f'[ИНФОРМАЦИЯ] JSON-файл json/post_experiment/{filename}_{column}.json содержит данные. Загрузка ячеек...')
                    for index, row in df.iterrows():
                        text = str(row[column])
                        if text in content:
                            df.at[index, column] = content[text]
                    print(f'[ГОТОВО] Ответ: ячейки с мнениями участников переименованы из {filename}')
    return df


