import urllib
import requests
from pyparsing import unicode_set


def get_token(oauth_url='https://digital.iservices.rte-france.com/token/oauth/',
              client_id='7699170f-9898-40d0-b78a-354bae1f36e6',
              client_secret='969de489-1dca-4158-8ad4-9e1ab405cfeb'):

    r = requests.post(oauth_url, auth=(client_id, client_secret))
    acess_token = r.json()['access_token']
    token_type = r.json()['token_type']

    return token_type, acess_token

def get_tempo(start_date, end_date, token_type, acess_token, url_tempo='https://digital.iservices.rte-france.com/open_api/tempo_like_supply_contract/v1/tempo_like_calendars'):
    """

    :param start_date:
    :param end_date:
    :param token_type:
    :param acess_token:
    :param url_tempo:
    :return:
    """

    start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')
    end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')

    param = {'start_date': start_str, 'end_date': end_str}
    url_tempo = url_tempo
    url_tempo += '?' + urllib.parse.urlencode(param).replace("%3A", ":")

    r = requests.get(url_tempo, headers={'Authorization': f'{token_type} {acess_token}'}, params=param)

    return r


def get_production(start_date, end_date, token_type, acess_token,
                   url_tempo='https://digital.iservices.rte-france.com/open_api/generation_forecast/v2/forecasts'):

    """

    :param start_date: starting date of format %Y-%m-%dT%H:%M:%S  (Local French Time)
    :param end_date: end date of format %Y-%m-%dT%H:%M:%S  (Local French Time)
    :param token_type: Bearer
    :param acess_token: Token code access
    :param production_type: None (default), AGGREGATED_FRANCE, WIND, SOLAR, AGGREGATED_CPC, MDSE
    :param type:
    :param url_tempo:
    :return:
    """

    start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')
    end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')

    param = {'start_date': start_str, 'end_date': end_str}
    url  = url_tempo+'?' + urllib.parse.urlencode(param).replace("%3A", ":").replace('%2C', ',')
    r = requests.get(url, headers={'Authorization': f'{token_type} {acess_token}'}, params=param)

    return r.json()


def json_to_pd_tempo(r_tempo):

    import pandas as pd

    list = r_tempo.json().get('tempo_like_calendars').get('values')

    start  = []
    end    = []
    value  = []
    update = []

    for d in list:
        start.append(d['start_date'])
        end.append(d['end_date'])
        value.append(d['value'])
        update.append(d['updated_date'])

    df_tempo        = pd.DataFrame({'start_date'   : start, 'end_date' : end,
                                    'updated_date' : update, 'value'   : value}, index=start)
    df_tempo.start_date   = pd.to_datetime(df_tempo.start_date,     format='%Y-%m-%d %H:%M:%S', utc=True)
    df_tempo.index        = pd.to_datetime(df_tempo.index,          format='%Y-%m-%d %H:%M:%S', utc=True)
    df_tempo.end_date     = pd.to_datetime(df_tempo.end_date,       format='%Y-%m-%d %H:%M:%S', utc=True)
    df_tempo.updated_date = pd.to_datetime(df_tempo.updated_date,   format='%Y-%m-%d %H:%M:%S', utc=True)

    return df_tempo


def json_to_pd_prod(r_prod):
    import pandas as pd

    colname = []
    start = []
    end = []
    value = []
    update = []

    df = {}

    for col in range(len(r_prod.get('forecasts'))):
        json_col = r_prod.get('forecasts')[col]
        name = json_col['production_type'] + '_' + json_col['type']
        if 'sub_type' in json_col.keys():
            name += '_' + json_col['sub_type']

        colname.append(name)
        start.append([])
        end.append([])
        value.append([])
        update.append([])

        for d in r_prod.get('forecasts')[col].get('values'):
            start[col].append(d['start_date'])
            end[col].append(d['end_date'])
            value[col].append(d['value'])
            update[col].append(d['updated_date'])

        df[colname[col]] = pd.DataFrame({'start_date': start[col], colname[col] + '_value': value[col]},
                                        index=start[col])

    df2 = pd.merge(df[colname[0]], df[colname[1]], on='start_date', how='outer')

    for col in range(2, len(r_prod.get('forecasts'))):
        df2 = pd.merge(df2, df[colname[col]], on='start_date', how='outer')

    df2.start_date = pd.to_datetime(df2.start_date, format='%Y-%m-%d %H:%M:%S', utc=True)

    KEYS = ['start_date',
            'AGGREGATED_PROGRAMMABLE_FRANCE_D-1_value', 'AGGREGATED_NON_PROGRAMMABLE_FRANCE_D-1_value',
            'WIND_D-1_value', 'WIND_ID_value', 'WIND_CURRENT_value',
            'SOLAR_D-1_value', 'SOLAR_ID_value', 'SOLAR_CURRENT_value']

    df2 = df2[KEYS]

    df2.index = df2.start_date
    df2.drop('start_date', axis=1, inplace=True)

    return df2