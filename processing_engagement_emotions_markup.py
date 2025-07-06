from common_func import *
import json, os

def pre_processing_engagement_emotions(df, filename, path):
    delete_empty_columns(df)
    df = df.fillna('Нет информации')
    column = df.columns[2]
    df[column] = df[column].str.capitalize()
    if not os.path.exists(f'json/engagement_emotions_markup/{filename}_columns.json') or os.path.getsize(f'json/engagement_emotions_markup/{filename}_columns.json') == 0:
        to_make_columns(df, path)
    else:
        print(f'[ИНФОРМАЦИЯ] JSON-файл json/engagement_emotions_markup/{filename}_columns.json содержит данные. Загрузка столбцов...')
        with open(f'json/engagement_emotions_markup/{filename}_columns.json', 'r', encoding='utf-8') as file:
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
                with open(f'json/engagement_emotions_markup/{filename}_columns.json', 'w', encoding='utf-8') as file:
                    json.dump(content, file, ensure_ascii=False, indent=4)
            print(f'[ГОТОВО] Столбцы переименованы из {filename}_columns')
    return df