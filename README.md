# API RTE Data

Code source for downloading rte data using rte digital on-line services : https://data.rte-france.com/

## Installation and configuration 

1) Install the api_rte package from git :
    
        pip install git+https://github.com/ReinboldV/api_rte.git

2) Create a profile at https://data.rte-france.com/.
    
3) Create an application for web server and start associating API to this application. Note that you won't have access to API if note associated with you application. 
        
    In the application tab, one will find the `client id` and the related `client secret` code needed for requesting data. Add those to the configuration file `api_rte\config.py`.

        CLIENT_ID     = '7699170f-9898-40d0-b78a-XXXXXXXXXXXX'
        CLIENT_SECRET = '969de489-1dca-4158-8ad4-XXXXXXXXXXXX'
    
4) Testing the configuration and the api :
    
        python tests/test_conf.py
        python tests/test_api.py

## Basic usage
        
1) Requesting data tempo tarif and production forecasts
  
    This code includes methods for downloading production forecasts and Tempo tarifs, respectively `get_tempo()` and `get_prod()`.
     
     Basically, those methods make a GET request to the server API, using `CLIENT_ID` and `CLIENT_SECRET` code, passing parameter such as dates, production type, and type of prediction,  depending on the API (see documentation for each API to learn about parameters and formats). 
     
     Here is a minimal example for tempo tarifs :
            
        from api_rte.api import *
        import datetime
        
        start_date = datetime.datetime.today() - datetime.timedelta(days=2) # before yesterday
        end_date   = datetime.datetime.today() + datetime.timedelta(days=1) # tomorrow 
        
        r_tempo = get_tempo(start_date, end_date)
        
     Here is a minimal example for one day ahead wind production forecasts :
     
        from api_rte.api import *
        import datetime
        
        start_date = datetime.datetime.today() - datetime.timedelta(days=2) # before yesterday
        end_date   = datetime.datetime.today() + datetime.timedelta(days=1) # tomorrow 
        
        r_prod = get_prod(start_date, end_date, production_type='WIND', type='D-1')
     
     For more detail on options you can pass to the api or error explanation, one can rely on the documentation available for each API available in api_rte/docs or on https://data.rte-france.com/. 
    
## References 
 
Generation Forecast documentation: https://data.rte-france.com/catalog/-/api/generation/Generation-Forecast/v2.0

Tempo like supply contract documentation: https://data.rte-france.com/catalog/-/api/doc/user-guide/Tempo+Like+Supply+Contract/1.1

Consumption documentation: https://data.rte-france.com/catalog/-/api/consumption/Consumption/v1.2

