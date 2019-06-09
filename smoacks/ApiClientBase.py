# ApiClientBase.py - Base object for API clients
from abc import ABC, abstractmethod
from smoacks.api_util import call_api

class ApiClientBase(ABC):
    _api_path = None
    _id_field = None

    @abstractmethod
    def get_id(self):
        pass

    def toJSON(self, deep=False):
        result = {}
        for key, value in vars(self).items():
            if not key.startswith('_'):
                result[key] = value
        return result

    def save_new(self, session):
        resp = call_api(session, 'POST',
                        '/{}'.format(self._api_path),
                        self.toJSON(True))
        if resp.status_code == 201:
            return True, resp.json()[self._id_field]
        return False, resp

    def save_update(self, session):
        resp = call_api(session, 'PUT',
                        '/{}/{}'.format(self._api_path, self.get_id()),
                        self.toJSON(False))
        if resp.status_code == 201:
            return True, None
        return False, resp

    def save_delete(self, session):
        resp = call_api(session, 'DELETE',
                        '/{}/{}'.format(self._api_path, self.get_id()))
        if resp.status_code == 204:
            return True, None
        return False, resp

    @classmethod
    def get(cls, session, id):
        resp = call_api(session, 'GET',
                        '/{}/{}'.format(cls._api_path, id))
        if resp.status_code == 200:
            return True, cls(**resp.json())
        return False, resp

    @classmethod
    def search(cls, session, text):
        resp = call_api(session, 'GET',
                        '/{}?search_text={}'.format(cls._api_path, text))
        if resp.status_code == 200:
            result = []
            resp_list = resp.json()
            for item in resp_list:
                result.append(cls(**item))
            return True, result
        return False, resp
