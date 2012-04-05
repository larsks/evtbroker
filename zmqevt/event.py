#!/usr/bin/python

import json

class Event (dict):
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        assert 'tag' in self, 'Missing required tag attribute.'

    def dump(self):
        assert 'tag' in self, 'Missing required tag attribute.'
        return (str(self['tag']), str(json.dumps(self)))

    @classmethod
    def load(cls, msg):
        assert len(msg) == 2, 'Invalid message length.'
        data = json.loads(msg[1])

        assert 'tag' in data, 'Missing required tag attribute.'
        assert msg[0] == data['tag'], 'Inconsistent tag/message content.'

        return cls(data)

