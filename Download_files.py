import glob
import pandas as pd
import aiohttp
import asyncio
import os

### specify path to file containing the URLs
#list_pth = 'K:/TextMining/02 Analysis 8/10 TextMining Projects/CSR/CSR Train/02 Supporting Scripts/01 Scripts input/GRI_2017_2020_SAHO.xlsx'
list_pth = 'Code/GRI_2017_2020.xlsx'

###specify Output folder (in this case it moves one folder up and saves in the script output folder)
#pth = 'K:/TextMining/02 Analysis 8/10 TextMining Projects/CSR/CSR Train/02 Supporting Scripts/03 Scripts output/'
pth = 'Code/ScriptOutput/GRI_2017_2020_with_download_status.xlsx'

###Specify path for existing downloads and for the downloaded pdf files
#dwn_pth = 'K:/TextMining/02 Analysis 8/10 TextMining Projects/CSR/CSR Train/02 Supporting Scripts/03 Scripts output/dwn/'
dwn_pth = 'Code/ScriptOutput/dwn'

# Finder ud af om dwn_pth-mappen findes
os.makedirs(dwn_pth, exist_ok=True)

# Downloader pdf filer, og giver et response hvis der er fejl og printer fejlen i terminalen
async def download_pdf(session, url, file_name):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                pdf_content = await response.read()
                with open(file_name, 'wb') as f:
                    f.write(pdf_content)
                print(f'Successfully downloaded {file_name}')
                return True  # Returner True, hvis download var succesfuld
            else:
                print(f'Failed to download {url}: Status {response.status}')
                return False  # Returner False, hvis download fejlede
    except Exception as e:
        print(f'Error downloading {url}: {e}')
        return False  # Returner False ved fejl

async def main():
    df = pd.read_excel(list_pth)
    # Prøver at slette alle rækker med de filer der er downloadet, men det virker ikke
    dwn_files = glob.glob(os.path.join(dwn_pth, "*.pdf")) 
    exist = [os.path.basename(f)[:-4] for f in dwn_files]
    df = df[~df.index.isin(exist)]
    
    df['Downloaded'] = 'No'

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, row in df.iterrows():
            #Bruger Url fra pdf_URL og hvis den ikke findes eller ikke virker bruger den Report Html Address kolonnen i stedet for
            url = row['Pdf_URL'] if pd.notnull(row['Pdf_URL']) else row['Report Html Address']
            if pd.isnull(url):  # Hvis begge URL'er er null, spring over
                print(f'Ingen gyldig URL {i}')
                continue

            # Navngiv filen efter BRnum, hvis BRnum ikke findes bruger den index
            brnum = row['BRnum'] if pd.notnull(row['BRnum']) else f"file_{i}"
            file_name = os.path.join(dwn_pth, f"{brnum}.pdf")
            
            # Tilføj en tuple med (index, download_opgave) til tasks
            tasks.append((i, download_pdf(session, url, file_name)))

            # Stop med at tilføje opgaver, hvis vi har nået 20, opgaver bliver tilføjen uanset omde virker eller ikke virker
            if len(tasks) >= 20:
                break

        # Begræns antallet af samtidige downloads til 10
        while tasks:
            current_tasks = tasks[:10]  # De første 10 opgaver
            tasks = tasks[10:]  # Fjerner de 10 første opgaver fra listen

            results = await asyncio.gather(*(task[1] for task in current_tasks))
            for result, (i, _) in zip(results, current_tasks):
                if result:  # Hvis download var succesfuld opdater downloaded til Yes
                    df.at[i, 'Downloaded'] = 'Yes'

    # Gem den opdaterede DataFrame til en ny Excel-fil
    df.to_excel(pth, index=False)
    print(f'har Gemt den opdaterede Excel fil i mappen {pth}')

if __name__ == "__main__":
    asyncio.run(main())