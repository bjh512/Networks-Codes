import nmap, optparse, pprint
import socket
from multiprocessing import Process
 
def NmapScan(TargetHost, TargetPort):
    print("Checking... // IP : {0} // Port : {1}".format(TargetHost, TargetPort))
    nmScan = nmap.PortScanner()
    nmScan.scan(TargetHost, TargetPort, '-T4')
    cnt = 0
    for scannedHost in nmScan.all_hosts():
        if nmScan[scannedHost]['tcp'][int(TargetPort)]['state'] == 'open':
            cnt = cnt + 1
            domain = socket.gethostbyaddr(scannedHost)[0]
            print("{0} : {1}  //  {2}".format(scannedHost, TargetPort, domain))
            #print(socket.gethostbyaddr(scannedHost+":"+TargetPort))
    print("\nTotal number of web servers : {0}".format(cnt))
    print("Scan duration : {0}".format(nmScan.scanstats()['elapsed']))
 
def main():
    parser = optparse.OptionParser(usage='usage %prog -H <TargetHost> -P <TargetPort>')
    parser.add_option('-H', dest = 'TargetHost', type='string', help ='Specify Target Hostname')
    parser.add_option('-P', dest = 'TargetPort', type='string', help = 'Sepcify Target Port')
    (options, args) = parser.parse_args()
 
    TargetHost = options.TargetHost
    TargetPort = str(options.TargetPort).split(',')
 
    if (TargetHost == None) | (TargetPort[0] == None):
        print(parser.usage)
        exit(0)
 
    procs = []

#Non-Multi와 Multi = 106+106 vs 172

    for port in TargetPort:
        p = Process(target=NmapScan, args=(TargetHost, port))
        procs.append(p)
        p.start()
        
    for proc in procs:
        proc.join()

if __name__ == '__main__':
    main()