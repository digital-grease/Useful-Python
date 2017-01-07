#%%
#imports etc
import dns.resolver, keyring, CloudFlare, time

cloudflare_api = "https://www.cloudflare.com/api_json.html"
auth_email = '[EMAIL]'
apikey = '[API_KEY]'
domain = 'DOMAIN'
wildcard = '*'
a_record = 'A'
wwwtype = 'www'
zoneid = '[ZONE_ID'
wildcard_id = '[WILDCARD_DNS_ID]'
a_record_id = '[NO_SUBDOMAIN_DNS_ID]'
www_id = '[WWW_DNS_ID]'
#%%
#use opendns servers to get public ip
def getip():
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ["208.67.222.222", "208.67.220.220"]
    return resolver.query('myip.opendns.com')[0]
#%%
#check current record
def cfcheck():
    cf = CloudFlare.CloudFlare(email=auth_email, token=apikey)
    asterisk = cf.zones.dns_records.get(zoneid, wildcard_id)['content']
    normal = cf.zones.dns_records.get(zoneid, a_record_id)['content']
    www = cf.zones.dns_records.get(zoneid, www_id)['content']
    return (asterisk, normal, www)
#%%
#use cloudflare_ddns to update dns record
def cfupdate(ip_on_record, recordname, record_id):
    cf = CloudFlare.CloudFlare(email=auth_email, token=apikey)
    currentip = str(getip())
    if recordname != a_record:
        newrecord = newrecord = {'name' : recordname+'.'+domain, 'type' : a_record, 'content' : currentip}
    else:
        newrecord = {'name' : domain, 'type' : a_record, 'content' : currentip}
        
    if ip_on_record != currentip:
        cf.zones.dns_records.put(zoneid, record_id, data=newrecord)
        print ('The {} record has been updated for {}.'.format(recordname, domain))
        time.sleep(3)
    elif ip_on_record == currentip:
        print ('The {} record for {} is still accurate.'.format(recordname, domain))
        time.sleep(3)
#%%
#call functions
def main():
    (wildcardrecord, arecord, wwwrecord) = cfcheck()
    cfupdate(wildcardrecord, wildcard, wildcard_id)
    cfupdate(arecord, a_record, a_record_id)
    cfupdate(wwwrecord, wwwtype, www_id)
    print ('Closing now!!!')
    time.sleep(2)
main()
exit()
