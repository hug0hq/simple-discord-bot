import pickledb

DB_PATH = "./../save"

# class DB:

#   def __init__(self, connection, name):
#       self.db = connection[name]
#       self.logger = logging.getLogger(__name__)

# async def createDB(self, db):


async def save(key, value):
    d = pickledb.load(DB_PATH+'/test.json', False)      
    print(f'save {value}')
    d.set(key, value)
    d.dadd('soundboard', ("apple", "banana", "cherry") )
    print(d.dgetall('soundboard') )
    print(d.dget('soundboard', 'apple'))
    d.dump()

async def saveTo(dic, value):
    d = pickledb.load(DB_PATH+'/test.json', False)      
    print(f'save {value} in {dic}')
    d.dadd(dic, value )
    d.dump()

async def createDictionary(dic):
    d = pickledb.load(DB_PATH+'/test.json', False)
    d.dcreate(dic)
    d.dump()     

async def getFrom(dic, key):
    d = pickledb.load(DB_PATH+'/test.json', False)
    return d.dget(dic, key)

async def get(key):
    d = pickledb.load('test', False)
    return d.get(key)


async def getAll():
    d = pickledb.load('test', False)
    return d.getall()
