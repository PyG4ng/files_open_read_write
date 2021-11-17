from pathlib import Path

CUR_DIR = Path(__file__).resolve().parent
DATA_FOLDER = CUR_DIR / 'sorted_files'
FILES = [file for file in DATA_FOLDER.iterdir() if file.is_file() and file.suffix == '.txt']


def get_files_data_sorted_by_number_of_lines(files_path: list) -> list:
    """
    Gets a list of paths to .txt files and returns a list of dictionaries with the name, the number of lines (length)
    and the content of .txt files

    Args:
        files_path (list): list of paths to .txt files

    Returns: A list of dictionaries

    """
    list_of_file_parameters = []
    for file in files_path:
        file_parameters = {}
        with open(file, 'r', encoding='utf-8-sig') as f:
            content = f.read().splitlines()
        file_parameters['name'] = file.name
        file_parameters['length'] = len(content)
        file_parameters['content'] = content
        list_of_file_parameters.append(file_parameters)
    return sorted(list_of_file_parameters, key=lambda file_param: file_param["length"])


def create_merged_file(merged_file_folder, files_path: list, merged_file_name: str):
    """Gets a list of paths to .txt files, merged them and creates a new .txt  file

    Args:
        merged_file_folder (path) : path to the folder to contain the merged file
        files_path (list): list of paths to the .txt files to merge
        merged_file_name (str): given name to the new file
    """

    list_of_file_param = get_files_data_sorted_by_number_of_lines(files_path)
    merged_file_folder.mkdir(exist_ok=True)
    with open(f'{merged_file_folder}/{merged_file_name}.txt', 'w', encoding='utf-8-sig') as new_file:
        for i in range(len(list_of_file_param)):
            new_file.write(list_of_file_param[i]['name'] + '\n')
            new_file.write(str(list_of_file_param[i]['length']) + '\n')
            for j in range(len(list_of_file_param[i]['content'])):
                # To avoid adding an empty line at the end of the file
                n = '' if i == len(list_of_file_param) - 1 and j == len(list_of_file_param[i]['content']) - 1 else '\n'
                new_file.write(list_of_file_param[i]['content'][j] + n)


create_merged_file(CUR_DIR / 'merged_file', FILES, 'merged_files')
