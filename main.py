from Cards import special_cards, Northern_Realms_cards
from database import initialize_db, add_player, save_player_deck, load_player_deck
from Classes import Unit
import random

def choose_deck(player_name):
    saved_deck = load_player_deck(player_name)

    if saved_deck:
        print(f"\nZnaleziono zapisaną talię dla {player_name}:")
        for card in saved_deck:
            print(f"- {card[0]} (Siła: {card[1]})")
        choice = input("Czy chcesz załadować tę talię? (tak/nie): ").lower()
        if choice == "tak":
            return [Unit(*card) for card in saved_deck], []

    units = Northern_Realms_cards[:]
    special = special_cards[:]
    chosen_cards = []
    chosen_special_cards = []

    print(f"\n{player_name}, wybierz karty do swojej talii (minimum 22 jednostki).")
    print("Możesz wpisywać kilka numerów kart oddzielonych spacją lub przecinkiem.")
    print('Gdy skończysz wybierać jednostki, wpisz "koniec".')

    # Wybór kart jednostek
    while True:
        print("\nDostępne karty jednostek:")
        for i, card in enumerate(units, 1):
            print(f"{i}. {card.name} - Siła: {card.strength}")

        choices = input("Podaj numery kart do dodania: ").replace(',', ' ').split()

        if "koniec" in choices:
            if len(chosen_cards) >= 22:
                break
            else:
                print("Musisz wybrać co najmniej 22 jednostki przed zakończeniem.")

        added = False
        for choice in choices:
            try:
                index = int(choice) - 1
                if 0 <= index < len(units):
                    chosen_cards.append(units.pop(index))
                    added = True
                else:
                    print(f"Nieprawidłowy numer karty: {choice}")
            except ValueError:
                if choice != "koniec":
                    print(f"Wpisz poprawny numer zamiast: {choice}")

        if added:
            print(f"Masz {len(chosen_cards)} kart w talii.")

    # Wyświetlenie kart wybranych przez gracza
    print("\nTwoja talia jednostek:")
    for card in chosen_cards:
        print(f"- {card.name} (Siła: {card.strength})")

    # Wybór kart specjalnych
    print("\nTeraz możesz wybrać karty specjalne (opcjonalnie).")
    print("Możesz wpisać numery kart specjalnych oddzielone spacją lub przecinkiem.")
    print('Jeśli nie chcesz wybrać żadnej, wpisz "koniec".')

    while True:
        print("\nDostępne karty specjalne:")
        for i, card in enumerate(special, 1):
            print(f"{i}. {card.name} - Efekt: {card.effect}")

        choices = input("Podaj numery kart specjalnych do dodania: ").replace(',', ' ').split()
        if "koniec" in choices:
            break

        added = False
        for choice in choices:
            try:
                index = int(choice) - 1
                if 0 <= index < len(special):
                    chosen_special_cards.append(special.pop(index))
                    added = True
                else:
                    print(f"Nieprawidłowy numer karty: {choice}")
            except ValueError:
                if choice != "koniec":
                    print(f"Wpisz poprawny numer zamiast: {choice}")

        if added:
            print(f"Masz {len(chosen_special_cards)} kart specjalnych w talii.")

    # Wyświetlenie kart specjalnych wybranych przez gracza
    print("\nTwoje karty specjalne:")
    for card in chosen_special_cards:
        print(f"- {card.name} (Efekt: {card.effect})")

    # Zapytanie gracza, czy chce zapisać talię
    save_choice = input("\nCzy chcesz zapisać tę talię w bazie danych? (tak/nie): ").lower()

    if save_choice == "tak":
        add_player(player_name)
        save_player_deck(player_name, chosen_cards + chosen_special_cards)
        print("Talia została zapisana w bazie danych.")
    else:
        print("Talia nie została zapisana.")

    return chosen_cards, chosen_special_cards




def draw_starting_hand(unit_deck, special_deck):
    """Losuje 10 kart dla gracza: jednostki + ewentualnie karty specjalne."""
    deck = unit_deck + special_deck  # Połączenie obu list kart
    random.shuffle(deck)  # Przetasowanie talii
    hand = deck[:10]  # Pobranie pierwszych 10 kart
    remaining_deck = deck[10:]  # Reszta kart pozostaje w talii
    return hand, remaining_deck


def swap_cards(hand, remaining_deck):
    """Wymusza wymianę dokładnie 3 kart, ale pozwala wybierać je pojedynczo lub wszystkie od razu."""

    print("\nTwoja początkowa ręka:")
    for i, card in enumerate(hand, 1):
        print(f"{i}. {card.name} - {card.strength if hasattr(card, 'strength') else card.effect}")

    swapped_cards = []
    new_cards = []

    print("\nMusisz wymienić dokładnie 3 karty.")
    print("Możesz wpisywać numery pojedynczo (wciskając Enter po każdym) albo wszystkie naraz.")
    print('Gdy wymienisz 3 karty, wymiana się zakończy.')

    while len(swapped_cards) < 3:
        remaining_swaps = 3 - len(swapped_cards)
        print(f"\nPozostało do wymiany: {remaining_swaps} karty.")

        choices = input("Podaj numer karty do wymiany (lub kilka oddzielonych spacją/przecinkiem): ").replace(',',
                                                                                                              ' ').split()

        for choice in choices:
            if len(swapped_cards) >= 3:
                break  # Nie pozwalamy wymienić więcej niż 3 kart

            try:
                index = int(choice) - 1
                if 0 <= index < len(hand):
                    if remaining_deck:
                        swapped_cards.append(hand[index])
                        new_card = remaining_deck.pop(random.randint(0, len(remaining_deck) - 1))
                        new_cards.append(new_card)
                        hand[index] = new_card  # Zamiana karty w ręce
                        print(f"Wymieniono: {swapped_cards[-1].name} → {new_card.name}")
                    else:
                        print("Brak dodatkowych kart w talii do wymiany!")
                        return hand  # Jeśli nie można wymienić, zwracamy aktualną rękę
                else:
                    print(f"Nieprawidłowy numer karty: {choice}")
            except ValueError:
                print(f"Wpisz poprawny numer zamiast: {choice}")

    # Wyświetlenie końcowej ręki po wymianie
    print("\nTwoja ostateczna ręka po wymianie:")
    for card in hand:
        print(f"- {card.name} - {card.strength if hasattr(card, 'strength') else card.effect}")

    return hand


def play_turn(player_name, player_hand, player_strength, passed):
    #Obsługuje turę gracza. Jeśli gracz spasował, nie może wykonać ruchu
    if passed[player_name]:
        print(f"{player_name} już spasował i nie może zagrywać kart.")
        return player_strength, passed

    print(f"\n{player_name}, twoja tura. Twoja siła: {player_strength}")
    print("Twoje karty: ")
    for i, card in enumerate(player_hand, 1):
        print(f"{i}. {card.name} - Siła: {card.strength}")

    while True:
        choice = input("Wybierz kartę do zagrania (numer karty) lub 'pass' aby spasować: ").lower()

        if choice == "pass":
            print(f"{player_name} spasował turę.")
            passed[player_name] = True
            break

        try:
            card_index = int(choice) - 1
            if 0 <= card_index < len(player_hand):
                card = player_hand.pop(card_index)
                player_strength += card.strength
                print(f"{player_name} zagrał {card.name} (Siła: {card.strength})")
                print(f"Nowa siła: {player_strength}")
                break
            else:
                print("Nieprawidłowy numer karty. Spróbuj ponownie.")
        except ValueError:
            print("Proszę podać numer karty lub 'pass'.")

    return player_strength, passed

def game_round(player1_name, player1_hand, player2_name, player2_hand):
    #Obsługuje jedną rundę gry
    player1_strength = 0
    player2_strength = 0
    passed = {player1_name: False, player2_name: False}

    while player1_hand or player2_hand:
        if passed[player1_name] and passed[player2_name]:
            break

        if not passed[player1_name]:
            player1_strength, passed = play_turn(player1_name, player1_hand, player1_strength, passed)

        if not passed[player2_name]:
            player2_strength, passed = play_turn(player2_name, player2_hand, player2_strength, passed)

    print("\n--- KONIEC RUNDY ---")
    print(f"{player1_name} - Siła: {player1_strength}")
    print(f"{player2_name} - Siła: {player2_strength}")

    if player1_strength > player2_strength:
        print(f"\n{player1_name} WYGRYWA RUNDĘ!")
        return player1_name
    elif player2_strength > player1_strength:
        print(f"\n{player2_name} WYGRYWA RUNDĘ!")
        return player2_name
    else:
        print("\nRunda zakończyła się remisem!")
        return None


def start_game(player1_name, player1_hand, player2_name, player2_hand):
    #Rozpoczyna grę, obsługując kolejne rundy aż do zakończenia meczu
    print(f"Zaczynamy grę! Gracz {player1_name} rozpoczyna!")

    rounds_played = 0  # Licznik rund
    player1_wins = 0
    player2_wins = 0

    while rounds_played < 3 and (player1_hand or player2_hand):
        winner = game_round(player1_name, player1_hand, player2_name, player2_hand)
        rounds_played += 1

        if winner == player1_name:
            player1_wins += 1
        elif winner == player2_name:
            player2_wins += 1

        if player1_wins == 2:
            print(f"\n{player1_name} wygrał mecz!")
            return
        elif player2_wins == 2:
            print(f"\n{player2_name} wygrał mecz!")
            return

    print("\nMecz zakończony! Sprawdźmy, kto wygrał:")
    if player1_wins > player2_wins:
        print(f"\n{player1_name} WYGRYWA!")
    elif player2_wins > player1_wins:
        print(f"\n{player2_name} WYGRYWA!")
    else:
        print("\nMecz zakończył się remisem!")

if __name__ == "__main__":
    initialize_db()

    # Pobranie nazw graczy
    player1_name = input("Podaj nazwę dla Gracza 1: ")
    player2_name = input("Podaj nazwę dla Gracza 2: ")

    print("\nLosowanie gracza rozpoczynającego...")
    first_player = random.choice([player1_name, player2_name])
    print(f"Grę rozpoczyna: {first_player}")

    # Wybór talii przez graczy
    player1_units, player1_specials = choose_deck(player1_name)
    player2_units, player2_specials = choose_deck(player2_name)

    # Rozdanie kart
    player1_hand, player1_deck = player1_units[:10], player1_units[10:]
    player2_hand, player2_deck = player2_units[:10], player2_units[10:]

    start_game(player1_name, player1_hand, player2_name, player2_hand)