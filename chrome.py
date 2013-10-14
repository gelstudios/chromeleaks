import urllib2
import json
import socket

URL='https://chrome.com/giveachromebook/submission_categories' #?lc=en_US&cursor=false
GEO='http://freegeoip.net/json/'

request = urllib2.urlopen(URL)
data = json.load(request)
priv = dict()

for s in data[u'submissions']:
    feat = s.get(u'featured')
    if feat:
        cat = list()
        for f in feat:
            tmp = {
            'name':f[u'first_name'],
            'img':f[u'rendered_url'],
            'ip':f[u'remote_addr'],
            'winner':f[u'is_winner']
            }
            try:
                hostname = socket.gethostbyaddr(f[u'remote_addr'])
                if hostname:
                    tmp['hostname'] = hostname[0]
            except:
                pass
            gurl = GEO
            if len(tmp['ip']) > 16 and tmp.get('hostname'):
                gurl += tmp['hostname']
            else:
                gurl += tmp['ip']
            try:
                print 'using '+gurl
                req = urllib2.urlopen(gurl)
                g = json.load(req)
                geod = {
                'city':g['city'],
                'region':g['region_name'],
                'country':g['country_code'],
                'lat':g['latitude'],
                'long':g['longitude']
                }
                tmp.update(geod)
            except:
                pass
                
            cat.append(tmp)
        priv[s[u'category']] = cat

f = open('data.json',"w")
f.write(json.dumps(priv, sort_keys=True, indent=2))
f.close()