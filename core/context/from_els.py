from core.context.db import Database
from elasticsearch import Elasticsearch


class ElasticsearchDB(Database):
    def __init__(self, url="", index=""):
        self.url = url
        self.index = index
        self.client = Elasticsearch(url)

    def find_contexts(self, question: str, n_contexts: int=100):
        resp = self.client.search(
            index=self.index, 
            query={
                "match": {
                    "text": {
                        "query": question
                    }
                }
            },
            size=n_contexts,
        )

        try:
            return [it["_source"] for it in resp["hits"]["hits"]]
            # for item in resp["hits"]["hits"]:
            #     yield item["_source"]
        except Exception as e:
            print(e)