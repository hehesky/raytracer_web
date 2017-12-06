"""Database library. Read, query and put """
from __future__ import print_function
import datetime
import os
import boto3
from boto3.dynamodb.conditions import Attr
REGION_NAME = 'us-east-2'
#try to get access key from os.environ
try:
    DB_ACCESS_KEY = os.environ["DB_ACCESS_KEY"]
    DB_SECRET = os.environ["DB_SECRET"]


except KeyError:
    raise EnvironmentError("DynamoDB related environment variable unavailable")
finally:
    DB_USER_TABLE='users'
    DB_REQ_TABLE='requests'
    dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME, 
                                aws_access_key_id=DB_ACCESS_KEY, 
                                aws_secret_access_key=DB_SECRET
                            )
    req_table = dynamodb.Table(DB_REQ_TABLE)
    user_table = dynamodb.Table(DB_USER_TABLE)

def add_user(username, salt, password):
    """Add new user info to DB_USER_TABLE"""
    entry={"username":username,
        "salt":salt,
        'password':password
        }
    user_table.put_item(Item=entry)

def get_user(username):

    response=user_table.get_item(Key={'username':username})
    if 'Item' not in response:
        return None
    return response['Item']

def get_user_requests(username):
    """Returns requests made by a user as a list of dictionaries
        key and values in these dictionaries are unicoded, so it may be necessary to cast them into str
        
        structure:
        {
            'stat': [str] -> status of this request, must be either 'pending','failed', or 'success',
            'username': [str] -> username
            'requestID': [str] -> unique ID (and file name) of rendered image, file extension included,
            'timestamp': [str] -> time stamp as YYMMDDhhmmss (20171125121530 -> 2017-11-25 12:25:30),
            'ownership': [str] -> 'public' or 'private'
        }
    """

    response= req_table.scan(FilterExpression=Attr("username").eq(username))
    return response['Items']

def get_image_entities(image_id):
    response= req_table.get_item(Key={'requestID':image_id})
    
    if 'Item' not in response:
        return None
    return response['Item']

def get_public_request():
    response= req_table.scan(FilterExpression=Attr("ownership").eq('public'))
    return response['Items']

def insert_pending_user_request(username,requestID, entities,ownership="private"):
    #get timestamp
    cur_time=datetime.datetime.now()
    timestamp=cur_time.strftime("%Y%m%d%H%M%S")

    entry = { "requestID":requestID,
        "username":username,
        'stat':'pending',
        'timestamp':timestamp,
        'ownership':ownership,
        'entities': entities
    }
    req_table.put_item(Item=entry)

def update_request(username, requestID, ownership):
    userImages = req_table.scan(FilterExpression=Attr("username").eq(username))
    
    if (userImages['Items']):
        currentImage = [item for item in userImages['Items'] if item['requestID'] == requestID]
        
        if (currentImage != []):
            if ownership == 'public':
                newOwnership = 'private'
            elif ownership == 'private':
                newOwnership = 'public'
                
            req_table.update_item(
                Key={
                    'requestID': requestID
                },
                UpdateExpression= "set ownership = :o",
                ExpressionAttributeValues={
                    ":o": newOwnership,
                }
            )
    
def delete_request(username, requestID):
    userImages = req_table.scan(FilterExpression=Attr("username").eq(username))
    
    if (userImages['Items']):
        currentImage = [item for item in userImages['Items'] if item['requestID'] == requestID]
    
        if(currentImage != []):
            req_table.delete_item(
                Key={
                    'requestID': requestID,
                }
            )
         

def set_request_stat(requestID,status):
    assert status in ["failed",'pending','success']
    req_table.update_item(Key={"requestID":requestID},
    UpdateExpression="SET stat = :val",
    ExpressionAttributeValues= {":val":status}) 
