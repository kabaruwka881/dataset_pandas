import numpy as np

from common_func import *
import json, sys, os

def pre_processing_game_preferences(df, filename, path):
    df = df.astype(str).fillna('Нет информации')
    df = fix_data(df)
    df = fix_gender(df)
    for column in df.columns:
        df[column] = df[column].apply(approximate_assessment)
    if not os.path.exists(f'json/game_preferences/{filename}_columns.json') or os.path.getsize(f'json/game_preferences/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл {filename}_columns содержит данные. Загрузка столбцов...')
        with open(f'json/game_preferences/{filename}_columns.json', 'r', encoding='utf-8') as file:
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
                with open(f'json/game_preferences/{filename}_columns.json', 'w', encoding='utf-8') as file:
                    json.dump(content, file, ensure_ascii=False, indent=4)
        print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')

    columns = df.iloc[:, 3:9].columns
    prompts = get_prompt('game_preferences')
    for i, column in enumerate(columns):
        is_renamed = False
        if not os.path.exists(f'json/game_preferences/{filename}_{column}.json') or os.path.getsize(f'json/game_preferences/{filename}_{column}.json') == 0:
            dirlist = os.listdir("json/game_preferences")
            for f in dirlist:
                if f.startswith(filename):
                    j = json.load(open(f'json/game_preferences/{f}', 'r', encoding='utf-8-sig'))
                    if df[column].iloc[0] in j:
                        os.rename(f'json/game_preferences/{f}', f'json/game_preferences/{filename}_{column}.json')
                        is_renamed = True
            if not is_renamed:
                df = get_short_user_experience_hours(df, column, prompts[i], filename)
        else:
            with open(f'json/game_preferences/{filename}_{column}.json', 'r', encoding='utf-8') as file:
                content = json.load(file)
                if not content:
                    df = get_short_user_experience_hours(df, column, prompts[i], filename)
                else:
                    print(f'[ИНФОРМАЦИЯ] JSON-файл {f'json/game_preferences/{filename}_{column}.json'} содержит данные. Загрузка ячеек...')
                    for index, row in df.iterrows():
                        text = str(row[column])
                        if text in content:
                            df.at[index, column] = content[text]
                        else:
                            deleted_answer = get_chat_answer_llama(prompts[i] + text)
                            content[text] = deleted_answer
                            df.at[index, column] = deleted_answer
                            print(f'[ИНФОРМАЦИЯ] Ответ на ячейку из таблицы был удален. Новый ответ: {deleted_answer}')
                    with open(f'json/game_preferences/{filename}_{column}.json', 'w', encoding='utf-8') as file:
                        json.dump(content, file, ensure_ascii=False, indent=4)
                    print(f'[ГОТОВО] Ответ: ячейки с игровым опытом участников переименованы из {f'json/game_preferences/{filename}_{column}.json'}')
    return df

def get_short_user_experience_hours(df, column, prompt, filename):
    new_answers = {}
    for index, row in df.iterrows():
        text = str(row[column])
        new_answers[text] = get_chat_answer_llama(prompt + text)
        print(f'[ПОЛУЧЕНО] Ответ: {new_answers[text]}')
        df.at[index, column] = new_answers[text]
    with open(f'json/game_preferences/{filename}_{column}.json', 'w', encoding='utf-8') as file:
        json.dump(new_answers, file, ensure_ascii=False, indent=4)
    return df
