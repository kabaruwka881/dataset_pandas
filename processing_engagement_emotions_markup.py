from common_func import *
from os import path
import json, sys, os

promt_rows_opinion = "Сократи предложение до самой сути (1-3 предложения). Предложение - ответ на вопрос 'Расскажите об ощущениях.'. Отправь только готовый ответ, и больше ничего. Предложение: "

def pre_processing(df):
    delete_empty_columns(df)
    df = fix_data(df)
    column = df.columns[2]
    df[column] = df[column].str.capitalize()
    if not os.path.exists(f'json/engagement_emotions_markup/{filename}_columns.json') or os.path.getsize(f'json/engagement_emotions_markup/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл {filename}_columns содержит данные. Загрузка столбцов...')
        with open(f'json/engagement_emotions_markup/{filename}_columns.json', 'r', encoding='utf-8') as file:
            column_mapping = json.load(file)
            df.rename(columns=column_mapping, inplace=True)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')
    return df


print('Обработка файлов участников их игрового опыта для эксперимента [game_preferences_form]\nВведите название файла (без формата):')
filename = input()

path = f'json/engagement_emotions_markup/{filename}_columns.json'

if not os.path.exists(f'files/{filename}.csv'):
    sys.exit('[ПРЕДУПРЕЖДЕНИЕ] Файла не существует, выход из программы...')

df = pd.read_csv("files/" + filename + '.csv', encoding='windows-1251')
df = pre_processing(df)
df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep = ',')

print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')

#engagement_emotions_markup