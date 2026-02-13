#!/usr/bin/env python3
"""
Blackjack Card Counter - Command-line Hi-Lo card counting system.

This program implements the Hi-Lo card counting strategy:
- Low cards (2-6): +1
- Neutral cards (7-9): 0
- High cards (10, J, Q, K, A): -1

The true count is calculated as: running_count / decks_remaining
"""


class CardCounter:
    """Card counter using the Hi-Lo counting system."""
    
    # Hi-Lo counting values
    CARD_VALUES = {
        '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
        '7': 0, '8': 0, '9': 0,
        '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
    }
    
    CARDS_PER_DECK = 52
    
    def __init__(self, num_decks=6):
        """Initialize the card counter.
        
        Args:
            num_decks: Number of decks in the shoe (default: 6)
        """
        self.num_decks = num_decks
        self.running_count = 0
        self.cards_dealt = 0
        self.total_cards = num_decks * self.CARDS_PER_DECK
    
    def count_card(self, card):
        """Add a card to the count.
        
        Args:
            card: Card value (2-10, J, Q, K, A)
            
        Returns:
            The count value for this card
        """
        card = card.upper().strip()
        if card not in self.CARD_VALUES:
            raise ValueError(f"Invalid card: {card}")
        
        count_value = self.CARD_VALUES[card]
        self.running_count += count_value
        self.cards_dealt += 1
        return count_value
    
    def get_decks_remaining(self):
        """Calculate the estimated number of decks remaining.
        
        Returns:
            Number of decks remaining (rounded to 0.5 deck precision)
        """
        cards_remaining = self.total_cards - self.cards_dealt
        decks_remaining = cards_remaining / self.CARDS_PER_DECK
        # Round to nearest 0.5 deck
        return round(decks_remaining * 2) / 2
    
    def get_true_count(self):
        """Calculate the true count.
        
        Returns:
            True count (running count adjusted for remaining decks)
        """
        decks_remaining = self.get_decks_remaining()
        if decks_remaining <= 0:
            return 0
        return self.running_count / decks_remaining
    
    def get_advantage(self):
        """Determine if the deck is player-favorable or dealer-favorable.
        
        Returns:
            String indicating advantage status
        """
        true_count = self.get_true_count()
        if true_count > 1:
            return "player-favorable"
        elif true_count < -1:
            return "dealer-favorable"
        else:
            return "neutral"
    
    def reset(self):
        """Reset the counter to initial state."""
        self.running_count = 0
        self.cards_dealt = 0
    
    def display_status(self):
        """Display the current counting status."""
        decks_remaining = self.get_decks_remaining()
        true_count = self.get_true_count()
        advantage = self.get_advantage()
        
        print(f"\n{'='*50}")
        print(f"Running Count:     {self.running_count:+d}")
        print(f"Decks Remaining:   {decks_remaining:.1f}")
        print(f"True Count:        {true_count:+.2f}")
        print(f"Deck Status:       {advantage.upper()}")
        print(f"{'='*50}\n")


def main():
    """Main function to run the card counter."""
    print("="*50)
    print("BLACKJACK CARD COUNTER - Hi-Lo System")
    print("="*50)
    print("\nCard Values:")
    print("  Low cards (2-6):   +1")
    print("  Neutral (7-9):      0")
    print("  High cards (10-A): -1")
    print("\nCommands:")
    print("  Enter card values (e.g., 2, K, 10, A)")
    print("  'reset' - Reset the count")
    print("  'status' - Show current status")
    print("  'quit' or 'exit' - Exit program")
    print("="*50)
    
    # Ask for number of decks
    while True:
        try:
            num_decks = input("\nHow many decks in the shoe? (default: 6): ").strip()
            if not num_decks:
                num_decks = 6
            else:
                num_decks = int(num_decks)
            if num_decks < 1 or num_decks > 8:
                print("Please enter a number between 1 and 8.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    counter = CardCounter(num_decks)
    counter.display_status()
    
    while True:
        try:
            user_input = input("Enter card(s) or command: ").strip()
            
            if not user_input:
                continue
            
            # Check for commands
            command = user_input.lower()
            if command in ['quit', 'exit', 'q']:
                print("\nThank you for using the Card Counter!")
                break
            elif command == 'reset':
                counter.reset()
                print("\n*** Counter reset ***")
                counter.display_status()
                continue
            elif command == 'status':
                counter.display_status()
                continue
            
            # Process cards (can be space or comma separated)
            cards = user_input.replace(',', ' ').split()
            
            for card in cards:
                try:
                    count_value = counter.count_card(card)
                    print(f"  {card.upper()}: {count_value:+d}")
                except ValueError as e:
                    print(f"  Error: {e}")
            
            counter.display_status()
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the Card Counter!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
