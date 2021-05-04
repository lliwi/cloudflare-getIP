#!/usr/bin/python3


import mmh3
import codecs
import shodan
from colorama import Fore, Back, Style
import requests
import os
import sys
from bs4 import BeautifulSoup
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
import dns.resolver


SHODAN_API_KEY = "xxxxxxxxAPI KEY HERE xxxxxxxx"

api = shodan.Shodan(SHODAN_API_KEY)

def favicon(target):
    print(Fore.BLUE + '[+] URL: ' + target + '/favicon.ico' + Style.RESET_ALL)

    response = requests.get(target + '/favicon.ico')
    favicon = codecs.encode(response.content,"base64")
    hash = mmh3.hash(favicon)
    print(Fore.YELLOW + str(hash) + Style.RESET_ALL)

    print(Fore.BLUE +  '[+] getting info from shodan... ' + Style.RESET_ALL )
    results = api.search('http.favicon.hash:' + str(hash))
    print(Fore.GREEN + '[+] Info found: ' + str(results['total']) + Style.RESET_ALL)
    print('')

    if results['total'] == 0:
        print(Fore.RED + 'No info found' + Style.RESET_ALL)
    else:

        for result in results['matches']:
            try:
                print(Back.GREEN + 'IP: {}'.format(result['ip_str']) + Style.RESET_ALL )
            except KeyError:
                pass
            try:
                print('HOSTNAMES: {}'.format(result['hostnames']))
            except KeyError:
                pass
            try:
                print('OS: {}'.format(result['os']))
            except KeyError:
                pass
            try:
                print('PORTS: {}'.format(result['port']))
            except KeyError:
                pass
            try:
                print('COMPANY: {}'.format(result['org']))
            except KeyError:
                pass
            try:
                print('VULNS: {}'.format(result['vulns']))
            except KeyError:
                pass

            print('')
            print(result['data'])
            print('')

def dnsdumpster(target):
    print(Fore.CYAN + "Testing for misconfigured DNS using dnsdumpster...")

    res = DNSDumpsterAPI(False).search(target)

    if res['dns_records']['host']:
        for entry in res['dns_records']['host']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print(Style.BRIGHT + Fore.WHITE + "[FOUND:HOST] " + Fore.GREEN + "{domain} {ip} {as} {provider} {country}".format(**entry))

    if res['dns_records']['dns']:
        for entry in res['dns_records']['dns']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print(Style.BRIGHT + Fore.WHITE + "[FOUND:DNS] " + Fore.GREEN + "{domain} {ip} {as} {provider} {country}".format(**entry))

    if res['dns_records']['mx']:
        for entry in res['dns_records']['mx']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print(Style.BRIGHT + Fore.WHITE + "[FOUND:MX] " + Fore.GREEN + "{ip} {as} {provider} {domain}".format(**entry))


def crimeflare(target):
    print(Fore.CYAN + "Cheking crimeflare database...")
    myobj = {'cfS': target}
    r = requests.post('http://www.crimeflare.org:82/cgi-bin/cfsearch.cgi', data=myobj)
    #print(r.text)
    index = r.text
    try:
        s = BeautifulSoup(index, 'html.parser')
        s = s.find('li')
        result = str(s).split(':')
        result = result[1].replace('</li>','')
        print(Style.BRIGHT + Fore.WHITE + result + Style.RESET_ALL)
    except IndexError:
        print(Fore.RED + 'No info found' + Style.RESET_ALL)



def main():


    if len(sys.argv) < 2:
        print("""Usage:
python3 cloudflare-getIP.py  https://www.yourdomain.com """)
    else:


        url = sys.argv[1]

        target = sys.argv[1].split(':')
        target = target[1].replace('/','')

        domain = target.split('.')
        domain = domain[1] + '.' + domain[2]


        favicon(url)
        crimeflare(target)
        dnsdumpster(domain)


    return 0

if __name__ == '__main__':
    main()
