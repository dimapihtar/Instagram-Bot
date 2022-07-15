# Instagram-Bot
Python Instagram Bot that sends messages. Ability to send messages using a proxy server to avoid a ban.
# Overview
This project has a few functions:
  - Proxy connection
  - Instagram authorization
  - Send messages
  - Save info about sent messages in .csv format
  
# Needed tools to run script:
  - Proxy server
  - Created Instagram account
  - [Google Chrome](https://www.google.com/chrome/)
  - [Chromedriver](https://chromedriver.chromium.org/downloads) in respect to your Chrome version. Download it and put in project's folder.
  - Python Libraries:
    - Selenium (```pip insatll selenium```)
    - Pandas (```pip install pandas```)
    
# Usage
Just run the main script (```python main.py```) with your proxy-server settings and Instagram login data. Change message text and usernames list you want to save message. Pay attention on keeping sleep time after some actions in Instagram. It avoids to be recognized as bot.
