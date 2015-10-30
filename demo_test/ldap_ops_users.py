#-*- coding:utf-8 -*-
import ldap
import json
import sys


try:
    config = json.load(open('./ldap.config.json'))
except Exception, ex:
    print str(ex)
    sys.exit(1)

l = ldap.initialize(config['server'])
l.simple_bind_s(config['user'], config['passwd'])

#query
def query():
    searchAttribute = ["uid","mail"]
    # search_s for multi returns
    # search for single return
    results = l.search_s(config['basedn'], ldap.SCOPE_SUBTREE, "uid=*", searchAttribute)
    return results
    # for r in results:
    #     print r

#create
def create():
    u = json.load(open('./new_user.json'))
    attrs = [(str(k), [str(v.encode('utf-8'))]) for (k, v) in u.items()]
    attrs.append(('objectClass',['top', 'person',
'organizationalPerson', 'inetOrgPerson']))
    print "cn=%s,%s"%("ming",config['basedn'])
    l.add_s("uid=%s,%s"%("ming",config['basedn']), attrs)


def update():
    modified_attr = [(ldap.MOD_REPLACE, 'mail', 'ming@gmail.com')]
    l.modify_s("uid=%s,%s"%("ming",config['basedn']), modified_attr)


def delete():
    l.delete_s("cn=%s,%s"%("ming",config['basedn']))


import time
t1 = time.time()
for i in xrange(10000):
    query()
print time.time() - t1







