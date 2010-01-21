#! /usr/bin/env python

import httplib
import uuid
import datetime
import hashlib
import base64

class Service(object):
  domain = 'mixi.jp'
  _diary_path_format = '/atom/diary/member_id=%s'

  def __init__(self, username, password, member_id):
    self.username = username
    self.password = password
    self.member_id = member_id
    self.diary_path = self._diary_path_format % member_id

  def _headers(self):
    nonce = uuid.uuid4().hex
    created_date = datetime.datetime.utcnow().isoformat()+'Z'
    hash = hashlib.sha1(nonce+created_date+self.password)
    digest = base64.b64encode(hash.digest())

    wsse_format = ('UsernameToken Username="%s", ' 
                   'PasswordDigest="%s", '
                   'Nonce="%s", '
                   'Created="%s"')
    return {'Content-Type': 'application/atom+xml',
            'Authorization': 'WSSE profile="UsernameToken"',
            'X-WSSE': wsse_format % (self.username,
                                     digest,
                                     base64.b64encode(nonce),
                                     created_date)}
  
  def postDiary(self, entry):
    connection = httplib.HTTPConnection(self.domain)
    connection.request('POST',
                       self.diary_path,
                       entry.toxml(),
                       self._headers())
    response = connection.getresponse()
    body = response.read()
    connection.close()
    return (response, body)


class DiaryEntry(object):
  _bodyxml_format = ("<?xml version='1.0' encoding='utf-8'?>"
                     "<entry xmlns='http://purl.org/atom/ns#'>"
                     "<title>%s</title>"
                     "<summary>%s</summary>"
                     "</entry>")
  def __init__(self):
    self.title = ''
    self.body = ''

  def toxml(self):
    return self._bodyxml_format % (self.title, self.body)

