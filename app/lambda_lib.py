import os
import json
import boto3

try:
    LAMBDA_ACCESS_KEY=os.environ["LAMBDA_ACCESS_KEY"]
    LAMBDA_SECRET=os.environ["LAMBDA_SECRET"]
except KeyError:
    raise EnvironmentError("Lambda related credential missing")

finally:
    REGION='us-east-2'
    FUNCTION_NAME='RayTracer'
    client=boto3.client('lambda',
        region_name=REGION,aws_access_key_id=LAMBDA_ACCESS_KEY,
        aws_secret_access_key=LAMBDA_SECRET)

def invoke_render(request_dict):
    """Assumes request_dict is a dictionary contains all info"""
    payload=json.dumps(request_dict).encode("ascii")#binary payload
    client.invoke(FunctionName=FUNCTION_NAME,InvocationType='Event',Payload=payload)

if __name__=='__main__':
    import uuid
    reqid=str(uuid.uuid4())

    d={
        'id':reqid+'.png',
        "entities":[
            {"type":"sphere","center":'2.5,2.5,0','radius':'2','color':'1,0,0.1','reflectivity':'0.5'},
            {"type":"sphere","center":'-2.5,2.5,0','radius':'2','color':'0,0,1','reflectivity':'0.5'},
            {"type":"sphere","center":'-2.5,-2.5,0','radius':'2','color':'0,1,0.1','reflectivity':'0.5'},
            {'position':'0,0,15','type':'light'}
        ]
    }
    invoke_render(d)