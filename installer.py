import os

print('Installing requirements')
os.system('pip install -r requirements.txt --break-system-packages')

from watchdict import WatchDict

wd = WatchDict('conf.json')
api_id = wd.get('api_id', None)
api_id = api_id if api_id else input('Api id: ')
api_hash = wd.get('api_hash', None)
api_hash = api_hash if api_hash else input('Api hash: ')
api_token = wd.get('api_token', None)
api_token = api_token if api_token else input('Api token: ')
wd['api_token'] = api_token
wd['api_id'] = api_id
wd['api_hash'] = api_hash

while True:
    admin = int(input('Do you wanna add any admin? Give me the UID in numbers [0 for cancel]: '))
    if not admin:
        break

    wd['admins'].append(admin)

print('Setup is complite. Use python app.py to start.')