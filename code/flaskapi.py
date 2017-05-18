#!/usr/bin/env python

from flask import Flask
from flask_restful import Api, Resource

class APIResource(Resource):

    _API_ROOT = '/'
    _API_REGISTER = {}
    _API_FPATH = None

    @classmethod
    def register_root(cls, api, root=''):
        api.add_resource(cls, root + cls._API_ROOT)

        cls._register(api, root)

    @classmethod
    def _register(cls, api, root):
        root = root + cls._API_ROOT
        for path, res in cls._API_REGISTER.items():
            res_path = '{}{}'.format(root, path)
            res._API_FPATH = res_path
            api.add_resource(res, res_path)
            res._register(api, root)

class APILvl1Lvl2(APIResource):

    def get(self):
        return {'path': self._API_FPATH}

class APILvl1(APIResource):

    class APILvl1SID(APIResource):

        def get(self, sid):
            return {'sid': sid, 'path': self._API_FPATH}

    _API_ROOT = 'lvl1/'
    _API_REGISTER = {
            '<int:sid>': APILvl1SID,
            'lvl2/': APILvl1Lvl2
        }

    def get(self):
        return {'path': self._API_FPATH}

class APIRoot(APIResource):

    _API_ROOT = '/'
    _API_REGISTER = {
            'lvl1/': APILvl1,
        }

    def get(self):
        return {'path': self._API_FPATH}

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
