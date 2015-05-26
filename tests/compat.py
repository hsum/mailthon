from sys import version_info

if version_info[0] == 3:
    unicode = str
else:
    def unicode(k):
        if hasattr(k, '__unicode__'):
            return k.__unicode__()
        return k.decode('utf8')
