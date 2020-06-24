# API RTE Data

Code source for downloading rte data using rte digital on-line services : https://data.rte-france.com/

Procedure to follow:

1) Create a profile at https://data.rte-france.com/.
    
2) Create an application for web server and start associating API to this application. Note that you won't have access to API if note associated with you application. 
        
    In the application tab, one will find the `client id` and the related `client secret` code needed for requesting data. Add those to the configuration file `api_config.py`.

        CLIENT_ID     = '7699170f-9898-40d0-b78a-XXXXXXXXXXXX'
        CLIENT_SECRET = '969de489-1dca-4158-8ad4-XXXXXXXXXXXX'
    
3) Testing the configuration and the api :
    
        python tests/test_conf.py
        python tests/test_api.py
        
4) Requesting data.

    For requesting data, one can rely on the documentation available for each API. See https://data.rte-france.com/catalog/-/api/user_guide/231845 for production for instance. 
    
    This code already include routine method for downloading production and Tempo tarifs, respectively `get_tempo()` and `get_prod()`.
     
     Basically, those method make a get request to the server API, using client id and client secret code, passing parameter such as dates, production type, depending on the API (see documentation for each API to learn about parameters and formats). 
            
            start_date = datetime.datetime.today() - datetime.timedelta(days=2) # before yesterday
            end_date   = datetime.datetime.today() + datetime.timedelta(days=1) # tomorrow 
            
            r_tempo = get_tempo(start_date, end_date)
    
    In this example, get_tempo() method returns data using pandas DataFrame.

5) Generation Forecast : https://data.rte-france.com/catalog/-/api/generation/Generation-Forecast/v2.0

Consumption : https://data.rte-france.com/catalog/-/api/consumption/Consumption/v1.2

