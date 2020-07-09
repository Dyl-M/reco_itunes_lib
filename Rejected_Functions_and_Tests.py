""" - TESTS - """

# artist_per_genre_db.to_csv("test.csv", index=False)

# data_treat = base_de_donnes_art
#
# entete = list(data_treat[1].keys())
# donnees_list = []
#
# for artist in data_treat:
#     value_list = []
#     for info in artist.values():
#         value_list.append(info)
#     donnees_list.append(value_list)
#
# df = pandas.DataFrame.from_records(donnees_list, columns=entete)

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

# def build_artist_db_v01(itunes_xml_path):
#     cpt_artist = 0
#     already_added = {}
#     library = Library(itunes_xml_path).songs.values()
#     genres_list = list_of_genre(library)
#     data = []
#     # Objet de type dictionnaire conservant toutes les musiques avec toutes les métadonnées associées.
#     for song in library:
#         artist_org = formating_artist(song.artist)  # Appel à la fonction de formatage
#         remixer_lst = formating_remixer(song)
#         all_artist = sorted(list(set(artist_org + remixer_lst)))
#         if song.composer is not None:
#             all_artist.append(song.composer)
#         all_artist = formating_with_alias(all_artist)
#         for un_artist in all_artist:
#             if un_artist not in already_added:
#                 cpt_artist += 1
#                 already_added.update({un_artist: cpt_artist})
#                 data.append({"Name": un_artist})
#                 data[cpt_artist - 1].update({genre: 0 for genre in genres_list})
#                 data[cpt_artist - 1][song.genre] += 1
#             else:
#                 data[already_added[un_artist] - 1][song.genre] += 1
#     return data

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
#
# def export_list_to_csv(a_list, csv_name="Artist_Library.csv"):
#     col_names = a_list[0].keys()
#     try:
#         with open(csv_name, 'w', encoding="utf-8-sig", newline='') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=col_names, delimiter=";")
#             writer.writeheader()
#             for data in a_list:
#                 writer.writerow(data)
#     except IOError:
#         print("I/O error")
