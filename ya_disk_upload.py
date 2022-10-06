# https://github.com/netology-code/py-homeworks-basic/tree/master/9.http.requests - задание 2
# В папке со скриптом "ya_disk_upload.py" должен лежать файл "token.txt" с токеном для Яндекс Диска
# Если согласиться на перенос отправленный файлов, то скрипт заботливо сложит их в папку "Uploaded" рядом с собой
# Если во время переноса файл с таким именем в папке "Uploads" уже существует, то перемещаемый будет переименован
# Надеюсь, читать эту книгу будет интересно :)
import requests
import os


class YaUploader:
    def __init__(self):
        with open('token.txt', 'r') as opened_file:
            self.token = opened_file.read()

    def get_upload_link(self, file_path):
        headers = {'Authorization': f'OAuth {self.token}'}
        path = f'disk:/Загрузки/{os.path.basename(file_path)}'
        params = {'path': path}
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        req = requests.get(url=url, headers=headers, params=params)
        if req.status_code == 200:
            jsoned_req = req.json()
            upload_link = jsoned_req['href']
            return upload_link
        elif req.status_code == 409:
            print(f'Warning! File "{os.path.basename(file_path)}" already exists on YaDisk!')
            return None
        else:
            print('Error! Something goes wrong!')
            return None

    def rename_file(self, file_path, c=0, k=0):
        if c == 0:
            new_name = f'Uploaded/{os.path.basename(file_path)}'
        else:
            splitted_name = os.path.basename(file_path).split(".")
            splitted_name[-2] = f'{splitted_name[-2]}-{c}'
            new_name = f'Uploaded/{".".join(splitted_name)}'
        try:
            os.rename(file_path, os.path.join(os.path.dirname(file_path), new_name))
            print(f' and moved to "Uploaded\\" folder as "{new_name.split("/")[1]}"')
        except FileExistsError:
            c += 1
            self.rename_file(file_path, c, k+1)

    def upload_file(self, file_path, move):
        upload_link = self.get_upload_link(file_path)
        if upload_link is not None:
            headers = {'Authorization': f'OAuth {self.token}'}
            params = {'overwrite': 'false'}
            with open(file_path, mode='rb') as opened_file:
                req = requests.put(url=upload_link, headers=headers, params=params, data=opened_file.read())
            if req.status_code == 201:
                print('File uploaded successfully', end='')
                if move == 1:
                    try:
                        os.mkdir(os.path.join(os.path.dirname(file_path), 'Uploaded'))
                    except FileExistsError:
                        pass
                    self.rename_file(file_path)
                else:
                    print('.')
            else:
                print('Something goes wrong!')

    @staticmethod
    def get_file_list(path):
        file_list = []
        if os.path.isfile(path):
            return path
        else:
            folder_entry_list = os.listdir(path)
            for entry in folder_entry_list:
                folder_entry_path = os.path.join(path, entry)
                if os.path.isfile(folder_entry_path):
                    file_list.append(folder_entry_path)
            return file_list

    def uploader(self, path, move):
        param = self.get_file_list(path)
        if type(param) is list:
            for file in param:
                print(f'Uploading "{os.path.basename(file)}"')
                self.upload_file(file, move)
        else:
            print(f'Uploading "{os.path.basename(param)}"')
            self.upload_file(path, move)


def main():
    a = YaUploader()
    input_path = input('\nEnter path to a file or folder with files you want to upload to YaDisk (eg: "c:/hiberfil.sys"\n'
                       'or "c:/windows/") or leave path empty to use project folder "YaUpload":\n')
    if input_path == '':
        try:
            os.mkdir('YaUpload')
            print('Folder "YaUpload" was not found. But dont worry, we have created it! '
                  'Now put some files here and restart script.')
        except FileExistsError:
            pass
    path = f'{os.getcwd()}/YaUpload' if input_path == '' else input_path
    try:
        if os.listdir(path) in ['None', []]:
            print('Folder is empty!')
            return
    except FileNotFoundError:
        print('Error. File or folder not found!')
        return
    except NotADirectoryError:
        pass
    move = input('Move uploaded files to Uploaded folder? y/n\n')
    if move == 'y':
        a.uploader(path, 1)
    elif move == 'n':
        a.uploader(path, 0)
    else:
        print('Wrong command, aborting.')
        return


main()
