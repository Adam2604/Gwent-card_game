from Classes import *

#zbiór kart pogodowych
special_cards = [
    Special_card("Czyste niebo", "analuje aktywne karty pogodowe"),
    Special_card("Czyste niebo", "analuje aktywne karty pogodowe"),
    Special_card("Ulewny deszcz", "zmienia siłę jednostek oblężniczych na 1"),
    Special_card("Ulewny deszcz", "zmienia siłę jednostek oblężniczych na 1"),
    Special_card("Gęsta mgła", "zmienia siłę jednostek dystansowych na 1"),
    Special_card("Gęsta mgła", "zmienia siłę jednostek dystansowych na 1"),
    Special_card("Gęsta mgła", "zmienia siłę jednostek dystansowych na 1"),
    Special_card("Trzaskający mróz", "zmienia siłę jednostek walczących w zwarciu na 1"),
    Special_card("Trzaskający mróz", "zmienia siłę jednostek walczących w zwarciu na 1"),
    Special_card("Trzaskający mróz", "zmienia siłę jednostek walczących w zwarciu na 1")
]

#zbiór kart Królestwa Północy
Northern_Realms_cards = [
    Siege_combat("Mistrz Oblężeń z Kaedwen", 1, "Królestwo Północy","plus_one_point"),  # efekt +1 dla wszystkich
    Siege_combat("Mistrz Oblężeń z Kaedwen", 1, "Królestwo Północy", "plus_one_point"),  # efekt +1 dla wszystkich
    Siege_combat("Mistrz Oblężeń z Kaedwen", 1, "Królestwo Północy", "plus_one_point"),  # efekt +1 dla wszystkich
    Close_combat("Redański Piechur", 1, "Królestwo Północy"),
    Close_combat("Redański Piechur", 1, "Królestwo Północy"),
    Close_combat("Biedna Pierdolona Piechota", 1, "Królestwo Północy", "double_points"),  # efekt - połączone podwajają punkty swoje
    Close_combat("Biedna Pierdolona Piechota", 1, "Królestwo Północy", "double_points"),
    Close_combat("Biedna Pierdolona Piechota", 1, "Królestwo Północy", "double_points"),
    Close_combat("Talar", 1, "Królestwo Północy"),  # szpieg
    Close_combat("Yarpen Zirgin", 2, "Królestwo Północy"),
    Close_combat("Komandos Niebieskich Pasów", 4, "Królestwo Północy", "double_points"),  # połączone podwajają punkty swoje
    Close_combat("Komandos Niebieskich Pasów", 4, "Królestwo Północy", "double_points"),
    Close_combat("Komandos Niebieskich Pasów", 4, "Królestwo Północy", "double_points"),
    Ranged_combat("Sheldon Skaggs", 4, "Królestwo Północy"),
    Ranged_combat("Sabrina Glevissig", 4, "Królestwo Północy"),
    Close_combat("Sigismund Dijkstra", 4, "Królestwo Północy"),  # szpieg
    Siege_combat("Medyczka Burej Chorągwi", 5, "Królestwo Północy"),  # przywraca kartę ze stosu odrzuconych
    Ranged_combat("Rębacze z Crifrid", 5, "Królestwo Północy", "double_points"),  # połączone podwajają punkty swoje
    Ranged_combat("Rębacze z Crifrid", 5, "Królestwo Północy", "double_points"),
    Ranged_combat("Rębacze z Crifrid", 5, "Królestwo Północy", "double_points"),
    Close_combat("Książe Stannis", 5, "Królestwo Północy"),  # szpieg
    Ranged_combat("Sheala the Tancarville", 5, "Królestwo Północy"),
    Ranged_combat("Keira Metz", 5, "Królestwo Północy"),
    Close_combat("Zygfryd z Denesle", 5, "Królestwo Północy"),
    Close_combat("Ves", 5, "Królestwo Północy"),
    Siege_combat("Wieża oblężnicza", 6, "Królestwo Północy"),
    Siege_combat("Balista", 6, "Królestwo Północy"),
    Siege_combat("Trebusz", 6, "Królestwo Północy"),
    Siege_combat("Trebusz", 6, "Królestwo Północy"),
    Ranged_combat("Detmold", 6, "Królestwo Północy"),
    Siege_combat("Katapulta", 8, "Królestwo Północy", "double_points"),  # połączone podwajają punkty swoje
    Siege_combat("Katapulta", 8, "Królestwo Północy", "double_points"),
    Hero("Philippa Eilhart", 10, "Królestwo Północy"),  # bohater
    Hero("Esterad Thyssen", 10, "Królestwo Północy"),  # bohater
    Hero("Jan Natalis", 10, "Królestwo Północy"),  # bohater
    Hero("Vernon Roche", 10, "Królestwo Północy")  # bohater
]