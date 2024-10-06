import random
from typing import List

# Card class represents a single card in the deck
class Card:
    def __init__(self, rank: str, suit: str) -> None:
        
        #Initializes a card with a rank (for example: 2, J, A) and a suit (for example: Hearts, Spades).
        
        self.rank: str = rank
        self.suit: str = suit

    def value(self) -> int:
        
        #Returns the value of the card. Number cards return their rank as an integer.
        #Face cards (J, Q, K) return 10, and Ace (A) returns 11.
        
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

    def __str__(self) -> str:
        
        #Returns the card as a readable string, e.g., "10 of Hearts".
        
        return f'{self.rank} of {self.suit}'

# Deck class represents a deck of 52 playing cards
class Deck:
    def __init__(self) -> None:
        
        #Creates a deck with 52 cards (13 ranks in 4 suits) and shuffles it.
        
        suits: List[str] = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks: List[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards: List[Card] = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)  # Shuffle the deck

    def draw_card(self) -> Card:
        
        #Draws and returns the top card from the deck.
    
        return self.cards.pop()

# Player class represents a player in the game (can be the user or the dealer)
class Player:
    def __init__(self, name: str) -> None:
        
        #Initializes a player with a name and an empty hand.
        
        self.name: str = name
        self.hand: List[Card] = []

    def draw(self, deck: Deck) -> None:
        
        #Draws a card from the deck and adds it to the player's hand.
        
        self.hand.append(deck.draw_card())

    def hand_value(self) -> int:
        
        #Calculates the total value of the player's hand, adjusting for aces if necessary.
        
        value: int = sum(card.value() for card in self.hand)
        aces: int = sum(1 for card in self.hand if card.rank == 'A')
        # If value is over 21 and there are aces, count some aces as 1 instead of 11
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def show_hand(self) -> None:
    
    #Displays the player's hand to the console.
    
        hand_str: str = ""
        for card in self.hand:
            hand_str += str(card) + ', '
        hand_str = hand_str[:-2]  # Removes the last comma and space
        print(f'{self.name}\'s hand: {hand_str} (Value: {self.hand_value()})')


# BlackjackGame class controls the game logic
class BlackjackGame:
    def __init__(self) -> None:
        
        #Initializes the game with a deck, a player, and a dealer.
        
        self.deck: Deck = Deck()
        self.player: Player = Player('Player')
        self.dealer: Player = Player('Dealer')

    def play(self) -> None:
        
        #Plays one round of Blackjack.
        
        # Player and dealer draw two cards each
        for _ in range(2):
            self.player.draw(self.deck)
            self.dealer.draw(self.deck)

        # Show the player's hand and one of the dealer's cards
        self.player.show_hand()
        print(f'{self.dealer.name} shows: {self.dealer.hand[0]}')

        # Player's turn: choose to hit or stand
        while self.player.hand_value() < 21:
            action: str   = input('Do you want to hit or stand? (h/s): ').lower()
            if action == 'h':
                self.player.draw(self.deck)
                self.player.show_hand()
            else:
                break

        # Check if player busts
        if self.player.hand_value() > 21:
            print('You busted! Dealer wins.')
            return

        # Dealer's turn: dealer hits until hand value is at least 17
        while self.dealer.hand_value() < 17:
            self.dealer.draw(self.deck)

        # Show the dealer's full hand
        self.dealer.show_hand()

        # Determine the winner
        if self.dealer.hand_value() > 21:
            print('Dealer busts! You win.')
        elif self.player.hand_value() > self.dealer.hand_value():
            print('You win!')
        elif self.player.hand_value() < self.dealer.hand_value():
            print('Dealer wins.')
        else:
            print('It\'s a tie!')

# Main function to start the game
def main() -> None:
    
    #Starts a new game of Blackjack.

    game: BlackjackGame = BlackjackGame()
    game.play()

if __name__ == '__main__':
    main()
