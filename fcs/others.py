# importing the required modules
import requests
import random
# importing the required modules end


# defining funtion to generate url for profile background image
def generate_url():
    api_key = '563492ad6f91700001000001eb52c9550b984f7eacd8644d821078be'

    url = 'https://api.pexels.com/v1/search?query=nature background'

# Sending request to the Pexels API
    try:
        response = requests.get(url, headers={
            "authorization": api_key
        })
        data = response.json()

        # picking an image at random and getting the URL
        img_url = random.choice(data['photos'])['src']['large']
        return img_url
    # passing the picked URL at output

    except requests.ConnectionError:
        return 'profile_bg.jpg'


# defining funtion to generate url for profile background image end
