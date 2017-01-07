#%%
#imports etc
import dns.resolver

#%%
#use opendns servers to get public ip
def getip():
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ["208.67.222.222", "208.67.220.220"]
    return resolver.query('myip.opendns.com')[0]
