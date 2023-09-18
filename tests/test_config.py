import unittest
from api_rte.config import *


class TestConfig(unittest.TestCase):

    def testAuth(self):
        import requests
        r = requests.post(OAUTH_URL, auth=(CLIENT_ID, CLIENT_SECRET))
        self.assertEqual(r.ok, True)
        self.assertEqual(r.status_code, 200)
        if r.ok:
            print(f'Authentication succeeded ')
        else:
            print(f'Authentication failed \n Reason: {r.reason} \n Status_code: {r.status_code}')


if __name__ == "__main__":
    unittest.main()
