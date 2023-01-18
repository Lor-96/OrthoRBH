def floatorint(string):
    if string.isdigit() == True :
        return int(string)
    elif string.isdigit() == False :
        return float(string)


def unique_file(file_name):
    import os
    name='output'
    if not os.path.exists(name):
        os.makedirs(name)
    
    file_name=f"{name}/{file_name}"

    filename, extension = os.path.splitext(file_name)
    i = 1

    while os.path.exists(file_name):
        file_name = filename + " (" + str(i) + ")" + extension
        i += 1

    return file_name
        








