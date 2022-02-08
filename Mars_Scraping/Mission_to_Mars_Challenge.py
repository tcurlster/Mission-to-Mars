#!/usr/bin/env python
# coding: utf-8

# In[241]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[242]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[243]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[244]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[245]:


slide_elem.find('div', class_='content_title')


# In[246]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[247]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[248]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[249]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[250]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[251]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[252]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[253]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[254]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[255]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[281]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[282]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Parse the HTML
html = browser.html
hemi_soup = soup(html, 'html.parser')

#Retrieve all results
results = hemi_soup.find_all('div', class_='item')


# Loop through all results
for result in results:
    # Store title
    title = result.find('h3').text
    
    # Create & store ending URL for image
    end_img_url = result.find('a', class_='itemLink product-item')['href']
    
    # Visit link with full image 
    browser.visit(url + end_img_url)
    
    # Object of each hemisphere from site
    end_img_html = browser.html
    
    #Parse each hemisphere from site
    img_soup = soup(end_img_html, 'html.parser')
    
    # Retrieve full image
    img_url = url + img_soup.find('img', class_='wide-image')['src']

    # Append title and image to hemisphere dictionary
    hemisphere_image_urls.append({"img_url" : img_url, "title" : title})


# In[283]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[284]:


# 5. Quit the browser
browser.quit()


# In[ ]:




