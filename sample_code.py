import requests
from bs4 import BeautifulSoup
from unshortenit import UnshortenIt


def get_title(soup):
    title = soup.find_all('span', attrs={'class': "a-size-large product-title-word-break"})[0].text.strip()
    return title


def get_about(soup):
    about = soup.find_all('div', attrs={'id': 'feature-bullets'})
    about_soup = BeautifulSoup(str(about), "html.parser")
    about_list = about_soup.find_all('ul', attrs={'class': 'a-unordered-list a-vertical a-spacing-mini'})
    about_list_soup = BeautifulSoup(str(about_list), "html.parser")
    about_list = about_list_soup.find_all('span', attrs={'class': 'a-list-item'})
    about_text = ''
    for about in about_list:
        about_text += '\n' + about.text
    return about_text.strip()


def get_description(soup):
    description = soup.find_all('div', attrs={'id': 'productDescription'})
    description_soup = BeautifulSoup(str(description), "html.parser")
    description_list = description_soup.find_all('span')
    description_text = ''
    for description in description_list:
        description_text += '\n' + description.text.strip()
    return description_text.strip()


def get_product_code(url):
    product_code = url.split('/')[4].split('?')[0]
    return product_code


def get_reviews(url, headers):
    product_code = get_product_code(url)
    page_number = 1
    total_count = 0
    total_review_text = ''
    while True:
        reviews_url = 'https://www.amazon.com/product-reviews/' + product_code + '/ref=acr_dp_hist_5?ie=UTF8&filterByStar=five_star&reviewerType=all_reviews&pageNumber=' + str(
            page_number) + '#reviews-filter-bar'
        page = requests.get(reviews_url, headers=headers)
        if page.status_code != 200:
            break
        soup = BeautifulSoup(page.content, "html.parser")
        review_list = soup.find_all('span', attrs={'data-hook': 'review-body'})
        for review in review_list:
            review_text = review.text.strip()
            if len(review_text) > 400:
                total_count += 1
                total_review_text += '\n' + review_text
            if total_count == 10:
                break
        if total_count == 10:
            break
        page_number += 1
    return total_review_text.strip()


def print_by_format(title, url, about, description, reviews):
    print(
        '************************************************************************************************************************************************************************')
    print("Title:")
    print(title)
    print('\n')
    print(url)
    print('\n')
    print('About this item:')
    print(about)
    print('\n')
    print(description)
    print('\n')
    print('Customer Reviews:')
    print(reviews)


def unshorten_url(url):
    unshortener = UnshortenIt()
    uri = unshortener.unshorten(url)
    return uri


def get_short_urls(path):
    short_urls = list()
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            short_urls.append(line.strip())
    return short_urls


path = '/Users/priagarwal/web_scraping/sample_web_scraping/url.txt'
short_urls = get_short_urls(path)

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    'Accept-Langugae': "en-US, en;q=0.5"}

#for short_url in short_urls:
if 1:
    '''
    if not short_url.startswith('https://'):
        short_url = 'https://' + short_url
    url = unshorten_url(short_url)
    '''
    url = "https://www.whitepages.com/phone/1-816-806-2289"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup)
    '''
    title = get_title(soup)
    about = get_about(soup)
    description = get_description(soup)
    reviews = get_reviews(url, headers)
    print_by_format(title, url, about, description, reviews)
    '''
