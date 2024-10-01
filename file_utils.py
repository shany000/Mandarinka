import os
import winshell
import subprocess

project_root = os.path.dirname(os.path.abspath(__file__))

applications_folder = os.path.join(project_root, 'applications')

if not os.path.exists(applications_folder):
    os.makedirs(applications_folder)


def add_shortcuts(keys, file_path):
    for key in keys:
        shortcut_path = os.path.join(applications_folder, f"{key}.lnk")
        with winshell.shortcut(shortcut_path) as link:
            link.path = file_path
            link.description = f"Ярлык для {file_path}"


def open_file_by_key(key):
    shortcut_path = os.path.join(applications_folder, f"{key}.lnk")
    if os.path.exists(shortcut_path):
        try:
            subprocess.run(['cmd', '/c', shortcut_path], check=True)
        except Exception as e:
            return f"Ошибка при открытии файла через ярлык: {e}"
    else:
        return f"Ярлык для ключа '{key}' не найден."

def search_files(root_dir, query):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            try:
                if query.lower() in file.lower():
                    print(f"Найден файл: {os.path.join(dirpath, file)}")
            except PermissionError:
                print(f"Нет доступа к: {dirpath}")
            except Exception as e:
                print(f"Ошибка: {e}")
