Other way to select the comment box
```py
EC.element_to_be_clickable((By.CLASS_NAME, "style-scope ytd-comment-simplebox-renderer"))
EC.element_to_be_clickable((By.CSS_SELECTOR, "#simplebox-placeholder"))
EC.element_to_be_clickable((By.CSS_SELECTOR, "#placeholder-area"))
EC.element_to_be_clickable((By.CSS_SELECTOR, "#placeholder-area > yt-formatted-string"))
EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[text()='Add a comment…']"))
```