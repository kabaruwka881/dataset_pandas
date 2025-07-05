from common_func import *
from os import path
import json, sys, os

promt_total_hours = "Напиши сколько человек отыгрывает часов в играх в неделю. Начинай ответ с: 'Я играю'. Не используй местоимения. Если не играет - напиши об этом. Если не играет сейчас, но играл: напиши сколько играл. Отправь только готовый ответ, и больше ничего. Предложение:"
promt_sort_games_and_hours = "Преобразуй ответ в нумерованный список игр формата: <Название игры на английском с заглавной буквы>: <количество часов> 'ч.'. Если количество часов не указано, напиши: неизвестно. Дай только ответ в указанном формате, без пояснений. Предложение:"
promt_rows_opinion_1 = "Сократи предложение до самой сути (1-3 предложения). Предложение - ответ на вопрос 'Почему вас так затянула эта игра?'. Отправь только готовый ответ, и больше ничего. Предложение: "
promt_top_games = "Пронумеруй список из игр (строго по пунктам 1. 2. и так далее). Нельзя писать названия игр, которых нет в списке. Если игры повторяются, то пиши 1 название. Если есть небольшие отличия, то пиши 2 названия. Название игр написать на английском. Отправь только готовый ответ, и больше ничего. Предложение:"
promt_rows_opinion_2 = "Cократи предложение до самой сути (1-3 предложения). Предложение - ответ на вопрос 'За что вы полюбили эти игры?'.Отправь только готовый ответ, и больше ничего. Предложение: "
promt_top_games_style = "Пронумеруй жанры в том порядке, в котором они указаны в предложении. Не добавляй новых жанров и не пиши один и тот же список дважды. Жанры пиши с больной буквы, если они начаты с маленькой (на том же языке). Если исходное предложение верное, то ничего не меняй. Формат строго: каждый пункт с новой строки (забудь про знак ->), например: 1. RPG\\n2. Shooter\\n3. Roguelike. Дай только список с исправленными жанрами, без пояснений. Предложение:"

promts = [promt_total_hours, promt_sort_games_and_hours, promt_rows_opinion_1, promt_top_games, promt_rows_opinion_2, promt_top_games_style]

def pre_processing(df):
    df.fillna('Нет информации', inplace=True)
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
    for i, column in enumerate(columns):
        if not os.path.exists(f'json/game_preferences/{filename}_{column}.json') or os.path.getsize(f'json/game_preferences/{filename}_{column}.json') == 0:
            df = get_short_user_experience_hours(df, column, promts[i])
        else:
            with open(f'json/game_preferences/{filename}_{column}.json', 'r', encoding='utf-8') as file:
                content = json.load(file)
                if not content:
                    df = get_short_user_experience_hours(df, column, promts[i])
                else:
                    print(f'[ИНФОРМАЦИЯ] JSON-файл {f'json/game_preferences/{filename}_{column}.json'} содержит данные. Загрузка ячеек...')
                    for index, row in df.iterrows():
                        text = str(row[column])
                        if text in content:
                            df.at[index, column] = content[text]
                    print(f'[ГОТОВО] Ответ: ячейки с игровым опытом участников переименованы из {f'json/game_preferences/{filename}_{column}.json'}')
    return df

def get_short_user_experience_hours(df, column, promt):
    new_answers = {}
    for index, row in df.iterrows():
        text = str(row[column])
        new_answers[text] = get_chat_answer_llama(text + promt)
        print(f'[ПОЛУЧЕНО] Ответ: {new_answers[text]}')
        df.at[index, column] = new_answers[text]
    with open(f'json/game_preferences/{filename}_{column}.json', 'w', encoding='utf-8') as file:
        json.dump(new_answers, file, ensure_ascii=False, indent=4)
    return df

print('Обработка файлов участников их игрового опыта для эксперимента [game_preferences_form]\nВведите название файла (без формата):')
filename = input()

path = f'json/game_preferences/{filename}_columns.json'

if not os.path.exists(f'files/{filename}.xlsx'):
    sys.exit('[ПРЕДУПРЕЖДЕНИЕ] Файла не существует, выход из программы...')

df = pd.read_excel("files/" + filename + '.xlsx', engine='openpyxl')
df = pre_processing(df)

df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep = ',')

print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')

# game_preferences_form_1