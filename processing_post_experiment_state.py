import json, os, os.path, sys
from common_func import *
from new_api import get_chat_answer_llama

promt_rows_opinion = "Твоя задача: сократи предложение до самой сути (2-4 предложения). Пиши только ответ, без дополнений. Предложение: "

def get_short_user_description(df, column):
    new_answers = {}
    for index, row in df.iterrows():
        text = str(row[column])
        request_message = promt_rows_opinion + text
        new_answers[text] = get_chat_answer_llama(request_message)
        df.at[index, column] = new_answers[text]
        print(f'[ПОЛУЧЕНО] Ответ: {new_answers[text]}')

    with open(f'json/post_experiment/{filename}_{column}.json', 'w', encoding='utf-8') as file:
        json.dump(new_answers, file, ensure_ascii=False, indent=4)
    return df

def pre_processing(df):
    delete_empty_columns(df)
    df.fillna('Нет информации', inplace=True)
    df = fix_data(df)
    for column in df.columns:
        df[column] = df[column].apply(approximate_assessment)
    if not os.path.exists(f'json/post_experiment/{filename}_columns.json') or os.path.getsize(f'json/post_experiment/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл {filename}_columns содержит данные. Загрузка столбцов...')
        with open(f'json/game_preferences/{filename}_columns.json', 'r', encoding='utf-8') as file:
            column_mapping = json.load(file)
            df.rename(columns=column_mapping, inplace=True)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')

    columns = df.iloc[:, 41:45].columns
    for i, column in enumerate(columns):
        if not os.path.exists(f'json/post_experiment/{filename}_{column}.json') or os.path.getsize(f'json/post_experiment/{filename}_{column}.json') == 0:
            df = get_short_user_description(df, column)
        else:
            with open(f'json/post_experiment/{filename}_{column}.json', 'r', encoding='utf-8') as file:
                content = json.load(file)
                if not content:
                    df = get_short_user_description(df, column)
                else:
                    print(f'[ИНФОРМАЦИЯ] JSON-файл {filename} содержит данные. Загрузка ячеек...')
                    for index, row in df.iterrows():
                        text = str(row[column])
                        if text in content:
                            df.at[index, column] = content[text]
                    print(f'[ГОТОВО] Ответ: ячейки с мнениями участников переименованы из {filename}')
    return df

print('Обработка файлов участников их состояния после эксперимента [post_experiment_state_form]\nВведите название файла (без формата):')
filename = input()

path = f'json/post_experiment/{filename}_columns.json'

if not os.path.exists(f'files/{filename}.xlsx'):
    sys.exit('[ПРЕДУПРЕЖДЕНИЕ] Файла не существует, выход из программы...')

df = pd.read_excel("files/" + filename + '.xlsx', engine='openpyxl')
df = pre_processing(df)

df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep = ',')

print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')

#post_experiment_state_form_2