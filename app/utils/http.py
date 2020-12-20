import aiohttp
import json
import mimetypes


async def get(url, type='json'):
    headers = {'Accept': 'application/json'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as r:
                if r.status == 200:
                    if type == 'json':
                        return await r.json()
                    elif type == 'text':
                        txt = await r.read()
                        return json.loads(txt)
                    else:
                        print('[Api] invalid type')
                        return 'error'
                else:
                    print("[Api] error", r.status, url)
                    return 'error'
    except aiohttp.ClientConnectorError as e:
        print("[Api] canceled,", e)
        return 'error'


def fileIsType(url, types):
    filetype = mimetypes.guess_type(url)
    fileextension = mimetypes.guess_extension(filetype[0])
    if fileextension not in types:
        return fileextension


async def isOn(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    return True
                else:
                    return False
    except aiohttp.ClientConnectorError as e:
        return False
