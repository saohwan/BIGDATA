import urllib.request
import datetime
import json

client_id = 'P1MSxMjGhJrx3fXFE2Ds'
client_secret = 'xKh_De62Uq'


# [code 1]
def get_request_url(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[$s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


# [CODE 2]
def get_naver_search(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "'%s.json" % node
    parameters = "?query=%s%start=%s%display=%s" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    response_decode = get_request_url(url)

    if response_decode is None:
        return None
    else:
        return json.loads(response_decode)


# [CODE 3]
def get_post_data(post, jsonResult, cnt):
    title = post['title']
    link = post['link']
    description = post['description']
    originallink = post['originallink']
    pubDate = post['pubDate']

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description, ';link': link, 'pubDate': pubDate,
                       'originallink': originallink})
    return


# [CODE 0]
def main():
    node = 'news'  # 크롤링 할 대상 : blog
    srcText = input('검색어를 입력하세요.')
    cnt = 0
    jsonResult = []

    jsonResponse = get_naver_search(node, srcText, 1, 100)  # [CODE 2]
    total = jsonResponse['total']

    while (jsonResponse != None) and (jsonResponse['display'] != 0):
        for post in jsonResponse['items']:
            cnt += 1
            get_post_data(post, jsonResult, cnt)

        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = get_naver_search(node, srcText, start, 100)  # [CODE 2]

    print('전체 검색 : %d 건' % total)

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)

        outfile.write(jsonFile)

    print('가져온 데아터 : %d 건' % total)
    print('%s_naver_%s.json SAVED' % (srcText, node))


if __name__ == '__main__':
    main()
