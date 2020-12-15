import aiohttp
import json


async def get(url, type='json'):
    """ api http get request """
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
