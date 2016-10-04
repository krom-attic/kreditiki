from lxml import html
import requests


class TestPages:
    def test_find_db_errors(self):
        errors = {}
        BASE_URL = 'http://127.0.0.1:8000'
        r = requests.get(BASE_URL + '/credit/')
        tree = html.fromstring(r.text)
        nodes = tree.xpath('//ul[@id="marks"]/li/a')
        for node in nodes:
            r = requests.get(BASE_URL + node.attrib['href'])
            tree = html.fromstring(r.text)
            nodes = tree.xpath('//ul[@id="model_family"]/li/a')
            for node in nodes:
                r = requests.get(BASE_URL + node.attrib['href'])
                tree = html.fromstring(r.text)
                nodes = tree.xpath('//ul[@id="modifications"]/li/a')
                for node in nodes:
                    r = requests.get(BASE_URL + node.attrib['href'])
                    if r.status_code != 200:
                        tree = html.fromstring(r.text)
                        error_type = tree.xpath('//div[@id="summary"]/table/tr[4]/td/text()')
                        errors.setdefault(error_type[0], []).append(r.url)
                        print(r.url)
                    # assert r.status_code in 200


