#!/usr/bin/env python

from flask import Flask
from flask_restful import Api, Resource

class APIResource(Resource):

    _ROOT = '/'
    _REGISTER = {}

    @classmethod
    def register_root(cls, api, root=''):
        api.add_resource(cls, root + cls._ROOT)

        cls._register(api, root)

    @classmethod
    def _register(cls, api, root):
        root = root + cls._ROOT
        for path, res in cls._REGISTER.items():
            res_path = '{}{}'.format(root, path)
            api.add_resource(res, res_path)
            res._register(api, root)

class APILvl1Lvl2(APIResource):

    def get(self):
        return {'path': '/lvl1/lvl2'}

class APILvl1(APIResource):

    class APILvl1SID(APIResource):

        def get(self, sid):
            return {'sid': sid}

    _ROOT = 'lvl1/'
    _REGISTER = {
            '<int:sid>': APILvl1SID,
            'lvl2/': APILvl1Lvl2
        }

    def get(self):
        return {'path': '/lvl1'}

class APIRoot(APIResource):

    _ROOT = '/'
    _REGISTER = {
            'lvl1/': APILvl1,
        }

    def get(self):
        return {'path': self._ROOT}

def main():
    app = Flask(__name__)
    api = Api(app)
    # localhost:5000/
    APIRoot.register_root(api)
    # localhost:5000/api/
    #APIRoot.register_root(api, root='/api')
    app.run()

if __name__ == '__main__':
    main()
