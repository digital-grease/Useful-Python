**Pingroute is a *very* rough implementation of traceroute designed to scan either a single ip, hostname (will resolve to an ip), or a CIDR block. Will detect if there is a routing loop, and stop.**

1. Will first ask for a target, ip/hostname/CIDR

2. Then parses input:
  * if CIDR, uses ipaddress library to return a list of all ip's in that range
  * if hostname, uses socket.gethostbyname to resolve to ip
  * if single ip, directly returns that
  
3. Will open sockets and test input passed to the main pingroute function

**_crappy commenting in this one, but most of it is pretty self explanatory_**

**pingroute_tcp is a syn only tcp version of pingroute**
