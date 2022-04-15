
"""
This gives 's1' as an obj with the binance keys, tho calling get_secrets() and having s1 appears redundant. This func just uses get_secrets()

gcloud functions deploy sell_binance \
    --runtime python39 \
    --trigger-http \
    --region=europe-west2 \
    --memory=128MB \
    --timeout=120S \
    --quiet \
    --allow-unauthenticated \
    --ingress-settings=internal-only \
    --set-secrets s1=binance-keys:latest \
    --source /home/adam_bricknell/binance_sell_function

gcloud functions call sell_binance --data '{"price":"18","quantity":"0.5","symbol":"DOTUSDT"}' --region=europe-west2

"""

from flask import escape
import functions_framework

import requests
import json
from datetime import datetime, timedelta
from google.cloud import storage
from google.cloud import secretmanager
from binance.client import Client


def get_secrets():
    """
    Access secrets from Secrets Manager
    """

    # Create the Secret Manager client.
    secrets_client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/543125676957/secrets/binance-keys/versions/latest"

    # Access the secret version.
    response = secrets_client.access_secret_version(request={"name": name})

    payload = response.payload.data.decode("UTF-8")
    return json.loads(payload)



@functions_framework.http
def sell_binance(request):
    
    """
    ADDS 0.01% OF VALUE TO MAKE THE TRADE GO THROUGH FASTER. OR IT MIGHT HELP
    """


    # extracting parameters
    request_args = request.args
    request_json = request.get_json(silent=True)
    
    if request_args and 'price' in request_args:
        price = float(request_args['price'])
    elif request_json and 'price' in request_json:
        price = float(request_json['price'])
    else:
        raise Exception('price not specified')

    if request_args and 'quantity' in request_args:
        quantity = request_args['quantity']
    elif request_json and 'quantity' in request_json:
        quantity = request_json['quantity']
    else:
        raise Exception('quantity not specified')

    if request_args and 'symbol' in request_args:
        symbol = request_args['symbol']
    elif request_json and 'symbol' in request_json:
        symbol = request_json['symbol']
    else:
        raise Exception('symbol not specified')

    

    keys = get_secrets()
    binance_client = Client(keys['api_key'], keys['api_secret'])


    # rounding
    price_to_sell = str(price * 0.9999)[:5]


    try:
      buy_order_limit = client.create_order(
              symbol=f'{child_coin}USDT',
              side='SELL',
              type='LIMIT',
              timeInForce='GTC',  # gtc = good til cancelled. Other options: 'GTD' (till date), 'Day' (calendar day)
              quantity=quantity,
              price=price_to_sell)

    except Exception as e:
      print(e)
    



