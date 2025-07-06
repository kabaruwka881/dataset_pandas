from common_func import *
import json, os

prompt_rows_opinion = "Сократи предложение до самой сути (1-3 предложения). Предложение - ответ на вопрос 'Расскажите об ощущениях.'. Отправь только готовый ответ, и больше ничего. Предложение: "

def pre_processing_engagement_emotions(df, filename, path):
    delete_empty_columns(df)
    df.astype(str).fillna('Нет информации')
    df = fix_data(df)
    column = df.columns[2]
    df[column] = df[column].str.capitalize()
    if not os.path.exists(f'json/engagement_emotions_markup/{filename}_columns.json') or os.path.getsize(f'json/engagement_emotions_markup/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл json/engagement_emotions_markup/{filename}_columns.json содержит данные. Загрузка столбцов...')
        with open(f'json/engagement_emotions_markup/{filename}_columns.json', 'r', encoding='utf-8') as file:
            column_mapping = json.load(file)
            df.rename(columns=column_mapping, inplace=True)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')
    return df