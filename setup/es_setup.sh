#Create custom mapping to use source_link as id
curl -XPUT http://localhost:9200/news/?pretty -d '{
"mappings" : {
"article": {
"_id" : { "path" : "source_link" },
"properties":{
"meta_information":{
"type": "nested"
}
},
"dynamic_date_formats" : ["yyyy-MM-dd hh:mm"]
}
}
}'
