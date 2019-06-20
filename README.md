# API RTE Data

Code source for downloading rte data using rte digital on-line services : https://data.rte-france.com/

Procedure to follow :

1) Create a profile
 Go to https://data.rte-france.com/ and create a profile.
2) Create an application associated to one or several API  and get yourclient id and client secret code 
Create an application for web server and start associating API to this application. Note that you won't have access to API if note associated with you application. 
In the application tab, one will find the `client id` and the related `client secret` code needed for requesting data. 

        client_id     = '7699170f-9898-40d0-b78a-XXXXXXXXXXXX'
        client_secret = '969de489-1dca-4158-8ad4-XXXXXXXXXXXX'
    
    The first request to the server must be to requiere a token, i.e. an access to the API. 

        token_type, acess_token = get_token(client_id=client_id, client_secret=client_secret)
    
    This method make a post request to the authentication service at this adress : oauth_url='https://digital.iservices.rte-france.com/token/oauth/'. If the request succeeded, it returns a token access, e.g.  ahzBiRlKTbKyUrGf9Wy7d5zxjgm1k2dJyDxQnOeH8WS8wFZE6V7NRQ that will be valide for two hours. 
    
3) Requesting data.

    For requesting data, one can rely on the documentation available for each API. See https://data.rte-france.com/catalog/-/api/user_guide/231845 for production for instance. 
    This code already include routine method for downloading production and Tempo tarifs, respectively `get_tempo()` and `get_production()`. 
    Basically, those method make a get request to the server API, using client id and client secret code, passing parameter such as dates, production type, depending on the API (see documentation for each API to learn about parameters and formats). 
    
        start_date = datetime.datetime.today() - datetime.timedelta(days=2) # before yesterday
        end_date   = datetime.datetime.today() + datetime.timedelta(days=1) # tomorrow 
        
        r_tempo = get_tempo(start_date, end_date, token_type, access_token)

    In this example, get_tempo() method returns data using json format, that can be parsed using the API documentation. See `update_rte_data.py` for example of use.  
