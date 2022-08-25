import unittest
from packages import create_ec2_instance


class TestEc2(unittest.TestCase):
    def test_ec2_instance(self):
        assert create_ec2_instance()


if __name__ == '__main__':
    unittest.main()
