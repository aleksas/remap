from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import process, core, utils

core.__verbose__ = True

class BasicTest(TestCase):
    text_0 = ' AAA BBB CCC DDD '
    text_1 = ' AAA BBB AAA BBB '
    text_2 = ' BBB AAA AAA BBB '
    text_3 = ' AAA AAA AAA AAA '

    modifiers_0 = [
        ( r'(AAA)',  { 1: 'ZZZ' } ),
        ( r'(BBB)',  { 1: 'YYY' } ),
        ( r'(CCC)',  { 1: 'XXX' } ),
        ( r'(DDD)',  { 1: 'WWW' } )
    ]

    modifiers_1 = [
        ( r'(AAA)',  { 1: 'BBB' } ),
    ]

    modifiers_2 = [
        ( r'(AAA)',  { 1: 'BBB' } ),
        ( r'(BBB)',  { 1: 'YYY' } ),
    ]

    modifiers_3 = [
        ( r'(AAA) (BBB)',  { 1: 'CCC', 2: 'CCC' } ),
        ( r'(DDD)',  { 1: 'CCC' } ),
    ]

    modifiers_4 = [
        ( r'(AAA) (BBB) (CCC)',  { 1: 'CCCC', 2: 'CCCC', 3: 'CCCC' } ),
        ( r'(DDD)',  { 1: 'CCCC' } ),
    ]

    modifiers_5 = [
        ( r'(AAA) (BBB) (CCC)',  { 1: 'ZZZZ', 2: 'YYYYY', 3: 'XXXXXX' } ),
        ( r'((YYYYY)|(ZZZZ))',  { 1: 'WWWWWW' } ),
        ( r'(WWWWWW)',  { 1: 'QQQQQQQ' } ),
    ]


    span_map = [
        ((1, 4), (1, 4)),
        ((5, 8), (5, 8)),
        ((9, 12), (9, 12)),
        ((13, 16), (13, 16))
    ]

    span_map_1_1 = [
        ((1, 4), (1, 4)),
        ((9, 12), (9, 12))
    ]

    span_map_2 = [
        ((1, 4), (1, 4)),
        ((5, 8), (5, 8)),
        ((13, 16), (13, 16))
    ]

    span_map_3 = [
        ((1, 4), (1, 5)),
        ((5, 8), (6, 10)),
        ((9, 12), (11, 15)),
        ((13, 16), (16, 20))
    ]

    span_map_4 = [
        ((1, 4), (1, 8)),
        ((5, 8), (9, 16)),
        ((9, 12), (17, 23))
    ]

    def test_0(self):
        text = str(self.text_0)
        text_processed, span_map = process(text, self.modifiers_0)
        self.assertEqual( text_processed, ' ZZZ YYY XXX WWW ' )
        self.assertEqual( span_map, self.span_map )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 111 222 333 ' )
        self.assertEqual( text_processed_decorated, ' 000 111 222 333 ' )

    def test_1(self):
        text = str(self.text_1)
        text_processed, span_map = process(text, self.modifiers_0)
        self.assertEqual( text_processed, ' ZZZ YYY ZZZ YYY ' )
        self.assertEqual( span_map, self.span_map )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 111 222 333 ' )
        self.assertEqual( text_processed_decorated, ' 000 111 222 333 ' )

    def test_2a(self):
        text = str(self.text_1)
        text_processed, span_map = process(text, self.modifiers_1)

        self.assertEqual( text_processed, ' BBB BBB BBB BBB ' )
        self.assertEqual( span_map, self.span_map_1_1 )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 BBB 111 BBB ' )
        self.assertEqual( text_processed_decorated, ' 000 BBB 111 BBB ' )

    def test_2b(self):
        text = str(self.text_3)
        text_processed, span_map = process(text, self.modifiers_1)

        self.assertEqual( text_processed, ' BBB BBB BBB BBB ' )
        self.assertEqual( span_map, self.span_map )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 111 222 333 ' )
        self.assertEqual( text_processed_decorated, ' 000 111 222 333 ' )

    def test_3(self):
        text = str(self.text_2)
        text_processed, span_map = process(text, self.modifiers_0)
        self.assertEqual( text_processed, ' YYY ZZZ ZZZ YYY ' )
        self.assertEqual( span_map, self.span_map )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 111 222 333 ' )
        self.assertEqual( text_processed_decorated, ' 000 111 222 333 ' )

    def test_4(self):
        text = str(self.text_0)
        text_processed, span_map = process(text, self.modifiers_3)
        self.assertEqual( text_processed, ' CCC CCC CCC CCC ' )
        self.assertEqual( span_map, self.span_map_2 )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 111 CCC 222 ' )
        self.assertEqual( text_processed_decorated, ' 000 111 CCC 222 ' )

    def test_5(self):
        text = str(self.text_0)
        text_processed, span_map = process(text, self.modifiers_4)

        self.assertEqual( text_processed, ' CCCC CCCC CCCC CCCC ' )
        self.assertEqual( span_map, self.span_map_3 )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 111 222 333 ' )
        self.assertEqual( text_processed_decorated, ' 0000 1111 2222 3333 ' )

    def test_chain_1(self):
        text = str(self.text_2)
        text_processed, span_map = process(text, self.modifiers_2)

        self.assertEqual( text_processed, ' YYY YYY YYY YYY ' )
        self.assertEqual( span_map, self.span_map )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 111 222 333 ' )
        self.assertEqual( text_processed_decorated, ' 000 111 222 333 ' )

    def test_chain_2(self):
        text = str(self.text_0)
        text_processed, span_map = process(text, self.modifiers_5)

        self.assertEqual( text_processed, ' QQQQQQQ QQQQQQQ XXXXXX DDD ' )
        self.assertEqual( span_map, self.span_map_4 )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_processed_decorated, ' 0000000 1111111 222222 DDD ' )
        self.assertEqual( text_decorated, ' 000 111 222 DDD ' )

    def test_chain_3(self):
        text = 'AZA'

        modifiers = [
            ( r'(A)',  { 1: 'BB' } ),
            ( r'(BB)',  { 1: 'DD' } )
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'DDZDD' )
        self.assertEqual( span_map, [ ((0, 1), (0, 2)), ((2, 3), (3, 5)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '0Z1' )
        self.assertEqual( text_processed_decorated, '00Z11' )


if __name__ == '__main__':
    bt = BasicTest()
    bt.test_chain_2()
    #main()