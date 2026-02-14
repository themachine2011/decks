#!/usr/bin/env python3
"""
Tests for the card counter system with per-rank validation.
"""

from card_counter import CardCounter, Colors


def test_basic_counting():
    """Test basic Hi-Lo counting."""
    print(f"{Colors.BOLD}Test 1: Basic Hi-Lo counting{Colors.RESET}")
    counter = CardCounter()
    
    # Test example: A K 10 7 9 5 2
    cards = ['A', 'K', '10', '7', '9', '5', '2']
    for card in cards:
        counter.count_card(card)
    
    # Expected: A=-1, K=-1, 10=-1, 7=0, 9=0, 5=+1, 2=+1 => Total = -1
    assert counter.running_count == -1, f"Expected -1, got {counter.running_count}"
    assert counter.cards_dealt == 7, f"Expected 7 cards dealt, got {counter.cards_dealt}"
    print(f"  {Colors.GREEN}✓ Running count: {counter.running_count}, Cards dealt: {counter.cards_dealt}{Colors.RESET}\n")


def test_32_aces_limit():
    """Test that exactly 32 Aces can be entered, but 33rd is rejected."""
    print(f"{Colors.BOLD}Test 2: 32 Aces limit{Colors.RESET}")
    counter = CardCounter()
    
    # Enter 32 Aces in batches
    for i in range(4):
        cards = ['A'] * 8
        is_valid, error = counter.validate_batch(cards)
        assert is_valid, f"Batch {i+1} should be valid"
        for card in cards:
            counter.count_card(card)
    
    assert counter.rank_counts['A'] == 32, f"Expected 32 Aces, got {counter.rank_counts['A']}"
    print(f"  {Colors.GREEN}✓ Successfully entered 32 Aces{Colors.RESET}")
    
    # Try to enter 33rd Ace
    is_valid, error = counter.validate_batch(['A'])
    assert not is_valid, "33rd Ace should be rejected"
    assert 'would exceed max for A' in error, f"Expected rejection message, got: {error}"
    print(f"  {Colors.GREEN}✓ 33rd Ace correctly rejected: {error}{Colors.RESET}\n")


def test_atomic_batch_rejection():
    """Test that batch rejection is atomic - no partial application."""
    print(f"{Colors.BOLD}Test 3: Atomic batch rejection{Colors.RESET}")
    counter = CardCounter()
    
    # Enter 30 Aces
    for i in range(30):
        counter.count_card('A')
    
    initial_count = counter.running_count
    initial_aces = counter.rank_counts['A']
    initial_cards_dealt = counter.cards_dealt
    
    # Try to enter batch with 3 Aces (would push to 33)
    batch = ['A', 'A', 'A']
    is_valid, error = counter.validate_batch(batch)
    assert not is_valid, "Batch should be rejected"
    
    # Verify nothing was applied
    assert counter.running_count == initial_count, "Running count should not change"
    assert counter.rank_counts['A'] == initial_aces, "Ace count should not change"
    assert counter.cards_dealt == initial_cards_dealt, "Cards dealt should not change"
    print(f"  {Colors.GREEN}✓ Batch atomically rejected, no state changes{Colors.RESET}\n")


def test_reset_clears_rank_counts():
    """Test that reset clears per-rank counts."""
    print(f"{Colors.BOLD}Test 4: Reset clears rank counts{Colors.RESET}")
    counter = CardCounter()
    
    # Enter 20 Aces
    for i in range(20):
        counter.count_card('A')
    
    assert counter.rank_counts['A'] == 20, "Should have 20 Aces"
    
    # Reset
    counter.reset()
    
    assert counter.rank_counts['A'] == 0, "Aces should be reset to 0"
    assert counter.running_count == 0, "Running count should be 0"
    assert counter.cards_dealt == 0, "Cards dealt should be 0"
    
    # Verify we can enter Aces again from 0
    is_valid, error = counter.validate_batch(['A'] * 10)
    assert is_valid, "Should be able to enter Aces after reset"
    print(f"  {Colors.GREEN}✓ Reset cleared rank counts, can enter Aces again{Colors.RESET}\n")


def test_multiple_ranks():
    """Test validation across multiple ranks."""
    print(f"{Colors.BOLD}Test 5: Multiple rank validation{Colors.RESET}")
    counter = CardCounter()
    
    # Enter 32 Kings
    for i in range(32):
        counter.count_card('K')
    
    # Try to enter mixed batch with another King
    batch = ['2', '3', 'K']
    is_valid, error = counter.validate_batch(batch)
    assert not is_valid, "Batch should be rejected due to King"
    assert 'K' in error, f"Error should mention King, got: {error}"
    
    # Enter batch without King
    batch = ['2', '3', '4']
    is_valid, error = counter.validate_batch(batch)
    assert is_valid, "Batch without King should be valid"
    
    for card in batch:
        counter.count_card(card)
    
    assert counter.rank_counts['2'] == 1, "Should have 1 two"
    assert counter.rank_counts['3'] == 1, "Should have 1 three"
    assert counter.rank_counts['4'] == 1, "Should have 1 four"
    assert counter.rank_counts['K'] == 32, "Should still have 32 Kings"
    print(f"  {Colors.GREEN}✓ Multiple rank validation working{Colors.RESET}\n")


def test_t_for_10():
    """Test that 't' or 'T' is accepted as '10'."""
    print(f"{Colors.BOLD}Test 6: Accept 'T' for '10'{Colors.RESET}")
    counter = CardCounter()
    
    counter.count_card('t')
    counter.count_card('T')
    counter.count_card('10')
    
    assert counter.rank_counts['10'] == 3, f"Expected 3 tens, got {counter.rank_counts['10']}"
    assert counter.running_count == -3, f"Expected -3 running count, got {counter.running_count}"
    print(f"  {Colors.GREEN}✓ 'T' and 't' correctly parsed as '10'{Colors.RESET}\n")


def run_all_tests():
    """Run all tests."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print("RUNNING CARD COUNTER TESTS")
    print(f"{'='*60}{Colors.RESET}\n")
    
    try:
        test_basic_counting()
        test_32_aces_limit()
        test_atomic_batch_rejection()
        test_reset_clears_rank_counts()
        test_multiple_ranks()
        test_t_for_10()
        
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}")
        print("ALL TESTS PASSED ✓")
        print(f"{'='*60}{Colors.RESET}\n")
    except AssertionError as e:
        print(f"\n{Colors.RED}{Colors.BOLD}TEST FAILED: {e}{Colors.RESET}\n")
        raise


if __name__ == "__main__":
    run_all_tests()
