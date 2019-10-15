from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import process, utils

class SingleModifierTestCase(TestCase):
    def test_a(self):
        text = 'ABAB'
        modifiers = [ ( r'(A)(B)',  { 1: 'CC', 2:'D'} ) ]

        processed_text, span_map = process(text, modifiers)
        self.assertEqual( processed_text, 'CCDCCD' )
        self.assertEqual( span_map, [((0, 1), (0, 2)), ((1, 2), (2, 3)), ((2, 3), (3, 5)), ((3, 4), (5, 6))] )

        text_decorated, decorated_processed_text = utils.decorate(text, processed_text, span_map)

        self.assertEqual( text_decorated, '0123' )
        self.assertEqual( decorated_processed_text, '001223' )

    def test_b(self):
        text = 'AABAAB'
        modifiers = [ ( r'(AA)(B)',  { 1: 'C', 2:'D'} ) ]

        processed_text, span_map = process(text, modifiers)
        self.assertEqual( processed_text, 'CDCD' )
        self.assertEqual( span_map, [((0, 2), (0, 1)), ((2, 3), (1, 2)), ((3, 5), (2, 3)), ((5, 6), (3, 4))] )

        text_decorated, decorated_processed_text = utils.decorate(text, processed_text, span_map)

        self.assertEqual( text_decorated, '001223' )
        self.assertEqual( decorated_processed_text, '0123' )

    def test_c(self):
        text = 'ABBABB'
        modifiers = [ ( r'(A)(BB)',  { 1: 'CC', 2:'D'} ) ]

        processed_text, span_map = process(text, modifiers)
        self.assertEqual( processed_text, 'CCDCCD' )
        self.assertEqual( span_map, [((0, 1), (0, 2)), ((1, 3), (2, 3)), ((3, 4), (3, 5)), ((4, 6), (5, 6))] )

        text_decorated, decorated_processed_text = utils.decorate(text, processed_text, span_map)

        self.assertEqual( text_decorated, '011233' )
        self.assertEqual( decorated_processed_text, '001223' )

    def test_new(self):
        numbers = {5: 'five', 8: 'eight', 10: 'ten'}
        orginal_numbers = {1: 'first', 2: 'second'}

        modifiers = [
            ( r'der (G\.) Be',  { 1: 'Graham'} ),
            ( r' (&) ',  { 1: 'and'} ),
            ( r' (etc)\.',  { 1: 'et cetera'} ),
            ( r' ((\d+)((st)|(nd)|(rd)|(th))) ',  { 2: lambda x: orginal_numbers[int(x)], 3: '' } ),
            ( r' (\d+) ',  { 1: lambda x: numbers[int(x)] } ),
            ( r'([^ ]+)',  { 1: lambda x: x } ),
        ]

        text = 'Alexander G. Bell ate 10 apples & 8 cucumbers. The 1st apple was rotten, the 2nd was too, also the third, fourth etc.'
                
        processed_text, span_map = process(text, modifiers)

        text_decorated, decorated_processed_text = utils.decorate(text, processed_text, span_map)

        print (text)
        print (text_decorated)
        print (decorated_processed_text)
        print (processed_text)
        print (span_map)

if __name__ == '__main__':
    tc = SingleModifierTestCase()
    tc.test_new()

    #main()