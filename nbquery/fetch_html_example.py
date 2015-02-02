from nbquery import NBQueryCLI

nb_cli = NBQueryCLI("island2.cs.columbia.edu")
# Specify the url pattern of the source can be in regex
# Location to save html source
# Number of articles that you would like returned
nb_cli.get_html_source("www.nytimes.com*","/tmp/html/",100)


