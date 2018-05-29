import requests, re
from bs4 import BeautifulSoup
import json

li = dict()
for i in range(0,35):
	if i == 0:
		req = requests.get('https://ics-cert.us-cert.gov/advisories')
	else:
		req = requests.get('https://ics-cert.us-cert.gov/advisories?page='+str(i))

	html = req.text
	soup = BeautifulSoup(html, 'html.parser')

	vul = soup.find_all('span', class_="field-content")

	for j in range(len(vul)):
		if j%2==1:
			print(vul[j-1].text)
			try:
				int(vul[j-1].text[-1])
				req_detail = requests.get('https://ics-cert.us-cert.gov/advisories/'+vul[j-1].text)	
			except:
				req_detail = requests.get('https://ics-cert.us-cert.gov/advisories/'+vul[j-1].text[:-1])
			
			html_detail = req_detail.text
			soup_detail = BeautifulSoup(html_detail, 'html.parser')

			li[vul[j-1].text] = {"title" : vul[j].text}

			try:
				for i in soup_detail.find_all('ul')[2]:
					spl = i.text.split(": ")
					#print(spl)
					
					p = re.compile('CVSS*')
					m = p.match(spl[0])
					
					if m:
						continue

					#print(spl)
					li[vul[j-1].text][spl[0]] = spl[1]
			except:
				try:
					spl = soup_detail.find_all('li',class_='footnote')[0].text.split(". ")[1].split(",")[0].split(": ")
					#print(spl)
					li[vul[j-1].text]["vulnerability"] = spl
				except:
					pass

js = json.dumps(li, indent=4)
f = open("ics-cert-vulnerability.json",'w')
print(js, file=f)