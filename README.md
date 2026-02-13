# Blackjack Card Counter

A command-line card-counting system for blackjack using the Hi-Lo counting strategy with color-coded visual feedback, batch temperature tracking, and history features.

## Features

- **Hi-Lo Counting System**: Standard card counting where low cards (2-6) add +1, high cards (10-A) subtract -1, and neutral cards (7-9) have no effect
- **Color-Coded Display**: Visual feedback with colors for different card types:
  - 🔵 Blue for "cold" cards (low cards: 2-6)
  - 🔴 Red for "hot" cards (high cards: 10-A)
  - 🟡 Yellow for neutral cards (7-9)
  - 🟢 Green for player-favorable deck status
- **Temperature Summary**: After each batch of cards, see how many hot, cold, and neutral cards were dealt
- **Cumulative Totals**: Track total hot, cold, and neutral cards dealt throughout the session
- **Batch History**: Review the last 5 batches of cards entered with their temperature breakdown
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
- **history**: View the last 5 batches of cards entered with temperature breakdown
- **reset**: Reset the counter to zero (clears all data including history)
- **quit** or **exit**: Exit the program

## Example Session

```
============================================================
BLACKJACK CARD COUNTER - Hi-Lo System
============================================================

Card Values:
  Cold cards (2-6):   +1 (Low cards)
  Neutral (7-9):      0 (Mid cards)
  Hot cards (10-A):  -1 (High cards)

Commands:
  Enter card values (e.g., 2, K, 10, A)
  'status' - Show current status
  'history' - Show card batch history
  'reset' - Reset the count
  'quit' or 'exit' - Exit program
============================================================

How many decks in the shoe? (default: 6): 6

============================================================
DECK STATUS
============================================================
Running Count:     +0
Decks Remaining:   6.0
True Count:        +0.00
Deck Status:       NEUTRAL

CUMULATIVE CARD TOTALS:
  Hot cards (High):     0
  Cold cards (Low):    0
  Neutral cards (Mid):  0
============================================================

Enter card(s) or command: 2 3 4 5 6

  2: +1 (cold)
  3: +1 (cold)
  4: +1 (cold)
  5: +1 (cold)
  6: +1 (cold)

Batch Temperature Summary:
  Hot (High):     0
  Cold (Low):    5
  Neutral (Mid):  0

============================================================
DECK STATUS
============================================================
Running Count:     +5
Decks Remaining:   6.0
True Count:        +0.83
Deck Status:       NEUTRAL

CUMULATIVE CARD TOTALS:
  Hot cards (High):     0
  Cold cards (Low):    5
  Neutral cards (Mid):  0
============================================================

Enter card(s) or command: K K K Q J 10 A

  K: -1 (hot)
  K: -1 (hot)
  K: -1 (hot)
  Q: -1 (hot)
  J: -1 (hot)
  10: -1 (hot)
  A: -1 (hot)

Batch Temperature Summary:
  Hot (High):     7
  Cold (Low):    0
  Neutral (Mid):  0

============================================================
DECK STATUS
============================================================
Running Count:     -2
Decks Remaining:   6.0
True Count:        -0.33
Deck Status:       NEUTRAL

CUMULATIVE CARD TOTALS:
  Hot cards (High):     7
  Cold cards (Low):    5
  Neutral cards (Mid):  0
============================================================

Enter card(s) or command: history

============================================================
CARD BATCH HISTORY (Last 2 batches)
============================================================

Batch 1: 2, 3, 4, 5, 6
  Hot (High cards):     0
  Cold (Low cards):    5
  Neutral (Mid cards):  0

Batch 2: K, K, K, Q, J, 10, A
  Hot (High cards):     7
  Cold (Low cards):    0
  Neutral (Mid cards):  0

============================================================
```

## How It Works

### Hi-Lo Card Counting System

The Hi-Lo card counting system assigns values to cards:
- **Cold cards (2, 3, 4, 5, 6)**: +1 each (low cards)
- **Neutral cards (7, 8, 9)**: 0 each (mid cards)
- **Hot cards (10, J, Q, K, A)**: -1 each (high cards)

### Temperature Classification

Each card is classified by "temperature":
- **Cold cards** (+1 value): Low cards that favor the dealer when remaining in the deck
- **Hot cards** (-1 value): High cards that favor the player when remaining in the deck
- **Neutral cards** (0 value): Mid-range cards with no significant advantage

### Counting Process

As cards are dealt:
1. The **running count** accumulates card values
2. Each card is classified as hot, cold, or neutral
3. A **batch temperature summary** shows the composition of each batch of cards entered
4. **Cumulative totals** track all hot, cold, and neutral cards dealt so far
5. The **decks remaining** is estimated based on cards dealt
6. The **true count** is calculated: running count ÷ decks remaining
7. The **deck status** indicates advantage:
   - True count > +1: Player-favorable (more high cards remaining)
   - True count < -1: Dealer-favorable (more low cards remaining)
   - Otherwise: Neutral

### History Feature

The system maintains a history of the last 5 batches of cards entered. Each batch entry includes:
- The cards in the batch
- Number of hot, cold, and neutral cards
- This helps you review recent patterns and verify your entries

### Color Coding

Visual feedback through colors helps quickly identify card types and deck status:
- **Blue**: Cold/low cards and their counts
- **Red**: Hot/high cards and their counts (also used for dealer-favorable status)
- **Yellow**: Neutral/mid cards and their counts
- **Green**: Player-favorable deck status
- **Cyan**: Informational messages and headers

A positive true count suggests the remaining deck has more high cards, which favors the player.