from itertools import chain

from geopy import Nominatim
import reverse_geocoder as rg
import numpy as np
from search_engine_parser.core.engines.google import Search as GoogleSearch
import newspaper
from newspaper import Article
from urllib.parse import urlparse
import json
import uuid
import pathlib
import concurrent.futures


def get_new_coordinate(latitude, longitude, distance, bearing):
    R = 6378.1  # Radius of the Earth
    lat1 = np.radians(latitude)
    lon1 = np.radians(longitude)
    lat2 = np.arcsin(np.sin(lat1) * np.cos(distance / R) +
                     np.cos(lat1) * np.sin(distance / R) * np.cos(bearing))
    lon2 = lon1 + np.arctan2(np.sin(bearing) * np.sin(distance / R) * np.cos(lat1),
                             np.cos(distance / R) - np.sin(lat1) * np.sin(lat2))
    return get_decoded_location([np.degrees(lat2), np.degrees(lon2)])


def get_decoded_location(coordinate):
    temp = (rg.search(coordinate, mode=1))
    city = temp[0]["name"]
    prov = temp[0]["admin1"]
    return (city, prov)


def get_nearby_cities(latitude, longitude, radius):
    nearby_cities = []
    for bearing in range(0, 360, 20):
        for distance in range(0, radius, 30):
            nearby_cities.append(get_new_coordinate(latitude, longitude, distance, bearing))
    nearby_cities = list(set(nearby_cities))
    return nearby_cities


def get_newspapers(city_list):
    newspaper_list = []
    gsearch = GoogleSearch()
    for each in city_list:
        query = ("+".join((("+".join(each), "local", "news")))).replace(" ", "+")
        results = gsearch.search(query)
        url = (results[0]["link"])
        print(urlparse(str(urlparse(url).query)[2:]).scheme + "://" + urlparse(str(urlparse(url).query)[2:]).netloc)
        newspaper_list.append(
            urlparse(str(urlparse(url).query)[2:]).scheme + "://" + urlparse(str(urlparse(url).query)[2:]).netloc)
    return newspaper_list


def get_headlines(newspapers, cities):
    articles = []
    for i, paper in enumerate(newspapers):
        headlines = []
        paper = newspaper.build(paper, memoize_articles=False)
        for article in paper.articles:
            headlines.append((article.url, cities[i]))
        articles.append(headlines[0:20])
    return articles


def get_url_data(headline_urls):
    headline_urls = list(chain.from_iterable(headline_urls))
    MAX_THREADS = 8
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(write_json, headline_urls)


def write_json(each_url):
    article = Article(each_url[0])
    article.download()
    article.html
    article.parse()
    try:
        authors = article.authors
    except AttributeError:
        authors = ""
    try:
        content = article.text
    except AttributeError:
        content = ""
    try:
        date = article.publish_date
    except AttributeError:
        date = ""
    try:
        title = article.title
    except AttributeError:
        title = ""
    article_content = {
        "authors": authors,
        "content": content,
        "city": each_url[1],
        "publication date": str(date),
        "title": title,
        "url": each_url,
    }
    print(article_content)
    with open(pathlib.Path("news_data", str(uuid.uuid1().int) + ".json"), "w+") as outfile:
        json.dump(article_content, outfile, indent=4)


def main(location, radius, cities_to_remove):
    locator = Nominatim(user_agent="CPSC473")
    location = locator.geocode(location, timeout=10)
    cities = get_nearby_cities(location.latitude, location.longitude, radius)
    cities_to_remove = []
    for each in cities_to_remove:
        if each in cities:
            cities.remove(each)
    city_newspapers = get_newspapers(cities)
    headline_urls = get_headlines(city_newspapers, cities)
    get_url_data(headline_urls)


main("Kitimat", 100, [])