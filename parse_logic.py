# Определение класса request
import grequests
import requests
import json
import numpy
import seaborn as sns
import matplotlib.pyplot as mp
import pandas as pd
import time







class getSkillsFromPage:
    def __init__(self, *args, **kwargs):
        self.plot_path = 'F:/SkillBot/data/plots' + str(time.time()) + '.png'
        self.site = 'http://api.hh.ru/vacancies'
        self.text = kwargs['text']
        self.numpages = kwargs['numpages']
        self.vacancies_found = 0
        self.result_dict = self.get_skills()
        self.result = self.transform_result()


    def get_page(self, page_number: int):
        result = {}
        params = {
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
        self.vacancies_found = len(skills)
        return numpy.hstack(skills)


    def get_skills(self):
        result = []
        for i in range(self.numpages):
            result.append(self.get_page_data(self.get_page(i)))
        unique, counts = numpy.unique(numpy.hstack(result), return_counts=True)
        return dict(zip(unique, counts))


    def transform_result(self):
        __result = pd.DataFrame.from_dict(self.result_dict,
                                             orient='index',
                                             columns=['Occurrence'])
        __result['Skill'] = __result.index
        __result = __result.sort_values(by=['Occurrence'],
                                              ascending=False).head(10)

        return __result



    def visualize_skills(self):
        self.result['Skill'] = self.result.index
        sns.set_theme()
        mp.figure(figsize=(9,5))
        mp.tight_layout()
        plot = sns.barplot(data=self.result,
                    x='Occurrence',
                    y='Skill')
        plot.set_yticklabels(plot.get_yticklabels(), rotation=40, ha="right", fontsize=8)
        plot.set_title(f"Data based on {self.vacancies_found} user-imitated searches", fontsize=12)
        mp.savefig(self.plot_path, bbox_inches='tight')
        mp.show()