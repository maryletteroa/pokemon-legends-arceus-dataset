import os
from glob import glob

from get_pokemons import (download_attributes, download_pokemon_from_pokedex,
                          download_pokemon_species_from_pokedex,
                          get_ability_details, get_evolution_chain_details,
                          get_move_details, get_pokemon_details,
                          get_pokemon_species_details, get_type_details)

# download pokemon from pokedex hisui
download_pokemon_from_pokedex(name="hisui")
download_pokemon_species_from_pokedex(name="hisui")

# download the pokemon json files

for i, file in enumerate(glob("out/pokemons/*.json"), start=1):
    pokemon_name = os.path.basename(file).split(".")[0]
    print("-----------", i, pokemon_name, "-----------")

    # download moves
    download_attributes(
        name=pokemon_name,
        dir_name="pokemons",
        tags="moves",
        tag="move",
        out_dir_name="moves",
    )

    # download abilities
    download_attributes(
        name=pokemon_name,
        dir_name="pokemons",
        tags="abilities",
        tag="ability",
        out_dir_name="abilities",
    )

    # download types (pokemons)
    download_attributes(
        name=pokemon_name,
        dir_name="pokemons",
        tags="types",
        tag="type",
        out_dir_name="types",
    )


for i, file in enumerate(glob("out/pokemon_species/*.json"), start=1):
    pokemon_name = os.path.basename(file).split(".")[0]
    print("-----------", i, pokemon_name, "-----------")

    # download evolution_chain (pokemons)
    download_attributes(
        name=pokemon_name,
        dir_name="pokemon_species",
        tags="",
        tag="evolution_chain",
        out_dir_name="evolution_chains",
    )


for i, file in enumerate(glob("out/moves/*.json"), start=1):
    move_name = os.path.basename(file).split(".")[0]
    print("-----------", i, move_name, "-----------")
    # download types (moves)
    download_attributes(
        name=move_name,
        dir_name="moves",
        tags="types",
        tag="type",
        out_dir_name="types",
    )


get_pokemon_details(output=True)
get_pokemon_species_details(output=True)
get_move_details(output=True)
get_ability_details(output=True)
get_type_details(output=True)
get_evolution_chain_details(output=True)
