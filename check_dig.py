#!/usr/bin/python

import dns.resolver

resolvers = {
    "Google":               "8.8.8.8",
    "Comodo":               "8.26.56.26",
    "OpenDNS":              "208.67.222.222",
#    "Advantage":            "156.154.70.1",
#    "Norton":               "198.153.192.40",
#    "GreenTeam":            "81.218.119.11",
#    "SafeDNS":              "195.46.39.39",
#    "OpenNIC":              "216.87.84.211",
#    "SmartViper":           "208.76.50.50",
#    "Dyn":                  "216.146.35.35",
#    "Censurfridns":         "89.233.43.71",
#    "HurricaneElectric":    "74.82.42.42",
#    "PuntCAT":              "109.69.8.51",
}
result = {}
domain = "google.com"
record = ["DMARC", "A", "MX", "NS", "TXT", "SPF"]
#record = ("MX", "NS", "A", "SOA", "SPF", "TXT", "DMARC", "DKIM")

def parse_response(query, resolver):
    i = 0
    if query == "SPF":
        result[resolver][query] = {}
        result[resolver][query][i] = {"value": "SPF Record Not Configured"}
    else:
        for res in query:
            res_type = res.__class__.__name__
#        print(res_type)
            if i == 0:
                result[resolver][res_type] = {}
            if res_type in ('MX'):
                result[resolver][res_type][i] = {
                    "value": str(res.exchange),
                    "prio": str(res.preference),
                }
            elif res_type in ('NS'):
                result[resolver][res_type][i] = {
                    "value": str(res.target),
                }
            elif res_type in ('A', 'AAAA'):
                result[resolver][res_type][i] = {
                    "value": str(res.address),
                }
            elif res_type in ('TXT', 'SPF'):
                result[resolver][res_type][i] = {
                    "value": str(res.strings)
                }
            elif res_type in ('SOA'):
                result[resolver][res_type][i] = {
                    "expire": str(res.expire),
                    "minimum": str(res.minimum),
                    "refresh": str(res.refresh),
                    "retry": str(res.retry),
                    "serial": str(res.serial),
                }
        
            i += 1

def main():
    my_resolver = dns.resolver.Resolver()
    for resolver in resolvers:
        result[resolver] = {}
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = [resolvers[resolver]]
        for rec in record:
            try:
                if rec == "DMARC":
                    query  = my_resolver.query("_dmarc." + domain,"TXT")
                else:
                    query  = my_resolver.query(domain,rec)
            except dns.resolver.NoAnswer:
                query = "SPF"
            parse_response(query, resolver)
    
    for i in result:
        print(i)
        for j in result[i]:
            print("|__ " + str(j))
            for k in result[i][j]:
                print("   |__ " + str(result[i][j][k]))

if __name__ == '__main__':
    main()

