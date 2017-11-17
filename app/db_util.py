import os
import boto3
from boto3.dynamodb.conditions import Attr



#try to get access key from 
try:
    DB_ACCESS_KEY=os.environ["DB_ACCESS_KEY"]
    DB_SECRET= os.environ["DB_SECRET"]
    REGION_NAME=os.environ["REGION_NAME"]
    DB_TABLE=os.environ["DB_TABLE"]
except KeyError:
    from app.config import DB_ACCESS_KEY,DB_SECRET,REGION_NAME, DB_TABLE
finally:
 
    dynamodb = boto3.resource('dynamodb',region_name=REGION_NAME,
    aws_access_key_id=DB_ACCESS_KEY,aws_secret_access_key=DB_SECRET)
    table = dynamodb.Table(DB_TABLE)

def get_user_requests(username):
    """Returns requests made by a user as a list of dictionaries
        key and values in these dictionaries are unicoded, so it may be necessary to cast them into str
        
        structure:
        {
            'stat': [str] -> status of this request, must be either 'pending','failed', or 'success',
            'user': [str] -> username
            'requestID': [str] -> unique ID (and file name) of rendered image, file extension included
        }
    """

    response= table.scan(FilterExpression=Attr("user").eq(username))
    return response['Items']

def insert_pending_user_request(username,requestID):
    entry = { "requestID":requestID,
    "user":username,
    'stat':'pending'
    }
    table.put_item(Item=entry)

def set_request_stat(requestID,status):
    assert status in ["failed",'pending','success']
    table.update_item(Key={"requestID":requestID},UpdateExpression="SET stat = :val",
    ExpressionAttributeValues= {":val":status}
) 
