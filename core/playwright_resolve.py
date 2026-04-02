import asyncio
import csv
from playwright.async_api import async_playwright

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

async def scrape():
    async with async_playwright() as p:
        # Launch headful browser to bypass WAF bot detection
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"Starting Playwright lookup for {len(companies)} companies...")
        
        for idx, comp in enumerate(companies, start=1):
            try:
                print(f"[{idx}/{len(companies)}] Searching: {comp}...")
                search_url = f"https://find-and-update.company-information.service.gov.uk/search/companies?q={comp}"
                
                await page.goto(search_url)
                # Wait for results or 'no results' element
                await page.wait_for_selector("#results, .search-header", timeout=10000)
                
                # Check for list items
                items = await page.query_selector_all("li.results-item")
                if items:
                    first_item = items[0]
                    name_el = await first_item.query_selector("a")
                    sub_el = await first_item.query_selector("p.subtext")
                    
                    company_name = await name_el.inner_text() if name_el else "N/A"
                    sub_text = await sub_el.inner_text() if sub_el else "N/A"
                    
                    company_number = "N/A"
                    if "—" in sub_text:
                         company_number = sub_text.split("—")[0].strip()
                    
                    print(f"Found: {company_name} ({company_number})")
                    results.append([company_number, company_name])
                else:
                    print(f"No results found for {comp}")
                    results.append(["N/A", comp])
                    
            except Exception as e:
                print(f"Error searching {comp}: {str(e)}")
                results.append(["N/A", comp])
            
            await asyncio.sleep(0.5) # rate limits respect
            
        await browser.close()

    # Write output to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['company_number', 'company_name', 'counterparty_type'])
        for res in results:
            if res[0] != "N/A" and any(c.isdigit() for c in res[0]):
                # Clean up any non-digit prefixes (like FC, BR, etc. - keep them if they are valid prefixes!)
                formatted_num = res[0].replace(" ", "")
                writer.writerow([formatted_num, res[1], 'BORROWER'])

    print(f"\nDone! CSV saved to {output_file}")

# Run main
asyncio.run(scrape())
