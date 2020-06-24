import unittest
from api_config import *
from api_rte import *
import datetime


class TestApiRte(unittest.TestCase):

    def test_get_token(self):
        token_type, token = get_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, oauth_url=OAUTH_URL)
        self.assertIsNotNone(token, msg='Authentication failed')
        self.assertIsNotNone(token_type, msg='Authentication failed')

    def test_get_prod_json(self):
        token_type, token = get_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, oauth_url=OAUTH_URL)

        TSTART = datetime.datetime.today() - datetime.timedelta(days=2)
        TEND = datetime.datetime.today()

        r = get_production_json(start_date=TSTART, end_date=TEND, token_type=token_type, access_token=token)
        self.assertTrue('forecasts' in r.keys())
        self.assertFalse('error' in r.keys())

        r = get_production_json(start_date=TSTART,
                                end_date=TEND,
                                token_type=token_type,
                                access_token=token,
                                production_type='WIND',
                                type='D-1')
        self.assertTrue('forecasts' in r.keys())
        self.assertFalse('error' in r.keys())

        r = get_production_json(start_date=TSTART,
                                end_date=TEND,
                                token_type=token_type,
                                access_token=token,
                                production_type='WIND',
                                type='ID')
        self.assertTrue('forecasts' in r.keys())
        self.assertFalse('error' in r.keys())

        r = get_production_json(start_date=TSTART,
                                end_date=TEND,
                                token_type=token_type,
                                access_token=token,
                                production_type='WIND',
                                type='CURRENT')
        self.assertTrue('forecasts' in r.keys())
        self.assertFalse('error' in r.keys())

        r = get_production_json(start_date=TSTART,
                                end_date=TEND,
                                token_type=token_type,
                                access_token=token,
                                production_type='SOLAR',
                                type='D-1')
        self.assertTrue('forecasts' in r.keys())
        self.assertFalse('error' in r.keys())

        r = get_production_json(start_date=TSTART,
                                end_date=TEND,
                                token_type=token_type,
                                access_token=token,
                                production_type='SOLAR',
                                type='CURRENT')
        self.assertTrue('forecasts' in r.keys())
        self.assertFalse('error' in r.keys())

        r = get_production_json(start_date=TSTART,
                                end_date=TEND,
                                token_type=token_type,
                                access_token=token,
                                production_type='SOLAR',
                                type='ID')
        self.assertTrue('forecasts' in r.keys())
        self.assertFalse('error' in r.keys())

    def test_get_tempo_json(self):
        token_type, token = get_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, oauth_url=OAUTH_URL)

        TSTART = datetime.datetime.today() - datetime.timedelta(days=2)
        TEND = datetime.datetime.today() + datetime.timedelta(days=1)
        r = get_tempo_json(start_date=TSTART, end_date=TEND, token_type=token_type, access_token=token)
        self.assertTrue('tempo_like_calendars' in r.keys())
        self.assertFalse('error' in r.keys())

    def test_parse_production(self):
        token_type, token = get_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, oauth_url=OAUTH_URL)

        TSTART = datetime.datetime.today() - datetime.timedelta(days=2)
        TEND = datetime.datetime.today() + datetime.timedelta(days=1)
        r = get_production_json(start_date=TSTART, end_date=TEND, token_type=token_type, access_token=token)
        d = parse_production(r)
        self.assertTrue(isinstance(d, list))
        self.assertTrue(isinstance(d[0], dict))

    def test_get_prod(self):
        TSTART = datetime.datetime.today() - datetime.timedelta(days=2)
        TEND = datetime.datetime.today() + datetime.timedelta(days=0)

        r = get_prod(TSTART, TEND, production_type='SOLAR', type='D-1')
        self.assertTrue(isinstance(r, list))
        self.assertTrue(isinstance(r[0], dict))
        self.assertTrue(isinstance(r[0]['values'], pd.DataFrame))

        r = get_prod(TSTART, TEND, production_type='SOLAR', type='ID')
        self.assertTrue(isinstance(r, list))
        self.assertTrue(isinstance(r[0], dict))
        self.assertTrue(isinstance(r[0]['values'], pd.DataFrame))

        r = get_prod(TSTART, TEND, production_type='SOLAR', type='CURRENT')
        self.assertTrue(isinstance(r, list))
        self.assertTrue(isinstance(r[0], dict))
        self.assertTrue(isinstance(r[0]['values'], pd.DataFrame))


if __name__ == '__main__':
    unittest.main(verbosity=2)
