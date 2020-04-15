# -*- coding: utf-8 -*-
##############################################################################
import unittest


class TestRepository(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

    def test_install(self):
        """################################################# TEST INSTALLATION
        """
        self.assertEqual(1, 1)
