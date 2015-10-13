from pprint import pprint
import os
import pymongo 
import yaml

class MongoStore(object):


    def __init__(self):

        #Settings from config file
        self.module_path = os.path.dirname(os.path.realpath(__file__))
        self.config_dir = os.path.join(self.module_path,os.path.join('..' + os.sep + 'configs' ))
        self.file_path = os.path.abspath(self.config_dir) + os.sep + 'settings.yaml'
        self.config_file = open(self.file_path,'r')
        self.config_data = yaml.load(self.config_file)
       
        pprint(self.config_data)
 
        self.client = pymongo.MongoClient(self.config_data['mongodb']['hostname'],self.config_data['mongodb']['port'])
        self.db = self.client[self.config_data['mongodb']['database']] 
        self.collection = self.db[self.config_data['mongodb']['article_collection']]
    
    def insert_article(self,article):
        self.collection.update({'title':article['title']},
                                    article,
                                    True )

    def insert_summary(self, summary):
        #self.db
            
        #            {"_id": article["_id"]}, {"$set": {"clustered": True}},)
        return self.db.summaries.insert(summary)

    def insert_clusters(self, clusters):
        return self.db.clusters.insert_many(clusters)

    def get_pending_clusters(self):
        clusters = self.db.clusters.find(
                {"summarized": False}, {"_id": 1, "articles":1, "date": 1})
        return clusters

    def get_pending_articles(self):
        articles = self.collection.find(
                {"clustered": False}, {"_id": 1, "text_content":1, "title": 1})
        return articles

    def set_clustered_flag(self, articles):
        for article in articles:
            self.collection.update_one(
                    {"_id": article["_id"]}, {"$set": {"clustered": True}},)

    def set_summarized_flag(self, cluster):
            self.db.clusters.update_one(
                {"_id": cluster["_id"]}, {"$set": {"summarized": True}},)




    def get_articles_from_ids(self, article_ids):
        articles = self.collection.find(
                {"_id": {"$in": article_ids}}, 
                {"_id": 1, "text_content":1, "title": 1})
        return [a for a in articles]


    def done(self):
        self.client.close()



if __name__=='__main__':
    pass
    #db = MongoStore()
    #db.insert_article({'title':'Good','authors':['Dwayne','Kellye'] })
    #db.done()
