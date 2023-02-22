import os
from frameworks.fastapi.utils import SETTINGS, INIT_ROUTER, README, ENV, MAIN_UTIL

class FastApiFramework:
    def __init__(self):
        self.path = 'api'
        self.folders = ['server', 'repositories', 'routers', 'config', 'schemas']
        self.is_exists = os.path.exists(self.path)

    def create_fastapi_architecture(self, db):
        if db == 'mongodb':
            from frameworks.fastapi.dbs.templates_mongo import  MAIN, ROUTER, SCHEMA, DATABASE, REPOSITORY, REQUIREMENTS
        elif db in ['mysql', 'postgresql']:
            from frameworks.fastapi.dbs.templates_relational import MAIN, ROUTER, SCHEMA, DATABASE, REPOSITORY, MODELS, REQUIREMENTS
            self.folders.append('models')
        else:
            self.handle_the_code('main.py', MAIN_UTIL)
            return True
                           
        self.__create_three_directories()
        
        paths = [('main.py', MAIN),
                 ('__init__.py', ''),
                 ('requirements.txt', REQUIREMENTS),
                 ('README.md', README),
                 ('.env', ENV),
                 (f'{self.path}/server/database.py', DATABASE),
                 (f'{self.path}/config/settings.py', SETTINGS),
                 (f'{self.path}/routers/user.py', ROUTER),
                 (f'{self.path}/routers/__init__.py', INIT_ROUTER),
                 (f'{self.path}/schemas/user.py', SCHEMA),
                 (f'{self.path}/repositories/user.py', REPOSITORY)]
        
        if db != 'mongodb':
            paths.append((f'{self.path}/models/user.py', MODELS))
            
        for path in paths:
            self.handle_the_code(path[0], path[1])

    def handle_the_code(self, path, code):
        with open(path, 'w') as f:
            f.write(code)

    def __create_three_directories(self):
        if not self.is_exists:
            os.makedirs(self.path)
            with open(f'{self.path}/__init__.py', 'w'): pass
            for folder in self.folders:
                os.mkdir(os.path.join(self.path, folder))
                with open(f'{self.path}/{folder}/__init__.py', 'w'): pass