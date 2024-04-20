import fileinput
import concurrent.futures as cf
import json
import requests
from bs4 import BeautifulSoup
import regex as re

def extract_logo(url, soup):
    img_tags = soup.find_all("img")
    for img_tag in img_tags:
        logo_url = img_tag.get("src")
        if logo_url and not logo_url.startswith('data:'):
            if "logo" in logo_url.lower() or "logo" in img_tag.get("alt", "").lower() or any("logo" in c.lower() for c in img_tag.get("class", [])):
                if logo_url.startswith("//"):
                    return "https:" + logo_url
                if logo_url.startswith("/"):
                    splitted = url.split("/", 3)
                    return splitted[0] + "//" + splitted[2] + logo_url
                if not logo_url.startswith('http'):
                    logo_url = url + logo_url
                return logo_url
    return None

def extract_phones(soup):
    innerText = soup.get_text()
    pattern = re.compile(r'(?<!&copy;\s*)(?<=^|\s|>)(?:[\+]\s?[0-9]{1,3}\s?-?)?(?:\([0-9]{2,3}\)[-\s\.]?|[0-9]{2,3}[-\s\.]?)?\d(?:[ -]?\d){6,9}(?=<|\s|$)')
    return pattern.findall(innerText)

def parse_url(website):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    with requests.get(website, headers=headers, stream=True) as r:
        soup = BeautifulSoup(r.text, 'html.parser')
        logo = extract_logo(website, soup)
        phones = extract_phones(soup)

        return json.dumps({
            "logo": logo,
            "phones": phones,
            "website": website
        })

def main():
    with cf.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(parse_url, url.rstrip()): url.rstrip() for url in fileinput.input()}
        for future in cf.as_completed(future_to_url):
            try:
                json = future.result() 
                print(json)
            except Exception as exc:
                url = future_to_url[future]
                print('%r generated an exception: %s' % (url, exc))


if __name__ == "__main__":
    main()
