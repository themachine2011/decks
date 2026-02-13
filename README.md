# Blackjack Card Counter

A command-line card-counting system for blackjack using the Hi-Lo counting strategy.

## Features

- **Hi-Lo Counting System**: Standard card counting where low cards (2-6) add +1, high cards (10-A) subtract -1, and neutral cards (7-9) have no effect
- **Running Count**: Tracks the cumulative count of all cards dealt
- **True Count**: Adjusts the running count based on remaining decks (running count / decks remaining)
- **Deck Status**: Indicates if the deck is player-favorable, dealer-favorable, or neutral
- **Multi-deck Support**: Configure for 1-8 decks in the shoe

## Usage

Run the card counter:

```bash
python3 card_counter.py
```

### Commands

- **Enter cards**: Type card values (2-10, J, Q, K, A) separated by spaces or commas
  - Example: `2 5 K A` or `2, 5, K, A`
- **status**: Display current counting statistics
- **reset**: Reset the counter to zero
- **quit** or **exit**: Exit the program

## Example Session

```
BLACKJACK CARD COUNTER - Hi-Lo System
==================================================

Card Values:
  Low cards (2-6):   +1
  Neutral (7-9):      0
  High cards (10-A): -1

Commands:
  Enter card values (e.g., 2, K, 10, A)
  'reset' - Reset the count
  'status' - Show current status
  'quit' or 'exit' - Exit program
==================================================

How many decks in the shoe? (default: 6): 6

==================================================
Running Count:     +0
Decks Remaining:   6.0
True Count:        +0.00
Deck Status:       NEUTRAL
==================================================

Enter card(s) or command: 2 3 K A
  2: +1
  3: +1
  K: -1
  A: -1

==================================================
Running Count:     +0
Decks Remaining:   6.0
True Count:        +0.00
Deck Status:       NEUTRAL
==================================================

Enter card(s) or command: 2 2 3 4 5 6
  2: +1
  2: +1
  3: +1
  4: +1
  5: +1
  6: +1

==================================================
Running Count:     +6
Decks Remaining:   6.0
True Count:        +1.00
Deck Status:       NEUTRAL
==================================================
```

## How It Works

The Hi-Lo card counting system assigns values to cards:
- **Low cards (2, 3, 4, 5, 6)**: +1 each
- **Neutral cards (7, 8, 9)**: 0 each
- **High cards (10, J, Q, K, A)**: -1 each

As cards are dealt:
1. The **running count** accumulates these values
2. The **decks remaining** is estimated based on cards dealt
3. The **true count** is calculated: running count ÷ decks remaining
4. The **deck status** indicates advantage:
   - True count > +1: Player-favorable (more high cards remaining)
   - True count < -1: Dealer-favorable (more low cards remaining)
   - Otherwise: Neutral

A positive true count suggests the remaining deck has more high cards, which favors the player.