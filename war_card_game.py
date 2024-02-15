'''
Usage: war_card_game.py [--names <name> <name>] [--peace]

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

        if self.rank in ranks:
            self.rank = ranks[self.value]


class Deck:
    SUITS = ['spades', 'clubs', 'hearts', 'diamonds']
    def __init__(self) -> None:
        self.cards: list[Card] = [Card(suit=color, value=value)for value
                                  in range(1, 14) for color in Deck.SUITS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)


class Player:
    pile: list[Card] = []

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.cards: list[Card] = []

    def draw_card(self) -> Card:
        '''Take a card from the top of the deck.

        Returns:
            tuple: with card value and color, e.g. (4, 'spades')
        '''
        if not self.cards:
            sys.exit(f'No more cards left for {self.name}. Oponent won')

        return self.cards.pop(0)

    def add_cards(self, card: Card) -> None:
        '''Add card to the bottom of the deck.

        Args:
            cards (list): with card value and color, e.g. [(4, 'spades')]
        '''
        self.cards.append(card)

        if Player.pile:
            print(f'Cards left in pile: {len(Player.pile)}')
            self.cards = Player.pile + self.cards
            Player.pile = []

    def cards_left(self) -> int:
        return len(self.cards)


def draw(p1: Player, p2: Player, peace: bool) -> None:
    card1, card2 = p1.draw_card(), p2.draw_card()
    print(f'{p1.name} "{card1.suit} {card1.value}" vs {p2.name} "{card2.suit} {card2.value}"')

    if peace:
        if card1.value < card2.value:
            p1.add_cards(card1)
            p1.add_cards(card2)
        elif card2.value < card1.value:
            p2.add_cards(card2)
            p2.add_cards(card1)
        else:
            print('Draw')
            Player.pile.extend([card1] + [card2] + [p1.draw_card()] + [p2.draw_card()])
    else:
        if card1.value > card2.value:
            p1.add_cards(card1)
            p1.add_cards(card2)
        elif card2.value > card1.value:
            p2.add_cards(card2)
            p2.add_cards(card1)
        else:
            print('Draw')
            Player.pile.extend([card1] + [card2] + [p1.draw_card()] + [p2.draw_card()])

    print(f'{p1.name} cards: {p1.cards_left()}, {p2.name} cards: {p2.cards_left()}')
    print('-' * 50)

def main() -> None:
    args: dict = docopt(__doc__)

    names: list[str] = ["Player", "ClosedAI"]
    if args["--names"]:
        names = args["<name>"]

    deck: Deck = Deck()

    player, computer = Player(names[0]), Player(names[1])
    player.cards, computer.cards = deck.cards[::2], deck.cards[1::2]

    round = 1
    while player.cards and computer.cards:
        print(f'Round {round}:')

        draw(player, computer, args['--peace'])

        round += 1

        if not len(player.cards):
            print(f'{computer.name} won.')
        if not len(computer.cards):
            print(f'{player.name} won.')


if __name__ == '__main__':
    main()
