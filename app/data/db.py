import pickledb
import os

PATH = os.environ['SAVE_PATH']


def delKey(guild, dic, key):
    """ delete one key/value on a dictionary """
    pk = pickledb.load(f'{PATH}/{guild}.json', True)
    if pk.dexists(dic, key):
        pk.dpop(dic, key)


def delAll(guild, dic):
    """ delete all the keys/values on a dictionary """
    pk = pickledb.load(f'{PATH}/{guild}.json', True)
    if pk.exists(dic):
        pk.drem(dic)


def nuke(guild):
    """ delete db """
    pk = pickledb.load(f'{PATH}/{guild}.json', True)
    pk.deldb()


def saveTo(guild, dic, key, value):
    """ save a key/value on a dictionary """
    pk = pickledb.load(f'{PATH}/{guild}.json', True)
    if not pk.exists(dic):
        pk.dcreate(dic)
    if pk.dexists(dic, key):
        return 'exists'

    pk.dadd(dic, (key, value))


def getFrom(guild, dic, key):
    """ get a values from a dictionary """
    pk = pickledb.load(f'{PATH}/{guild}.json', False)
    return pk.dget(dic, key)


def listKeysFrom(guild, dic):
    """ get all the keys/values on a dictionary """
    pk = pickledb.load(f'{PATH}/{guild}.json', False)
    return pk.dkeys(dic)
