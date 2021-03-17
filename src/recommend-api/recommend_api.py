from typing import Optional
from fastapi import Cookie, FastAPI, HTTPException
from fastapi.responses import JSONResponse
import boto3

api = FastAPI()

@api.get("/")
def read_root():
    return {"Hello": "World"}

@api.get("/recommend")
def read_item(USER_ID = Cookie(None)):
    if not USER_ID:
        raise HTTPException(status_code=403, detail="Forbidden")
    client = boto3.client('personalize-runtime', 'ap-northeast-2')
    response = client.get_recommendations(
        campaignArn='<CAMPAIGN_ARN>',
        userId=USER_ID,
        numResults=3,
    )
    result = {
        "USER_ID": USER_ID,
        "itemList": response["itemList"]
    }
    return result
