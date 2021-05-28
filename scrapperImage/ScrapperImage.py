# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:51:15 2020

@author: krish.naik
"""

from bs4 import BeautifulSoup as bs
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from urllib.request import urlretrieve

class ScrapperImage:
    
    ## Create  Image URl
    def createImageUrl(searchterm):
        searchterm=searchterm.split()
        searchterm="+".join(searchterm)
        #web_url="https://www.google.co.in/search?q=" + searchterm + "&source=lnms&tbm=isch"
        web_url="https://www.google.com/search?q="+ searchterm +"&hl=EN&tbm=isch&sxsrf=ALeKk02YSwXvk8wXhT11coYU_2j5mZAEfg%3A1622029857798&source=hp&biw=1280&bih=578&ei=ITauYM26LqOV4-EPtuuLgAI&oq="+ searchterm +"&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQsQMyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDMgUIABCxAzoHCCMQ6gIQJzoICAAQsQMQgwFQnQxY4A1giRNoAXAAeACAAfYBiAHtBJIBBTAuMS4ymAEAoAEBqgELZ3dzLXdpei1pbWewAQo&sclient=img&ved=0ahUKEwiNz_KLpOfwAhWjyjgGHbb1AiAQ4dUDCAc&uact=5"
        return web_url
    
   # get Raw HTML
    def scrap_html_data(url,header):
        
        request=urllib.request.Request(url,headers=header)
        response = urllib.request.urlopen(request)
        responseData = response.read()
        html = bs(responseData, 'html.parser')
        return html
    
    # contains the link for Large original images, type of  image
    def getimageUrlList(rawHtml):
        imageUrlList = []
        for a in rawHtml.findAll('img', {'class': 'rg_i Q4LuWd'}):
            #print(a)
            #break
             try:
                link, imageExtension = a['data-src'],  'jpg'
                imageUrlList.append((link, imageExtension))
            
             except KeyError:
                 
                 continue

        print("there are total", len(imageUrlList), "images")
        return imageUrlList
    
    def downloadImagesFromURL(imageUrlList,image_name, header):
        masterListOfImages = []
        count=0
        ###print images
        imageFiles = []
        imageTypes = []
        image_counter=0
        for i, (img, Type) in enumerate(imageUrlList):
            try:
                if (count > 5):
                    break
                else:
                    count = count + 1
                    
                req = urllib.request.Request(img, headers=header)
                #print(img)
                try:
                    urllib.request.urlretrieve(img,"./static/"+image_name+str(image_counter)+".jpg")
                    image_counter=image_counter+1
                except Exception as e:
                    print("Image write failed:  ",e)
                    image_counter = image_counter + 1
                respData = urllib.request.urlopen(req)
                raw_img = respData.read()
                # soup = bs(respData, 'html.parser')

                imageFiles.append(raw_img)
                imageTypes.append(Type)

            except Exception as e:
                print("could not load : " + img)
                print(e)
                count = count + 1
        masterListOfImages.append(imageFiles)
        masterListOfImages.append(imageTypes)

        return masterListOfImages
    
    def delete_downloaded_images(self,list_of_images):
        for self.image in list_of_images:
            try:
                os.remove("./static/"+self.image)
            except Exception as e:
                print('error in deleting:  ',e)
        print("Done")
        return 0
    
   
    
    
    
    