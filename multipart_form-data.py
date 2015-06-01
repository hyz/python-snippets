import os
import posixpath
import http.server
import urllib.request, urllib.parse, urllib.error
import cgi
import shutil
import mimetypes
import re
import html
import subprocess
import io
 
Null = open(os.devnull) #_Empty()

class Part(object):
    #CONTENT_DISPOSITION = 'Content-Disposition'
    #DEFAULT_CONTENT_TYPE = 'application/octet-stream'

    def __init__(self): #(self, name=None, filename=None, body=None, headers={}):
        #self.headers = None
        self.name = None
        self.filename = None
        self.body = None # io.BytesIO()
        self._last = None

    def parse(self, line):
        if self.body is None:
            if line == b'\r\n':
                self.body = [] #io.BytesIO()
            else:
                self._parse_header(line)
        else:
            if self._last:
                self.body.append(self._last)
            self._last = line

    def end(self):
        if self._last:
            assert self._last.endswith(b'\r\n')
            la = self._last[:-2]
            if la:
                self.body.append(la)
            del self._last
        return self

    def __str__(self):
        return str(self.__dict__)

    def _parse_header(self, line):
        m = re.match(b'^Content-Disposition.*name="(.*)"; filename="(.*)"\r\n$', line)
        if m:
            self.name     = html.unescape(m.group(1).decode())
            self.filename = html.unescape(m.group(2).decode())
        #if self._filename == None:
        #    self._headers[Part.CONTENT_DISPOSITION] = ('form-data; name="%s"' % self._name)
        #else:
        #    self._headers[Part.CONTENT_DISPOSITION] = ('form-data; name="%s"; filename="%s"' % (self._name, self._filename))

def multipart(rfile, content_type):
    boundary = rfile.readline().strip()

    m = re.match(r'^multipart/form-data;\s*boundary=(.*)$', content_type)
    if not m:
        raise ValueError('Content_Type invalid') 
    if not re.match(b'^-*' + m.group(1).encode() + b'-*$', boundary):
        print(m.group(1))
        print(boundary.decode())
        raise ValueError('multipart/form-data boundary mismatch') 

    part = Part()
    for line in rfile:
        if line.startswith(boundary):
            part.end()
            yield part
            part = Part()
        part.parse(line)

def test():
    for part in multipart(open('/tmp/multipart_form-data', 'rb'), 'multipart/form-data; boundary=---------------------------18044279811739068280261685895'):
        print(part)

if __name__ == '__main__':
    test()

