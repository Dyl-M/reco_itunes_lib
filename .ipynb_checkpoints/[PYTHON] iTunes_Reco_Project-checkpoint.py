from libpytunes import Library
from datetime import datetime
from time import mktime
import csv
import pandas

""" - SCRIPT INFORMATRION | INFORMATION SCRIPT - """

# !/usr/bin/python3
# -*- coding:utf8 -*-

# Project Name: Recommendations based on iTunes libray
# File Name: [PYTHON] iTunes_Reco_Project.py
# Author: Dyl_M (MONFRET Dylan, GH: Dyl-M)
# Project languages: Python / R (?)
# Comment Language: Mostly in French for now / Majoritairement en français pour le moment

# Ce script s'exécute avec le package "libpytunes" conçu par Liam Kaufman, permettant une lecture simplifié du fichier
# de base de données "iTunes Library.xml". Un grand merci à lui.

# Son GitHub : https://github.com/liamks
# Lien direct du package : https://github.com/liamks/libpytunes

""" - DISCLAIMER | AVERTISSEMENT - """

# [EN]

# This project will only deal with music from an iTunes database.

# This project offers (or rather will offer) some analysis possibilities around the database we can build with iTunes.
# As each user has his own way of arranging music with iTunes, the method of "cleaning" the data, the construction of
# global variables or any other manipulation of the data would not necessarily make sense for a different library than
# mine. Theoretically, I will comment enough on the project to make it understandable to everyone and the specifics of
# my layout as well.

# [FR]

# Ce project ne traitera que les musiques d'une base de données iTunes.

# Ce projet offre (ou plutôt offrira) des pistes d'analyse autour de la base données que nous pouvons construire avec
# iTunes. Comme chaque utilisateur à sa propre manière d'agencer les musiques avec iTunes, la méthode de "nettoyage" des
# données, la construction des variables globales ou toute autre manipulation des données n'aurait pas forcément de sens
# pour une bibliothèque différente de la mienne. Théoriquement, je vais commenter suffisamment le projet pour qu'il soit
# compréhensible de tous et que les spécificité de mon agencement le soit aussi.

""" - GLOBAL VARIABLES / DATA | VARIABLES / DONNEES GLOBALES - """

# Ensemble des duos de la base de données, sert au bon référencement des duos comme "une seule entité artiste"
duos = ["A Girl & A Gun", "ANDY & FILIPE SILVEIRA", "ARICK & DUNNO", "Above & Beyond", "Amadou & Mariam",
        "Asketa & Natan Chaim", "Bigflo & Oli", "Case & Point", "DJ KUBA & NEITAN", "Dimitri Vangelis & Wyman",
        "Dimitri Vegas & Like Mike", "Dodge & Fuski", "Dzeko & Torres", "Edward Sharpe & The Magnetic Zeros",
        "Gent & Jawns", "Holl & Rush", "Jack & Jordan", "Jaxx & Vega", "Jewelz & Sparks", "Klauss & Turino",
        "Lucas & Steve", "Lush & Simon", "Matisse & Sadko", "Mave & Zac", "Merk & Kremont", "Mr. Belt & Wezol",
        "Nico & Vinz", "PBH & Jack Shizzle", "Paris & Simo", "Pep & Rash", "Petterson & Findus", "Phats & Small",
        "Rave & Crave", "Raven & Kreyn", "Relanium & Deen West", "Rico & Miella", "Riggi & Piros", "Slips & Slurs",
        "Sunnery James & Ryan Marciano", "Tegan & Sara", "The Flexican & FS Green", "Tom & Jame", "Vargas & Lagola",
        "Volt & State", "W&W", "Will & Tim", "nFiX & Candice"]

# Ensemble des alias d'artiste "fort" : se rapporte à un autre nom d'artiste actif, ou à un side-project actif ou non
# déclaré comme arrêté.
alias = {"Daffy Muffin": "Lucas & Steve", "AREA21": ["Martin Garrix", "Maejor"],
         "Major Lazer": ["Diplo", "Walshy Fire", "Ape Drums"], "VIRTUAL SELF": "Porter Robinson", "Streex": "Razihel",
         "Jack Ü": ["Skrillex", "Diplo"], "Axwell Λ Ingrosso": ["Sebastian Ingrosso", "Axwell"],
         "Swedish House Mafia": ["Axwell", "Sebastian Ingrosso", "Steve Angello"],
         "Casseurs Flowters": ["OrelSan", "Gringe"], "NWYR": "W&W", "Shindeai": "STARRYSKY", "Sasha": "STARRYSKY",
         "Sinnoh Fusion Ensemble": "insaneintherainmusic", "Big Pineapple": "Don Diablo"}

# Ensemble des alias secondaires dits "faibles" : se rapporte à un autre nom d'artiste dans la base de données ayant
# peut de valeur pour l'analyse ou n'étant plus actif donc plus intéressant à suivre.
weak_alias = {"AvB": "Armin van Buuren", "Rising Star": "Armin van Buuren", "NLW": "Afrojack",
              "Jayden Jaxx": "Crime Zcene", "Chill Harris": "Kill Paris", "DJ Afrojack": "Afrojack",
              "Ravitez": "Chico Rose", "GRX": "Martin Garrix", "Kerafix & Vultaire": "KEVU",
              "Lush & Simon": ["Simon Says", "Zen/It"], "Matthew Ros": "MWRS", "Grant Bowtie": "Grant",
              "M.E.G. & N.E.R.A.K.": "DJ M.E.G.", "MEG / NERAK": "DJ M.E.G.", "Dzeko & Torres": "Dzeko",
              "X-Teef": "Stemalø", "Paris & Simo": "Prince Paris", "The Eden Project": "EDEN",
              "Slips & Slurs": "Slippy", "Vorwerk": "Maarten Vorwerk", "Will & Tim": "NewGamePlus",
              "DBSTF": "D-Block & S-te-Fan"}

# Liste d'élément STRING permettant de définir si une piste n'est pas un remix.
not_remix_tag = (
    '[2017 Trap Reboot]', '[2K16 Edit]', "[90's Remix]", '[Acoustic]', '[Album Version]', '[Bonus Track]', '[Bonus]',
    '[CANCELED]', '[Celebration Club Mix]', '[Clip Version]', '[Club Mix]', '[Cover]', '[Dub Mix]',
    '[EDM × Metal Remix]', '[English Version]', '[Eurovision 2015 Live Version]', '[Evian Version]', '[Extended Mix]',
    '[Extended Version]', '[Festival Mix]', '[Festival Version]', '[French Version]', '[GoPro HERO3 Edit]',
    '[Instrumental Edit.]', '[Instrumental Mix]', '[Instrumental]', '[Intro Mix]', '[Japanese Version]',
    '[LIVE Performance]', '[Live Version]', '[Main Theme]', '[Orchestra Version]', '[Orchestral Remix]',
    '[Orchestral Version]', '[Original Club Mix]', '[Original Mix]', '[Piano Version]', '[Pro Mix]', '[Radio Edit]',
    '[Remix]', '[SAO Main Theme]', '[Shippuden OST 1]', '[Shippuden OST 2]', '[T&T Festival Trap Remix]',
    '[Trap Remix]', '[UMF 2015 Intro Edit]', '[Ultra 2015 Instrumental Edit]', '[Ultra Edit]', '[VIP Mix]',
    '[VIP Remix]', '[Violin Version]', '[Zen @coustic]', "[Orchestral Cover]", "[Orchestral Suite]",
    "[Electro House Remix]")

# Caractère de séparation d'artiste (plus de détail prochainement)
cara_sep_artist = (
    " (feat. ", " (w/ ", " + ", " w/ ", " × ", " | ", " vs. ", " V/S ", " VS ", " V.S ", " VS. ", " vs ", "), ")

# Caractère à supprimer dans le champ "name" pour les remix, pour extraire les remixers.
cara_del_remix = (
    "[", "]", " BONUS TRACK", "ADE Intro | ", " Remake", " Rebuild", " Blastersmash",
    " Re-Crank", "'s 2k17 Bootleg", " Bootleg", "'s VIP Mix", "'s VIP Remix", " Rework", " UMF 2017 Mashup",
    " UMF Edit", "'s Swede Remix", " Flip", " FLIP", " Heaven Trap Remix", " VIP Mix", " Power-Up",
    "'s Disco House Remix", " ReBoot", " Vocal Edit", " Extended Remix", " Festival Mix", " Brown Note Remix",
    " 2016 Remix", " Remix", " Mix", " Mashup", " VIP Edit", " Edit")

""" - LOCAL FUNCTIONS | FONCTIONS LOCALES- """


# Fonction de base pour transformer la base de données iTunes en une liste de titre avec un identifiant et les
# informations de base conservées sous la forme de dictionnaires (ID généré automatiquement, Titre, Album, Artiste ,
# Artiste de l'Album, Genre, Année, Date d'ajout, Groupe (ici label, sinon case vide), Nombre de lecture).
def itunes_lib_xml_to_lst(xml_path):
    biblio = Library(xml_path)
    itunes_data_ld = []
    i = 0
    for song in biblio.songs.values():
        i += 1
        if song.play_count is None:
            count = 0
        else:
            count = song.play_count
        itunes_data_ld.append(
            {"Track_ID": "T{:04d}".format(i), "Name": song.name, "Album": song.album, "Artist": song.artist,
             "Album_Artist": song.album_artist, "Genre": song.genre, "Year": song.year,
             "Date_Added": datetime.fromtimestamp(mktime(song.date_added)),
             "Group": song.grouping, "Play_Count": count})
    return itunes_data_ld


# Fonction d'export d'une base de données iTunes en .csv (fonctionne avec "itunes_lib_xml_to_list" et son format de
# retour).
def db_track_csv(xml_path, csv_name="iTunes_Library.csv"):
    lst_data_base = itunes_lib_xml_to_lst(xml_path)
    col_names = lst_data_base[0].keys()
    try:
        with open(csv_name, 'w', encoding="utf-8-sig", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=col_names, delimiter=";")
            writer.writeheader()
            for data in lst_data_base:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def export_list_to_csv(a_list, csv_name="Artist_Library.csv"):
    col_names = a_list[0].keys()
    try:
        with open(csv_name, 'w', encoding="utf-8-sig", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=col_names, delimiter=";")
            writer.writeheader()
            for data in a_list:
                writer.writerow(data)
    except IOError:
        print("I/O error")


# Fonction de visualisation des tests pour exporter une liste en .txt.
def list_to_txt(db_list, name_txt):
    with open(name_txt, 'w', encoding="utf-8-sig") as text_obj:
        for elem in db_list:
            text_obj.write('%s\n' % elem)
        text_obj.close()


# Fonction de nettoyage et de construction d'une base de donnéees d'artiste.
# OBJECTIFS :
#   - Séparer convenablement chaque artiste sur une même piste
#   - Inclure les (potentielles) remixers comme artistes ayant participer à un morceaux.
#   - Faire l'association avec les alias et "weak" alias (propriétés à définir)
#   - Ajouter les artistes à la base de données avec le nombre de participation par genre.
#   - Exporter le tout en .csv (optionnel).

def build_artist_db(itunes_xml_path, user_name="iTunes_User"):
    cpt_artist = 0
    already_added = {}
    library = Library(itunes_xml_path).songs.values()
    genres_list = list_of_genre(library)
    data = [{"ID": "A0000", "Name": user_name}]
    data[0].update({genre: 0 for genre in genres_list})
    # noinspection PyTypeChecker
    data[0].update(dict(TOTAL=0))
    # Objet de type dictionnaire conservant toutes les musiques avec toutes les métadonnées associées.
    for song in library:
        artist_org = formating_artist(song.artist)  # Appel à la fonction de formatage
        remixer_lst = formating_remixer(song)
        all_artist = sorted(list(set(artist_org + remixer_lst)))
        if song.composer is not None:
            all_artist.append(song.composer)
        all_artist = formating_with_alias(all_artist)
        data[0][song.genre] += 1
        data[0]["TOTAL"] += 1
        for un_artist in all_artist:
            if un_artist not in already_added:
                cpt_artist += 1
                already_added.update({un_artist: cpt_artist})
                data.append({"ID": "A{:04d}".format(cpt_artist), "Name": un_artist})
                data[cpt_artist].update({genre: 0 for genre in genres_list})
                data[cpt_artist].update(dict(TOTAL=1))
                data[cpt_artist][song.genre] += 1
            else:
                data[already_added[un_artist]][song.genre] += 1
                data[already_added[un_artist]]["TOTAL"] += 1
    return data


def list_of_genre(library):
    list_genre = []
    for song in library:
        if song.genre not in list_genre:
            list_genre.append(song.genre)
    list_genre = sorted(list_genre)
    return list_genre


# Fonction de formatage prenant en compte les alias
def formating_with_alias(artist_list):
    alias_on_track = []
    for un_artist in artist_list:
        if un_artist in alias:
            if isinstance(alias[un_artist], list):
                alias_on_track = alias[un_artist]
            else:
                alias_on_track.append(alias[un_artist])
    all_artist = artist_list + alias_on_track
    for un_artist in all_artist:
        if un_artist in weak_alias:
            if isinstance(weak_alias[un_artist], list):
                all_artist = all_artist + weak_alias[un_artist]
                all_artist.remove(un_artist)
            else:
                all_artist.append(weak_alias[un_artist])
                all_artist.remove(un_artist)
    return all_artist


# Fonction de formattage des remixers
def formating_remixer(song_object):
    remixer_lst = []
    if "[" in song_object.name and song_object.name[song_object.name.index("["):] not in not_remix_tag:
        remixer = song_object.name[song_object.name.index("[") + 1:-1]
        for string_to_del in cara_del_remix:
            remixer = remixer.replace(string_to_del, "")
        remixer_lst = formating_artist(remixer)
    return remixer_lst


# Fonction de formatage des artistes en une liste d'artiste.
# La fonction sépare les artistes en fonction chaines de caractères séparatrice dans le champ "Artiste", comme le 'feat'
# qui arrive après le nom de l'artiste principal du morceau (ex : David Guetta feat. Sia - Titanium) ou la croix '×'
# (assez souvent simplifiée en simple "x" ailleurs, c'est juste moi qui préfère l'esthétique de la croix) séparant
# souvant 2 duos pour mieux les distiguer en présence du "&". Ces chaines sont toutes référencées dans le tuple
# "cara_sep_artist", avec souvent une parenthèse les précédant, propre à ma gestion du champ "Artiste" que j'ai adopté
# (les artistes secondaires étant toujours écrit entre parenthèse).

def formating_artist(artist_object):
    artist_txt = artist_object
    if artist_txt[-1] == ')':  # Suppression d'éventuelle dernière parenthèse, en présence d'artiste secondaire
        artist_txt = artist_txt[:-1]
    for sepa in cara_sep_artist:  # On boucle sur la chaîne de caractère pour bien séparer chaque artiste.
        artist_txt = artist_txt.replace(sepa, ", ")
    artist_lst = finding_duos(artist_txt)  # Appel à la fonction qui distingue les duos s'écrivant avec un "&"
    return artist_lst


# Fonction permettant la détection des duos dans une liste d'artiste.
# Cette fonction sert détecter les duos dans le champ artiste si ce champ présente un "&". Puisque l'esperluette (c'est
# son nom) peut aussi bien servir d'élément de séparation entre 2 artistes / entitées distinctes (ex :
# Afrojack & Martin Garrix - Turn Up The Speakers) que d'élément purement esthétique dans le nom d'un duo (ex :
# Tom & Jame - Hold Up). Afrojack et Martin Garrix étant deux entités à part entière, là où Tom & Jame n'en forme qu'une
# seule. C'est d'autant plus complexe (sinon chiant) qu'un duo peut collaborer avec artiste seul (ex : Dimitri Vegas &
# Like Mike & Martin Garrix - Tremor, et 2 fois "&" dans le champ "Artiste"), voir même que 2 duos puissent collaborer
# ensemble (ex : Holl & Rush × Raven & Kreyn (feat. Ryan Konline) - Faith). Les duos sont référencés dans la liste de
# même nom. Cette liste est succeptible d'évoluer avec les ajouts à la bibliothèque iTunes.

def finding_duos(artist_txt):
    artist_lst = []  # Liste à retourner
    for duo in duos:  # Bouclage sur les duos pour tous les détecter correctement.
        if duo in artist_txt:
            # Si un duo est dans le champ "Artiste" pré-traité (string), alors on l'ajoute à la liste à retourner, et on
            # le supprime de la chaîne de caractère en traitement.
            artist_lst.append(duo)
            artist_txt = artist_txt.replace(duo, "")
    # On sépare les artistes restant dans la chaîne de caractère, par le "&" et la virgule, et on supprime d'éventuels
    # doublons.
    artist_lst = list(set(artist_lst + artist_txt.replace(" & ", ", ").split(", ")))
    # Les seules doublons restant sont en fait des chaines de caractères vides issues de la boucle précédente. On va
    # donc les supprimer.
    if "" in artist_lst:
        artist_lst.remove("")
    return sorted(artist_lst)  # Retour de la liste d'artiste triée.


""" - PROGRAM MAIN BODY | CORPS PRINCIPAL DU PROGRAMME - """

xml = "../../../Music/iTunes/iTunes Music Library.xml"

utilisateur = "Dyl_M"

base_de_donnes_art = build_artist_db(xml, utilisateur)

# print(base_de_donnes_art[0])

data_treat = base_de_donnes_art[1:]

entete = list(data_treat[1].keys())
donnees_list = []
print(entete)

for artist in data_treat:
    value_list = []
    for info in artist.values():
        value_list.append(info)
    donnees_list.append(value_list)

df = pandas.DataFrame.from_records(donnees_list, columns=entete)

print(df)

# export_list_to_csv(base_de_donnes_art)

""" - TESTS - """

# library = Library(xml)

# [Orchestral Suite] / [Cover] / [Ochestral Cover]

# mon_itunes = itunes_lib_xml_to_lst()
# print(mon_itunes)

# db_track_csv(xml)

# db_artist_csv()

# ch_test = "Tom & Jame × Holl & Rush & Above & Beyond (feat. A Girl & A Gun) | Raven & Kreyn w/ (G)I-DLE"

# for cara_separateur in cara_sep_artist:
#     ch_test = ch_test.replace(cara_separateur, ", ")
#
# tri = []
#
# if "(G)I-DLE" in ch_test:
#     ch_test = ch_test.replace("(G)I-DLE", "")
#     tri.append("(G)I-DLE")
#     print(tri)
#
# ch_test = ch_test.replace(")", "")
# tri += ch_test.split(", ")
# tri.remove("")
#
# print(tri)
#
# tri2 = []
# for artist in tri:
#     if artist not in tri2:
#         if " & " in artist:
#             for duo in duos:
#                 if duo in artist:
#                     artist = artist.replace(duo, "")
#                     tri2.append(duo)
#         else:
#             tri2.append(artist)
#
# print(tri2)

# print(sorted(track_ignore_lst))

# C:\Users\USER\Documents\[!] PROJETS PERSONNELS\[ITUNES] Recommendations based on iTunes library
# C:\Users\USER\Music\iTunes

# lst_remix = []
#
# for song in library.songs.values():
#     if "[" in song.name:
#         lst_remix.append(song.name)
#
# for song in sorted(lst_remix):
#     decideur = True
#     for tag in track_ignore_lst:
#         if tag in song:
#             decideur = False
#     if not decideur:
#         lst_remix.remove(song)
#
# for i, remix in enumerate(lst_remix):
#     lst_remix[i] = remix[remix.find("["):]
#
# lst_remix_corrected = []
#
# for remix_corr in lst_remix:
#     for c_del in cara_del_remix:
#         if c_del in remix_corr:
#             remix_corr = remix_corr.replace(c_del, "")
#     for c_sep in cara_sep_artist:
#         remix_corr = remix_corr.replace(c_sep, ", ")
#     remix_corr = remix_corr.split(", ")
#     if remix_corr not in lst_remix_corrected:
#         lst_remix_corrected.append(remix_corr)
#
# lst_remix_corrected.sort()
#
# for remix in lst_remix_corrected:
#     print(remix)

""" - REJECTED FUNCTIONS |  FONCTIONS REJETEES - """

# def pre_build_db_artist(xml_path):
#     biblio = Library(xml_path)
#     artist_step1 = []
#     artist_step2 = []
#     artist_step3 = []
#     for song in biblio.songs.values():
#         if song.artist not in artist_step1:
#             artist_step1.append(song.artist)
#     for element in artist_step1:
#         if element not in artist_step2:
#             if "(G)I-DLE" not in element:
#                 element = element.replace(")", "")
#             else:
#                 element = "K/DA (feat. Madison Beer, (G)I-DLE, Jaira Burns"
#             for cara_sep in cara_sep_artist:
#                 element = element.replace(cara_sep, ", ")
#             if ", " in element:
#                 for artist in element.split(sep=", "):
#                     if artist not in artist_step2:
#                         artist_step2.append(artist)
#             else:
#                 artist_step2.append(element)
#     artist_step2.sort()
#     for artist in artist_step2:
#         if " & " in artist:
#             art_corrected = None
#             for each_duo in duos:
#                 if each_duo in artist:
#                     if each_duo not in artist_step3:
#                         artist_step3.append(each_duo)
#                     art_corrected = artist.replace(each_duo, "")
#                     if " & " in art_corrected:
#                         art_corrected = art_corrected.replace(" & ", "")
#             if art_corrected is not None and art_corrected != "" and art_corrected not in artist_step3:
#                 artist_step3.append(art_corrected)
#         else:
#             for art_indiv in artist.split(sep=" & "):
#                 if art_indiv not in artist_step3:
#                     artist_step3.append(art_indiv)
#     artist_step3.sort()
#     return artist_step3


# def db_artist_csv(xml_path):
#     biblio = Library(xml_path)
#     lst_genres = []
#     pre_db_list = pre_build_db_artist(xml_path)
#     for artist in pre_db_list:
#         if artist in tuple(alias.keys()):
#             if type(alias[artist]) is list:
#                 for individual in alias[artist]:
#                     if individual not in pre_db_list:
#                         pre_db_list.append(individual)
#             else:
#                 if alias[artist] not in pre_db_list:
#                     pre_db_list.append(alias[artist])
#     pre_db_list.sort()
#     print(pre_db_list)
#     db_list_artist = []
#     ind = 0
#     for song in biblio.songs.values():
#         if song.genre not in lst_genres:
#             lst_genres.append(song.genre)
#     lst_genres.sort()
#     for artist in pre_db_list:
#         if ind == 0:
#             temp_dict = {"Artist_ID": "AR0000".format(ind), "Artist": "USER::@Dyl_M"}
#         else:
#             temp_dict = {"Artist_ID": "AR{:04d}".format(ind), "Artist": artist}
#         temp_dict2 = {genre: 0 for genre in lst_genres}
#         temp_dict.update(temp_dict2)
#         db_list_artist.append(temp_dict)
#         ind += 1
#     print(db_list_artist[0])
#     # list_to_txt(post_db_list, "test1.txt")


""" - ELEMENTS IN /song/ OBJECT | ELEMENTS DANS UN OBJET /songs/ """

# name(String)
# album = None(String)
# artist(String)
# album_artist(String)
# genre = None(String)
# year = None(Integer)
# date_added = None(Time)
# play_count = None(Integer)
# grouping = None(String)
# composer = None(String)

# comments = None(String)
# persistent_id(String)
# kind = None(String)
# size = None(Integer)
# total_time = None(Integer)
# track_number = None(Integer)
# track_count = None(Integer)
# disc_number = None(Integer)
# disc_count = None(Integer)
# date_modified = None(Time)
# bit_rate = None(Integer)
# sample_rate = None(Integer)
# rating = None(Integer)
# album_rating = None(Integer)
# location = None(String)
# location_escaped = None(String)
# compilation = False(Boolean)
# lastplayed = None(Time)
# skip_count = None(Integer)
# skip_date = None(Time)
# length = None(Integer)
# work = None(String)
# movement_name = None(String)
# movement_number = None(Integer)
# movement_count = None(Integer)
# loved = False(Boolean)
# album_loved = False(Boolean)
