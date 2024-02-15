'''
Usage: war_card_game.py [--names <name> <name>] [--peace]

Try:
  war_card_game.py --names Tom Jerry

Options:
  -h --help     Show this screen.
  -n --names    Names of the players.
  --peace       Peace mode (lowest card wins).
'''

import random
import sys

from dataclasses import dataclass
from docopt import docopt


@dataclass
class Card:
    suit: str
    value: int
    rank: str = ''

    def __post_init__(self):
        ranks = {11: 'Jack', 12: 'Queen', 13: 'King', 1: 'Ace'}

        if self.value in ranks:
            self.rank = ranks[self.value]
        else:
            self.rank = str(self.value)


class Deck:
    SUITS = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

    def __init__(self) -> None:
        self.cards = [
            Card(suit, value) for value in range(1, 14) for suit in Deck.SUITS
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)


class Player:
    pile: list[Card] = []

    def add_to_pile(cls, *cards: Card):
        for card in cards:
            Player.pile.append(card)

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.cards: list[Card]

    def draw_card(self) -> Card:
        '''
        Draw single card from the top of the deck (end of list).
        '''
        if not self.cards:
            sys.exit(f'No more cards left for {self.name}. Oponent won')

        return self.cards.pop(0)

    def take_pile(self) -> None:
        print(f'{len(Player.pile)} cards taken from pile.')
        self.cards = Player.pile + self.cards
        Player.pile = []

    def take_cards(self, *cards: Card) -> None:
        '''
        Add cards to the bottom of the deck.
        '''
        for card in cards:
            self.cards.append(card)

        if Player.pile:
            self.take_pile()

    def cards_left(self) -> int:
        return len(self.cards)


def draw(player1: Player, player2: Player, peace: bool) -> None:
    card1, card2 = player1.draw_card(), player2.draw_card()
    print(f'{player1.name} "{card1.suit} {card1.rank}" vs '
          f'{player2.name} "{card2.suit} {card2.rank}"')

    if peace:
        if card1.value < card2.value:
            player1.take_cards(card1, card2)
        elif card2.value < card1.value:
            player2.take_cards(card2, card1)
        else:
            print('Draw')
            Player.add_to_pile(card1, card2, player1.draw_card(), player2.draw_card())
    else:
        if card1.value > card2.value:
            player1.take_cards(card1, card2)
        elif card2.value > card1.value:
            player2.take_cards(card2, card1)
        else:
            print('Draw')
            Player.add_to_pile(card1, card2, player1.draw_card(), player2.draw_card())

    print(f'{player1.name} cards: {player1.cards_left()}, '
          f'{player2.name} cards: {player2.cards_left()}')


def main() -> None:
    args: dict = docopt(__doc__)

    names: list[str] = ["Player", "ClosedAI"]
    if args["--names"]:
        names = args["<name>"]

    deck: Deck = Deck()

    player1, player2 = Player(names[0]), Player(names[1])
    player1.cards, player2.cards = deck.cards[::2], deck.cards[1::2]

    round = 1
    while player1.cards and player2.cards:
        print(f'{"-" * 50}\nRound {round}:')

        draw(player1, player2, args['--peace'])

        round += 1

        if not len(player1.cards):
            print(f'{"-"*50}\n{player2.name} won.')
        elif not len(player2.cards):
            print(f'{"-"*50}\n{player1.name} won.')


if __name__ == '__main__':
    main()
