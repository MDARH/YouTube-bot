from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# Load comments from a file
def get_comments_from_file(filename):
    try:
        # Open the file with the correct encoding (utf-8)
        with open(file_path, "r", encoding="utf-8") as file:
            comments = [line.strip() for line in file.readlines()]
        return comments
    except UnicodeDecodeError as e:
        print(f"Unicode error while reading the file: {e}")
        return []  # Return an empty list or handle as needed
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Get the list of comments from 'comments.txt'
comments = get_comments_from_file("comments.txt")

# Load video titles from a file
def get_titles_from_file(filename):
    """Reads video titles from a text file and returns them as a list."""
    with open(filename, "r") as file:
        titles = [line.strip() for line in file.readlines()]
    return titles

# Get the list of titles from 'titles.txt'
titles = get_titles_from_file("titles.txt")

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

# Start timing
start_time = time.time()

try:
    # Navigate to YouTube
    driver.get("https://www.youtube.com")

    # Select a random title from the list of titles
    title = random.choice(titles)
    print(f"Searching for: {title}")

    # Find the search box and search for the video title
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(title)
    search_box.send_keys(Keys.RETURN)  # Press Enter to start search

    # Wait for the search results to load
    wait = WebDriverWait(driver, 10)
    first_video = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer #thumbnail")))

    # Safely get the href attribute of the first video
    video_href = first_video.get_attribute("href")

    # Check if the href attribute is found and if the video is a Shorts video
    if video_href and "shorts" in video_href:
        print("First video is a Shorts. Searching for a longer video...")
        # Select the next available video (not a Shorts)
        videos = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
        for video in videos:
            video_href = video.get_attribute("href")
            if video_href and "shorts" not in video_href:
                driver.execute_script("arguments[0].click();", video.find_element(By.CSS_SELECTOR, "#thumbnail"))
                print(f"Condition One: {driver.title}")
                break
    else:
        driver.execute_script("arguments[0].click();", first_video)
        print(f"Now playing with Else: {driver.title}")

    # Wait for the video to start playing
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))
    print(f"Video is Clicked and Playing: {driver.title}")

    # Wait for the video to start (adjust time as needed)
    time.sleep(5)  # Wait a few seconds for the video to load

    # Scroll down to ensure the comment box is visible
    print("Scrolling down to reveal the comment box...")
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(5)  # Wait for the page to load

    # Wait for the comment box to be clickable (based on the placeholder element)
    print("Waiting for the comment box...")
    comment_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "simplebox-placeholder"))
    )
    print("Comment box found. Scrolling into view...")
    comment_box.click()
    time.sleep(5)

    # Debugging: Confirm the placeholder element was activated
    print("Placeholder clicked. Attempting to locate the active input box...")

    # Locate the active input box
    active_input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comment-simplebox-renderer #contenteditable-root"))
    )
    print("Active input box located.")

    # Ensure the element is ready for input
    driver.execute_script("arguments[0].focus();", active_input_box)

    # Debugging: Print the selected comment before typing
    comment = random.choice(comments)
    print(f"Selected comment: {comment}")

    # Type the comment
    print("Typing the comment...")
    active_input_box.send_keys(comment)

    # Wait for the post button to be present
    print("Waiting for the post button...")
    post_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-button-renderer#submit-button button"))
    )
    print("Post button found. Attempting to click...")

    # Check if the button is enabled and clickable
    if post_button.get_attribute("aria-disabled") == "false":
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post_button)
        time.sleep(1)  # Small pause to ensure stability
        post_button.click()
        print("Post button clicked! Comment submitted.")
    else:
        print("Post button is disabled. Unable to submit the comment.")

except Exception as e:
    print(f"Error: {e}")

finally:
    input("Press Enter to exit...")
    driver.quit()