# Tibber ams_han
AMS han port dev area for Tibber pulse

## Prerequisite
- get a Tibber pulse, install it
- apply to local utility company for opening up HAN port function on your AMS

## Installation
1. clone repo
2. create virtual environment using tool of your choice
3. activate environment
4. run:
   
        pip install -r requirements.txt

## Useage
### Get Tibber pulse development token
- https://developer.tibber.com/settings/accesstoken
- copy token to clipboard
### Create .env file
        touch .env
        echo "TIBBER_TOKEN=##PASTE YOUR TOKEN FROM CLIPBOARD## >> .env
### Run tests
in your active environments:

        pytest

