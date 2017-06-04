import requests, sys, threading, argparse, json


def test_proxycandidates(proxycandidates):
    for proxycandidate in proxycandidates:
        proxies = {'http': proxycandidate}
        try:
            a = requests.get('http://api.ipify.org?format=json',proxies=proxies,timeout=5).text
            try:
                json.loads(a)
                print '--------'
                print proxycandidate
                print a
                print '--------'
            except Exception as e:
                pass
        except Exception as e:
            pass

        sys.stdout.flush()

parser = argparse.ArgumentParser(description='Test proxies')
parser.add_argument('-f', '--filename', dest='fname', action='store', help='file containing proxy list')
parser.add_argument('-N', '--number-of-threads', dest='N', action='store', help='number of threads')

args = parser.parse_args()

fname = args.fname
N = int(args.N)
if None in [fname,N]:
    print 'you have to enter both filename (-f) and number of threads (-N)'
    exit()

with open(fname) as f:
    content = f.readlines()

proxylist = [x.strip() for x in content]

L = len(proxylist)

i = 0
while i <= L:
    sub_proxycandidates = proxylist[i:i+L/N]
    i += L/N
    threading.Thread(target=test_proxycandidates, args=[sub_proxycandidates]).start()
