"""
This file does the web scraping of food nutrition of Pizza Hut's menu items
and stores it in a csv file

@author: Ritika Prasad
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import csv


nutrition_url = 'https://m.nutritionix.com/pizza-hut/menu/premium/'
browser = webdriver.Chrome()
browser.get(nutrition_url)
time.sleep(1)#wait for the page to load

#expand all view-more
viewMore = browser.find_elements_by_class_name("viewMore")
for v in viewMore:
	v.click()
	time.sleep(3)
itemCount = len(browser.find_elements_by_class_name("ui-li-has-count"))

#save the main window
main_window = browser.current_window_handle

with open('../NutritionData/PizzaHut_NutritionData.csv', 'a', newline="") as csv_file:
	writer = csv.writer(csv_file)
	count = 0
	while count < itemCount:
		#find the element having link to each menu item
		item = browser.find_elements_by_class_name("ui-li-has-count")[count]

		#open the link of each item in new tab
		link = item.find_element_by_tag_name('a')
		link.send_keys(Keys.CONTROL,Keys.RETURN)
		for window in browser.window_handles:
			if(window != main_window):
				side_window = window
		browser.switch_to_window(side_window)

		time.sleep(1)#wait for the page to load

		#we are now on nutrient page
		#use beautiful soup to extract the nutrient content
		
		soup = BeautifulSoup(browser.page_source, 'html.parser')
		
		#product name
		product = soup.find('div', attrs={'class':'name'})
		if product != None:
			product = product.text
		else:
			#nutrition content doesnt exist for this item => go to next item
			#close tab and switch to main window
			browser.close()
			browser.switch_to_window(main_window)
			time.sleep(1)#wait for the page to load
			count += 1
			continue

		#serving size
		servingSize = soup.find(itemprop="servingSize")
		if servingSize != None:
			servingSize = servingSize.text.split()[0]
		else:
			servingSize = "N/A"

		foodDict = {}
		#fat content
		fat = soup.find(itemprop="fatContent").text.split()
		foodDict["Total Fat"] = fat[0] if(fat[0] != "<") else fat[1]
		#Carbohydrates
		carbs = soup.find(itemprop="carbohydrateContent").text.split()
		foodDict["Carbohydrates"] = carbs[0] if(carbs[0] != "<") else carbs[1]
		#Proteins
		proteins = soup.find(itemprop="proteinContent").text.split() 
		foodDict["Protein"] = proteins[0] if(proteins[0] != "<") else proteins[1]
		#Sugar
		sugar = soup.find(itemprop="sugarContent").text.split()
		foodDict["Sugar"] = sugar[0] if(sugar[0] != "<") else sugar[1]
		#Fiber
		fiber = soup.find(itemprop="fiberContent").text.split()
		foodDict["Fiber"] = fiber[0] if(fiber[0] != "<") else fiber[1]
		#Sodium
		sodium = soup.find(itemprop="sodiumContent").text.split() 
		foodDict["Sodium"] = sodium[0] if(sodium[0] != "<") else sodium[1]
		#Cholesterol
		cholesterol = soup.find(itemprop="cholesterolContent").text.split()
		foodDict["Cholesterol"] = cholesterol[0] if(cholesterol[0] != "<") else cholesterol[1]
		#Calories
		calories = soup.find(itemprop="calories").text.split()
		foodDict["Calories"] = calories[0] if(calories[0] != "<") else calories[1]
		#Saturated Fat
		saturatedFat = soup.find(itemprop="saturatedFatContent").text.split()
		foodDict["Saturated Fat"] = saturatedFat[0] if(saturatedFat[0] != "<") else saturatedFat[1]
		#Trans Fat
		transFat = soup.find(itemprop="transFatContent").text.split()
		foodDict["Trans Fat"] = transFat[0] if(transFat[0] != "<") else transFat[1]

		#write header
		if(count == 0):
			header = ["Item", "Serving Size"]
			header.extend(list(foodDict.keys()))
			writer.writerow(header)
		
		#write product name and nutrition content values
		rowEntry = [product, servingSize]
		rowEntry.extend([value for key,value in foodDict.items()])
		writer.writerow(rowEntry)

		#close tab and switch to main window
		browser.close()
		browser.switch_to_window(main_window)
		time.sleep(1)#wait for the page to load
		count += 1
	#close main window
	browser.close()