#!/usr/bin/python2.7
#-*- coding:  UTF8

import dns.resolver
import sys
import socket
import argparse

# VARIABLES ###
'''
    Counter : Dict which save number of occurences for each record type,
            per domain
        Counter[domain] : Dict of all records parsed
            Counter[domain][record type] : number of occurence. Start to 0

    Correspondance : correspondance between the data asked and the record used

    Resolvers : List of many open resolvers. List available on
        http://pcsupport.about.com/od/tipstricks/a/free-public-dns-servers.htm

    Result : Dict of returned results
        Result[resolver] : Dict of results returned by this resolver
            Result[resolver][record_type] : Dict of returned result by this
                                                resolver, for this record type
                Result[resolver][record_type][id] : Dict of all datas for
                                                     one answer

    Record : Tuple of required records
'''

counter = {}
result = {}
correspondance = {
    "DMARC": "TXT",
    "DKIM": "TXT",
    "DOMAINKEY": "TXT",
}
resolvers = {
    "Google": "8.8.8.8",
    "OpenDNS": "208.67.222.222",
    "Norton": "198.153.192.40",
    "SafeDNS": "195.46.39.39",
}
verbose = 0

# FUNCTIONS ###


def parse_response(query, resolver, rec, my_records):
    '''
        Query : Result send by the resolver
        Resolver : Resolver used
        Rec : Record type used
        My_records : main dict
    '''
    for res in query:
        res_type = res.__class__.__name__
        if res_type in ('MX'):
            my_records.append(res_type + "|" + str(
                res.exchange) + "|" + str(res.preference))
        elif res_type in ('NS'):
            my_records.append(res_type + "|" + str(res.target))
        elif res_type in ('A', 'AAAA'):
            # 67.215.65.132 is the default answer from openDNS instead of NXDOMAIN. Must be ignored to prevent against false positive
            if str(res.address) == "67.215.65.132":
                continue
            else:
                my_records.append(res_type + "|" + str(res.address))
        elif res_type in ('TXT', 'SPF'):
            if rec == "DKIM":
                my_records.append("DKIM|" + str(res.strings[0]))
            elif rec == "SPF":
                my_records.append("SPF|" + str(res.strings[0]))
            elif rec == "DMARC":
                my_records.append("DMARC|" + str(res.strings[0]))
            elif rec == "DOMAINKEY":
                my_records.append("DOMAINKEY|" + str(res.strings[0]))
            else:
                my_records.append(rec + "|" + str(res.strings[0]))
        elif res_type in ('SOA'):
            my_records.append(res_type + "|" + str(res.expire) + "|" + str(
                res.minimum) + "|" + str(res.refresh) + "|" + str(res.retry) + "|" + str(res.serial))


def compare_results(result, domain, verbose):
    '''
        Result :
    '''
    for resolver in result:
        if resolver == "Official":
            continue
        else:
            if cmp(result["Official"], result[resolver]) == 0:
                if verbose >= 1:
                    print(
                        "[OK] - " + resolver + " resolver is up to date with " + domain + " nameservers")
            else:
                print(
                    "[NOK] - " + resolver + " resolver is not up to date with " + domain + " nameservers")


def display_results(result):
    for resolver in result:
        print("---------------------------------")
        print(resolver + " : " + resolvers[resolver])
        for rec_type in result[resolver]:
            print rec_type.split("|")
    print("---------------------------------")


def do_query(domain, rr, my_resolver):
    try:
        return my_resolver.query(domain, rr, tcp=1)
    except dns.resolver.NoAnswer:
        verbose_output("No such record " + rr + " for " + domain, 0)
        return "QueryError"
    except dns.resolver.Timeout:
        verbose_output("DNS server " + str(my_resolver.nameservers)
                       + " is not reachable. Domain : " + domain + " - Record : " + rr, 2)
        return "QueryError"
    except dns.resolver.NXDOMAIN:
        verbose_output("No such record " + rr + " for " + domain, 0)
        return "QueryError"
    except dns.rdatatype.UnknownRdatatype:
        verbose_output(
            "RR type '" + rr + "' is not an supported Record type", 1)
        return "QueryError"


def verbose_output(message, criticity):
    if criticity == 0 and verbose == 1:
        print "[INFO] - " + message
    elif criticity == 1:
        print "[WARN] - " + message
    elif criticity == 2:
        print "[CRIT] - " + message


def get_ns(resolvers, domain, my_resolver):
    if not "Official" in resolvers:
        try:
            ns_fqdn = my_resolver.query(str(domain), "NS")
            resolvers["Official"] = socket.gethostbyname(str(ns_fqdn[0]))
        except dns.resolver.NXDOMAIN:
            verbose_output("Nameserver not found for this domain", 2)
            sys.exit(2)
        except dns.resolver.NoAnswer:
            parent_domain = domain.split(".", 1)[1]
            get_ns(resolvers, parent_domain, my_resolver)


def main(argv):
    ''' Main function '''

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="Domain name to check", dest="domain", action="store", required=True)
    parser.add_argument("-S", "--selector", help="DKIM selector. Must be used with DKIM record type", dest="selector")
    parser.add_argument("-s", "--server", '-@', help="Reference nameserver for the domain", dest="server")
    parser.add_argument("-t", "--type", nargs='*', help="List of record type which must be checked. Fully supported : A AAAA SOA NS MX TXT SPF DKIM DOMAINKEY DMARC. Default value is A", dest="type")
    parser.add_argument("-v", "--verbose", help="Increase Output verbosity", dest="verbose", action="count", default=0)

    args = parser.parse_args()

    if args.domain:
        domain = args.domain
    if args.server:
        resolvers["Official"] = args.server
    if args.type:
        tmp_list = []
        for i in args.type:
            tmp_list.append(i.upper())
        record = tmp_list
        del tmp_list
    else:
        record = "A"
    if args.verbose >= 2:
        verbose = 2
    elif args.verbose == 1:
        verbose = 1
    else:
        verbose = 0
    if args.selector and "DKIM" in record:
        dkim_selector = args.selector
    elif "DKIM" in record:
        print "DKIM selector must be set"
        parser.print_usage()
        sys.exit(2)
    my_resolver = dns.resolver.Resolver()

    get_ns(resolvers, domain, my_resolver)

    # Get resolvers datas ###
    for resolver in resolvers:
        my_records = []
        my_resolver.nameservers = [resolvers[resolver]]
        my_resolver.lifetime = 5
        for rec in record:
            if not rec in correspondance:
                rr_type = rec
            else:
                rr_type = str(correspondance[rec])

            if rec == "DOMAINKEY":
                query = do_query("_domainkey." + domain, rr_type, my_resolver)
            elif rec == "DMARC":
                query = do_query(
                    "_dmarc." + domain, rr_type, my_resolver)
            elif rec == "DKIM":
                query = do_query(dkim_selector + "._domainkey." + domain, rr_type, my_resolver)
            else:
                query = do_query(domain, rr_type, my_resolver)

            if query == "QueryError":
                continue
            else:
                parse_response(query, resolver, rec, my_records)

        my_records.sort()
        result[resolver] = (my_records)

    if verbose == 2:
        display_results(result)

    compare_results(result, domain, verbose)
if __name__ == '__main__':
    main(sys.argv[1:])
