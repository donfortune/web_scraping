import requests  #get page source and save as string
import selectorlib #extracts particular value btw h tags

URL = "http://programmer100.pythonanywhere.com/tours/"



def scrape(url):
    response = requests.get(URL)
    content = response.text
    return content


if __name__ == "__main__":
    print(scrape(URL))



