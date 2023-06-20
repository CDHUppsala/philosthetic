import requests
from bs4 import BeautifulSoup
import time
import os
'''
One example of scraping archive.org
sonata bethoven
Change the base URL to run another search
Change the range according to the number of pages of results
NOTE: Re run the script several times as all the archives are not downloaded systematically
'''

#base_url = 'https://archive.org/details/pub_musical-times?&sort=-week&page='
base_url = 'https://archive.org/details/pub_musical-times?query=beethoven+sonata&sin=TXT&sort=-week&page='
end_url = ""#"&scroll=1"
#user agent
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.65'}

"""
The base_url needs to be changed to get the next page
"""

r = requests.get(base_url, headers=headers)
html = r.text
listOfdivs = []
for i in range(13):#Change the range HERE
    print(i)
    time.sleep(3)
    current_url = base_url+str(i)+end_url
    print(current_url)
    r = requests.get(current_url, headers=headers)
    print(r)
    html += r.text
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', {'class': 'item-ttl'})
    listOfdivs.append(divs)

       

## OBS! The href is not the full url, it is missing the base url
"""
From 
/details/sim_musical-times_1909-10-01_50_800?q=beethoven+sonata
we must get:
https://archive.org/stream/sim_musical-times_1909-10-01_50_800/sim_musical-times_1909-10-01_50_800_djvu.txt
to download the text file

"""
text_urls = []
root_url = 'https://archive.org/details/'
for divs in listOfdivs:
    for div in divs:
        #get the href
        href = div.find('a')['href']
        #get the id
        id = href.split('/')[2]
        id = id.split('?')[0]
        #get the text url
        text_url = root_url + id + '/' + id + '_djvu.txt'
        text_url = text_url.replace('details', 'stream')
        text_urls.append(text_url)
#Always check that all the search results have been collected and remove duplicates
print(len(text_urls))
text_urls = set(text_urls)
print("unique")
print(len(text_urls))
#write the links in a file
with open('archive_urls.txt', 'w') as f:
    for url in text_urls:
        f.write(url)
        f.write('\n')
#TODO: scrape the text from the urls currently not working
# checking if the directory demo_folder 
# exist or not.
if not os.path.exists(".collected"):
      
    # if the demo_folder directory is not present 
    # then create it.
    os.makedirs("collected")
for url in text_urls:
    #scrape the text part of the page
    print(url)
    r = requests.get(url, headers=headers)
    html = r.text
    #get the text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('pre').text
    #write the text to a file
    filename = url.split('/')[-1]
    with open("collected/"+filename, 'w') as f:
        f.write(text)

#https://medium.com/@harshvb7/scraping-from-a-website-with-infinite-scrolling-7e080ea8768e
