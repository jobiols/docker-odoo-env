# -*- coding: utf-8 -*-

import unittest


class TestRepository(unittest.TestCase):
    def test_install(self):
        a = 1
        return 'ok' + int(a)