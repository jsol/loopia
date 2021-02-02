#!/usr/local/bin/python  
# -*- coding: utf-8 -*-  
  
import calendar  
import sys  
import os
import time  
import xmlrpclib  
import ipaddress
import urllib2

def main():  
    global_username = os.environ['LOOPIA_USER']
    global_password = os.environ['LOOPIA_PASS']

    global_domain_server_url = 'https://api.loopia.se/RPCSERV'   

    try:
        new_ip = urllib2.urlopen("http://api.ipify.org").read()
        ipaddress.ip_address(unicode(new_ip))
    except ValueError:
        sys.exit(1)
    except:
        print('Could not fetch new ip')
        sys.exit(1)

    f = open("/var/currentip", "r")
    old_ip = f.readline()
    f.close()

    if old_ip == new_ip:
      sys.exit(0)

    f = open("/var/currentip", "w")
    f.write(new_ip)
    f.close()

    print "New ip: %s (%s)" % (new_ip, old_ip)

    client = xmlrpclib.ServerProxy(uri =
        global_domain_server_url, encoding = 'utf-8')  
  
    response = client.getDomains(global_username, global_password)

    print 'Domains: %s\n' % response  

    for domain in response:
        d = domain["domain"]
        subdomains = client.getSubdomains(global_username, global_password, d)
        for sub in subdomains:
            data = client.getZoneRecords(global_username, global_password, d, str(sub))
            for record in data:
                if record['type'] == 'A' and record['rdata'] != new_ip:
                    record["rdata"] = new_ip
                    print "Updating %s.%s from %s" % (sub, d, record['rdata'])
                    update = client.updateZoneRecord(global_username, global_password, d, str(sub), record)
                    print "Subdomain updated: %s\n\n" % update


if __name__ == '__main__':  
    main()  
  
