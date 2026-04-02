import requests
from bs4 import BeautifulSoup
import csv
import time
import os

companies = [
    "Creditfix", "FRA", "Evergreen", "Kalibrate", "Seasalt", "MVF", "Air Charter", "Identity",
    "Wasdell", "BVG", "Gluco Rx", "Autovista", "Pharmacy2u", "Adder Tech", "Willerby", "Keys Group",
    "Active Care", "Stokvis Tapes", "Lifetime Training", "The APS Group", "Global Auto", "SSS Super",
    "Cooper & Turner", "Oddballs", "Adaptive Fi", "Neom Organics", "Hill Biscuit", "Crowdcomms",
    "12 Group", "Wowcher", "Whistl", "Deallus Consulting", "Red Industrials", "Advanced Insulation",
    "Camira Group", "Nurseplus", "Momentum", "Gama Healthcare", "Catalis", "Ooni Limited",
    "Trooli", "Citation", "Net Native", "Bladnoch Distillery", "Moda Furn", "The Cotswold",
    "Liberty Steel", "Agilisys", "Mapway", "PetShop.co.uk", "vio Health", "Hallmarq Veterinary",
    "Unisurge", "Albany Beck", "QA Group", "Tiger Tracks", "Peach", "Helping Hands", "Dental Defence",
    "Plurimi Wealth", "Providence", "Camden Market", "Carter Jonas", "ES Broadcast", "Ve Global",
    "Rosemont", "Converger", "TaxCalc", "Omar Group", "Mdgroup", "LB Reusables", "Rocksteady",
    "Nisbets", "Greencore", "Claims Solutions", "Western Group", "London School of Alternative",
    "Medication Cardboards", "Balance Me", "Original Factory", "Piling Equipment", "Red Bee Media",
    "Game Nation", "Finastra", "Peppermint Legal", "Alpha CRC", "John Henry Group", "Sustainability",
    "Giggling Squid", "Marketing Horizon", "Center Parcs", "Babble", "UK Addiction", "Croft Communications",
    "Ascona", "Phoebus Software", "Mamas & Papas", "Blatchford", "Premier Vet", "Viper Innovations",
    "Big Bus Tours", "Nexgen Group", "Clyde Munro", "Restaurant Group", "GenAir UK", "Wondr"
]

results = []
output_file = "resolved_portfolio.csv"

# Free Public Search
search_url = "https://find-and-update.company-information.service.gov.uk/search/companies?q="

print(f"Starting lookup for {len(companies)} companies...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for idx, comp in enumerate(companies, start=1):
    try:
        print(f"[{idx}/{len(companies)}] Searching: {comp}...")
        response = requests.get(search_url + requests.utils.quote(comp), headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Look for the first result card
            results_list = soup.find('ul', id='results')
            if results_list:
                first_item = results_list.find('li', class_='results-item')
                if first_item:
                    name_tag = first_item.find('a')
                    company_name = name_tag.text.strip() if name_tag else "N/A"
                    
                    p_tag = first_item.find('p', class_='subtext')
                    company_number = "N/A"
                    if p_tag:
                         p_text = p_tag.text.strip().replace(" ", "")
                         if "—" in p_text:
                              company_number = p_text.split("—")[0].strip()
                    
                    print(f"Found: {company_name} ({company_number})")
                    results.append([company_number, company_name])
                else:
                    print(f"No results found for {comp}")
                    results.append(["N/A", comp])
            else:
                print(f"No items in results list for {comp}")
                results.append(["N/A", comp])
        else:
            print(f"Failed to search {comp} (Status {response.status_code})")
            results.append(["N/A", comp])
            
        time.sleep(1) # Be nice to rate limits
         
    except Exception as e:
        print(f"Error searching {comp}: {str(e)}")
        results.append(["N/A", comp])

# Write output template
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['company_number', 'company_name', 'counterparty_type'])
    for res in results:
         # Exclude N/A numbers from CSV to keep template valid, or user can fix it
         if res[0] != "N/A" and res[0].isdigit():
             formatted_num = res[0].zfill(8)
             writer.writerow([formatted_num, res[1], 'BORROWER'])

print(f"\nDone! CSV saved to {output_file}")
print("Please review and fix any N/A manual items back before hitting the API upload!")
