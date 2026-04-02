import requests
from bs4 import BeautifulSoup

search_url = "https://find-and-update.company-information.service.gov.uk/search/companies?q=Creditfix"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

response = requests.get(search_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print("Status:", response.status_code)
print("Title:", soup.title.text if soup.title else "No Title")
# Print first 500 chars of body
print("Body Preview:", soup.text[:500].replace("\n", " ") )
