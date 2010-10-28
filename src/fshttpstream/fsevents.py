import datetime
import uuid
import urllib
try: import json
except ImportError: import simplejson as json


def localdate():
    return datetime.datetime.now().strftime("%Y-%m-%d %T")


class Event(object):
    def __init__(self, raw_event, flushbuffer=False):
        self._flush = flushbuffer
        self.uuid = str(uuid.uuid4())
        self.raw_event = raw_event
        self.dict_event = {}
        self.json_event = ''
        self.__parse()

    def get_uuid(self):
        return self.uuid

    def get_raw(self):
        return self.raw_event

    def get_json(self):
        return self.json_event

    def get_dict(self):
        return self.dict_event

    def __parse(self):
        self.dict_event = {}
        if self._flush:
            l = len(self.raw_event)
            bufferl = 1024-l
            if bufferl > 0: self.dict_event['Flush-Browser-Buffer'] = 'X'*bufferl
        for line in self.raw_event.splitlines():
            if line and ': ' in line:
                var, val = line.split(': ', 1)
                var = var.strip()
                val = urllib.unquote_plus(val.strip())
                self.dict_event[var] = val
        self.json_event = json.dumps(self.dict_event)


class PingEvent(Event):
    def __init__(self):
        Event.__init__(self, raw_event='Event-Name: Ping\r\nEvent-Date-Local: %s\r\n' \
                       % urllib.quote_plus(localdate()))


class FlushBufferEvent(Event):
    def __init__(self):
        Event.__init__(self, raw_event='Event-Name: FlushBuffer\r\nEvent-Date-Local: %s\r\n' \
                       % urllib.quote_plus(localdate()), flushbuffer=True)

