from requests import get
from bs4 import BeautifulSoup

def extract_rmt_jobs(keyword):
	base_url = f"https://remoteok.com/remote-{keyword}-jobs"
	response = get(base_url, headers={"User-Agent": "Kimchi"})
	if response.status_code!=200:
		print("Can't request website")
	else:
		results = []
		soup = BeautifulSoup(response.text, "html.parser")
		jobs = soup.find_all('tr', class_='job')
		for job in jobs:
			anchors = job.find_all('a')
			anchor = anchors[1]
			link = anchor['href']
			link = f'https://remoteok.com{link}'
			company = job.find('h3', itemprop='name').string
			position = job.find('h2', itemprop='title').string
			location = job.find('div', class_='location')
			location = location.string
			for loc in location:
				if '$' in loc:
					location = "N/A"
			job_data = {
				'company': company.strip(),
				'position': position.strip(),
				'location': location,
				'link': link
			}
			results.append(job_data)
		return results

