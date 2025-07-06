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
            content = json.load(file)
            old_columns = set(df.columns)
            df.rename(columns=content, inplace=True)
            new_columns = set(df.columns)
            unchanged_columns = new_columns & old_columns
            if unchanged_columns:
                for col in unchanged_columns:
                    prompt = get_prompt('common_functions')[0]
                    deleted_column = get_chat_answer_llama(prompt + str(col))
                    print(f'[ИНФОРМАЦИЯ] Ответ на колонку из таблицы был удален. Новый ответ: {deleted_column} для {col}')
                    content[col] = deleted_column
                df.rename(columns=content, inplace=True)
                with open(f'json/pre_experiment/{filename}_columns.json', 'w', encoding='utf-8') as file:
                    json.dump(content, file, ensure_ascii=False, indent=4)
        print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')

    if not os.path.exists(f'json/pre_experiment/{filename}_opinion.json') or os.path.getsize(f'json/pre_experiment/{filename}_columns.json') == 0:
        get_short_user_description(df, filename)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл json/pre_experiment/{filename}_opinion.json содержит данные. Загрузка ячеек...')
        with open(f'json/pre_experiment/{filename}_opinion.json', 'r', encoding='utf-8') as file:
            column = df.columns[2]
            content = json.load(file)
            for index, row in df.iterrows():
                text = str(row[column])
                if text in content:
                    df.at[index, column] = content[text]
                else:
                    prompt = get_prompt('pre_experiment')[0]
                    deleted_answer = get_chat_answer_llama(prompt + text)
                    content[text] = deleted_answer
                    df.at[index, column] = deleted_answer
                    print(f'[ИНФОРМАЦИЯ] Ответ на ячейку из таблицы был удален. Новый ответ: {deleted_answer}')
            with open(f'json/pre_experiment/{filename}_opinion.json', 'w', encoding='utf-8') as file:
                json.dump(content, file, ensure_ascii=False, indent=4)
            print(f'[ГОТОВО] Ответ: ячейки с мнениями участников переименованы из {filename}_opinion.json')
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