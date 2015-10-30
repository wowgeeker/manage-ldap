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
    searchAttribute = ["member"]
    # search_s for multi returns
    # search for single return
    results = l.search_s("cn=exampleGroup,ou=groups,dc=myorga", ldap.SCOPE_SUBTREE, "cn=exampleGroup", searchAttribute)
    print results
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
    new_member = str("uid=%s,%s"%("ming", config['basedn']))
    modified_attr = [(ldap.MOD_ADD, 'member', [new_member])]
    l.modify_s("cn=exampleGroup,ou=groups,dc=myorga", modified_attr)


def delete():
    new_member = str("uid=%s,%s"%("ming", config['basedn']))
    modified_attr = [(ldap.MOD_DELETE, 'member', [new_member])]
    l.modify_s("cn=exampleGroup,ou=groups,dc=myorga", modified_attr)


query()
