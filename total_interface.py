from processing_game_preferences_form import *
from processing_pre_experiment_state import *
from processing_post_experiment_state import *
from processing_engagement_emotions_markup import *

expected_column_size = {
    1: 8,
    2: 49,
    3: 33,
    4: 8
}

def is_correct_table_type(a, format):
    global df
    try:
        if format == '.xlsx':
            df = pd.read_excel('files/' + filename + format, engine='openpyxl')
        elif format == '.csv':
            df = pd.read_csv('files/' + filename + format, encoding='windows-1251')
    except Exception:
        print(f"[ОШИБКА] Ошибка формата файлов")
        return False
    if df.shape[1] != expected_column_size[a]:
        print("[ОШИБКА] Формат таблицы не соответствует статичному типу необработанной таблицы")
        return False
    return True

a = -1
while True:
    a = int(input("Выберите тип таблицы, которую следует обработать:\n" 
                  "1. pre_experiment_state.xlsx\n"
                  "2. post_experiment_state.xlsx\n" 
                  "3. game_preferences_form.xlsx\n" 
                  "4. engagement_emotions_markup.csv\n" 
                  "5. exit\n"
                  "Ответ: "))
    if a == 5:
        break
    filename = input("Введите название файла [без формата .csv / .xlsx]: ")

    if not(os.path.exists(f'files/{filename}.xlsx') or os.path.exists(f'files/{filename}.csv')):
        sys.exit('[ПРЕДУПРЕЖДЕНИЕ] Файла не существует, выход из программы...')

    match a:
        case 1:
            # pre_experiment_state_form_2
            path = f'json/pre_experiment/{filename}_columns.json'
            if not is_correct_table_type(a, '.xlsx'):
                continue
            df = pd.read_excel("files/" + filename + '.xlsx', engine='openpyxl')
            df = pre_processing_pre_experiment(df, filename, path)
            df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep=',')
            print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')
        case 2:
            # post_experiment_state_form_2
            path = f'json/post_experiment/{filename}_columns.json'
            if not is_correct_table_type(a, '.xlsx'):
                continue
            df = pd.read_excel("files/" + filename + '.xlsx', engine='openpyxl')
            df = pre_processing_post_experiment(df, filename, path)
            df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep=',')
            print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')
        case 3:
            # game_preferences_form_1
            path = f'json/game_preferences/{filename}_columns.json'
            if not is_correct_table_type(a, '.xlsx'):
                continue
            df = pd.read_excel("files/" + filename + '.xlsx', engine='openpyxl')
            df = pre_processing_game_preferences(df, filename, path)
            df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep=',')
            print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')
        case 4:
            # engagement_emotions_markup
            path = f'json/engagement_emotions_markup/{filename}_columns.json'
            if not is_correct_table_type(a, '.csv'):
                continue
            df = pd.read_csv('files/' + filename + '.csv', encoding='windows-1251')
            if df.columns[2] is None:
                continue
            df = pre_processing_engagement_emotions(df, filename, path)
            df.to_csv(f'processed_csv/{filename}.csv', index=False, encoding='utf-8-sig', sep = ',')
            print('[УСПЕШНО] Файл формата .csv был добавлен в директорию "processed_csv" в папке проекта')
        case _:
            print("Неизвестный выбор")
    print('')
