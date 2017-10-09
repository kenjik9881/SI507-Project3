from bs4 import BeautifulSoup
# from urllib2 import urlopen
import unittest
import requests

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
try:
  cat_data = open("cat.html",'r').read()
except:
  cat_data = requests.get("http://newmantaylor.com/gallery.html").text
  f = open("cat.html",'w')
  f.write(cat_data)
  f.close()

cat_soup = BeautifulSoup(cat_data, 'html.parser')

all_cat_imgs = cat_soup.find_all('img')
for i in all_cat_imgs:
	print(i.get('alt',"No alternative text provided!"))

######### PART 1 #########

# Get the main page data...
try:
  nps_gov_data = open("nps_gov_data.html",'r').read()
except:
  nps_gov_data = requests.get("https://www.nps.gov/index.htm").text
  f = open("nps_gov_data.html",'w')
  f.write(nps_gov_data)
  f.close()

gov_soup = BeautifulSoup(nps_gov_data, 'html.parser')

the_links = gov_soup.find_all('a')

state_part = gov_soup.find("ul",{"class":"dropdown-menu SearchBar-keywordSearch"})

all_state_links = state_part.find_all('a')

selected_states = ['Michigan', 'Arkansas', 'California']
for item in all_state_links:
  state_name = item.text
  if state_name in selected_states:
    state_link = "https://www.nps.gov" + item.get('href')
    file_name = state_name.lower() + "_data.html"
    try:
      state_name_data = open(file_name, 'r').read()
    except:
      state_name_data = requests.get(state_link).text
      f = open(file_name,'w')
      f.write(state_name_data)
      f.close()

michigan_data = open("michigan_data.html", "r").read()
michigan_soup = BeautifulSoup(michigan_data, 'html.parser')

arkansas_data = open("arkansas_data.html", "r").read()
arkansas_soup = BeautifulSoup(arkansas_data, 'html.parser')

california_data = open("california_data.html", "r").read()
california_soup = BeautifulSoup(california_data, 'html.parser')


# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.





# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.

# TRY:
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.



######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...


## Define your class NationalSite here:

def get_park_list(state_soup): #getting a list of all the parks in state
  soup_list = state_soup.find("ul", {"id":"list_parks"}).find_all("li", {"class":"clearfix"})
  return soup_list

class NationalSite(object):
  def __init__(self, park_soup):
      self.location = park_soup.find("h4").get_text()
      self.name = park_soup.find("h3").get_text()
      links = park_soup.find_all('a')[2]
      self.url = links['href']
      try:
        self.type = park_soup.find("h2").get_text()
        self.description = park_soup.find("p").get_text().strip()
      except:
        self.type = "None"
        self.description = "None"


  def __str__(self):
    return "{} | {}".format(self.name, self.location)

  def __contains__(self, astring):
    return astring in self.name

  def get_mailing_address(self):
    try:
      park_html_data = requests.get(self.url)
      basic_info_soup = BeautifulSoup(park_html_data.content, 'html.parser')
      full_address_block = basic_info_soup.find('div', {"itemprop": "address"})
      street_address = full_address_block.find('span', {"itemprop": "streetAddress"}).text.strip()
      city = full_address_block.find('span', {"itemprop": "addressLocality"}).text.strip()
      state = full_address_block.find('span', {"itemprop": "addressRegion"}).text.strip()
      zip_code = full_address_block.find('span', {"itemprop": "postalCode"}).text.strip()
      mail_address = street_address + " / " + city + " / " + state + " / " + zip_code
      return mail_address
    except:
      return ""


sample_alcatraz = get_park_list(california_soup)[0] #test function
sample_class = NationalSite(sample_alcatraz) #test class

print(sample_class)
print(sample_class.url)


print(sample_class.get_mailing_address())

# sample_test = NationalSite(california_soup)
# sample_test2 = NationalSite(arkansas_soup)
# # #
# print(sample_test)
# print(sample_test2)

#National Park/Site/Monument Name | Location

## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.


# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

ark_list = get_park_list(arkansas_soup)
cal_list = get_park_list(california_soup)
mi_list = get_park_list(michigan_soup)

arkansas_natl_sites = []
for item in ark_list:
  x = NationalSite(item)
  arkansas_natl_sites.append(x)

california_natl_sites = []
for item in cal_list:
  x = NationalSite(item)
  california_natl_sites.append(x)

michigan_natl_sites = []
for item in mi_list:
  x = NationalSite(item)
  michigan_natl_sites.append(x)

#Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########
import csv
with open("arkansas.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        f.write("Name, Location, Type, Address, Description\n")
        for obj in arkansas_natl_sites:
		        writer.writerow([obj.name, obj.location, obj.type, obj.get_mailing_address(), obj.description])

with open("california.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        f.write("Name, Location, Type, Address, Description\n")
        for obj in california_natl_sites:
		        writer.writerow([obj.name, obj.location, obj.type, obj.get_mailing_address(), obj.description])

with open("michigan.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        f.write("Name, Location, Type, Address, Description\n")
        for obj in michigan_natl_sites:
		        writer.writerow([obj.name, obj.location, obj.type, obj.get_mailing_address(), obj.description])

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
