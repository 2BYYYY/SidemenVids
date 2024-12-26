from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import csv

# URL and WebDriver setup
url = "https://www.youtube.com/@Sidemen/videos"
service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.get(url=url)

# Infinite scroll to load all videos
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    # Scroll to the bottom
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(10)  # Adjust wait time as necessary
    
    # Calculate new scroll height and compare
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract video details
videos = driver.find_elements(By.CLASS_NAME, "style-scope ytd-rich-grid-media")
list_Vids = []

for video in videos:
    try:
        # Extract video details
        title = video.find_element(By.XPATH, './/*[@id="video-title"]').text
        views = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
        date = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text
        duration = video.find_element(By.XPATH, './/*[@class="badge-shape-wiz__text"]').text
        if (duration == ''):
            duration = "Potential Delays or Dynamic Loading"
        
        # Append to the list
        list_Vids.append([title, views, date, duration])
    except Exception as e:
        print("Error extracting video details:", e)

# Print video details
for vids in list_Vids:
    print(vids)

confirm = input("Write to csv? Y or N: ")
if (confirm.upper() == "Y"):
    with open("sidemenVids.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Views", "Date", "Duration"])  # CSV header
    # Write details to the CSV file
        for list in list_Vids:
            writer.writerow(list)
else: 
    print("try again")
# Clean up
driver.quit()
