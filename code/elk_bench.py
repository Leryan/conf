#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Florent Peterschmitt <florent@peterschmitt.fr> - 2016

import random
import string
import json
import time
import datetime

import requests

DATE_FORMAT=r'%Y/%m/%d %H:%M:%S'

DOC_CREATE_INDEX = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "bench_event": {
            "properties": {
                "@timestamp": {
                    "type": "date",
                    "format": "epoch_millis"
                }
            }
        }
    }
}

def timestampToDate(dateformat, timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime(dateformat)

class ESBench(object):

    def __init__(self, *args, **kwargs):
        super(ESBench, self).__init__(*args, **kwargs)

        self._s = requests.Session()

        self._es_location = 'http://localhost:9200'

        self._es_idx_count = 0
        self._es_idx_name_tmpl = 'bench_idx_{0}'

        self._es_field_names = []

        self._data_pool_strings = []
        self._data_pool_documents = []

    def generate_random_string(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def generate_random_string_pool(self, count=1000, sizes=[10, 15, 20, 75]):
        for i in range(0, int(count / 4)):
            for s in sizes:
                self._data_pool_strings.append(self.generate_random_string(s))

    def generate_random_data(self, max_fields=20):
        """
        Prepare enough random data before running bench.
        """
        for i in range(0, max_fields):
            field_name = 'bench_field_{0}'.format(self.generate_random_string())
            self._es_field_names.append(field_name)

        self.generate_random_string_pool()
        self.generate_random_documents()

    def generate_random_documents(self, count=18000):
        self._data_pool_documents = []

        for i in range(0, count):
            self._data_pool_documents.append(self.generate_document())

    def generate_index(self):
        """
        Generate a new index name. This doesn't check if the index exists
        into the ES database.

        :return: string
        """
        idx_name = self._es_idx_name_tmpl.format(self._es_idx_count)
        self._es_idx_count += 1
        return idx_name

    def generate_document(self):
        document = {}

        for field_name in self._es_field_names:
            idx_string = random.randint(0, len(self._data_pool_strings) - 1)
            field_data = self._data_pool_strings[idx_string]
            document[field_name] = field_data

        return document

    ###

    def create_index(self):
        idx_name = self.generate_index()

        self._s.put('{0}/{1}'.format(self._es_location, idx_name),
            data=json.dumps(DOC_CREATE_INDEX))

        return idx_name

    def insert_documents(self, idx_name):
        for document in self._data_pool_documents:
            document['@timestamp'] = int(time.time() * 1000)
            self._s.post('{0}/{1}/{2}'.format(self._es_location, idx_name, 'bench_event'),
                data=json.dumps(document))

    def run(self):
        print('{0} | Preparing random data...'.format(timestampToDate(DATE_FORMAT, time.time())))
        self.generate_random_data()

        while self._es_idx_count < 90:
            idx_name = self.create_index()
            print('{1} | Creating new index: {0}'.format(idx_name, timestampToDate(DATE_FORMAT, time.time())))
            self.insert_documents(idx_name)

    @staticmethod
    def main():
        o = ESBench()
        o.run()


if __name__ == '__main__':
    ESBench.main()
