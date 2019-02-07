import pytest
from aiohttp import web
from serverRt.server import server_init
from argparse import Namespace
import json
import os, shutil

FOLDER_NAME = './test_folder'

@pytest.fixture
def cli(loop, aiohttp_client):
    args = Namespace()
    args.port = 5005
    args.folder = FOLDER_NAME
    app = server_init(args)
    return loop.run_until_complete(aiohttp_client(app))


async def test_hello(cli):
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.json(content_type='application/json') == {'info files': []}


async def test_create_file(cli):
    data = {'content': 'pytest'}
    resp = await cli.post('/notes', data=json.dumps(data))
    assert resp.status == 200
    filename = os.listdir(FOLDER_NAME)
    filename = filename[0].split('.')[0]
    assert await resp.json(content_type='application/json') == {'note id': filename}


async def test_get_notes(cli):
    resp = await cli.get('/')
    assert resp.status == 200
    check = await resp.json(content_type='application/json')
    print(check['info files'])
    filename = os.listdir(FOLDER_NAME)[0]
    assert True == any(filename in namesDict for namesDict in check['info files'])
    assert True == any(contentDict['content'] == 'pytest' for contentDict in check['info files'][0].values())
    assert True == ('pytest' in check['info files'][0][filename].values())

async def test_delete_notes(cli):
    filename = os.listdir(FOLDER_NAME)
    url = '/{}/{}'.format('notes', filename[0].split('.')[0]) 
    resp = await cli.delete(url)
    assert resp.status == 200
    assert await resp.json(content_type='application/json') == {'status': 'deleted'}
    shutil.rmtree(FOLDER_NAME)