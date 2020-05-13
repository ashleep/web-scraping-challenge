def scrape():
    
    #!/usr/bin/env python
    # coding: utf-8

    # In[1]:


    # Dependencies
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser
    import pandas as pd
    from selenium import webdriver
    import time


    # In[3]:


    # Get Most recent NASA News Title

    driver_path = r'/Users/apounds/Desktop/Bootcamp/Notes/chromedriver'
    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get("https://mars.nasa.gov/news/")
    time.sleep(2)
    get_element  = browser.find_elements_by_class_name("image_and_description_container")
    time.sleep(2)
    NASA_html = get_element[0].get_attribute('innerHTML')
    time.sleep(2)
    NASAsoup = bs(NASA_html, 'html.parser')
    time.sleep(2)
    NASA_News_Title = NASAsoup.find('h3').text.strip()
    NASA_News_Paragraph = NASAsoup.find(class_='article_teaser_body').text.strip()



    browser.close()


    print(NASA_News_Title)
    print(NASA_News_Paragraph)



    # In[4]:


    # Get JPL Mars Space Images - Featured Image

    driver_path = r'/Users/apounds/Desktop/Bootcamp/Notes/chromedriver'
    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    time.sleep(2)

    browser.find_element_by_css_selector('.button').click()
    time.sleep(2)

    img_site_html = browser.find_elements_by_class_name("fancybox-inner")

    image_url = browser.find_element_by_class_name("fancybox-image").get_attribute('src')
    print(image_url)



    browser.close()


    # In[5]:

    # Get Mars Weather
    driver_path = r'/Users/apounds/Desktop/Bootcamp/Notes/chromedriver'
    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get("https://twitter.com/marswxreport?lang=en")

    time.sleep(2)
    get_element = browser.find_elements_by_class_name("css-1dbjc4n")
    # for i in range(0,len(get_element)-1):
    #     print(f"#{i} = {get_element[i].get_attribute('innerHTML')}")
    #     print(" ")
    #     print(" ")
    time.sleep(2)
    twitter_html = get_element[137].get_attribute('innerHTML')
    time.sleep(2)
    twittersoup = bs(twitter_html, 'html.parser')
    time.sleep(2)
    tweet = twittersoup.find('span').text.strip()


    print(tweet)


    browser.close()


    # In[6]:


    # Get Mars Facts
    url_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_facts)
    facts_table = tables[0]

    facts_table.columns=["0","values"]

    facts_table = facts_table.set_index("0")
        
    html_facts = facts_table.to_html(index_names=False)
    print(html_facts)


    # In[7]:


    # Get Mars Hemispheres
    hemis_list = ["Cerberus Hemisphere", "Schiaparelli Hemisphere", "Syrtis Major Hemisphere", "Valles Marineris Hemisphere"]

    img_url_list=[]
    name_list = []

    for item in hemis_list:
        executable_path = {'executable_path': '/Users/apounds/Desktop/Bootcamp/Notes/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_hemi)
        browser.click_link_by_partial_text(item)
        
        html_hemis = browser.html
        soup_hemis = bs(html_hemis, 'lxml')
        img = soup_hemis.body.find_all(class_="wide-image")
        img = img[0].attrs['src']
        img_url_list.append("https://astrogeology.usgs.gov"+img)
        name = soup_hemis.body.find_all('h2')
        name = name[0].text.strip()
        name = name.replace(" Enhanced","")
        name_list.append(name)

            
    hemi_dict=[
        {"title": name_list[0], "img_url":img_url_list[0]},
        {"title": name_list[1], "img_url":img_url_list[1]},
        {"title": name_list[2], "img_url":img_url_list[2]},
        {"title": name_list[3], "img_url":img_url_list[3]},
    ]
    print(hemi_dict)


    # In[9]:


    data={}

    data["NewsTitle"] = NASA_News_Title
    data["NewsText"] = NASA_News_Paragraph
    data["JPLImg"] = image_url
    data["Weather"] = tweet
    data["Facts"] = html_facts
    data["Hemis1Name"] = hemi_dict[0]["title"]
    data["Hemis1URL"] = hemi_dict[0]["img_url"]
    data["Hemis2Name"] = hemi_dict[1]["title"]
    data["Hemis2URL"] = hemi_dict[1]["img_url"]
    data["Hemis3Name"] = hemi_dict[2]["title"]
    data["Hemis3URL"] = hemi_dict[2]["img_url"]
    data["Hemis4Name"] = hemi_dict[3]["title"]
    data["Hemis4URL"] = hemi_dict[3]["img_url"]




    return data




