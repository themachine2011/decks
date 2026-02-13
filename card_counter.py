# card_counter.py
# Blackjack Hi-Lo Card Counter (CLI)
# Hi-Lo: 2-6 = +1, 7-9 = 0, 10-A = -1

from __future__ import annotations

import math

HIGH = {"10", "J", "Q", "K", "A"}
LOW = {"2", "3", "4", "5", "6"}
NEUTRAL = {"7", "8", "9"}

ALL_RANKS = HIGH | LOW | NEUTRAL

def normalize_token(tok: str) -> str:
    t = tok.strip().upper()
    if t in {"T"}:
        return "10"
    return t

def hilo_value(rank: str) -> int:
    if rank in LOW:
        return +1
    if rank in HIGH:
        return -1
    return 0

def status_from_true_count(tc: float) -> str:
    if tc > 1:
        return "Player-favorable"
    if tc < -1:
        return "Dealer-favorable"
    return "Neutral"

def parse_cards(line: str) -> list[str]:
    # Accept space or comma separated inputs: "A K 10" or "A,K,10"
    raw = line.replace(",", " ").split()
    cards: list[str] = []
    for tok in raw:
        r = normalize_token(tok)
        if r not in ALL_RANKS:
            raise ValueError(f"Carta inválida: '{tok}' (use 2-10, J, Q, K, A)")
        cards.append(r)
    return cards

def prompt_decks() -> int:
    while True:
        s = input("Shoe decks (1-8): ").strip()
        try:
            n = int(s)
            if 1 <= n <= 8:
                return n
        except ValueError:
            pass
        print("Entrada inválida. Digita um número de 1 a 8.")

def print_help() -> None:
    print("\nComandos:")
    print("  <cartas>   Ex: A K 10 5 2   (pode usar vírgulas também)")
    print("  status    Mostra estado atual")
    print("  reset     Zera contagem e volta o shoe ao início")
    print("  help      Mostra esta ajuda")
    print("  quit      Sai\n")

def main() -> None:
    print("Blackjack Hi-Lo Counter (CLI)")
    print("Hi-Lo: 2-6=+1, 7-9=0, 10-A=-1\n")

    total_decks = prompt_decks()
    total_cards = total_decks * 52

    running_count = 0
    seen_cards = 0

    print_help()

    while True:
        line = input("> ").strip()
        if not line:
            continue

        cmd = line.lower().strip()

        if cmd in {"quit", "exit", "q"}:
            print("Bye.")
            return

        if cmd in {"help", "h", "?"}:
            print_help()
            continue

        if cmd == "reset":
            running_count = 0
            seen_cards = 0
            print("Resetado. Running Count = 0, cartas vistas = 0.")
            continue

        # compute + show status
        def show_status() -> None:
            remaining_cards = max(total_cards - seen_cards, 0)
            decks_remaining = max(remaining_cards / 52.0, 0.0)

            # Avoid division by zero: if almost no cards remaining, treat as 0.25 deck
            denom = max(decks_remaining, 0.25)
            true_count = running_count / denom

            print(f"Running Count: {running_count}")
            print(f"Cards Seen: {seen_cards}/{total_cards}")
            print(f"Cards Remaining: {remaining_cards}")
            print(f"Decks Remaining: {decks_remaining:.2f}")
            print(f"True Count: {true_count:.2f}")
            print(f"Status: {status_from_true_count(true_count)}")

        if cmd == "status":
            show_status()
            continue

        # otherwise parse as cards
        try:
            cards = parse_cards(line)
        except ValueError as e:
            print(e)
            continue

        for r in cards:
            # If shoe is "empty", prevent counting beyond total cards
            if seen_cards >= total_cards:
                print("Shoe acabou (já contou todas as cartas). Use 'reset' ou escolha mais decks.")
                break
            running_count += hilo_value(r)
            seen_cards += 1

        show_status()

if __name__ == "__main__":
    main()
