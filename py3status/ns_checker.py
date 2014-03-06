import dns.resolver
import socket


class Py3status:
    """
    This module launch a simple query on each nameservers for the specified domain.
    Nameservers are dynamically retrieved. The FQDN is the only one mandatory parameter.
    It's also possible to add additional nameservers by appending them in nameservers list.

    The default resolver can be overwritten with my_resolver.nameservers parameter.

    Written and contributed by @nawadanp
    """
    def ns_checker(self, json, i3status_config):
        response = {'full_text': '', 'name': 'ns_checker'}
        position = 0
        counter = 0
        nameservers = []
        error = False

        domain = ''

        my_resolver = dns.resolver.Resolver()
        my_resolver.lifetime = 0.3

        my_ns = my_resolver.query(domain, 'NS')

        # Insert each NS ip address in nameservers
        for r in my_ns:
            nameservers.append(str(socket.gethostbyname(str(r))))

        # Perform a simple DNS query, for each NS servers
        for ns in nameservers:
            my_resolver.nameservers = [ns]
            counter += 1
            try:
                my_resolver.query(domain, 'A')
            except:
                error = True

        if error:
            response['full_text'] = 'NS NOK - ' + str(counter) + ' NS Found'
            response['color'] = i3status_config['color_bad']
        else:
            response['full_text'] = 'NS OK - ' + str(counter) + ' NS Found'
            response['color'] = i3status_config['color_good']

        return (position, response)
