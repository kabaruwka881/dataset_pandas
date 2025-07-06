from common_func import *
import json, sys, os

def pre_processing_game_preferences(df, filename, path):
    df = df.astype(str).fillna('Нет информации')
    df = fix_data(df)
    for column in df.columns:
        df[column] = df[column].apply(approximate_assessment)
    if not os.path.exists(f'json/game_preferences/{filename}_columns.json') or os.path.getsize(f'json/game_preferences/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл {filename}_columns содержит данные. Загрузка столбцов...')
        with open(f'json/game_preferences/{filename}_columns.json', 'r', encoding='utf-8') as file:
            column_mapping = json.load(file)
            df.rename(columns=column_mapping, inplace=True)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')

    columns = df.iloc[:, 3:9].columns
    prompts = get_prompt('game_preferences')
    for i, column in enumerate(columns):
        if not os.path.exists(f'json/game_preferences/{filename}_{column}.json') or os.path.getsize(f'json/game_preferences/{filename}_{column}.json') == 0:
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
                    print(f'[ГОТОВО] Ответ: ячейки с игровым опытом участников переименованы из {f'json/game_preferences/{filename}_{column}.json'}')
    return df

def get_short_user_experience_hours(df, column, prompt, filename):
    new_answers = {}
    for index, row in df.iterrows():
        text = str(row[column])
        new_answers[text] = get_chat_answer_llama(text + prompt)
        print(f'[ПОЛУЧЕНО] Ответ: {new_answers[text]}')
        df.at[index, column] = new_answers[text]
    with open(f'json/game_preferences/{filename}_{column}.json', 'w', encoding='utf-8') as file:
        json.dump(new_answers, file, ensure_ascii=False, indent=4)
    return df
