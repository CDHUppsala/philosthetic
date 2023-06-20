## Prerequisites with Virtual env
If you use virtual env you can directly run these commands:
```bash
cd path/to/philosthetic
#Initiate your environment (only run the first time)
python3 -m venv .env
source .env/bin/activate 
pip install -r requirements.txt
#activate your environment
source .env/bin/activate 

```
## Content
- scrape_archive.py : based on a link of search downloads all the corporas in txt format output both an excel and all the corpora collected.
- clean_archive.sh simple script to remove year based catalogs
- stripper.py 
- sitemap.json
- gale_All.csv collected via sitemap.json used on webscraper.io
- archive.csv
- nineteenth.csv
- get_adjectives.py count the number of interesting adjectives and puts
this count per adjectives in the databasis
- fusion_2_ridgeline.png makes the graphics out of "fusion_adj_decade.csv"

# collect of the data basis
nineteenth.csv comes from the following query and was collected with webscraper.io. 
[http://c19index.chadwyck.com/displayCollectionsResults.do?queryType=quick&activeMultiResults=periodicals&forward=quickfull&pageSize=600&PageNumber=1](http://c19index.chadwyck.com/displayCollectionsResults.do?queryType=quick&activeMultiResults=periodicals&forward=quickfull&pageSize=600&PageNumber=1)


# Description


# Usage


# Context


# Authors:
Original project of [AnnaCarin Billing](https://www.katalog.uu.se/empinfo/?id=N96-2024). Pilot project at CDHU
Engineer:
Marie Dubremetz
Gitlab:
[@mardub](https://gitlab.com/mardub)
Github:
[@mardub1635](https://github.com/mardub1635)
Website:
[http://www.uppsala.ai](http://www.uppsala.ai)
e-mail:
mardubr-github@yahoo.com

