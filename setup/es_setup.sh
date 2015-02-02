#Create custom mapping to use source_link as id
curl -XPOST http://island2.cs.columbia.edu:9200/news/?pretty -d '{
"mappings" : {
"article": {
"_id" : { "path" : "source_link" },
"properties":{
 "time_of_crawl": {
                 "type": "date"
             },
"meta_information":{
"type": "nested",
"properties":{date_published: {"type": "date" }     }
}
},
"dynamic_date_formats" : ["yyyy-MM-dd hh:mm"]
}
}
}'
