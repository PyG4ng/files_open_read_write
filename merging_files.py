from pathlib import Path


CUR_DIR = Path(__file__).resolve().parent
DATA_FOLDER = CUR_DIR / 'sorted'
FILES = [f for f in DATA_FOLDER.iterdir()]

def get_file_data(files_path : list) -> list:
    """Get the name, lenth and content of .txt files

    Args:
        files_path (list): list of path to the files

    Returns:
        list: list of dictionnaries
    """
    file_content_dict=[]
    for elem in files_path:
        file_ = {}
        with open(elem, 'r', encoding='utf-8-sig') as f:
            content = f.read().splitlines()
        file_['name'] = elem.name
        file_['lenth'] = len(content)
        file_['content'] = content
        file_content_dict.append(file_)
    return file_content_dict


def sort_file_content_by_lenth(files_path : list) -> list:
    """Sort a list of files content by lenth (number of line inside the file)

    Args:
        files_path (list): list of path to the files

    Returns:
        list: Sorted list of dictionnaries by lenth value
    """
    sorted_file_content=[]
    file_content_dict = get_file_data(files_path)
    while file_content_dict:
        lenn = float('inf')
        for i in range(len(file_content_dict)):
            if float(file_content_dict[i].get('lenth')) < lenn:
                lenn = file_content_dict[i].get('lenth')
                k = i
        sorted_file_content.append(file_content_dict[k])
        file_content_dict.remove(file_content_dict[k])
    return sorted_file_content


def create_merged_file(data_folder ,files_path : list, merged_file_name : str):
    """Create a .txt file

    Args:
        data_folder (pathlib.WindowsPath) : path to the folder containig the merged file
        files_path (list): list of path to the files to merge
        merged_file_name (str): wanted name of the created file
    """
    sorted_list = sort_file_content_by_lenth(files_path)
    with open(f'{data_folder}/{merged_file_name}.txt', 'w', encoding='utf-8-sig') as f:
        for i in range(len(sorted_list)):
            f.write(sorted_list[i]['name'] + '\n')
            f.write(str(sorted_list[i]['lenth']) + '\n')
            for j in range(len(sorted_list[i]['content'])):
                n = '' if i == len(sorted_list)-1 and j == len(sorted_list[i]['content'])-1 else '\n'
                f.write(sorted_list[i]['content'][j] + n)

create_merged_file(DATA_FOLDER,FILES,'merged_files')


