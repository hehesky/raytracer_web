import uuid
import rendering


id=str(uuid.uuid4())

d={
    'id':id+'.png',
    "entities":[
        {"type":"sphere","center":'2.5,2.5,0','radius':'2','color':'1,0,0.1','reflectivity':'0.8'},
        {"type":"sphere","center":'-2.5,2.5,0','radius':'2','color':'0.4,0.5,0.1','reflectivity':'0.8'},
        {"type":"sphere","center":'-2.5,-2.5,0','radius':'2','color':'0.4,1,0.1','reflectivity':'0.8'},
        {'position':'0,0,15','type':'light'}
    ]
}

rendering.lambda_handler(d, None)
