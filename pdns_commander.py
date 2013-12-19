#!/usr/bin/python3

import sqlite3, sys, getopt

pdns_bdd='/tmp/bdd2.sqlite3'
domain=''
query='select * from domains'

class PdnsDomain:
    def __init__(self, name, type="NATIVE"):
        self.name = name
        self.type = type

    def add_domain(self):
        query = "INSERT INTO domains(name, type) values ('"+self.name+"','"+self.type+"')"
        bdd_modif("/tmp/bdd2.sqlite3", query)
    
    def del_domain(self):
        query = "DELETE FROM domains WHERE name='"+self.name+"'"
        bdd_modif("/tmp/bdd2.sqlite3", query)

    def show_domain(self):
        query = "SELECT id FROM domains WHERE name='"+self.name+"'"
        result = bdd_select(pdns_bdd, query)
        result2 = result.fetchone()
        self.id = result2[0]
        query = "SELECT * FROM records WHERE Domain_Id='"+str(self.id)+"'"
        result = bdd_select(pdns_bdd, query)
        return result
        

class PdnsRecord:
    def __init__(self, id, domain_id, name, type, content, ttl, priority, change_date):
        id = id
        self.domain_id = domain_id
        self.name = name
        self.type = type
        self.content = content
        self.ttl = ttl
        self.priority = priority
        self.change_date = change_date

    def 

def bdd_select(database,query):
    database = sqlite3.connect(database)
    cursor = database.cursor()
    return cursor.execute(query)
    database.close()

def bdd_modif(database,query):
    database = sqlite3.connect(database)
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    database.close()

def list_domains():
    query = "SELECT id, name, type FROM domains"
    domains = bdd_select(pdns_bdd, query)
#    print(domains.fetchall())
    for domain in domains.fetchall():
        print(domain)
#        print(domain[0])
#    for domain in domains.fetchall():
#        domainlist.append(domain)
#        print domainlist

def usage():
    print("RTFM Noob")

def main(argv):
    try: 
        opts, args = getopt.getopt(argv, "ha:n:t:v:", ["help", "action=", "type=", "name=", "value="])

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("HELP")
            usage()
            sys.exit(0)
        elif opt in ("-a", "--action"):
            action = arg
        elif opt in ("-t", "--type"):
            type = arg
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-v", "--value"):
            value = arg

    if action == "add":
        if type == "domain":
            MyDomain = PdnsDomain(value)
            MyDomain.add_domain()
        elif type == "record":
            MyRecord = PdnsRecord(value)
            MyRecord.add_record()
        else:
            print("Type "+type+" not available")
            usage()
    elif (action == "delete" or action == "del"):
        if type == "domain":
            MyDomain = PdnsDomain(value)
            Mydomain.deldomain()
        elif type == "record":
            MyRecord = PdnsRecord(value)
            MyRecord.delrecord
        else:
            print("Type "+type+" not available")
            usage()
    elif action == "list":
         if type == "domain":
            list_domains() 
    elif action == "show":
        if type == "domain":
            MyDomain = PdnsDomain(value)
            domains = MyDomain.show_domain()
            for i in domains.fetchall():
                print(i)
        #    print(domains.fetchall())
        elif type == "record":
            MyRecord = PdnsRecord(value)
            MyRecord.showRecord()
        else:
            print("Type "+type+" not available")
            usage()

main(sys.argv[1:])



    #domainlist = list_domains()

    #for domain in domainlist:
    #    print(domain)


#mydomain = PdnsDomain("mondomaine2.fr")
#mydomain.del_domain()


#result = bdd_select("/tmp/bdd2.sqlite3", "SELECT * FROM domains")
#for row in result:
#    print(row)
#
#def interact_bdd(bdname,action):
#    if action == 'connect':
#        print("connect to bdd")
#        return sqlite3.connect(bdname)
#    elif action == 'disconnect':
#        return bdd.close()
#    else:
#        print("Action not found")
#
#bdd = interact_bdd(bdname,"connect")
#

##print(query % domain)
#result = bdd.cursor()
#
#
#for row in result:
#print(type(result))
#
#
##interact_bdd(bdname,"disconnect")
##bdd.close()
#def bdd_queries(request):
#    if request == "list_domains":
#        return "SELECT * FROM domains"
#    if request == "show_domain":
#        return 'SELECT * FROM domains WHERE name="%(domain)s"'
#    if request == "del_domain":
#        return 'DELETE FROM domains WHERE name="%(domain)s"'
#    if request == "add_domain":
#        return 'INSERT INTO domains(name,type) values (\'%(domain)s\',\'NATIVE\')'

