import urllib

from bs4 import BeautifulSoup
import urllib.request
import re

#%%
data = "DataMining.txt"

#%%
k = 200

IN = open(data)
base = list()
line = IN.readline()
while line != '':
    a = line.split()
    base.append(a[0])
    line = IN.readline()
IN.close()

nbrhd = [page for page in base]
n = 30
b = 0
adj = {}
for page in base:
    b+=1
    try:
        resp = urllib.request.urlopen(page)
    except urllib.error.HTTPError as e:
        continue
    except urllib.error.URLError as e:
        continue
    adj[b] = set()
    c = 0
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        lnk = link['href']
        if re.search("^http", lnk):
            if lnk not in nbrhd:
                nbrhd.append(lnk)
                n+=1
                adj[b].add(n)
            else:
                t = nbrhd.index(lnk) + 1
                adj[b].add(t)
            c+=1
        if c > k/30:
            break
        
#%%

n = -1
adj = {}    
for page in nbrhd:
    n+=1
    try:
        resp = urllib.request.urlopen(page)
    except urllib.error.HTTPError as e:
        if e.code in (..., 403, ...):
            continue
    except urllib.error.URLError as e:
        continue
    adj[n] = set()
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        lnk = link['href']
        if re.search("^http", lnk):
            if lnk in nbrhd and lnk != page:
                t = nbrhd.index(lnk)
                adj[n].add(t)

#%%

for edges in adj:
    adj[edges] = list(adj[edges])

#%%
Itr = 10

vert = len(nbrhd)
auth = []
hub = []
for i in range(vert):
    auth.append(1)
    hub.append(1)

for itr in range(Itr):
    
    auth = [0 for a in auth]
    for u in adj:
        for v in adj[u]:
            auth[v] += hub[u]
    norm = 0
    for a in auth:
        norm += a**2
    norm = norm**0.5
    auth = [a/norm for a in auth]
    
    hub = [0 for h in hub]
    norm = 0
    for u in adj:
        for v in adj[u]:
            hub[u] += auth[v]
        norm += hub[u]**2
    norm = norm**0.5
    hub = [h/norm for h in hub]

#%%
N = 10

au = {}
for i in range(vert):
    au[i] = auth[i]

print("The top " + str(N) + " Authority weights are for the following websites:")
print("Authority Weight \t Hub Weight \t\t Website")
for n in range(N):
    m = max(au, key=lambda key: au[key])
    au.pop(m)
    print(str(auth[m]) +'\t'+ str(hub[m]) +'\t'+ nbrhd[m])

#%%

hu = {}
for i in range(vert):
    hu[i] = hub[i]

print("The top " + str(N) + " Hub weights are for the following websites:")
print("Hub Weight \t\t Authority Weight \t Website")
for n in range(N):
    m = max(hu, key=lambda key: hu[key])
    hu.pop(m)
    print(str(hub[m]) +'\t'+ str(auth[m]) +'\t'+ nbrhd[m])

#%%

for page in nbrhd:
    print(page)
    try:
        resp = urllib.request.urlopen(page)
    except urllib.error.HTTPError as e:
        if e.code in (..., 403, ...):
            print("\n\n")
            continue
    except urllib.error.URLError as e:
        print("\n\n")
        continue
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    try:
        print(soup.find('p').get_text())
    except AttributeError as e:
        print("\n\n")
        continue
    print("\n\n")
