#modified from https://blogs.oracle.com/ksplice/entry/learning_by_doing_writing_your
#%%
#traceroute/ping with routing loop detection

import socket, ipaddress
#%%
#take input, filter by single ip/hostname/range
def targetrange(targetaddress):
    try:
        if '/' in targetaddress:
            ip_net = ipaddress.ip_network(targetaddress)
            hostlist = list(ip_net.hosts())
            return hostlist
        elif '/' not in targetaddress:
            return targetaddress
        elif '.' not in targetaddress:
            hostip = socket.gethostbyname(targetaddress)
            return hostip
    except:
        print ("""Error in target parsing:
            Please ensure your target was a single IP address, or in CIDR format.""")
#%%
#pingroute function implements traceroute, stops upon detection of routing loop
#split into list/notlist
def pingroute(targets):
    hoplist = []
    if isinstance(targets, list):
        #initialize parameters
        for i in targets:
            dest_addr = i
            icmp = socket.getprotobyname('icmp')
            udp = socket.getprotobyname('udp')
            ttl = 1
            port = 33434
            hops = 30
            while True:
                #initialize sockets and socket options
                rec_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
                send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
                send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
                rec_socket.bind(("", port))
                send_socket.sendto("".encode(), (dest_addr, port))
                currentip = None
                currentname = None
                try:
                    __, currentip = rec_socket.recvfrom(512)
                    currentip = currentip[0]
                    try:
                        currentname = socket.gethostbyaddr(currentip)[0]
                    except socket.error:
                        currentname = currentip
                except socket.error:
                    pass
                finally:
                   send_socket.close()
                   rec_socket.close()
                if currentip is not None:
                    currenthost = "%s (%s)" % (currentname, currentip)
                    hoplist.append(currentip)
                else:
                    currenthost = "*"
                if currentip not in hoplist:
                    print ("%d\t%s" % (ttl, currenthost))
                    ttl += 1
                else:
                    print ("Routing loop detected on path to %s. Moving on to next trace." % i)
                    break
                if currentip == i or ttl > hops:
                    break
    else:
        dest_addr = targets
        icmp = socket.getprotobyname('icmp')
        udp = socket.getprotobyname('udp')
        ttl = 1
        port = 33434
        hops = 30
        while True:
            rec_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            rec_socket.bind(("", port))
            send_socket.sendto("".encode(), (dest_addr, port))
            currentip = None
            currentname = None
            try:
                __, currentip = rec_socket.recvfrom(512)
                currentip = currentip[0]
                try:
                    currentname = socket.gethostbyaddr(currentip)[0]
                except socket.error:
                    currentname = currentip
            except socket.error:
                pass
            finally:
               send_socket.close()
               rec_socket.close()
            if currentip is not None:
                currenthost = "%s (%s)" % (currentname, currentip)
                hoplist.append(currentip)
            else:
                currenthost = "*"
            if currentip not in hoplist:
                print ("%d\t%s" % (ttl, currenthost))
                ttl += 1
            else:
                print ("Routing loop detected on path to %s. Stopping." % targets)
                break
            if currentip == dest_addr or ttl > hops:
                break
#%%
#call previous
def main():
    try:
        target = input("Enter IP/Hostname for single target, or CIDR format for range: ")
    except:
        print ('target input failed')
    try:
        pingroutetarget = targetrange(target)
    except:
        print ('target resolution failed')
    try:
        pingroute(pingroutetarget)
        print ("All done!!!")
    except:
        print ("Something broke, sorry!!!")
if __name__ == "__main__":
    main()
