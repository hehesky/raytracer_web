import json
from rendering import render
from obj_parser import parse

d={
    'id':"123.png",
    "entities":[
        {"type":"triangle","A":"1.2,1.5,3","B":"1.0,6,1","C":'0,0,0','color':'0,1,0'},
        {"type":"sphere","center":'0,0,0','radius':'1.2','color':'0.4,0.5,0.1',},
        {'position':'1,2,3','type':'light'}
    ]
}
s=json.dumps(d)
ents=parse(s)
render(ents)
