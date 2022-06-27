from hashlib import md5
from json import load
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests as HTTP_Client
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import pprint
import os
import time
import hashlib
# Create your views here.

load_dotenv()

pp = pprint.PrettyPrinter(indent=2, depth=2)

def index(request):
    response = render(request, "show_and_tell_app/index.html")
    return response

def get_character(request, hero):
    timestamp = time.time()
    str_timedtamp = str(timestamp)
    byte_timestamp = bytes(str_timedtamp, "utf-8")
    privatekey = os.environ["privatekey"]
    apikey = os.environ["apikey"]
    myhash = hashlib.md5((str_timedtamp + privatekey + apikey ).encode())
    auth = OAuth1(os.environ["apikey"], os.environ["privatekey"])


    endpoint = f"https://gateway.marvel.com:443/v1/public/characters?nameStartsWith={hero}&ts={timestamp}&apikey=5fc13150e1a4905b2cfcb253d7eebf8f&hash={myhash.hexdigest()}"


    API_response = HTTP_Client.get(endpoint, auth=auth)
    responseJSON = API_response.json()

    picture = responseJSON["data"]["results"][0]["thumbnail"]["path"] + ".jpg"
    print(picture)
    name = responseJSON["data"]["results"][0]["name"]

    

    response = render(request, "show_and_tell_app/character.html", {"picture": picture, "name": name})
    return response 