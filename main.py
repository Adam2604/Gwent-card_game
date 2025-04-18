from Cards import special_cards, Northern_Realms_cards
from database import initialize_db, add_player, save_player_deck, load_player_deck
from game_results import initialize_results_db, add_or_update_winner, get_player_wins, update_match_result, get_match_results

from Classes import Unit
import random


def edit_deck(saved_deck_obj):
    """
    Pozwala graczowi edytować zapisaną talię:
      - Wyświetla zapisaną talię i pyta, które karty usunąć.
        Gracz może pominąć ten etap, wpisując "pomiń".
      - Następnie gracz może dobrać dodatkowe karty (wybierając je z dostępnej puli)
        aż łączna liczba kart jednostek w talii będzie wynosić co najmniej 22.
      - Gracz ma możliwość dobierania kart pojedynczo lub partiami.
      - Jeśli gracz wpisze "koniec", proces dobierania się zakończy (pod warunkiem, że talia ma co najmniej 22 karty).
    Zwraca nową, zedytowaną talię.
    """
    print("\nTwoja zapisana talia:")
    for i, card in enumerate(saved_deck_obj, 1):
        print(f"{i}. {card.name} - Siła: {card.strength}")

    # Opcjonalny etap usuwania kart
    indices_str = input(
        "Podaj numery kart do usunięcia (oddzielone spacją) lub wpisz 'pomiń', aby pominąć ten etap: ").strip().lower()
    if indices_str == "pomiń":
        print("Pominęto usuwanie kart.")
    else:
        indices = []
        for s in indices_str.split():
            if s.isdigit():
                indices.append(int(s) - 1)
        if indices:
            indices = sorted(indices, reverse=True)
            for idx in indices:
                if 0 <= idx < len(saved_deck_obj):
                    removed = saved_deck_obj.pop(idx)
                    print(f"Usunięto: {removed.name}")
                else:
                    print(f"Nieprawidłowy numer karty: {idx + 1}")
        else:
            print("Nie podano żadnych numerów. Przechodzimy dalej.")

    current_count = len(saved_deck_obj)
    print(f"\nObecnie talia zawiera {current_count} kart jednostek.")

    # Przygotowanie puli kart do doboru – kopiujemy Northern_Realms_cards
    available_pool = Northern_Realms_cards[:]
    # Opcjonalnie usuwamy z puli karty, które już znajdują się w zedytowanej talii,
    # aby uniknąć duplikatów
    for card in saved_deck_obj:
        available_pool = [c for c in available_pool if c.name != card.name]

    if not available_pool and len(saved_deck_obj) < 22:
        print("Brak dostępnych kart do doboru!")
        return saved_deck_obj

    # Pętla doboru nowych kart – gracz może wpisywać numery nowych kart,
    # a jeśli wpisze "koniec", proces zakończy się (pod warunkiem, że jest minimum 22 kart)
    while True:
        print(f"\nObecnie talia zawiera {len(saved_deck_obj)} kart jednostek.")
        new_choices_line = input(
            "Podaj numery nowych kart do dołączenia (lub wpisz 'koniec', aby zakończyć dobieranie): ").replace(',', ' ')
        new_choices = new_choices_line.split()
        if "koniec" in new_choices:
            if len(saved_deck_obj) >= 22:
                break
            else:
                print(f"Nie możesz zakończyć – w talii musi być co najmniej 22 kart (obecnie {len(saved_deck_obj)}).")
                continue

        added = False
        for s in new_choices:
            try:
                index = int(s) - 1
                if 0 <= index < len(available_pool):
                    saved_deck_obj.append(available_pool[index])
                    print(f"Dodano: {available_pool[index].name}")
                    added = True
                else:
                    print(f"Nieprawidłowy numer karty: {s}")
            except ValueError:
                print(f"Wpisz poprawny numer zamiast: {s}")
        if added:
            print(f"Obecnie talia zawiera {len(saved_deck_obj)} kart jednostek.")
    print("\nNowa talia po edycji:")
    for i, card in enumerate(saved_deck_obj, 1):
        print(f"{i}. {card.name} - Siła: {card.strength}")
    return saved_deck_obj


def choose_deck(player_name):
    saved_deck = load_player_deck(player_name)

    if saved_deck:
        print(f"\nZnaleziono zapisaną talię dla {player_name}:")
        for card in saved_deck:
            print(f"- {card[0]} (Siła: {card[1]})")
        choice = input("Czy chcesz załadować tę talię? (tak/nie/edycja): ").lower()
        if choice == "tak":
            return [Unit(*card) for card in saved_deck], []
        elif choice == "edycja":
            # Najpierw zamieniamy zapisany deck na obiekty
            saved_objects = [Unit(*card) for card in saved_deck]
            # Edytujemy talię – gracz usuwa i dobiera nowe karty
            edited_deck = edit_deck(saved_objects)
            # Możemy zapytać, czy chcemy zapisać zedytowaną talię
            save_choice = input("\nCzy chcesz zapisać zedytowaną talię? (tak/nie): ").lower()
            if save_choice == "tak":
                add_player(player_name)
                save_player_deck(player_name, edited_deck)
                print("Zedytowana talia została zapisana w bazie danych.")
            else:
                print("Zedytowana talia nie została zapisana.")
            return edited_deck, []

    # Jeśli nie ma zapisanej talii lub gracz wybrał "nie"
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
    #Losuje 10 kart dla gracza: jednostki + ewentualnie karty specjalne
    deck = unit_deck + special_deck  # Połączenie obu list kart
    random.shuffle(deck)  # Przetasowanie talii
    hand = deck[:10]  # Pobranie pierwszych 10 kart
    remaining_deck = deck[10:]  # Reszta kart pozostaje w talii
    return hand, remaining_deck


def swap_cards(hand, remaining_deck):
    #Wymusza wymianę dokładnie 3 kart, ale pozwala wybierać je pojedynczo lub wszystkie od razu

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
                break  # 3 karty wymienione więc zakończ

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

def game_round(player1_name, player1_hand, player1_deck, player2_name, player2_hand, player2_deck, score):
    #Obsługuje jedną rundę gry i przyznaje dodatkową kartę zwycięzcy
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
        score[player1_name] += 1
        if player1_deck and score[player1_name] < 2:
            new_card = player1_deck.pop(random.randint(0, len(player1_deck) - 1))
            player1_hand.append(new_card)
            print(f"{player1_name} otrzymuje dodatkową kartę: {new_card.name}")
    elif player2_strength > player1_strength:
        print(f"\n{player2_name} WYGRYWA RUNDĘ!")
        score[player2_name] += 1
        if player2_deck and score[player2_name] < 2:
            new_card = player2_deck.pop(random.randint(0, len(player2_deck) - 1))
            player2_hand.append(new_card)
            print(f"{player2_name} otrzymuje dodatkową kartę: {new_card.name}")
    else:
        print("\nRunda zakończyła się remisem!")

    return score


def start_game(player1_name, player1_hand, player1_deck, player2_name, player2_hand, player2_deck):
    #Rozpoczyna grę i kontroluje warunki zwycięstwa
    print(f"Zaczynamy grę! Gracz {player1_name} rozpoczyna!")

    score = {player1_name: 0, player2_name: 0}

    while score[player1_name] < 2 and score[player2_name] < 2:
        score = game_round(player1_name, player1_hand, player1_deck,
                           player2_name, player2_hand, player2_deck, score)

    winner = player1_name if score[player1_name] == 2 else player2_name
    loser = player1_name if winner == player2_name else player2_name
    add_or_update_winner(winner)
    update_match_result(winner, loser)
    total_wins = get_player_wins(winner)
    print(f"Gratulacje, {winner}! Łącznie wygrałeś {total_wins} razy!")

    match_result = get_match_results(player1_name, player2_name)
    if match_result:
        player1_wins, player2_wins = match_result
        print(f"Wynik wszystkich pojedynków {player1_name} - {player2_name}: {player1_wins}:{player2_wins}")
    else:
        print(f"Brak wyników dla pojedynku {player1_name} - {player2_name}.")


if __name__ == "__main__":
    initialize_db()
    initialize_results_db()

    # Pobranie nazw graczy
    player1_name = input("Podaj nazwę dla Gracza 1: ").capitalize()
    player2_name = input("Podaj nazwę dla Gracza 2: ").capitalize()

    print("\nLosowanie gracza rozpoczynającego...")
    first_player = random.choice([player1_name, player2_name])
    second_player = player1_name if first_player == player2_name else player2_name
    print(f"Grę rozpoczyna: {first_player}")

    # Wybór talii przez graczy
    first_player_units, first_player_specials = choose_deck(first_player)
    second_player_units, second_player_specials = choose_deck(second_player)

    # Rozdanie kart
    random.shuffle(first_player_units)
    random.shuffle(second_player_units)
    player1_hand, player1_deck = first_player_units[:10], first_player_units[10:]
    player2_hand, player2_deck = second_player_units[:10], second_player_units[10:]

    start_game(first_player, player1_hand, player1_deck, second_player, player2_hand, player2_deck)

