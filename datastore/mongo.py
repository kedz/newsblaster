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
        
    def get_pending_summarization(self):
        pass


    def done(self):
        self.client.close()



if __name__=='__main__':
    pass
    #db = MongoStore()
    #db.insert_article({'title':'Good','authors':['Dwayne','Kellye'] })
    #db.done()
