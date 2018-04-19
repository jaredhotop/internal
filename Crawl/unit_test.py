import unittest
import entry_class
import stores

class LinkTest(unittest.TestCase):

    def test_menards(self):
        obj = entry_class.Entry('7','1234','4665',False,False,'1',\
        'https://www.menards.com/main/building-materials/panel-products/construction-panels/sheathing/osb-sheathing/4-x-8-osb/p-1444422395209-c-13330.htm','90')
        obj.crawl()
        print(obj)
        self.assertEqual('16.25',obj.comp_price)
        print('testing')

unittest.main()
