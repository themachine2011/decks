#!/usr/bin/env python3
"""
Blackjack Card Counter - Command-line Hi-Lo card counting system.

This program implements the Hi-Lo card counting strategy:
- Low cards (2-6): +1
- Neutral cards (7-9): 0
- High cards (10, J, Q, K, A): -1

The true count is calculated as: running_count / decks_remaining
"""


# ANSI color codes for visual feedback
class Colors:
    RED = '\033[91m'      # Hot cards (high)
    BLUE = '\033[94m'     # Cold cards (low)
    YELLOW = '\033[93m'   # Neutral cards
    GREEN = '\033[92m'    # Player favorable
    CYAN = '\033[96m'     # Information
    BOLD = '\033[1m'
    RESET = '\033[0m'


class CardCounter:
    """Card counter using the Hi-Lo counting system."""
    
    # Hi-Lo counting values
    CARD_VALUES = {
        '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
        '7': 0, '8': 0, '9': 0,
        '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
    }
    
    # All ranks in the shoe
    ALL_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    CARDS_PER_DECK = 52
    MAX_HISTORY = 5  # Keep last 5 batches in history
    COLD_CARDS_THRESHOLD = 60  # Threshold of low cards (2-6) dealt for player-favorable game
    
    def __init__(self, num_decks=8):
        """Initialize the card counter.
        
        Args:
            num_decks: Number of decks in the shoe (fixed at 8 for real shoe validation)
        """
        self.num_decks = 8  # Fixed at 8 decks for per-rank validation
        self.running_count = 0
        self.cards_dealt = 0
        self.total_cards = self.num_decks * self.CARDS_PER_DECK  # 416 cards
        self.max_per_rank = 4 * self.num_decks  # 32 cards per rank in 8 decks
        
        # Temperature tracking
        self.total_hot = 0      # Total high cards dealt
        self.total_cold = 0     # Total low cards dealt
        self.total_neutral = 0  # Total neutral cards dealt
        
        # Per-rank tracking for real shoe validation
        self.rank_counts = {rank: 0 for rank in self.ALL_RANKS}
        
        # History of batches
        self.history = []  # List of (batch_cards, hot, cold, neutral) tuples
    
    def normalize_card(self, card):
        """Normalize card input (handle 't' -> '10', case, whitespace).
        
        Args:
            card: Raw card input string
            
        Returns:
            Normalized card string
        """
        card = card.upper().strip()
        # Handle 't' or 'T' as '10'
        if card == 'T':
            card = '10'
        return card
    
    def validate_batch(self, cards):
        """Validate that a batch of cards doesn't exceed per-rank limits.
        
        Args:
            cards: List of card strings to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Count cards in this batch by rank
        batch_counts = {rank: 0 for rank in self.ALL_RANKS}
        
        for card in cards:
            normalized = self.normalize_card(card)
            if normalized not in self.CARD_VALUES:
                return False, f"Invalid card: {card}"
            batch_counts[normalized] += 1
        
        # Check if applying this batch would exceed any rank limits
        for rank in self.ALL_RANKS:
            new_count = self.rank_counts[rank] + batch_counts[rank]
            if new_count > self.max_per_rank:
                return False, f"would exceed max for {rank} (attempted {new_count}/{self.max_per_rank})"
        
        return True, None
    
    def count_card(self, card):
        """Add a card to the count.
        
        Args:
            card: Card value (2-10, J, Q, K, A, or T for 10)
            
        Returns:
            Tuple of (count_value, temperature) where temperature is:
            - 'hot': High cards (10-A) with -1 value
            - 'cold': Low cards (2-6) with +1 value
            - 'neutral': Mid cards (7-9) with 0 value
            
        Note: Temperature describes cards dealt (removed from deck).
        """
        card = self.normalize_card(card)
        if card not in self.CARD_VALUES:
            raise ValueError(f"Invalid card: {card}")
        
        count_value = self.CARD_VALUES[card]
        self.running_count += count_value
        self.cards_dealt += 1
        
        # Update per-rank count
        self.rank_counts[card] += 1
        
        # Determine card temperature based on Hi-Lo value
        # 'cold' = low cards (2-6) that add +1 to count
        # 'hot' = high cards (10-A) that subtract -1 from count
        # 'neutral' = mid cards (7-9) with 0 effect
        if count_value > 0:
            temperature = 'cold'
            self.total_cold += 1
        elif count_value < 0:
            temperature = 'hot'
            self.total_hot += 1
        else:
            temperature = 'neutral'
            self.total_neutral += 1
        
        return count_value, temperature
    
    def get_card_color(self, temperature):
        """Get the color code for a card based on its temperature.
        
        Args:
            temperature: 'hot', 'cold', or 'neutral'
            
        Returns:
            ANSI color code
        """
        if temperature == 'hot':
            return Colors.RED
        elif temperature == 'cold':
            return Colors.BLUE
        else:
            return Colors.YELLOW
    
    def get_decks_remaining(self):
        """Calculate the estimated number of decks remaining.
        
        Returns:
            Number of decks remaining (rounded to 0.5 deck precision)
        """
        cards_remaining = self.total_cards - self.cards_dealt
        decks_remaining = cards_remaining / self.CARDS_PER_DECK
        # Round to nearest 0.5 deck, with minimum of 0.5 to prevent extreme values
        rounded = round(decks_remaining * 2) / 2
        return max(0.5, rounded)
    
    def get_true_count(self):
        """Calculate the true count.
        
        Returns:
            True count (running count adjusted for remaining decks)
        """
        decks_remaining = self.get_decks_remaining()
        return self.running_count / decks_remaining
    
    def is_60_card_favorable(self):
        """Check if the game is favorable due to 60+ cold cards dealt.
        
        Returns:
            True if 60 or more cold cards (low cards 2-6) have been dealt
        """
        return self.total_cold >= self.COLD_CARDS_THRESHOLD
    
    def get_advantage(self):
        """Determine if the deck is player-favorable or dealer-favorable.
        
        Returns:
            String indicating advantage status
        """
        # Check if 60+ cold cards (low cards) have been dealt
        if self.is_60_card_favorable():
            return "player-favorable"
        
        # Otherwise, use true count logic
        true_count = self.get_true_count()
        if true_count > 1:
            return "player-favorable"
        elif true_count < -1:
            return "dealer-favorable"
        else:
            return "neutral"
    
    def add_to_history(self, batch_cards, hot_count, cold_count, neutral_count):
        """Add a batch of cards to the history.
        
        Args:
            batch_cards: List of card strings in the batch
            hot_count: Number of hot cards in the batch
            cold_count: Number of cold cards in the batch
            neutral_count: Number of neutral cards in the batch
        """
        self.history.append({
            'cards': batch_cards,
            'hot': hot_count,
            'cold': cold_count,
            'neutral': neutral_count
        })
        
        # Keep only the last MAX_HISTORY batches
        if len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)
    
    def display_history(self):
        """Display the history of card batches."""
        if not self.history:
            print(f"\n{Colors.CYAN}No history available yet.{Colors.RESET}\n")
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
        print(f"CARD BATCH HISTORY (Last {len(self.history)} batches)")
        print(f"{'='*60}{Colors.RESET}\n")
        
        for i, batch in enumerate(self.history, 1):
            cards_str = ', '.join(batch['cards'])
            print(f"{Colors.BOLD}Batch {i}:{Colors.RESET} {cards_str}")
            print(f"  {Colors.RED}Hot (High cards):{Colors.RESET}     {batch['hot']}")
            print(f"  {Colors.BLUE}Cold (Low cards):{Colors.RESET}    {batch['cold']}")
            print(f"  {Colors.YELLOW}Neutral (Mid cards):{Colors.RESET}  {batch['neutral']}")
            print()
        
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")
    
    def display_composition(self):
        """Display the current per-rank card counts."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
        print(f"CARD COMPOSITION (Per-Rank Counts)")
        print(f"{'='*60}{Colors.RESET}\n")
        
        for rank in self.ALL_RANKS:
            count = self.rank_counts[rank]
            remaining = self.max_per_rank - count
            bar_length = int((count / self.max_per_rank) * 20)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            
            # Color based on how many dealt
            if count == 0:
                color = Colors.RESET
            elif count < self.max_per_rank // 2:
                color = Colors.GREEN
            elif count < self.max_per_rank:
                color = Colors.YELLOW
            else:
                color = Colors.RED
            
            print(f"  {color}{rank:>2}: {count:2}/{self.max_per_rank} {bar} ({remaining} remaining){Colors.RESET}")
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}\n")
    
    def reset(self):
        """Reset the counter to initial state."""
        self.running_count = 0
        self.cards_dealt = 0
        self.total_hot = 0
        self.total_cold = 0
        self.total_neutral = 0
        self.rank_counts = {rank: 0 for rank in self.ALL_RANKS}
        self.history = []
    
    def display_status(self):
        """Display the current counting status."""
        decks_remaining = self.get_decks_remaining()
        true_count = self.get_true_count()
        advantage = self.get_advantage()
        
        # Determine status color
        if advantage == "player-favorable":
            status_color = Colors.GREEN
        elif advantage == "dealer-favorable":
            status_color = Colors.RED
        else:
            status_color = Colors.YELLOW
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
        print(f"DECK STATUS")
        print(f"{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}Running Count:{Colors.RESET}     {self.running_count:+d}")
        print(f"{Colors.BOLD}Decks Remaining:{Colors.RESET}   {decks_remaining:.1f}")
        print(f"{Colors.BOLD}True Count:{Colors.RESET}        {true_count:+.2f}")
        print(f"{Colors.BOLD}Deck Status:{Colors.RESET}       {status_color}{advantage.upper()}{Colors.RESET}")
        
        # Special message when 60+ cold cards have been dealt
        if self.is_60_card_favorable():
            print(f"\n{Colors.BOLD}{Colors.GREEN}*** Jogo favoravel ao jogador! (60+ cartas baixas sairam) ***{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}CUMULATIVE CARD TOTALS:{Colors.RESET}")
        print(f"  {Colors.RED}Hot cards (High):{Colors.RESET}     {self.total_hot}")
        print(f"  {Colors.BLUE}Cold cards (Low):{Colors.RESET}    {self.total_cold}")
        print(f"  {Colors.YELLOW}Neutral cards (Mid):{Colors.RESET}  {self.total_neutral}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")


def main():
    """Main function to run the card counter."""
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print("BLACKJACK CARD COUNTER - Hi-Lo System (8-Deck Shoe)")
    print(f"{'='*60}{Colors.RESET}")
    print(f"\n{Colors.BOLD}Card Values:{Colors.RESET}")
    print(f"  {Colors.BLUE}Cold cards (2-6):{Colors.RESET}   +1 (Low cards)")
    print(f"  {Colors.YELLOW}Neutral (7-9):{Colors.RESET}      0 (Mid cards)")
    print(f"  {Colors.RED}Hot cards (10-A):{Colors.RESET}  -1 (High cards)")
    print(f"\n{Colors.BOLD}Commands:{Colors.RESET}")
    print("  Enter card values (e.g., 2, K, 10, A, or T for 10)")
    print("  'status' - Show current status")
    print("  'history' - Show card batch history")
    print("  'composition' - Show per-rank card counts")
    print("  'reset' - Reset the count")
    print("  'quit' or 'exit' - Exit program")
    print(f"\n{Colors.BOLD}Note:{Colors.RESET} 8-deck shoe (416 cards), max 32 per rank")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    counter = CardCounter()
    counter.display_status()
    
    while True:
        try:
            user_input = input("Enter card(s) or command: ").strip()
            
            if not user_input:
                continue
            
            # Check for commands
            command = user_input.lower()
            if command in ['quit', 'exit']:
                print(f"\n{Colors.CYAN}Thank you for using the Card Counter!{Colors.RESET}")
                break
            elif command == 'reset':
                counter.reset()
                print(f"\n{Colors.YELLOW}*** Counter reset ***{Colors.RESET}")
                counter.display_status()
                continue
            elif command == 'status':
                counter.display_status()
                continue
            elif command == 'history':
                counter.display_history()
                continue
            elif command in ['composition', 'counts']:
                counter.display_composition()
                continue
            
            # Process cards (can be space or comma separated)
            cards = user_input.replace(',', ' ').split()
            
            # Validate batch before applying
            is_valid, error_msg = counter.validate_batch(cards)
            if not is_valid:
                print(f"\n{Colors.RED}Invalid input: {error_msg}. Batch ignored.{Colors.RESET}\n")
                continue
            
            # Track temperature for this batch
            batch_hot = 0
            batch_cold = 0
            batch_neutral = 0
            valid_cards = []
            
            print()  # Add spacing
            for card in cards:
                try:
                    count_value, temperature = counter.count_card(card)
                    color = counter.get_card_color(temperature)
                    normalized = counter.normalize_card(card)
                    print(f"  {color}{normalized}: {count_value:+d} ({temperature}){Colors.RESET}")
                    
                    # Track batch statistics
                    if temperature == 'hot':
                        batch_hot += 1
                    elif temperature == 'cold':
                        batch_cold += 1
                    else:
                        batch_neutral += 1
                    
                    valid_cards.append(normalized)
                except ValueError as e:
                    print(f"  {Colors.RED}Error: {e}{Colors.RESET}")
            
            # Display batch temperature summary
            if valid_cards:
                print(f"\n{Colors.BOLD}Batch Temperature Summary:{Colors.RESET}")
                print(f"  {Colors.RED}Hot (High):{Colors.RESET}     {batch_hot}")
                print(f"  {Colors.BLUE}Cold (Low):{Colors.RESET}    {batch_cold}")
                print(f"  {Colors.YELLOW}Neutral (Mid):{Colors.RESET}  {batch_neutral}")
                
                # Add to history
                counter.add_to_history(valid_cards, batch_hot, batch_cold, batch_neutral)
            
            counter.display_status()
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}Thank you for using the Card Counter!{Colors.RESET}")
            break


if __name__ == "__main__":
    main()
