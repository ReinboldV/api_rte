import urllib
import requests
import pandas as pd

from api_config import *


def get_token(oauth_url=OAUTH_URL,
              client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET):
    """

    :param oauth_url:
    :param client_id:
    :param client_secret:
    :return: [token_type, access_token]
    """

    r = requests.post(oauth_url, auth=(client_id, client_secret))
    if r.ok:
        access_token = r.json()['access_token']
        token_type = r.json()['token_type']
    else:
        Warning("Authentication failed")
        access_token = None
        token_type = None

    return token_type, access_token


def get_tempo(start_date, end_date,
              oauth_url=OAUTH_URL,
              client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              url_tempo=URL_TEMPO):
    """

    :param client_secret:
    :param client_id:
    :param oauth_url:
    :param start_date:
    :param end_date:
    :param url_tempo:
    :return:
    """

    token_type, access_token = get_token(oauth_url=oauth_url, client_id=client_id, client_secret=client_secret)
    r_json = get_tempo_json(start_date, end_date, token_type, access_token, url_tempo=url_tempo)
    df = json_to_pd_tempo(r_json)

    return df


def get_prod(start_date, end_date, production_type=None, type=None,
             oauth_url=OAUTH_URL,
             client_id=CLIENT_ID,
             client_secret=CLIENT_SECRET,
             url_prod=URL_PROD):
    """ General method to download RTE forecasts production

    :param start_date:
    :param end_date:
    :param production_type:
    :param type:
    :param oauth_url:
    :param client_id:
    :param client_secret:
    :param url_prod:
    :return:
    """
    token_type, access_token = get_token(oauth_url=oauth_url, client_id=client_id,
                                         client_secret=client_secret)
    res_json = get_production_json(start_date, end_date, token_type, access_token,
                                   production_type=production_type, type=type, url_prod=url_prod)

    res = parse_production(res_json)
    return res


def get_tempo_json(start_date, end_date, token_type, access_token, url_tempo=URL_TEMPO):
    """

    :param access_token:
    :param start_date:
    :param end_date:
    :param token_type:
    :param url_tempo:
    :return:
    """

    start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')
    end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')

    param = {'start_date': start_str, 'end_date': end_str}
    url_tempo = url_tempo
    url_tempo += '?' + urllib.parse.urlencode(param).replace("%3A", ":")

    r = requests.get(url_tempo, headers={'Authorization': f'{token_type} {access_token}'}, params=param)

    return r.json()


def get_production_json(start_date, end_date, token_type,
                        access_token, production_type=None, type=None, url_prod=URL_PROD):
    """

    :param str type:
    :param str production_type:
    :param start_date: starting date of format %Y-%m-%dT%H:%M:%S  (Local French Time)
    :param end_date: end date of format %Y-%m-%dT%H:%M:%S  (Local French Time)
    :param token_type: Bearer
    :param access_token: Token access code
    :param str url_prod: url of the rte production forecasts api (default in api_config.py)
    :return: json forecasts
    """

    start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')
    end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')

    param = {'start_date': start_str, 'end_date': end_str}
    if production_type is not None:
        if production_type in PRODUCTION_TYPE:
            param.update({'production_type': production_type})
        elif production_type is None:
            pass
        else:
            raise ValueError(f'The given production_type={production_type} does not exist in PRODUCTION_TYPE.')
        if type in TYPE:
            param.update({'type': type})
        elif type is None:
            pass
        else:
            raise ValueError(f'The given type={type} does not exist in TYPE.')

    url = url_prod + '?' + urllib.parse.urlencode(param).replace("%3A", ":").replace('%2C', ',')
    r_json = requests.get(url, headers={'Authorization': f'{token_type} {access_token}'}, params=param)

    if not r_json.ok:
        str = f'The request return an error. Status code : {r_json.status_code}, reason : {r_json.reason}. ' \
              f'\n\n {r_json.content}'

        raise ImportError(str)

    return r_json.json()


def _parse_json_values(values):
    """ Convert RTE data data from dictionnry form to pandas DataFrame.

    :param values:
    :return: pandas.DataFrame
    """
    df = pd.DataFrame.from_dict(values)
    df.index = df.start_date
    df.start_date = pd.to_datetime(df.start_date, format='%Y-%m-%d %H:%M:%S', utc=True)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S', utc=True)
    df.updated_date = pd.to_datetime(df.updated_date, format='%Y-%m-%d %H:%M:%S', utc=True)
    df.end_date = pd.to_datetime(df.end_date, format='%Y-%m-%d %H:%M:%S', utc=True)

    return df


def json_to_pd_tempo(r_tempo):
    """ Convert Tempo RTE data from json to pandas data frame

    :param r_tempo:
    :return: pandas.DataFrame
    """
    values_dict = r_tempo.json().get('tempo_like_calendars').get('values')
    df = _parse_json_values(values_dict)
    return df


def parse_production(r):
    """
    Convert Production forecasts RTE data from json to a list of data frames

    :param r:json results of rte production api
    """
    d = []

    for i in range(len(r.get('forecasts'))):

        d.append({})
        forecast = r.get('forecasts')[i]

        d[i]['production_type'] = forecast['production_type']
        d[i]['type'] = forecast['type']

        if 'sub_type' in forecast:
            d[i]['sub_type'] = forecast['sub_type']

        df = _parse_json_values(forecast['values'])
        d[i]['values'] = df
    return d


def json_to_pd_prod(r_prod):
    """
    DEPRECIATED

    Parsing Production RTE data from json to pandas data frame

    :param r_prod:
    :return: pandas.DataFrame
    """

    Warning("json_to_pd_prod() is depreciated and will not be integrated in version 1.2 ")

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


if __name__ == '__main__':
    from api_rte import *
    from api_config import *
    import datetime

    token_type, token = get_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, oauth_url=OAUTH_URL)
    TSTART = datetime.datetime.today() - datetime.timedelta(days=2)
    TEND = datetime.datetime.today() + datetime.timedelta(days=0)

    r = get_prod(TSTART, TEND, production_type='SOLAR', type='ID')
