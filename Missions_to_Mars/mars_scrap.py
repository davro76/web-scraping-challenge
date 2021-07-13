# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Executable path to driver
    executable_path={"executable_path":ChromeDriverManager().install()}
    browser=Browser("chrome",**executable_path,headless=False)

    #visit redplanetscience.com
    url="https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(1)

    # Create a HTML object 
    html_page = browser.html

    # Parsing the html_page with BeautifulSoup 
    soup_page = bs(html_page, 'html.parser')

    # Grab and display the latest News Title and Paragraph Text
    NASA_soups = soup_page.find_all('div', id='news')
    for NASA_soup in NASA_soups:

        #get news title
        news_title = soup_page.find("div",class_="content_title").get_text()
        #get news paragraph
        news_p = soup_page.find("div",class_="article_teaser_body").get_text()

    # URL to scrap image from
    url1="https://spaceimages-mars.com"
    browser.visit(url1)
    time.sleep(1)

    # Create a .jpg image  
    Image_page = browser.html

    # Parsing the Image_page with BeautifulSoup 
    soup_image = bs(Image_page, 'html.parser')

    # Find the image url and assign the url string to a variable called featured_image_url
    NASA_images = soup_image.find_all('div', class_='floating_text_area')

    for NASA_image in NASA_images:

        #get the anchor tag 'a'
        NASA_image_link = NASA_image.find('a')
    
        #get the reference 'href'
        NASA_image_url = NASA_image_link["href"]

        #get whole url
        image_src1=url1+NASA_image_url


     #visit marshemisphere.com
    
    # URL to scrap  
    mars_hemispheres_url = "https://marshemispheres.com/" 
    browser.visit(mars_hemispheres_url)

    # Parsing the web page with BeautifulSoup 
    mars_hemispheres_html = browser.html
    mars_hemispheres_soup = bs(mars_hemispheres_html, "html.parser")

    #get item
    mars_hemispheres_images = mars_hemispheres_soup.find_all("div", class_= "item")

    #create empty list and dictionary
    mars_hemisphere_image_urls = []
    mars_hemisphere_dic = {}

    for mars_hemispheres_image in mars_hemispheres_images:

        #get img tag
        image_tag = mars_hemispheres_image.find("img")
    
        #get img alt
        image_alt = image_tag["alt"]
    
        #split img alt and remove the last two
        mars_image = image_alt.split(" ")[0:-2]
    
        #rejoin the splitted img alt
        mars_image1 =" ".join(mars_image)
    
        #get img src
        mars_image_url =  image_tag["src"]
    
        #get whole url
        mars_image_url1 = mars_hemispheres_url + mars_image_url
    
        #set up mars_hemisphere_dic
        mars_hemisphere_dic = {"title":mars_image1,"img_url":mars_image_url1}
    
        #append the mars_hemisphere_dic to list of hemisphere_image_urls
        mars_hemisphere_image_urls.append(mars_hemisphere_dic)
    
    #store data in a dictionary
    mars={"news_title":news_title,"news_p":news_p,"featured_image_url":image_src1,"hemisphere_image_urls":mars_hemisphere_image_urls}
    #quit the browser
    browser.quit()
    
    return(mars)

