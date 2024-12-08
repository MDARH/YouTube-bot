import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load video titles from a file
def get_titles_from_file(filename):
    """Reads video titles from a text file and returns them as a list."""
    with open(filename, "r") as file:
        titles = [line.strip() for line in file.readlines()]
    return titles

# Get the list of titles from 'titles.txt'
titles = get_titles_from_file("titles.txt")

# Load comments from a file
def get_comments_from_file(filename):
    """Reads comments from a text file and returns them as a list."""
    with open(filename, "r", encoding="utf-8") as file:
        comments = [line.strip() for line in file.readlines()]
    return comments

# Get the list of comments from 'comments.txt'
comments = get_comments_from_file("comments.txt")

# Set the path to Brave browser executable C:\Users\mdarh\AppData\Local\BraveSoftware\Brave-Browser\Application
brave_path = "C:\\Users\\mdarh\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# Configure Chrome options
options = Options()
options.binary_location = brave_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  
options.add_argument("user-data-dir=C:\\Users\\mdarh\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data")
options.add_argument("profile-directory=Default")  # Change 'YT Bot' to the name of your profile
options.add_argument("--disable-gpu")
options.add_argument("--enable-unsafe-swiftshader")

# Path to ChromeDriver
driver_path = "C:\\laragon\\www\\ytbot\\chromedriver-win64\\chromedriver.exe"

# Initialize the Service object with the path to ChromeDriver
service = Service(driver_path)

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Function to search for a video and post a comment
def search_and_comment(driver, video_title):
    # Search for the video
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(video_title)
    search_box.send_keys(Keys.RETURN)  # Press Enter to start search

    # Wait for the search results to load and click on the first video
    wait = WebDriverWait(driver, 10)
    first_video = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer #thumbnail")))

    # Click the first video
    driver.execute_script("arguments[0].click();", first_video)
    print(f"Now playing: {video_title}")

    # Wait for the video to start playing
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))
    print(f"Video is Clicked and Playing: {driver.title}")

    # Wait for a moment to ensure the video and comment box are fully loaded
    time.sleep(5)  # Adjust as needed

    # Scroll down to ensure the comment box is visible
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(3)  # Adjust as needed

    # Wait for the comment box to be clickable (based on the placeholder element)
    print("Waiting for the comment box...")
    comment_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "simplebox-placeholder"))
    )

    # Click on the comment box to focus
    print("Comment box found. Clicking to focus...")
    comment_box.click()

    # Ensure the element is ready for input
    driver.execute_script("arguments[0].focus();", comment_box)

    # Select a random comment and type it
    comment_to_post = random.choice(comments)
    print(f"Typing the comment: {comment_to_post}")
    comment_box.send_keys(comment_to_post)

    # Wait for the post button to be clickable and click it
    print("Waiting for the post button...")
    post_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//yt-button-renderer[@id='submit-button']"))
    )
    post_button.click()
    print("Comment posted!")

    # Wait a few seconds to ensure comment is posted
    time.sleep(3)  # Adjust as needed


# Main execution
try:
   
    # Open YouTube
    driver.get("https://www.youtube.com")
    
    # Loop through the titles and post comments
    for _ in range(5):  # You can set the number of videos to comment on (e.g., 5)
        title = random.choice(titles)  # Randomly choose a video title
        print(f"Searching for: {title}")
        
        # Call the function to search and post a comment
        search_and_comment(driver, title)

        # Wait between each video search to prevent being flagged as spam
        time.sleep(random.randint(10, 20))  # Adjust the time delay as necessary

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up: close the browser after the loop
    driver.quit()
