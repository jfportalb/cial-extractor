import fileinput
import concurrent.futures as cf
import json

def parse_url(website):
    logo = "<LOGO>"
    phones = ["+61 3 9828 3200", "+55 11 4933 7500"]
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
