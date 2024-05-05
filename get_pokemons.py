import json
import os
from glob import glob

import requests


def download_data(out_dir_name: str, url: str, tag: str):

    out_dir = f"./out/{out_dir_name}"

    if not os.path.exists(f"./{out_dir}"):
        os.mkdir(out_dir)

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    data = json.loads(response_text)
    if data.get(tag):
        name = data.get(tag).get("name")
    else:
        if data.get("name"):
            name = data.get("name")
        else:
            name = data.get("id")
    outfile = f"{out_dir}/{name}.json"
    if not os.path.exists(outfile):
        print(tag, name)
        with open(f"{out_dir}/{name}.json", "w", encoding="utf-8") as outf:
            print(response_text, file=outf)
    else:
        print(tag, name, "already downloaded")


def download_pokemon_from_pokedex(name: str):
    url = f"https://pokeapi.co/api/v2/pokedex/{name}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    data = json.loads(response_text)

    for pokemon_entry in data.get("pokemon_entries"):
        pokemon_name = pokemon_entry.get("pokemon_species").get("name")

        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

        try:
            download_data(out_dir_name="pokemons", url=url, tag="species")
        except json.decoder.JSONDecodeError:
            print(f"{pokemon_name} no /pokemon/ data")
            pass


def download_pokemon_species_from_pokedex(name: str):
    url = f"https://pokeapi.co/api/v2/pokedex/{name}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    data = json.loads(response_text)

    for pokemon_entry in data.get("pokemon_entries"):
        pokemon_name = pokemon_entry.get("pokemon_species").get("name")

        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"

        try:
            download_data(out_dir_name="pokemon_species", url=url, tag="species")
        except json.decoder.JSONDecodeError:
            print(f"{pokemon_name} no /pokemon-species/ data")
            pass


def get_data(name: str, dir_name: str):
    with open(f"{dir_name}/{name}.json", "r", encoding="utf-8") as inf:
        data = json.loads(inf.read())
    return data


def download_attributes(
    name: str, dir_name: str, tags: str, tag: str, out_dir_name: str
):
    data = get_data(name=name, dir_name=f"out/{dir_name}")
    if data.get(tags):
        for _ in data.get(tags):
            name = _.get(tag).get("name")
            url = _.get(tag).get("url")
            download_data(out_dir_name=out_dir_name, url=url, tag=tag)
    else:
        if data.get(tag).get("name"):
            name = data.get(tag).get("name")
        else:
            name = data.get(tag).get("url").split("/")[-2]
        url = data.get(tag).get("url")
        download_data(out_dir_name=out_dir_name, url=url, tag=tag)


def write_details(out_text: str, out_path: str):

    if os.path.exists(out_path):
        mode = "a"
    else:
        mode = "w"
    with open(out_path, mode=mode, encoding="utf-8") as outf:
        print(out_text, file=outf, end="\n")


def get_pokemon_details(output: bool = False):
    for i, file in enumerate(glob("out/pokemons/*.json"), start=1):
        pokemon_name = os.path.basename(file).split(".")[0]
        print("-----------", i, pokemon_name, "-----------")
        data = get_data(name=pokemon_name, dir_name="out/pokemons")
        id = data.get("id")
        pokename = data.get("species").get("name")
        sprite = data.get("sprites").get("front_default")
        height = data.get("height")
        weight = data.get("weight")
        base_experience = data.get("base_experience")
        order = data.get("order")
        stats = data.get("stats")

        for stat in stats:
            stat_name = stat.get("stat").get("name")
            if stat_name == "hp":
                hp = stat.get("base_stat")
            elif stat_name == "attack":
                attack = stat.get("base_stat")
            elif stat_name == "defense":
                defense = stat.get("base_stat")
            elif stat_name == "special-attack":
                special_attack = stat.get("base_stat")
            elif stat_name == "special-defense":
                special_defense = stat.get("base_stat")
            else:
                speed = stat.get("base_stat")

        stat_text = [
            str(s)
            for s in [hp, attack, defense, special_attack, special_defense, speed]
        ]

        moves = ",".join(
            [m.get("move").get("name").replace("-", " ") for m in data.get("moves")]
        )
        abilities = ",".join(
            [
                a.get("ability").get("name").replace("-", " ")
                for a in data.get("abilities")
            ]
        )
        types = ",".join([t.get("type").get("name") for t in data.get("types")])

        out_text = "\t".join(
            [
                str(id),
                pokename,
                sprite,
                str(height),
                str(weight),
                str(order),
                moves,
                abilities,
                types,
            ]
            + stat_text
            + [str(base_experience)]
        )

        header = "\t".join(
            [
                "pokemon_id",
                "pokemon_name",
                "sprite_url",
                "height",
                "weight",
                "order",
                "moves",
                "abilities",
                "types",
                "hp",
                "attack",
                "defense",
                "special_attack",
                "special_defense",
                "speed",
                "base_experience",
            ]
        )

        if output:
            out_path = "out/dataset/pokemons.tsv"
            if i == 1:
                if os.path.exists(out_path):
                    os.remove(out_path)
                    write_details(header, out_path=out_path)
            write_details(out_text, out_path=out_path)


def get_pokemon_species_details(output: bool = False):
    for i, file in enumerate(glob("out/pokemon_species/*.json"), start=1):
        pokemon_name = os.path.basename(file).split(".")[0]
        print("-----------", i, pokemon_name, "-----------")
        data = get_data(name=pokemon_name, dir_name="out/pokemon_species")
        id = data.get("id")
        base_happiness = data.get("base_happiness")
        capture_rate = data.get("capture_rate")
        try:
            habitat = data.get("habitat").get("name")
        except AttributeError:
            habitat = None
        is_baby = data.get("is_baby")
        is_legendary = data.get("is_legendary")
        is_mythical = data.get("is_mythical")
        has_gender_differences = data.get("has_gender_differences")
        try:
            evolution_chain_id = data.get("evolution_chain").get("url").split("/")[-2]
        except AttributeError:
            evolution_chain_id = None
        shape = data.get("shape").get("name")
        names = data.get("names")

        if not data.get("flavor_text_entries"):
            text = ""
        else:
            for text in data.get("flavor_text_entries"):
                language = text.get("language").get("name")
                if language == "en":
                    text = (
                        text.get("flavor_text")
                        .replace("\n", " ")
                        .replace("\u000c", " ")
                    )
                    break

        for name in names:
            language = name.get("language").get("name")
            if language == "en":
                name_en = name.get("name")
            if language == "ja-Hrkt":
                name_jp = name.get("name")

        out_text = "\t".join(
            [
                str(e)
                for e in [
                    id,
                    name_en,
                    name_jp,
                    base_happiness,
                    capture_rate,
                    habitat,
                    shape,
                    is_baby,
                    is_legendary,
                    is_mythical,
                    has_gender_differences,
                    evolution_chain_id,
                    text,
                ]
            ]
        )
        header = "\t".join(
            [
                "pokemon_species_id",
                "pokemon_name_en",
                "pokemon_name_jp",
                "base_happiness",
                "capture_rate",
                "habitat",
                "shape",
                "is_baby",
                "is_legendary",
                "is_mythical",
                "has_gender_differences",
                "evolution_chain_id",
                "about",
            ]
        )

        if output:
            out_path = "out/dataset/pokemon_species.tsv"
            if i == 1:
                if os.path.exists(out_path):
                    os.remove(out_path)
                    write_details(header, out_path=out_path)
            write_details(out_text, out_path=out_path)


def get_move_details(output: bool = False):
    for i, file in enumerate(glob("out/moves/*.json"), start=1):
        move_name = os.path.basename(file).split(".")[0]
        print("-----------", i, move_name, "-----------")
        data = get_data(name=move_name, dir_name="out/moves")
        id = data.get("id")
        name = data.get("name").replace("-", " ")
        type = data.get("type").get("name")

        if not data.get("flavor_text_entries"):
            text = ""
        else:
            for text in data.get("flavor_text_entries"):
                language = text.get("language").get("name")
                if language == "en":
                    text = text.get("flavor_text").replace("\n", " ")
                    break

        if not data.get("effect_entries"):
            effect = ""
            short_effect = ""
        else:
            for eff in data.get("effect_entries"):
                language = eff.get("language").get("name")
                if language == "en":
                    effect = eff.get("effect").replace("\n", " ")
                    short_effect = eff.get("short_effect")
                    break

        out_text = "\t".join(
            [str(e) for e in [id, name, type, text, effect, short_effect]]
        )

        header = "\t".join(
            [
                "move_id",
                "name",
                "type",
                "about",
                "effect",
                "short_effect",
            ]
        )

        if output:
            out_path = "out/dataset/moves.tsv"
            if i == 1:
                if os.path.exists(out_path):
                    os.remove(out_path)
                    write_details(header, out_path=out_path)
            write_details(out_text, out_path=out_path)


def get_ability_details(output: bool = False):
    for i, file in enumerate(glob("out/abilities/*.json"), start=1):
        ability_name = os.path.basename(file).split(".")[0]
        print("-----------", i, ability_name, "-----------")
        data = get_data(name=ability_name, dir_name="out/abilities")
        id = data.get("id")
        name = data.get("name").replace("-", " ")

        if not data.get("flavor_text_entries"):
            text = ""
        else:
            for text in data.get("flavor_text_entries"):
                language = text.get("language").get("name")
                if language == "en":
                    text = text.get("flavor_text").replace("\n", " ")
                    break

        if not data.get("effect_entries"):
            effect = ""
            short_effect = ""
        else:
            for eff in data.get("effect_entries"):
                language = eff.get("language").get("name")
                if language == "en":
                    effect = eff.get("effect").replace("\n", " ")
                    short_effect = eff.get("short_effect")
                    break

        out_text = "\t".join([str(e) for e in [id, name, text, effect, short_effect]])

        header = "\t".join(["ability_id", "name", "about", "effect", "short_effect"])

        if output:
            out_path = "out/dataset/abilities.tsv"
            if i == 1:
                if os.path.exists(out_path):
                    os.remove(out_path)
                    write_details(header, out_path=out_path)
            write_details(out_text, out_path=out_path)


def get_type_details(output: bool = False):
    for i, file in enumerate(glob("out/types/*.json"), start=1):
        type_name = os.path.basename(file).split(".")[0]
        print("-----------", i, type_name, "-----------")
        data = get_data(name=type_name, dir_name="out/types")
        id = data.get("id")
        name = data.get("name")
        if data.get("move_damage_class"):
            move_damage_class = data.get("move_damage_class").get("name")
        else:
            move_damage_class = ""
        damage_relations = data.get("damage_relations")
        double_damage_from = ",".join(
            [d.get("name") for d in damage_relations.get("double_damage_from")]
        )
        double_damage_to = ",".join(
            [d.get("name") for d in damage_relations.get("double_damage_to")]
        )
        half_damage_from = ",".join(
            [d.get("name") for d in damage_relations.get("half_damage_from")]
        )
        half_damage_to = ",".join(
            [d.get("name") for d in damage_relations.get("half_damage_to")]
        )
        no_damage_from = ",".join(
            [d.get("name") for d in damage_relations.get("no_damage_from")]
        )
        no_damage_to = ",".join(
            [d.get("name") for d in damage_relations.get("no_damage_to")]
        )

        out_text = "\t".join(
            [
                str(e)
                for e in [
                    id,
                    name,
                    move_damage_class,
                    double_damage_from,
                    double_damage_to,
                    half_damage_from,
                    half_damage_to,
                    no_damage_from,
                    no_damage_to,
                ]
            ]
        )

        header = "\t".join(
            [
                "type_id",
                "name",
                "move_damage_class",
                "double_damage_from",
                "double_damage_to",
                "half_damage_from",
                "half_damage_to",
                "no_damage_from",
                "no_damage_to",
            ]
        )

        if output:
            out_path = "out/dataset/types.tsv"
            if i == 1:
                if os.path.exists(out_path):
                    os.remove(out_path)
                    write_details(header, out_path=out_path)
            write_details(out_text, out_path=out_path)


def get_evolution_chain_details(output: bool = False):
    for i, file in enumerate(glob("out/evolution_chains/*.json"), start=1):
        evolution_chain_name = os.path.basename(file).split(".")[0]
        print("-----------", i, evolution_chain_name, "-----------")
        data = get_data(name=evolution_chain_name, dir_name="out/evolution_chains")
        id = data.get("id")
        chain = data.get("chain")
        species_1 = chain.get("species").get("name")
        try:
            species_2 = chain.get("evolves_to")[0].get("species").get("name")
        except IndexError:
            species_2 = None
        try:
            species_3 = (
                chain.get("evolves_to")[0]
                .get("evolves_to")[0]
                .get("species")
                .get("name")
            )
        except IndexError:
            species_3 = None

        out_text = "\t".join(
            [
                str(e)
                for e in [
                    id,
                    species_1,
                    species_2,
                    species_3,
                ]
            ]
        )
        header = "\t".join(
            ["evolution_chain_id", "species_1", "species_2", "species_3"]
        )

        if output:
            out_path = "out/dataset/evolution_chains.tsv"
            if i == 1:
                if os.path.exists(out_path):
                    os.remove(out_path)
                    write_details(header, out_path=out_path)
            write_details(out_text, out_path=out_path)
