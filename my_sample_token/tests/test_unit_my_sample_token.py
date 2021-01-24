from ..my_sample_token import MySampleToken
from tbears.libs.scoretest.score_test_case import ScoreTestCase


class TestMySampleToken(ScoreTestCase):

    def setUp(self):
        super().setUp()
        self.score = self.get_score_instance(MySampleToken, self.test_account1)

    def test_hello(self):
        self.assertEqual(self.score.hello(), "Hello")
