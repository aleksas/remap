from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import process, core, utils

core.__verbose__ = True

class IntersectingModifierTestCase(TestCase):
    def test_chain_1(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(C BBBBB C)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'DD' )
        self.assertEqual( span_map, [ ((1, 4), (1, 3)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '000' )
        self.assertEqual( text_processed_decorated, '00' )

if __name__ == '__main__':
    main()