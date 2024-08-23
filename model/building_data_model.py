import mysql.connector
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import make_response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

class building_data_model():

            

            

    def __init__(self):
        
        
        
        self.headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
        #connection establishment code

        
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="HETul@906", database="demo_scrapper")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print("connection successful")
        except :
            print("error in database connection")

    def request(self, x):
        baseurl = f'https://duproprio.com/en/search/list?search=true&parent=1&pageNumber=1&sort=-published_at'
        self.baseur = baseurl
        r = requests.get(baseurl, headers = self.headers)
        soup = BeautifulSoup(r.content, features = 'html.parser')
        return soup.find_all('li', class_='search-results-listings-list__item')
    
    # def extract_image_url_from_html(self.html):



    def parser(self, listings) : 
        propertylinks = []
        properties = []
        
        for property in listings :
            # print(property)
            # break
            # if property.find('li', class_='ad-zone search-results-listings-list__item') :
            #     print("helo we are in list of ad")
            #     continue
            if property.get('class') and 'ad-zone' in property.get('class'):
                print("Skipping ad block")
                continue
            link = property.find('a', class_='search-results-listings-list__item-image-link')
            propertylinks.append(link['href'])
            print(len(propertylinks))
                    
            # for link in property.find_all('a', href='true') :
            #     propertylinks.append(link['href'])
            #     print(link['href'])
            # selling_price = property.find({})
        for link in propertylinks:
            property_details = {}
            r = requests.get(link, headers=self.headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            # Extract the price
            price = soup.find('div', class_='listing-price__amount').text.strip()
            year_of_construction = '' 
            style = soup.find('p', class_='listing-location__title').text.strip()[:-9]
            location_code = soup.find('h2', class_='listing-location__code')
            building_dimensions = ''
            external_facing = soup.find('img', class_='photo-viewer__image')
            srcset=''
            
            
            #set up selenium webdriver
            chrome_option = Options()
            chrome_option.add_argument("--headless")

            service = Service("D:\HETUL\paul tech\chromedriver-win64\chromedriver-win64\chromedriver.exe")
            driver = webdriver.Chrome(service = service, options=chrome_option)
            driver.get(link)
            # html=driver.page_source
          
            # onetrust-accept-btn-handler
            # WebDriverWait(driver, 10).until(
            #     EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe'))
            # )
            html = driver.page_source
            sou = BeautifulSoup(html, 'html.parser')

            image_ele = sou.find('img', class_='photo-viewer__image')
            print("image is here")
            print(image_ele)
            img_ur = ''
            if image_ele:
                src = image_ele.get('data-lazy') 
                if src :
                    print(f"image url : {src}")
                    property_details['external_facing'] = src
                else :
                    print("image url not found")
            else :
                print("image element not found.")

            # if srcset :
            
            #     srcset_urls = srcset.split(',')
            #     for url in srcset_urls:
            #         url = url.strip()
            #         print(url)
            #         if url.endswith('600w'):
            #             print("600w inside: "+url)
            #             property_details['external_facing'] = url.split(' ')[0]
            #             break

            property_details['external_facing'] = property_details.get('external_facing', '')
    
#             try :
               

#                 cookie_button = WebDriverWait(driver,30).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler'))
# # onetrust-accept-btn-handler
#                 )
#                 cookie_button.click()
#                 print("Cookie consent button clicked.")
#                 # driver.switch_to.default_content()
            
#             except Exception as e:
#                 print(f"Cookie consent button not found or not clickable: {e}")

#             try :

#                 # driver.get(link)
#                 # time.sleep(5)
#                 image_element = WebDriverWait(driver, 30).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, '#react-component-PhotoViewer'))
# # photo-viewer__image
#                 )
#                 print("image element "+image_element)

#                 #fetch the 'srcset attribute
#                 # src = image_element.get_attribute('src')
#                 # print("src:", src)
#             except Exception as e:
#                 print(f"An error occured: {e}")

#             finally:
               
#                 # print("html : "+html)
#                 # with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
#                 #     writer = csv.writer(file)
#                 #     writer.writerow(['HTML Content'])
#                 #     writer.writerow([html])

#                 print("HTML content written to output.csv")
#                 driver.quit()  
#             # print("src is here : " + src)
#             # property_details['external_facing'] = src  

#             # try:
#             #     image_element = driver.find_element(By.CSS_SELECTOR, '#react-component-PhotoViewer')
#             #     property_details['external_facing'] = image_element.get_attribute('srcset')
#             # except Exception as e:
#             #     print(f"Could not find image for : {str(e)}")
#             #     property_details['external_facing'] = None
            
#             print("check over here")
           
            if location_code : 
                location_code = location_code.text.strip()
            # print(style)
            details = {}
            # print(f'location_code {location_code}')
            
                
            # Corrected class name
            for row in soup.find_all('div', class_='listing-box__dotted-row'):
                label = row.find_all('div')[0].get_text(strip=True)
                value = row.find_all('div')[2].get_text(strip=True)
                details[label] = value
            

             ################################


            ################################################################
            # Define a dictionary to store the characteristics
            property_characteristics = {}

            lot_dimensions_elements = soup.find_all('div', class_='listing-main-characteristics__item--lot-dimensions')
            lot_dimensions = [elem.find('span', class_='listing-main-characteristics__number listing-main-characteristics__number--dimensions').text.strip() for elem in lot_dimensions_elements]
            
            property_details['Lot Dimensions'] = lot_dimensions[0] if len(lot_dimensions) > 0 else None

            

           
            
            # # Extract number of bedrooms
            bedroom_elements = soup.find_all('div', class_='listing-main-characteristics__item')
            bedroom_counts = [elem.find('span', class_='listing-main-characteristics__number').text.strip() for elem in bedroom_elements if 'bedrooms' in elem.find('span', class_='listing-main-characteristics__title').text.lower()]
            property_details['Bedrooms'] = bedroom_counts[0] if len(bedroom_counts) > 0 else None

            # Extract number of bathrooms
            bathroom_elements = soup.find_all('div', class_='listing-main-characteristics__item--bathrooms')
            bathroom_counts = [elem.find('span', class_='listing-main-characteristics__number').text.strip() for elem in bathroom_elements]
            property_details['Bathrooms'] = bathroom_counts[0] if len(bathroom_counts)>0 else None

            # Extract number of levels
            level_elements = soup.find_all('div', class_='listing-main-characteristics__item')
            level_counts = [elem.find('span', class_='listing-main-characteristics__number').text.strip() for elem in level_elements if 'levels' in elem.find('span', class_='listing-main-characteristics__title').text.lower()]
            property_details['Levels'] = level_counts[0] if len(level_counts)>0 else None

            # Extract living space area
            living_space_elements = soup.find_all('div', class_='listing-main-characteristics__item--living-space-area')
            living_space_area = [elem.find('span', class_='listing-main-characteristics__number listing-main-characteristics__number--dimensions').text.strip() for elem in living_space_elements]
            property_details['Living Space Area'] = living_space_area[0] if len(living_space_area) > 0 else None


            # print( property_characteristics)     
            
            
            print()
               
                
            for label, value in details.items():
                if label == 'Year of construction' :
                    year_of_construction = value

                if label == 'Building dimensions' :
                    building_dimensions = value    
                # print(f"{label} : {value}")
                            # print(price)
            # print(year_of_construction)
            # print(f'building dimension {building_dimensions}')
            if price :
                print(price)
                property_details['selling_price'] = float(price.replace('$', '').replace(',', ''))
            if year_of_construction :

                property_details['year_of_construction'] = int(year_of_construction)
            else :
                property_details['year_of_construction'] = 0    
            property_details['style'] = style
            property_details['building_dimensions'] = building_dimensions
            property_details['location_code'] = location_code
            # print(property_details)
            properties.append(property_details)
            print(property_details['selling_price'], property_details['year_of_construction'])
            
        return properties    

    def scrape_data_model(self):
        print("check model")
        
        x = 1
               
        listings = self.request(x)
        properties = self.parser(listings)
        print(properties)
        # print(listings)
        print(len(properties))
        
        for data in properties :
            sql_query = (
                f"INSERT INTO properties(lot_dimensions, bedrooms, bathrooms, levels, living_space_area, "
                f"selling_price, year_of_construction, style, building_dimensions, location_code, external_facing) VALUES ("
                f"'{data['Lot Dimensions']}',"
                f"'{data['Bedrooms']}',"
                f"'{data['Bathrooms']}',"
                f"'{data['Levels']}',"
                f"'{data['Living Space Area']}',"
                f"{data['selling_price']},"
                f"{data['year_of_construction']},"
                f"'{data['style']}',"
                f"'{data['building_dimensions']}',"
                f"'{data['location_code']}',"
                f"'{data['external_facing']}')"
            )


            self.cur.execute(sql_query)
            print(x)
            x = x+1
        return make_response({"message":properties},201)

    def get_properties_model(self, lowest_price, recently_built, style):

       

        query = "SELECT * FROM properties  WHERE 1 = 1 "

        if lowest_price :
            query += f" ORDER BY selling_price ASC "

        if recently_built :
            if "ORDER BY" in query :
                query = query.replace("ORDER BY", "ORDER BY year_of_construction DESC, ")
            else :
                query += f" ORDER BY year_of_construction DESC"

        if style :
            if "ORDER BY" in query :
                query = query.replace("ORDER BY", f"AND style = '{style}' ORDER BY")
            else :
                query += f" AND style = '{style}'"

        self.cur.execute(query)
        result = self.cur.fetchall()

        if len(result) > 0 :
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else :
            return make_response({"message": "No Data Found"}, 204)


    def properties_del_model(self):
        self.cur.execute(f"DELETE FROM properties")
        if self.cur.rowcount>0:
            return make_response({"message": "Properties data deleted successfully"}, 200)
        else :
            return make_response({"message": "Nothing to Delete"}, 202)


            