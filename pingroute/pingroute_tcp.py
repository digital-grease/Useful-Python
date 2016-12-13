#modified from https://blogs.oracle.com/ksplice/entry/learning_by_doing_writing_your
#%%
#traceroute/ping with routing loop detection

import socket, ipaddress, struct, random
host = socket.gethostbyname(socket.gethostname())
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
#several functions to make packet
def tcpcheck(msgin):
    s = 0
    for i in range(0, len(msgin), 2):
        w = ord(msgin[i]) + (ord(msgin[i+1]) << 8 )
        s = s + w
    s = (s>>16) + (s & 0xffff);
    s = s + (s >> 16);
    #complement and mask to 4 byte short
    s = ~s & 0xffff
    return s
def iphdr(src, dst):
    headerlen = 5
    version = 4
    tos = 0
    tot_len = 20 + 20
    id = random.randrange(18000,65535,1)
    frag_off = 0
    ttl = 255
    protocol = socket.IPPROTO_TCP
    check = 10
    saddr = socket.inet_aton (src)
    daddr = socket.inet_aton (dst)
    hl_version = (version << 4) + headerlen
    ip_header = struct.pack('!BBHHHBBH4s4s', hl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
    return ip_header
def synheader(src, dst, prt):
    source = random.randrange(32000,62000,1)    # source port
    seq = 0
    ack_seq = 0
    doff = 5
    # tcp flags
    fin = 0
    syn = 1
    rst = 0
    psh = 0
    ack = 0
    urg = 0
    window = socket.htons (8192)    # maximum window size
    check = 0
    urg_ptr = 0
    offset_res = (doff << 4) + 0
    tcp_flags = fin + (syn<<1) + (rst<<2) + (psh<<3) + (ack<<4) + (urg<<5)
    tcp_header = struct.pack('!HHLLBBHHH', source, prt, seq, ack_seq, offset_res, tcp_flags, window, check, urg_ptr)
    #pseudo header fields
    source_address = socket.inet_aton(src)
    dest_address = socket.inet_aton(dst)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)
    psh = struct.pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    psh = psh + tcp_header
    tcp_checksum = tcpcheck(psh)
    tcp_header = struct.pack('!HHLLBBHHH', source, dst, seq, ack_seq, offset_res, tcp_flags, window, tcp_checksum, urg_ptr)
    return tcp_header
#%%
#pingroute function implements traceroute, stops upon detection of routing loop
#split into list/notlist
def pingroute_list(targets, tryports):
    hoplist = []
    #initialize parameters
    for i in targets:
        ttl = 1
        inc = 0
        port = int(tryports) + inc
        hops = 30
        ipheader = iphdr(host, i)
        tcpheader = synheader(host, i, port)
        packet = ipheader + tcpheader
        for thing in range(len(hops)):
            ssocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
            ssocket.setsockopt(socket.IPPROTO_TCP, socket.IP_HDRINCL, 1, socket.IP_TTL, ttl)
            try:
                ssocket.sendto(packet, (i, port))
            except socket.error:
                pass
            while True:
                rsocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
                rsocket.bind(("", port))
                currentip = None
                currentname = None
                try:
                    __, currentip = rsocket.recvfrom(512)
                    currentip = currentip[0]
                    try:
                        currentname = socket.gethostbyaddr(currentip)[0]
                    except socket.error:
                        currentname = currentip
                except socket.error:
                    pass
                finally:
                   ssocket.close()
                if currentip is not None:
                    currenthost = "%s (%s)" % (currentname, currentip)
                else:
                    currenthost = "*"
                if currentip not in hoplist:
                    print ("%p\t%d\t%s" % (inc, ttl, currenthost))
                    hoplist.append(currentip)
                    ttl += 1
                    inc += 1
                else:
                    print ("Routing loop detected on path to %s. Moving on to next trace." % i)
                    break
                if currentip == i or ttl > hops:
                    break
def pingroute(targets, tryports):
    hoplist = []
    ttl = 1
    inc = 0
    port = int(tryports) + inc
    hops = 30
    ipheader = iphdr(host, targets)
    tcpheader = synheader(host, targets, port)
    packet = ipheader + tcpheader
    for thing in range(len(hops)):
        ssocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        ssocket.setsockopt(socket.IPPROTO_TCP, socket.IP_HDRINCL, 1, socket.IP_TTL, ttl)
        try:
            ssocket.sendto(packet, (targets, port))
        except socket.error:
            pass
        while True:
            rsocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
            rsocket.bind(("", port))
            currentip = None
            currentname = None
            try:
                __, currentip = rsocket.recvfrom(512)
                currentip = currentip[0]
                try:
                    currentname = socket.gethostbyaddr(currentip)[0]
                except socket.error:
                    currentname = currentip
            except socket.error:
                pass
            finally:
               ssocket.close()
            if currentip is not None:
                currenthost = "%s (%s)" % (currentname, currentip)
            else:
                currenthost = "*"
            if currentip not in hoplist:
                print ("%p\t%d\t%s" % (inc, ttl, currenthost))
                hoplist.append(currentip)
                ttl += 1
                inc += 1
            else:
                print ("Routing loop detected on path to %s. Moving on to next trace." % targets)
                break
            if currentip == targets or ttl > hops:
                break
#%%
#call previous
def main():
    try:
        target = input("Enter IP/Hostname for single target, or CIDR format for range: ")
        tryport = input("Enter the port you'd like to try: ")
    except:
        print ('target input failed')
    try:
        pingroutetarget = targetrange(target)
    except:
        print ('target resolution failed')
    try:
        if isinstance(pingroutetarget, list):
            pingroute_list(pingroutetarget, tryport)
        else:
            pingroute(pingroutetarget, tryport)
        print ("All done!!!")
    except:
        print ("Something broke, sorry!!!")
if __name__ == "__main__":
    main()
