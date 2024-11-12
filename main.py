from bottle import Bottle, run, request, response, static_file
import bs4
import requests

app = Bottle()


@app.route('/')
def index():
    return static_file('index.html', root='static')

@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@app.route('/filter.xml')
def filter():
    # expecting query params: url, include, exclude
    url = request.query.url
    include = request.query.include
    exclude = request.query.exclude
    print(f'Filtering {url} with include={include} exclude={exclude}')

    if not url:
        response.status = 400
        return 'url is required'
    if not include and not exclude:
        response.status = 400
        return 'exactly one of include or exclude is required'
    if include and exclude:
        response.status = 400
        return 'exactly one of include or exclude is required'

    # url points to an rss feed
    # fetch the feed
    rss = requests.get(url)
    if rss.status_code == 404:
        response.status = 404
        return 'FilterFeeder: original feed not found'
    rss.raise_for_status()

    # parse the feed
    soup = bs4.BeautifulSoup(rss.text, 'xml')
    print(f'Parsed {url}:')

    # filter the feed
    items = soup.find_all('item')
    print(f'Found {len(items)} items')
    filtered_items = []
    for item in items:
        title = item.find('title').text
        if include and include not in title:
            continue
        if exclude and exclude in title:
            continue
        filtered_items.append(item)
    channel = soup.find('channel')
    for item in channel.find_all('item'):
        if item not in filtered_items:
            item.decompose()

    print(f'Filtered to {len(filtered_items)} items')
    print(f"soup name: {soup.name}")

    empty_name_count = 0
    # remove none-named tags
    for tag in soup.find_all():
        if tag.name is None:
            tag.name = 'wasNoneName'
            empty_name_count += 1
    print(f"Fixed {empty_name_count} empty tags")
    
    return soup.prettify()

if __name__ == '__main__':
    run(app, host='localhost', port=3333)