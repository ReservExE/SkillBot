import os
from collections import defaultdict
import pandas as pd
data_path = 'F:/SkillBot/data'

class directory_handler:
    def __init__(self, request_tokens):
        self.request: list = request_tokens
        self.cluster_list = os.listdir(data_path)
        self.matching_list = defaultdict(int)
        self.is_match = False
        self.result = []
        self.check_library_keys()

    def check_library_keys(self):
        for index, _dir in enumerate(self.cluster_list):
            for token in self.request:
                if token in _dir:
                    self.matching_list[_dir] += 1

        ser = pd.Series(self.matching_list, dtype='float64')
        if len(ser) != 0:
            self.is_match = True
            self.result = ser.sort_values(ascending=False).nlargest(n=3).index.tolist()





