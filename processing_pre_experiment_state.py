from common_func import *
from os import path
import json, sys, os

promt_rows_opinion = "Сократи предложение до самой сути (1-3 предложения). Предложение - ответ на вопрос 'Расскажите об ощущениях.'. Отправь только готовый ответ, и больше ничего. Предложение: "

def pre_processing(df):
    delete_empty_columns(df)
    df = fix_data(df)
    if not os.path.exists(f'json/pre_experiment/{filename}_columns.json') or os.path.getsize(f'json/pre_experiment/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл {filename}_columns содержит данные. Загрузка столбцов...')
        with open(f'json/pre_experiment/{filename}_columns.json', 'r', encoding='utf-8') as file:
            column_mapping = json.load(file)
            df.rename(columns=column_mapping, inplace=True)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')

    if not os.path.exists(f'json/pre_experiment/{filename}_opinion.json') or os.path.getsize(f'json/pre_experiment/{filename}_columns.json') == 0:
        get_short_user_description(df)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл {filename}_opinion содержит данные. Загрузка ячеек...')
        with open(f'json/pre_experiment/{filename}_opinion.json', 'r', encoding='utf-8') as file:
            column = df.columns[2]
            opinion_mapping = json.load(file)
            for index, row in df.iterrows():
                text = str(row[column])
                df.at[index, column] = opinion_mapping[text]
            print(f'[ГОТОВО] Ответ: ячейки с мнениями участников переименованы из {filename}_opinion')
    return df

def get_short_user_description(df):
    column = df.columns[2]
    new_answers = {}
    for index, row in df.iterrows():
        text = str(row[column])
        ans = get_chat_answer_llama(promt_rows_opinion + text)
        new_answers[text] = ans
        print(f'[ПОЛУЧЕНО] Ответ: {new_answers[text]}')
        df.at[index, column] = ans
    with open(f'json/pre_experiment/{filename}_opinion.json', 'w') as file:
        json.dump(new_answers, file, ensure_ascii=False, indent=4)
    return df

print('Обработка файлов участников их игрового опыта для эксперимента [game_preferences_form]\nВведите название файла (без формата):')
filename = input()

path = f'json/pre_experiment/{filename}_columns.json'

if not os.path.exists(f'files/{filename}.xlsx'):
    sys.exit('[ПРЕДУПРЕЖДЕНИЕ] Файла не существует, выход из программы...')

df = pd.read_excel("files/" + filename + '.xlsx', engine='openpyxl')
df = pre_processing(df)

df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep = ',')

print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')

#pre_experiment_state_form_2