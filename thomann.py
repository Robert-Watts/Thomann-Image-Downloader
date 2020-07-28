import requests
from bs4 import BeautifulSoup
import os



#Download the page
URL = input("URL to Download: ")
page = requests.get(URL)

#Create the soup object and Get the product name
soup = BeautifulSoup(page.content, 'html.parser')
productName = soup.find("h1", itemprop="name").text


#Get all the thumbnails on the page
thumbnailsList = soup.find_all('li', class_='prod-media-bdb')

#Make sure there are thumbnails to download
if (len(thumbnailsList) > 0):
    print()

    #Create the folder to save the images in
    folderName = productName.replace(" ", "_")
    folderLocation = os.path.join(os.getcwd(), folderName)
    if not os.path.exists(folderLocation):
        os.mkdir(folderLocation)


    for thumbnail in thumbnailsList:

        #get the image location and name
        imageURI = thumbnail.get('data-media-source')
        imageURL = "https://images.static-thomann.de/pics/bdb/" + imageURI
        imageName = imageURI.split("/")[1]
        imagePath = os.path.join(folderLocation, imageName)
        print("Found Image: " + imageURL)

        #Save Image
        with open(imagePath, 'wb') as handle:
            response = requests.get(imageURL, stream=True)
            if not response.ok:
                print (response)
                x = False
            else:
                print("Downloading Image")
                x = True
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
            if (x):
                print("Image Saved to " + imagePath)

        print()

else:
    print("Could not find any images to download.")
