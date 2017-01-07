#%%
#imports etc
import dns.resolver, keyring, CloudFlare, time

cloudflare_api = "https://www.cloudflare.com/api_json.html"
auth_email = 'm.flowersbusiness@gmail.com'
apikey = keyring.get_password('cloudflareapi', 'm.flowersbusiness@gmail.com')
domain = 'photosynthesize.me'
wildcard = '*'
a_record = 'A'
wwwtype = 'www'
zoneid = 'a6726d246329e56402b451209157e2f0'
wildcard_id = '95d4514cd25c5616156cf1464d2d623f'
a_record_id = '7eb88e4cb3397bc6bf74a3e26e307f4d'
www_id = 'd076c35adac2dc952ef532c22735c950'
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
