
def clean_directory_list(directorys):
    clean_directorys = []
    for dir in directorys:
        if dir[0] == '.':
            pass
        elif dir[0] == '_':
            pass
        else:
            clean_directorys.append(dir)

    return clean_directorys

def get_index_of_value_in_list(ls, value):
    for count, item in enumerate(ls):
        if item == value:
            return count

    return 0

