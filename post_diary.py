#! /usr/bin/env python

import mixi
from optparse import OptionParser


def main():
  parser = OptionParser()
  parser.add_option("-u", "--username",
                    help="username for login", metavar="NAME")
  parser.add_option("-p", "--password",
                    help="password for NAME", metavar="PASS")
  parser.add_option("-i", "--memberid",
                    help="as in http://mixi.jp/show_friend.pl?<ID>",
                    metavar="ID")
  parser.add_option("-t", "--title",
                    help="title of entry", metavar="TITLE")
  parser.add_option("-b", "--body",
                    help="entry body", metavar="BODY")
 
  (options, args) = parser.parse_args()
  
  if (options.username is None or
      options.password is None or
      options.memberid is None):
     print "\nusername, password, and memberid are all required\n"
     parser.print_help()
     exit(-1)

  service = mixi.Service(username=options.username,
                         password=options.password,
                         member_id=options.memberid)

  entry = mixi.DiaryEntry()
  entry.title = options.title
  entry.body = options.body

  (response, body) = service.postDiary(entry);
  print response.status, response.reason
  print body

if __name__ == '__main__': 
  main()

