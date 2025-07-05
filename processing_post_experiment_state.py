import json, os, os.path, sys
from common_func import *
from new_api import get_chat_answer_llama

promt_rows_opinion = "Твоя задача: сократи предложение до самой сути (2-4 предложения). Пиши только ответ, без дополнений. Предложение: "

def get_short_user_description(df):
    new_answers = {}
    for column in df.iloc[:, 41:45].columns:
        for index, row in df.iterrows():
            text = str(row[column])
            request_message = promt_rows_opinion + text
            new_answers[text] = get_chat_answer_llama(request_message)
            df.at[index, column] = new_answers[text]
            print(f'[ПОЛУЧЕНО] Ответ: {new_answers[text]}')
    with open(f'json/post_experiment/{filename}_opinon.json', 'w', encoding='utf-8') as file:
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
        with open(f'json/post_experiment/{filename}_columns.json', 'r', encoding='utf-8') as file:
            column_mapping = json.load(file)
            df.rename(columns=column_mapping, inplace=True)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')

    if not os.path.exists(f'json/post_experiment/{filename}_opinion.json') or os.path.getsize(f'json/post_experiment/{filename}_columns.json') == 0:
        get_short_user_description(df)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл {filename}_opinion содержит данные. Загрузка ячеек...')
        with open(f'json/post_experiment/{filename}_opinion.json', 'r', encoding='utf-8') as file:
            opinion_mapping = json.load(file)
            for column in df.iloc[:, 42:46].columns:
                for index, row in df.iterrows():
                    text = str(row[column])
                    df.at[index, column] = opinion_mapping[text]
            print(f'[ГОТОВО] Ответ: ячейки с мнениями участников переименованы из {filename}_opinion')
    return df

print('Обработка файлов участников их состояния после эксперимента [post_experiment_state_form]\nВведите название файла (без формата):')
filename = input()

path = f'json/post_experiment/{filename}_columns.json'

if not os.path.exists(f'files/{filename}.xlsx'):
    sys.exit('[ПРЕДУПРЕЖДЕНИЕ] Файла не существует, выход из программы...')

df = pd.read_excel("files/" + filename + '.xlsx', engine='openpyxl')
df = pre_processing(df)
for column in df.columns:
    print(column)
df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep = ',')

print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')

#post_experiment_state_form_2