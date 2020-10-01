# YOUTUBE

## 1. Collecting YouTube Data

### 1.1 Getting Started with YouTube API

Use Youtube API: https://developers.google.com/youtube/v3/quickstart/python

#### Activate API from Google console
Create a New Project:
- Login to Google, if you don't have an account create one and then login.
- Visit the Google developer dashboard, create a new project from the top of the page as in below image, click “Select a project” from the top :

![Image of Youtube API -1](https://lh6.googleusercontent.com/zJ_nff9EbRY5PPHP0s7REUynxw8mfOGPieZN5LV678WjZqIWZInWiEc0ydx4hfQFESaOAX1ZMqEci-tTNKmQTbWnijQKM7U4mDb2wafsWM9MR5-UOcojA1xJizcFqzrzCL8wexV1)

- Now Click on “New Project” as in the below one and proceed.

!['Image of Youtube API - 2'](https://lh5.googleusercontent.com/BsSMME3vzQ3RL17XPnz4EoDqq-9U9SDKJB99oCfH-I3F7dv1MDnNm9qhxEr_fOhEwRimKhUPUHW940LFQD3KAeITei8BLiCSXgf9_LyMA-dTWHilpqM09We9M4SP6YU3IG137QaR)

Once done you will be automatically redirected to the Google APIs dashboard.
- The next step is to activation of YouTube API, so for that navigate to the API & Services from the side panel.
- Then click on Enable API & Services from the top of the page.
- Search for Youtube and then select YouTube Data API v3.

![Image of Youtube API - 3](https://lh4.googleusercontent.com/6782PYxnPaoQKjJi3lXzFuxU5M_-ReJRAvTabjx0NDorBMHpcaUjtEcdUC5aHcB8dIUI6GSa2cC1Wqg1rczPX6YQ6b6N86dGYs6OChEmwcZg5pxYeW1Wx51K02jBO-JKxf1VO4ds)
- After that Enable the API by clicking on the Enable as shown in the below figure.

![Image of Youtube API - 4](https://lh3.googleusercontent.com/MGEwY67Wb18AuEGXXbkFBhzs74Uxe80SbdCUWE2xC4q7-pBtyEJpKb-e_pjMulncMvSb90pSFRDPTK0XIsoVcVy2c66ZrDeJagK0IJ8BRfGw377EKao225eFyTGqt94WFpFZR7CB)
- Now again click on the API & Services and select credentials. Navigate to the Create Credentials from the top of the page in that select API key.

![Image of Youtube API - 5](https://lh5.googleusercontent.com/d6eCMY5vi8oL2eLrDdhpX0NUN8KSdUGUhUn9PAyyCJjGaw6ZfsXy0oNyHQZK8ysDEOE_eHOkpBH6znQ_gtIcfMIpRmlrgnswHKjIHnxQpex_J9kI5U9aNBhQLTwmNSgGeM4r3p95)
- Now click the file download button (Download JSON) to the right of the client ID. Finally, move the downloaded file to your working directory where is "youtube_api.py" and rename it client_secret.json.

![Image of Youtube API - 6](https://python.gotrained.com/?attachment_id=1421)

#### Prerequisites: Client Installation
Now that you have setup the credentials to access the API, you need to install the Google API client library. 

Python 2.7 or Python 3.5+ 
The pip package management tool

```python
# The Google APIs Client Library for Python
pip install --upgrade google-api-python-client
# The google-auth-oauthlib and google-auth-httplib2 libraries for user authorization
pip install --upgrade google-auth-oauthlib google-auth-httplib2
```

#### Extraction of Data from YouTube Channels
Since the Google API client is usually used to access to access all Google APIs, you need to restrict the scope the to YouTube.

When you run the script you will be presented with an authorization URL. Copy it and open it in your browser.
![Image of Google API - 1](https://i2.wp.com/python.gotrained.com/wp-content/uploads/2019/02/screenshot20.png?w=1202&ssl=1)
Select your desired account and grant your script the requested permissions. Confirm your choice.
![Image of Google API - 2](https://python.gotrained.com/?attachment_id=1431)
Copy and paste the code from the browser back in the Terminal / Command Prompt.
At this point, your script should exit successfully indicating that you have properly setup your client.

If you run the script again you will notice that a file named token.pickle is created. Once this file is created, running the script again does not launch the authorization flow.

2. Build model

3. Creating DataBase


4. Run Application
 