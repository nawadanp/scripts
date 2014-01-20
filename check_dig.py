#!/usr/bin/python2.7
#-*- coding:  UTF8

import dns.resolver
import getopt
import sys
import socket

'''
    TODO :
        - Comparer résultats avec les valeurs officielles
        - Passer les champs a requeter en argument
        - Bug avec champs TXT et SPF
        - Gestion DMARC, DKIM...
    ------------
        - Passer les dict en tuple
        - PEP8 et FLAKE8 compliance
        - TIPS : for index, mx in enumerate(MV):
        - list.sort | tuple.sort
'''

### VARIABLES ###
'''
    Counter : Dict which save number of occurences for each record type, per 
            domain
	Counter[domain] : Dict of all records parsed
	    Counter[domain][record type] : number of occurence. Start to 0

    Correspondance : correspondance between the data asked and the record used

    Resolvers : List of many open resolvers. List available on http://pcsupport.about.com/od/tipstricks/a/free-public-dns-servers.htm

    Result : Dict of returned results
	Result[resolver] : Dict of results returned by this resolver
	    Result[resolver][record_type] : Dict of returned result by this resolver, for this record type
		Result[resolver][record_type][id] : Dict of all datas for one answer

    Record : Tuple of required records
'''

counter = {}
correspondance = {
    "A":		    "A",
    "MX":		    "MX",
    "SOA":		    "SOA",
    "AAAA":		    "AAAA",
    "NS":		    "NS",
    "SPF":		    "TXT",
    "TXT":		    "TXT",
    "DMARC":		    "TXT",
    "DKIM":		    "TXT",
    "SID":		    "TXT",
    "DOMAINKEY":	    "TXT",
}
resolvers = {
    "Google":               "8.8.8.8",
    "OpenDNS":              "208.67.222.222",
#    "Norton":               "198.153.192.40",
#    "SafeDNS":              "195.46.39.39",
#    "OpenNIC":              "216.87.84.211",
#    "Dyn":                  "216.146.35.35",
}
result = {}
record = ["MX", "NS", "TXT", "A"]

### FUNCTIONS ###

def parse_response(query, resolver, rec, my_records):
    '''
	Query : Result send by the resolver
	Resolver : Resolver used 
	Rec : Record type used
	Result : main dict
    '''
    for res in query:
	print "REC = " + rec
        res_type = res.__class__.__name__
        if res_type in ('MX'):
	    my_records.append(res_type + "|" + str(res.exchange) + "|" + str(res.preference))
        elif res_type in ('NS'):
	    my_records.append(res_type + "|" + str(res.target))
        elif res_type in ('A', 'AAAA'):
	    my_records.append(res_type + "|" + str(res.address))
        elif res_type in ('TXT', 'SPF'):
	    my_records.append(rec + "|" + str(res.strings))

def compare_results(result):
    for resolver in result:
	if resolver == "Official":
	    continue
	else:
	    if cmp(result["Official"], result[resolver]) == 0:
		print(resolver + " resolver is up to date with " + domain + " nameservers")
	    else:
		print(resolver + " resolver is not up to date with " + domain + " nameservers")

def display_results(result):
    for resolver in result:
	print("-------------------------------------------")
	print(resolver + " : " + resolvers[resolver])
        for rec_type in result[resolver]:
	    print rec_type.split("|")
	    
#            print("|__ " + str(rec_type))

def main(argv):
    ### Parse arguments ###
    opts, args = getopt.getopt(argv, "hd:r:", ["help", "domain="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("HELP")
            sys.exit(0)
        elif opt in ("-d", "--domain"):
            global domain 
	    domain = arg
    
    my_resolver = dns.resolver.Resolver()

    ### Get official datas ###
    try:
	ns_fqdn  = my_resolver.query(str(domain),"NS")
	resolvers["Official"] = socket.gethostbyname(str(ns_fqdn[0]))
    except dns.resolver.NXDOMAIN:
	print("NS not found")
	sys.exit(2)

    ### Get resolvers datas ###
    for resolver in resolvers:
	my_records = []
	my_resolver.nameservers = [resolvers[resolver]]
	for rec in record:
	    try:
		print "Record : " + rec
		print correspondance[rec]
		query = my_resolver.query(domain,str(correspondance[rec]))
	    parse_response(query, resolver, rec, my_records)
	    except dns.resolver.NoAnswer:
		print "TROLOLO"
		continue
	my_records.sort()
	result[resolver] = (my_records)
    
    compare_results(result)
    display_results(result)

if __name__ == '__main__':
    main(sys.argv[1:])

