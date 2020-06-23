"""
Script for configuring RTE API access.

This script is user dependant, Please change client ID and client secret code before using it.
working directory are also case dependant.
"""

# Client ID and secret code, you can get those at https://data.rte-france.com/
CLIENT_ID       = '7699170f-9898-40d0-b78a-XXXXXXXX'
CLIENT_SECRET   = '969de489-1dca-4158-8ad4-XXXXXXXX'

# URL for authentication and get a token access :
OAUTH_URL = 'https://digital.iservices.rte-france.com/token/oauth/'

# list of available API :
URL_TEMPO = 'https://digital.iservices.rte-france.com/open_api/tempo_like_supply_contract/v1/tempo_like_calendars'
URL_PROD  = 'https://digital.iservices.rte-france.com/open_api/generation_forecast/v2/forecasts'

