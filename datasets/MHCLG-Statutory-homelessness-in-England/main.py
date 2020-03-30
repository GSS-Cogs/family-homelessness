# # MHCLG Statutory homelessness in England 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

# + 
#### Add transformation script here #### 

scraper = Scraper(landingPage) 
scraper.select_dataset(latest=True) 
scraper 