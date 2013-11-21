# Author: Paul Kippes <kippesp@gmail.com>

import unittest
from pyspatialite import dbapi2 as sqlite

class SpatialTests(unittest.TestCase):
    def setUp(self):
        self.cx = sqlite.connect(":memory:")
        self.cu = self.cx.cursor()

    def tearDown(self):
        self.cx.close()

    def CheckSpatialiteVersion(self):
        s = "SELECT spatialite_version();"
        self.cu.execute(s)
        row = self.cu.fetchone()
        self.assertEqual(row[0], "2.3.1")
    def CheckAsText(self):
        s = "SELECT AsText(GeomFromText('POINT(-110 29)'));"
        self.cu.execute(s)
        row = self.cu.fetchone()
        self.assertEqual(row[0], "POINT(-110 29)")

def suite():
    return unittest.TestSuite(unittest.makeSuite(SpatialTests, "Check"))

def test():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == "__main__":
    test()
