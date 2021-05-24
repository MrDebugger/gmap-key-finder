from requests import get
import json,csv,art,re
from bs4 import BeautifulSoup as bs
art.tprint("GMap Key Finder")
cookies = {a['name']:a['value'] for a  in json.load(open('cookies.json'))}

def verify(key):
	r = get('https://maps.googleapis.com/maps/api/geocode/json?address=shabqadar&key='+key)
	if r.json().get('status') in ['OK','ZERO_RESULTS']:
		return "Working"
	if 'referer' in r.json().get('error_message','').lower():
		return "Referer"
	if 'not authorized' in r.json().get('error_message','').lower():
		return "Other"
	return 'Expired'
allKeys = []
f1 = open('Other Keys.csv','w',encoding='utf-8',newline='')
f2 = open('Referer Keys.csv','w',encoding='utf-8',newline='')
f3 = open('Expired Keys.csv','w',encoding='utf-8',newline='')
f4 = open('Working Keys.csv','w',encoding='utf-8',newline='')
files = {
		'Other': csv.writer(f1),
		'Referer': csv.writer(f2),
		'Expired': csv.writer(f3),
		'Working': csv.writer(f4),
		}
url = "https://github.com/search?&q=maps.googleapis.com+key%3D&s=indexed&type=Code"
print("[=] Getting Filters")
r = get(url,cookies=cookies)
soup = bs(r.text,'html.parser')
for filt in soup.findAll('a',class_='filter-item')[::-1]:
	filt.span.extract() if filt.span else None
	print("[+] Filter:",filt.text.strip())
	for page in range(1,101):
		print("\t[+] Page",page)
		r = get('https://github.com'+filt['href']+f'&o=asc&p={page}',cookies=cookies)
		soup = bs(r.text,'html.parser')
		codes = soup.findAll(class_='code-list-item')
		links = soup.findAll(class_='f4')
		for link,code in zip(links,codes):
			code = '\n'.join([a.text for a in code.findAll(class_='blob-code')])
			if 'key=' not in code:
				continue
			keys = re.findall('AIza[0-9A-Za-z\\-_]{35}',code)
			for key in keys:
				if key in allKeys:
					continue
				status = verify(key)
				print(f'\t\t[{len(allKeys)+1}]',key,status)
				files[status].writerow([key,'https://github.com/'+link.a['href']])
				allKeys.append(key)
	print()