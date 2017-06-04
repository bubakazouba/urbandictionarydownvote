import requests, sys, threading, argparse, json

def read_list_from_file(fname):
    with open(fname) as f:
        content = f.readlines()

    return [x.strip() for x in content]

def downvote_url_with_list(url, proxy_list, len_of_all_proxy_list, thread_number):
    global proxies_failed, proxies_succeeded, now_down, first_down
    for proxy in proxy_list:
        proxies_failed += 1
        proxies = {'http': proxy}
        try:
            a = json.loads(requests.get(url,proxies=proxies,timeout=5).text)
            try:
                proxies_succeeded += 1 if a["status"] == "saved" else 0
                now_down = a["down"]
                if first_down == None: first_down = now_down
            except Exception as e: pass
        except Exception as e: pass
        if None not in [first_down, now_down]:
            print '%d: %d/%d/%d. Down: %d-->%d' % (thread_number, proxies_succeeded, proxies_failed, len_of_all_proxy_list, first_down, now_down)
        sys.stdout.flush()

parser = argparse.ArgumentParser(description='Test proxies')
parser.add_argument('-f', '--proxylist-filename', dest='proxy_fname', action='store', help='file containing proxy list')
parser.add_argument('-x', '--urls-filename', dest='urls_fname', action='store', help='file containing urls')
parser.add_argument('-N', '--number-of-threads', dest='N', action='store', help='number of threads')

args = parser.parse_args()

urls_fname = args.urls_fname
proxy_fname = args.proxy_fname
N = int(args.N)

if None in [urls_fname,proxy_fname]:
    print 'you have to enter proxy filename (-f) and urls filename (-x) and number of threads (-N)'
    exit()

proxy_list = read_list_from_file(proxy_fname)
urls_list = read_list_from_file(urls_fname)

L = len(proxy_list)

print urls_list
for url in urls_list:
    proxies_failed =  proxies_succeeded = 0
    first_down = now_down = None

    print url
    print 'success-failure/total. Down: started_with-->now_at'
    i = 0
    thread_number = 0
    threads = []
    while i <= L:
        sub_proxy_list = proxy_list[i:i+L/N]
        i += L/N
        thread_number += 1
        threads.append(threading.Thread(target=downvote_url_with_list, args=[url, sub_proxy_list, L, thread_number]))
        threads[-1].start()
    print 'going to join nowwww'
    for thread in threads:
        print 'trying to join...'
        thread.join()
        print 'joined!!!!!!!!!!'
    print '---------------  done with url: '+url

    # join all threads before going to next url