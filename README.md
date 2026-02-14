# Blackjack Card Counter

A command-line card-counting system for blackjack using the Hi-Lo counting strategy with color-coded visual feedback, batch temperature tracking, history features, and real shoe validation for 8-deck games.

## Features

- **8-Deck Shoe with Real Validation**: Fixed at 8 decks (416 cards total) with per-rank validation ensuring no more than 32 cards of any rank can be entered
- **Hi-Lo Counting System**: Standard card counting where low cards (2-6) add +1, high cards (10-A) subtract -1, and neutral cards (7-9) have no effect
- **Atomic Batch Validation**: Card batches are validated before application - if any rank would exceed its limit, the entire batch is rejected with no state changes
- **Per-Rank Composition View**: See exactly how many cards of each rank have been dealt with the 'composition' command
- **60-Card Rule**: The game automatically becomes player-favorable when 60 or more low cards (2-6) have been dealt, indicating the remaining deck is rich in high cards
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
- **Flexible Input**: Accepts 'T' or 't' as an alias for '10', supports comma and space separation

## Usage

Run the card counter:

```bash
python3 card_counter.py
```

### Commands

- **Enter cards**: Type card values (2-10, J, Q, K, A, or T for 10) separated by spaces or commas
  - Example: `2 5 K A` or `2, 5, K, A` or `2 5 T A` (T = 10)
- **status**: Display current counting statistics
- **history**: View the last 5 batches of cards entered with temperature breakdown
- **composition** (or **counts**): View per-rank card counts showing how many of each rank have been dealt
- **reset**: Reset the counter to zero (clears all data including history and rank counts)
- **quit** or **exit**: Exit the program

## Example Session

```
============================================================
BLACKJACK CARD COUNTER - Hi-Lo System (8-Deck Shoe)
============================================================

Card Values:
  Cold cards (2-6):   +1 (Low cards)
  Neutral (7-9):      0 (Mid cards)
  Hot cards (10-A):  -1 (High cards)

Commands:
  Enter card values (e.g., 2, K, 10, A, or T for 10)
  'status' - Show current status
  'history' - Show card batch history
  'composition' - Show per-rank card counts
  'reset' - Reset the count
  'quit' or 'exit' - Exit program

Note: 8-deck shoe (416 cards), max 32 per rank
============================================================

============================================================
DECK STATUS
============================================================
Running Count:     +0
Decks Remaining:   8.0
True Count:        +0.00
Deck Status:       NEUTRAL

CUMULATIVE CARD TOTALS:
  Hot cards (High):     0
  Cold cards (Low):    0
  Neutral cards (Mid):  0
============================================================

Enter card(s) or command: A K 10 7 9 5 2

  A: -1 (hot)
  K: -1 (hot)
  10: -1 (hot)
  7: +0 (neutral)
  9: +0 (neutral)
  5: +1 (cold)
  2: +1 (cold)

Batch Temperature Summary:
  Hot (High):     3
  Cold (Low):    2
  Neutral (Mid):  2

============================================================
DECK STATUS
============================================================
Running Count:     -1
Decks Remaining:   8.0
True Count:        -0.12
Deck Status:       NEUTRAL

CUMULATIVE CARD TOTALS:
  Hot cards (High):     3
  Cold cards (Low):    2
  Neutral cards (Mid):  2
============================================================

Enter card(s) or command: composition

============================================================
CARD COMPOSITION (Per-Rank Counts)
============================================================

   2:  1/32 ░░░░░░░░░░░░░░░░░░░░ (31 remaining)
   3:  0/32 ░░░░░░░░░░░░░░░░░░░░ (32 remaining)
   4:  0/32 ░░░░░░░░░░░░░░░░░░░░ (32 remaining)
   5:  1/32 ░░░░░░░░░░░░░░░░░░░░ (31 remaining)
   6:  0/32 ░░░░░░░░░░░░░░░░░░░░ (32 remaining)
   7:  1/32 ░░░░░░░░░░░░░░░░░░░░ (31 remaining)
   8:  0/32 ░░░░░░░░░░░░░░░░░░░░ (32 remaining)
   9:  1/32 ░░░░░░░░░░░░░░░░░░░░ (31 remaining)
  10:  1/32 ░░░░░░░░░░░░░░░░░░░░ (31 remaining)
   J:  0/32 ░░░░░░░░░░░░░░░░░░░░ (32 remaining)
   Q:  0/32 ░░░░░░░░░░░░░░░░░░░░ (32 remaining)
   K:  1/32 ░░░░░░░░░░░░░░░░░░░░ (31 remaining)
   A:  1/32 ░░░░░░░░░░░░░░░░░░░░ (31 remaining)

============================================================
```

### Per-Rank Validation Example

```
Enter card(s) or command: A A A A A A A A
  (batches of 8 Aces entered 4 times = 32 total)

Enter card(s) or command: A A A

Invalid input: would exceed max for A (attempted 35/32). Batch ignored.
```

The system validates each batch before applying it. If entering the batch would cause any rank to exceed 32 cards, the entire batch is rejected atomically with no state changes.

## How It Works

### Hi-Lo Card Counting System

The Hi-Lo card counting system assigns values to cards:
- **Cold cards (2, 3, 4, 5, 6)**: +1 each (low cards)
- **Neutral cards (7, 8, 9)**: 0 each (mid cards)
- **Hot cards (10, J, Q, K, A)**: -1 each (high cards)

### Temperature Classification

Each card dealt is classified by "temperature" based on its Hi-Lo value:
- **Cold cards** (2-6): Cards with +1 value - called "cold" because dealing them removes cards that increase the count
- **Hot cards** (10-A): Cards with -1 value - called "hot" because dealing them removes high-value cards from the deck
- **Neutral cards** (7-9): Cards with 0 value - no impact on the count

**Important**: The temperature describes the cards *dealt* (removed from the deck). When many cold cards are dealt, the remaining deck becomes richer in high cards (player-favorable). When many hot cards are dealt, the remaining deck becomes richer in low cards (dealer-favorable).

### Counting Process

As cards are dealt:
1. **Batch validation**: Each batch of cards is validated to ensure no rank would exceed 32 cards
2. If validation passes, cards are processed:
   - The **running count** accumulates card values
   - Each card is classified as hot, cold, or neutral
   - **Per-rank counts** are updated
3. A **batch temperature summary** shows the composition of each batch of cards entered
4. **Cumulative totals** track all hot, cold, and neutral cards dealt so far
5. The **decks remaining** is estimated based on cards dealt
6. The **true count** is calculated: running count ÷ decks remaining
7. The **deck status** indicates advantage:
   - **60+ Cold Cards Rule**: When 60 or more low cards (2-6) have been dealt, the game automatically becomes player-favorable
   - True count > +1: Player-favorable (more high cards remaining)
   - True count < -1: Dealer-favorable (more low cards remaining)
   - Otherwise: Neutral

### Per-Rank Validation (8-Deck Real Shoe)

The system enforces real shoe constraints for an 8-deck game:
- **416 total cards**: 8 decks × 52 cards per deck
- **32 cards per rank**: 8 decks × 4 cards per rank
- **Atomic batch validation**: Before applying any batch, the system checks if it would cause any rank to exceed 32 cards
- **All-or-nothing**: If validation fails, the entire batch is rejected with no state changes to running count, cards dealt, or rank counts
- **Clear error messages**: Shows which rank would exceed its limit and the attempted count

Example: If 32 Aces have been dealt and you try to enter "A K Q", the system will reject the entire batch with:
```
Invalid input: would exceed max for A (attempted 33/32). Batch ignored.
```

This ensures the counter accurately reflects a real 8-deck shoe and prevents impossible card combinations.

### 60-Card Favorable Rule

A key feature of this system is the **60-card threshold**: when 60 or more cold cards (low cards: 2-6) have been dealt, the system automatically marks the game as **player-favorable**. This is because:
- With 60+ low cards removed from the deck, the remaining shoe is significantly richer in high cards (10, J, Q, K, A)
- High cards favor the player in blackjack by increasing the chances of naturals and strong hands
- The system displays a special message: **"*** Jogo favoravel ao jogador! (60+ cartas baixas sairam) ***"**
- This rule takes precedence over the true count calculation

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