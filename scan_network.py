import nmap
import optparse
import pprint
from multiprocessing import Pool
from itertools import product
 
def NmapScan(TargetHost, TargetPort):
    print(TargetHost, TargetPort)
    nmScan = nmap.PortScanner()
    pprint.pprint(nmScan.scan(TargetHost, TargetPort[0]))
    
 
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
 
    pool = Pool(processes = 1)
    for port in TargetPort:
        print(TargetHost, TargetPort)
        pool.starmap(NmapScan(TargetHost, TargetPort))
        #NmapScan(TargetHost, port)
 
if __name__ == '__main__':
    main()


#cd "C:\Users\Juhyeok\Google 드라이브\18-1\Information Security"