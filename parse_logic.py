#Определение класса request
import grequests
import requests
import json
import numpy
import itertools
from collections import Counter



class getSkillsFromPage:
    def __init__(self, *args, **kwargs):
        self.site = 'http://api.hh.ru/vacancies'
        self.text = kwargs['text']
        self.numpages = kwargs['numpages']
        self.result = self.get_skills()


    def get_page(self, page_number:int):
        result = {}
        params={
            'text': f'NAME:{self.text}',
            'page': page_number,
            'per_page': 100
        }

        r = requests.get(self.site, params)
        result = json.loads(r.content.decode())
        r.close()
        return result


    def get_page_data(self, page):
        skills = []
        urls = [url['url'] for url in page['items']]
        requests = [grequests.get(link) for link in urls]
        response = grequests.map(requests)

        for resp in response:
            data = json.loads(resp.content.decode())
            try:
                skills.append([data['key_skills'][i]['name'] for i in range(len(data['key_skills']))])
            except KeyError:
                pass

        return numpy.hstack(skills)


    def get_skills(self):
        result = []
        for i in range(self.numpages):
            result.append(self.get_page_data(self.get_page(i)))
        unique, counts = numpy.unique(numpy.hstack(result), return_counts=True)
        return dict(zip(unique, counts))



