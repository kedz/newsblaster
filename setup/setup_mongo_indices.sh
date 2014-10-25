#TODO read mongo path from environment variable produced from setup file

mongo archive --eval "db.articles.ensureIndex({'time_of_crawl':1,'date':1})"
mongo archive --eval "db.articles.ensureIndex({'time_of_crawl':1})"
mongo archive --eval "db.articles.ensureIndex({'title':1})"
mongo archive --eval "db.articles.ensureIndex({'meta_information':1})"

db.articles.find({"meta_information.author":'Alan Cowell'}).count()
db.articles.find({"meta_information.topics":{$in: [/^ebola/i,/^africa/i] }})
db.articles.find({"meta_information.topics":{$in: [/^ebola/i,/^africa/i,/^police/i] }}, { "title":1,"meta_information.topics":1 })
