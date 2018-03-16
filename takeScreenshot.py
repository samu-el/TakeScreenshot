from selenium import webdriver
from io import BytesIO
from PIL import Image


def takeScreenshot(url, driver):

        driver.get(url)
        js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

        scrollheight = driver.execute_script(js)
        
        slices = []
        offset = 0
        offset_arr = []

        # separate full screen in parts and make printscreens
        while offset < scrollheight:
            # scroll to size of page
            if (scrollheight) < offset:
                # if part of screen is the last one, we need to scroll just on rest of page
                driver.execute_script(
                    "window.scrollTo(0, %s);" % (scrollheight))
                offset_arr.append(scrollheight)

            else:
                driver.execute_script("window.scrollTo(0, %s);" % offset)
                offset_arr.append(offset)
    

            # create image (in Python 3.6 use BytesIO)
            img = Image.open(BytesIO(driver.get_screenshot_as_png()))

            offset += img.size[1]
            # append new printscreen to array
            slices.append(img)

        # create image with
        screenshot = Image.new('RGB', (slices[0].size[0], scrollheight))
        offset = 0
        offset2 = 0
        # now glue all images together
        for img in slices:
            screenshot.paste(img, (0, offset_arr[offset2]))
            offset += img.size[1]
            offset2 += 1

        screenshot.save(url.split("//")[1].split('/')[0]+'.png')

driver = webdriver.Chrome("chromedriver.exe")

takeScreenshot("https://python.org", driver)
takeScreenshot("https://en.wikipedia.org", driver)
