from re import search
from base64 import b64decode
from email import message_from_string
from email.header import make_header, decode_header
from email.message import Message
from .compat import unicode


class mimetest:
    def __init__(self, mime):
        if isinstance(mime, str):
            mime = message_from_string(mime)
        self.mime = mime

    def __getitem__(self, header):
        value = self.mime[header]
        if value is None:
            return None
        h = make_header(decode_header(value))
        return unicode(h)

    @property
    def transfer_encoding(self):
        return self['Content-Transfer-Encoding']

    @property
    def encoding(self):
        ctype = self['Content-Type'].split()
        if len(ctype) >= 2:
            match = search('charset="(.+?)"', ctype[1])
            if match:
                return match.group(1)

    @property
    def mimetype(self):
        return self['Content-Type'].split()[0].strip(';')

    @property
    def payload(self):
        payload = self.mime.get_payload().encode(self.encoding or 'ascii')
        if self.transfer_encoding == 'base64':
            return b64decode(payload)
        return payload

    @property
    def parts(self):
        payload = self.mime.get_payload()
        if not isinstance(payload, list):
            raise TypeError
        return [mimetest(k) for k in payload]


def blank():
    return Message()
