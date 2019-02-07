# -*- coding: utf-8 -*-
from aiohttp import web
from argparse import ArgumentParser
from os import listdir, getcwd, path, stat, remove, makedirs
import random
import aiofiles

routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
    '''
    index page перенаправление на /notes
    '''
    raise web.HTTPFound('/notes')


@routes.post('/notes')
async def create_new_file(request):
    '''
    функция создает новый файл с контентом из запроса

    '''
    def file_name_gen():
        '''генерирует рандомное имя файла'''
        return ''.join(
            random.choice(u'qwertyuiopasdfghjklzxcvbnm') for i in range(random.randint(5, 10)))
    data = await request.json()
    folder_name = request.app['settings'].folder
    file_name = file_name_gen()
    with open('{}/{}.txt'.format(folder_name, file_name), 'w', encoding='utf-8') as f:
        f.write(data['content'])
    return web.json_response({'note id': file_name})


@routes.get('/notes')
async def get_files_information(request):
    '''
    функция возвращает информацию по всем файлам в директории: мета и контент
    :return
        JSON 
        {
            'info files': [
                {file name: file info}
            ]
        }
    '''
    files_names = listdir(request.app['settings'].folder)
    response = {'info files': [await _info(file_name, request)
                               for file_name in files_names]}
    return web.json_response(response)


@routes.get('/notes/{filename}')
async def get_file_information(request):
    '''
    функция возвращает информацию по одному файлу
    :args 
        имя файла
    :return
        Json
        {
            'file name': file data
        }
    '''
    file_name = request.match_info['filename'] + '.txt'
    response = await _info(file_name, request)
    return web.json_response(response)


@routes.delete('/notes/{filename}')
async def delete_file(request):
    '''
    функция удаляет файл из директории
    :args 
        имя файла
    :return
        200 в случае успеха и 
        Json
            {'status': deleted}
        404 в случае, если файл не существует
    '''
    file_name = request.match_info['filename'] + '.txt'
    try:
        path_to_file = '{}/{}'.format(
            request.app['settings'].folder, file_name)
        remove(path_to_file)
        return web.json_response({'status': 'deleted'})
    except FileNotFoundError as e:
        raise web.HTTPNotFound(content_type='application/json')


async def _info(file_name, request):
    '''
    Функция возвращает метаданные и содержимое файла в директории по его имени
    :args
        имя файла
        реквест
    :return
        dict
            {
                имя файла: мета информация и контент файла
            }
        или
        Json 404 файл не найден
    '''
    path_to_file = '{}/{}'.format(request.app['settings'].folder, file_name)
    try:
        meta_values = list(stat(path_to_file))  # метаданные
        meta_keys = ['mode', 'ino', 'dev', 'nlink', 'uid',
                     'gid', 'size', 'atime', 'mtime', 'ctime']
        # Формирование словаря из метаданных
        file_meta = dict(zip(meta_keys, meta_values))
        async with aiofiles.open(path_to_file, mode='r', encoding='utf-8') as f:
            file_meta['content'] = await f.read()
        data = {file_name: file_meta}
        return data
    except FileNotFoundError as e:
        raise web.HTTPNotFound(content_type='application/json')


def server_init(args):
    '''
    фабрика приложений
    :args 
        аргументы коммандной строки
    :return
        aiohttp application
    '''
    app = web.Application()
    if not path.exists(args.folder):
        makedirs(args.folder)
    app["settings"] = args
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    pass
