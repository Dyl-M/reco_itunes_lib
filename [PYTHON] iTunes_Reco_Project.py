# __ INFORMATION SCRIPT __

# !/usr/bin/python3
# -*- coding:utf8 -*-
""" - Bref, j'ai hacké iTunes (c'est faux) - """

# fichier  : [PYTHON] Proj_iTunes_Library.XML.py
# Auteur : MONFRET Dylan

# __ IMPORTATION DE FONCTION EXTERNE & PACKAGE __

from libpytunes import Library
from datetime import datetime
from time import mktime
import csv

# __ DONNEES GLOBALES __

duos = {"A Girl & A Gun", "ANDY & FILIPE SILVEIRA", "ARICK & DUNNO", "Above & Beyond", "Amadou & Mariam",
        "Asketa & Natan Chaim", "Bigflo & Oli", "Case & Point", "DJ KUBA & NEITAN", "Dimitri Vangelis & Wyman",
        "Dimitri Vegas & Like Mike", "Dodge & Fuski", "Dzeko & Torres", "Edward Sharpe & The Magnetic Zeros",
        "Gent & Jawns", "Holl & Rush", "Jack & Jordan", "Jaxx & Vega", "Jewelz & Sparks", "Klauss & Turino",
        "Lucas & Steve", "Lush & Simon", "Matisse & Sadko", "Mave & Zac", "Merk & Kremont", "Mr. Belt & Wezol",
        "Nico & Vinz", "PBH & Jack Shizzle", "Paris & Simo", "Pep & Rash", "Petterson & Findus", "Phats & Small",
        "Rave & Crave", "Raven & Kreyn", "Relanium & Deen West", "Rico & Miella", "Riggi & Piros", "Slips & Slurs",
        "Sunnery James & Ryan Marciano", "Tegan & Sara", "The Flexican & FS Green", "Tom & Jame", "Vargas & Lagola",
        "Volt & State", "W&W", "Will & Tim", "nFiX & Candice"}

alias = {"AvB": "Armin van Buuren", "Rising Star": "Armin van Buuren", "NWL": "Afrojack", "DJ Afrojack": "Afrojack",
         "Ravitez": "Chico Rose", "GRX": "Martin Garrix", "Daffy Muffin": "Lucas & Steve",
         "AREA21": ["Martin Garrix", "Maejor"], "Matthew Ros": "MWRS", "Kerafix & Vultaire": "KEVU",
         "Dzeko & Torres": "Dzeko", "Lush & Simon": ["Simon Says", "Zen/It"], "M.E.G. & N.E.R.A.K.": "DJ M.E.G.",
         "MEG / NERAK": "DJ M.E.G.", "Grant Bowtie": "Grant", "Chill Harris": "Kill Paris",
         "Jayden Jaxx": "Crime Zcene", "Major Lazer": ["Diplo", "Walshy Fire", "Ape Drums"], "X-Teef": "Stemalø",
         "Paris & Simo": "Prince Paris", "VIRTUAL SELF": "Porter Robinson", "The Eden Project": "EDEN",
         "Streex": "Razihel", "Jack Ü": ["Skrillex", "Diplo"], "Slips & Slurs": "Slippy", "Vorwerk": "Maarten Vorwerk",
         "Will & Tim": "NewGamePlus", "Axwell Λ Ingrosso": ["Sebastian Ingrosso", "Axwell"],
         "Swedish House Mafia": ["Axwell", "Sebastian Ingrosso", "Steve Angello"],
         "Casseurs Flowters": ["OrelSan", "Gringe"], "NWYR": "W&W", "Shindeai": "STARRYSKY", "Sasha": "STARRYSKY",
         "Sinnoh Fusion Ensemble": "insaneintherainmusic"}

track_ignore_lst = (
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

cara_sep_artist = (
    " (feat. ", " (w/ ", " + ", " w/ ", " × ", " | ", " vs. ", " V/S ", " VS ", " V.S ", " VS. ", " vs ")

cara_del_remix = (
    "[", "]", " BONUS TRACK", "ADE Intro | ", " Remake", " Rebuild", " Blastersmash",
    " Re-Crank", "'s 2k17 Bootleg", " Bootleg", "'s VIP Mix", "'s VIP Remix", " Rework", " UMF 2017 Mashup",
    " UMF Edit", "'s Swede Remix", " Flip", " FLIP", " Heaven Trap Remix", " VIP Mix", " Power-Up",
    "'s Disco House Remix", " ReBoot", " Vocal Edit", " Extended Remix", " Festival Mix", " Brown Note Remix",
    " 2016 Remix", " Remix", " Mix", " Edit", " Mashup", " VIP Edit")


# __ DEFINITION DE FONCTIONS __

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


def list_to_txt(db_list, name_txt):
    with open(name_txt, 'w', encoding="utf-8-sig") as text_obj:
        for elem in db_list:
            text_obj.write('%s\n' % elem)
        text_obj.close()


def pre_build_db_artist(xml_path):
    biblio = Library(xml_path)
    artist_step1 = []
    artist_step2 = []
    artist_step3 = []
    for song in biblio.songs.values():
        if song.artist not in artist_step1:
            artist_step1.append(song.artist)
    for element in artist_step1:
        if element not in artist_step2:
            if "(G)I-DLE" not in element:
                element = element.replace(")", "")
            else:
                element = "K/DA (feat. Madison Beer, (G)I-DLE, Jaira Burns"
            for cara_sep in cara_sep_artist:
                element = element.replace(cara_sep, ", ")
            if ", " in element:
                for artist in element.split(sep=", "):
                    if artist not in artist_step2:
                        artist_step2.append(artist)
            else:
                artist_step2.append(element)
    artist_step2.sort()
    for artist in artist_step2:
        if " & " in artist:
            art_corrected = None
            for each_duo in duos:
                if each_duo in artist:
                    if each_duo not in artist_step3:
                        artist_step3.append(each_duo)
                    art_corrected = artist.replace(each_duo, "")
                    if " & " in art_corrected:
                        art_corrected = art_corrected.replace(" & ", "")
            if art_corrected is not None and art_corrected != "" and art_corrected not in artist_step3:
                artist_step3.append(art_corrected)
        else:
            for art_indiv in artist.split(sep=" & "):
                if art_indiv not in artist_step3:
                    artist_step3.append(art_indiv)
    artist_step3.sort()
    return artist_step3


def db_artist_csv(xml_path):
    biblio = Library(xml_path)
    lst_genres = []
    pre_db_list = pre_build_db_artist(xml_path)
    for artist in pre_db_list:
        if artist in tuple(alias.keys()):
            if type(alias[artist]) is list:
                for individual in alias[artist]:
                    if individual not in pre_db_list:
                        pre_db_list.append(individual)
            else:
                if alias[artist] not in pre_db_list:
                    pre_db_list.append(alias[artist])
    pre_db_list.sort()
    print(pre_db_list)
    db_list_artist = []
    ind = 0
    for song in biblio.songs.values():
        if song.genre not in lst_genres:
            lst_genres.append(song.genre)
    lst_genres.sort()
    for artist in pre_db_list:
        if ind == 0:
            temp_dict = {"Artist_ID": "AR0000".format(ind), "Artist": "USER::@Dyl_M"}
        else:
            temp_dict = {"Artist_ID": "AR{:04d}".format(ind), "Artist": artist}
        temp_dict2 = {genre: 0 for genre in lst_genres}
        temp_dict.update(temp_dict2)
        db_list_artist.append(temp_dict)
        ind += 1
    print(db_list_artist[0])
    # list_to_txt(post_db_list, "test1.txt")


# __ CORPS PRINCIPAL DU PROGRAMME __

xml = "../../../Music/iTunes/iTunes Music Library.xml"
library = Library(xml)

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

xml = "../../../Music/iTunes/iTunes Music Library.xml"
library = Library(xml)

# print(sorted(track_ignore_lst))

# C:\Users\USER\Documents\[!] PROJETS PERSONNELS\[ITUNES] Recommendations based on iTunes library
# C:\Users\USER\Music\iTunes

lst_remix = []

for song in library.songs.values():
    if "[" in song.name:
        lst_remix.append(song.name)

for song in sorted(lst_remix):
    decideur = True
    for tag in track_ignore_lst:
        if tag in song:
            decideur = False
    if not decideur:
        lst_remix.remove(song)

for i, remix in enumerate(lst_remix):
    lst_remix[i] = remix[remix.find("["):]

lst_remix_corrected = []

for remix_corr in lst_remix:
    for c_del in cara_del_remix:
        if c_del in remix_corr:
            remix_corr = remix_corr.replace(c_del, "")
    for c_sep in cara_sep_artist:
        remix_corr = remix_corr.replace(c_sep, ", ")
    remix_corr = remix_corr.split(", ")
    if remix_corr not in lst_remix_corrected:
        lst_remix_corrected.append(remix_corr)

lst_remix_corrected.sort()

for remix in lst_remix_corrected:
    print(remix)

""" - LISTE DES ELEMENTS TROUVABLES DANS L'OBJET DE TYPE/songs/ """

# name(String)
# album = None(String)
# artist(String)
# album_artist(String)
# genre = None(String)
# year = None(Integer)
# date_added = None(Time)
# play_count = None(Integer)
# grouping = None(String)

# comments = None(String)
# persistent_id(String)
# composer = None(String)
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
