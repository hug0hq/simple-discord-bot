import pickledb
import os

PATH = os.environ['SAVE_PATH']


def delKey(guild, dic, key):
    """ delete one key on a dictionary """
    pk = pickledb.load(f'{PATH}/{guild}.json', True)
    if pk.dexists(dic, key):
        pk.dpop(dic, key)


def delAll(guild, dic):
    """ delete all the keys on a dictionary """
    pk = pickledb.load(f'{PATH}/{guild}.json', True)
    if pk.exists(dic):
        pk.drem(dic)


def nuke(guild):
    """ delete db """
    pk = pickledb.load(f'{PATH}/{guild}.json', True)
    pk.deldb()


def saveTo(guild, dic, value):
    pk = pickledb.load(f'{PATH}/{guild}.json', True)
    if not pk.exists(dic):
        pk.dcreate(dic)

    print(f'save {value} in {dic}')
    pk.dadd(dic, value)


def getFrom(guild, dic, key):
    pk = pickledb.load(f'{PATH}/{guild}.json', False)
    return pk.dget(dic, key)
