from cleaning import load_and_clean_data

for year in range(2005, 2024):  # de 2005 à 2023 inclus
    load_and_clean_data(year)
