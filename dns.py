#!/usr/bin/python2.7

import dns.resolver

class Py3status:
        def check_ns(self, json, i3status_config):
                response = {'full_text': '', 'name': 'ns_checker'}
                position = 0

                my_resolver = dns.resolver.Resolver()
                my_resolver.lifetime = 0.2
                domain = ''
                nameservers = ('')
                error = False

                for ns in nameservers:
                        my_resolver.nameservers=[ns]
                        try:
                                my_resolver.query(domain, 'A')
                        except:
                                error = True

                if error:
                        response['full_text'] = 'NS NOK'
                        response['color'] = i3status_config['color_bad']
                else:
                        response['full_text'] = 'NS OK'
                        response['color'] = i3status_config['color_good']

                return (position, response)
