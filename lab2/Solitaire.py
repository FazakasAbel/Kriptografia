import numpy 

class Solitaire:

    deck = numpy.array([])

    def __init__(self, deck = []):
        print("initialized Solitaire")
        if len(deck) != 54:
            self.__init_deck()
        else:
            self.setDeck(numpy.array(deck))

    def __init_deck(self):
        self.deck = numpy.arange(1, 55)
        
    def setDeck(self, deck):
        self.deck = deck     

    def __find_white_joker(self):
        return numpy.where(self.deck == 53)[0][0]   

    def __find_black_joker(self):
        return numpy.where(self.deck == 54)[0][0]

    def __first_step(self):
        white_joker_pos = self.__find_white_joker()
        if white_joker_pos == 53:
            numpy.delete(self.deck, white_joker_pos)
            numpy.insert(self.deck, 1, 53)
            return 1

        self.deck[white_joker_pos], self.deck[white_joker_pos + 1] = self.deck[white_joker_pos + 1], self.deck[white_joker_pos]  
        return white_joker_pos + 1

    def __second_step(self):
        black_joker_pos = self.__find_black_joker()
        self.deck = numpy.delete(self.deck, black_joker_pos)

        if black_joker_pos == 53:
            self.deck = numpy.insert(self.deck, 2, 54)
            return 2

        if black_joker_pos == 52:
            self.deck = numpy.insert(self.deck, 1, 54)
            return 1   

        self.deck = numpy.insert(self.deck, black_joker_pos + 2, 54)
        return black_joker_pos + 2

    def __shuffle(self):
        first_joker_pos = self.__first_step()
        second_joker_pos = self.__second_step()
        if first_joker_pos > second_joker_pos:
            first_joker_pos, second_joker_pos = second_joker_pos, first_joker_pos

        self.deck = numpy.concatenate((self.deck[second_joker_pos + 1:], self.deck[first_joker_pos:second_joker_pos + 1], self.deck[0:first_joker_pos]))
        
        if self.deck[-1] < 53:
            self.deck = numpy.concatenate((self.deck[self.deck[-1]:-1], self.deck[0:self.deck[-1]], [self.deck[-1]]))
        
        if self.deck[0] < 53:
            return self.deck[self.deck[0]]
        
        return self.__shuffle()

    def generate_bits(self, amount):

        return [self.__shuffle() for i in range(amount)]           