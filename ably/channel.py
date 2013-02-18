import json

from ably.exceptions import catch_all

class Channel(object):
    def __init__(self, rest, name):
        self.__rest = rest
        self.__name = name

    @catch_all
    def presence(self, params=None):
        """Returns the presence for this channel"""
        params = params or {}
        headers = self.__rest.default_get_headers()
        path = '/channels/%s/presence' % self.__name
        return self.__rest.get(path, headers=headers, params=params).json()

    @catch_all
    def history(self, params=None):
        """Returns the history for this channel"""
        params = params or {}
        headers = self.__rest.default_get_headers()
        path = '/channels/%s/history' % self.__name
        return self.__rest.get(path, headers=headers, params=params).json()

    @catch_all
    def publish(self, name, data):
        """Publishes a message on this channel.

        :Parameters:
        - `name`: the name for this message
        - `data`: the data for this message
        """
        request_body = {
            'name': name,
            'data': data,
        }
        request_body = json.dumps(request_body)
        headers = self.__rest.default_post_headers()

        path = '/channels/%s/publish' % self.__name
        return self.__rest.post(path, data=request_body, headers=headers).json()


class Channels(object):
    def __init__(self, rest):
        self.__rest = rest
        self.__attached = {}

    def get(self, name):
        name = unicode(name)
        if name not in self.__attached:
            self.__attached[name] = Channel(self.__rest, name)
        return self.__attached[name]

    def __getitem__(self, key):
        return self.get(key)

    def __getattr__(self, name):
        try:
            return getattr(super(Channels, self), name)
        except AttributeError:
            return self.get(name)

