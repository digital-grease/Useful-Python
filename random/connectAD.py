# import class and constants
from ldap3 import Server, Connection, ALL, NTLM
import getpass


# define the server and the connection
server = Server('''servername''', use_ssl=True, get_info=ALL)
conn = Connection(server, user=input('Pls enter username in format: Domain\\username: '), password=getpass.getpass(), authentication=NTLM, auto_bind=True)

conn.search('dc="domain controller", dc="domain", dc="TLD"', '(&(mail="emailaddress"))')