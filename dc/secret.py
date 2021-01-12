import os

def secret_file(in_production=False,filename='shadow.dc.txt',secret_dir='atejas'):
    if in_production==False:
        # dev
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    else:
        # prodaction
        base = os.path.join('/','home','darkcreator')
    return os.path.join(base,secret_dir,filename)

def psql(in_production,db='psql'):
    # psql params from secret file
    # db = psql or mysql
    file = secret_file(in_production)
    with open(file,'r') as f:
        for row in f:
            if (row!='\n') and ('#' not in row[0:2]):
                # psql db name:user:password:host:port, none mean by default as ''
                ar = row.strip().split(':')
                r = {}
                # print(ar)
                if db in ar[0]:
                    r['name'] = ar[1]
                    r['user'] = ar[2]
                    r['password'] = ar[3]
                    r['host'] = ar[4]
                    r['port'] = ar[5] if ar[5]!='none' else ''
                    return r
        return False

def dsk(in_production):
    # django secret key from secret file
    file = secret_file(in_production)
    with open(file,'r') as f:
        for row in f:
            if (row!='\n') and ('#' not in row[0:2]):
                # dsk:secret_key
                ar = row.strip().split(':')
                # r = {}
                # print(ar)
                if 'dsk' in ar[0]:
                    return ar[1]
        return False

def get_vk_token(in_production):
    # django secret key from secret file
    file = secret_file(in_production)
    with open(file,'r') as f:
        for row in f:
            if (row!='\n') and ('#' not in row[0:2]):
                # vk:token
                ar = row.strip().split(':')
                if 'vk' == ar[0]:
                    return ar[1]
        return False

# print(vk_token(True))
# print(get_vk_token(False))
# print(psql(False,'mysql'))
