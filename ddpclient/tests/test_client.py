from unittest import TestCase

import ddpclient

class TestJoke(TestCase):
    def test_is_string(self):
        s = ddpclient.main()
        self.assertTrue(s == 'hello')