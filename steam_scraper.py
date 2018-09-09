from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re, time, json, os, csv

####################### Config ###############################
# configurable list of games to process
urls = [
        "https://store.steampowered.com/app/570/Dota_2/",
        "https://store.steampowered.com/app/271590/Grand_Theft_Auto_V/",        
        "https://store.steampowered.com/app/582010/MONSTER_HUNTER_WORLD/",
        "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/"
        ]

# place chromedriver.exe in this folder, output will also be written to this folder
working_directory = "C:\\Users\\dongdong\\Source\\Text Mining\\Steam"

# wait time in second
delay = 7
review_delay = 1

# number of scrolls in review section
review_scrolls = 10

#################### End of Config ###########################

os.chdir(working_directory)

# configure selenium
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
driver.set_page_load_timeout(delay)

outputs = []

def make_soup(url):
    driver.get(url)    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # load the review section
    time.sleep(delay)
    data = driver.page_source
    soupdata = BeautifulSoup(data, "html.parser")
    return soupdata

for url in urls:
    # game page section
    soup = make_soup(url)    

    game_name = soup.find_all(class_ = "apphub_AppName")[0].text

    details_block = soup.find_all(class_ = "details_block")
    genre = []
    for details in details_block:
    	for d in details.find_all('a', href = True):
    		    if "genre" in d['href']:    			
    			    genre.append(d.text)
    
    Developer = []
    for details in details_block:
    	for d in details.find_all('a', href = True):
    		    if "developer" in d['href']:    			
    			    Developer.append(d.text)
    
    Publisher = []
    for details in details_block:
    	for d in details.find_all('a', href = True):
    		    if "publisher" in d['href']:    			
    			    Publisher.append(d.text)
    
    Release_Date = soup.find_all("div", class_ = "date")[0].text    
    
    link_browse_all_reviews = soup.find_all(text = re.compile("Browse all "))[0].previous['href']

    game_output = {}
    game_output['name'] = game_name
    game_output['genre'] = genre[0]
    game_output['developer'] = Developer[0]
    game_output['publisher'] = Publisher[0]
    
    # review section
    driver.get(link_browse_all_reviews)
    for i in range(review_scrolls):
        driver.execute_script("window.scrollTo(0, 99999999999999);")
        time.sleep(review_delay)
    data = driver.page_source
    review_soup = BeautifulSoup(data, "html.parser")    
    
    reviews = review_soup.find_all(class_ = "apphub_UserReviewCardContent")
    
    game_review_outputs = []
    for review in reviews:        
        people_found = review.find_all(class_ = "found_helpful")[0].text        
        found_helpful = people_found[0: people_found.find(" people found this review helpful")].strip()
        found_funny =  people_found[people_found.find(" people found this review helpful") + 33 : ].replace(" people found this review funny", "").strip()    
        title = review.find_all(class_ = "title")[0].text
        hours_on_record = review.find_all(class_ = "hours")[0].text.replace(" hrs on record", "")
        date_posted = review.find_all(class_ = "date_posted")[0].text.replace("Posted: ", "")    
        review_body = review.find_all(class_ = "date_posted")[0].next.next.strip()
    
        
        review_output = {}
        review_output['recommended'] = title
        review_output['helpful_count'] = found_helpful
        review_output['funny_count'] = found_funny
        review_output['game_hour'] = hours_on_record
        review_output['review_date'] = date_posted
        review_output['review_content'] = review_body
        
        game_review_outputs.append(review_output)
        
    game_output['reviews'] = game_review_outputs
    outputs.append(game_output)

driver.close()



# write JSON output
with open('steam.json', 'w', encoding='utf-8') as outfile:
    json.dump(outputs, outfile)
    
# write CSV output
with open('games.csv','w', encoding='utf-8') as outfile:
    wr = csv.writer(outfile, lineterminator='\n', quoting=csv.QUOTE_ALL)    
    outfile.write('name,genre,developer,publisher\n')
    for output in outputs:
        wr.writerow([output['name'],output['genre'],output['developer'],output['publisher']])
        
reviews_flatten = []
for output in outputs:
    for review in output['reviews']:
        review['game'] = output['name']
        reviews_flatten.append(review)
        
with open('reviews.csv','w', encoding='utf-8') as outfile:
    wr = csv.writer(outfile, lineterminator='\n', quoting=csv.QUOTE_ALL)    
    outfile.write('game,recommended,helpful_count,funny_count,game_hour,review_date,review_content\n')
    for review in reviews_flatten:
        wr.writerow([review['game'],review['recommended'],review['helpful_count'],review['funny_count'],review['game_hour'],review['review_date'],review['review_content']])
