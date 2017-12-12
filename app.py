# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import re

from flask import Flask
from flask import request
from flask import make_response
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Flask app should start in global layout
app = Flask(__name__)


choices = ["Tera Mera Pyar Amar"
           "Tujhse Naraz Nahi Zindagi"
           "Tere Bina Besuaadi lage ye ratiyan"
           "01 Radha nam sang brij 84 kos"
           "01 SURAJ KI GARMI SE"
           "04 RAAM NAAM SE TUMNE BANDE"
           "06 KUCHH PAL KI ZINDAGI"
           "22 BHALA KISI KA KAR NA SAKO"
           "Sunder Kand(Mzc.in)"
           "Hanuman Ji Ki Aarti"
           "He Ram He Ram"
           "Jai Jai Hanuman Gunsai"
           "Kabir Amritvani - 1"
           "Kabir Amritvani - 2"
           "Manavta_ke_mann_mandir_mein"
           "Bandaa Re - www.Songs.PK"
           "Om Jagdish Hare"
           "Track01"
           "Sunder Kand(Mzc.in)"
           "Asha Bhosle"
           "Dr.Balamuralikrishna"
           "Pt.Ajoy Chakrabarty with Kaushiki Chakrabarty"
           "Pt.Hari Prasad Chaurasia"
           "Hariharan"
           "Lata Mangeshkar wav"
           "Maa Tujhe Salaam"
           "Mile sur mera tumhara"
           "National Anthem collective instrumental version"
           "National Anthem collective vocal version wav"
           " Vande Mataram '98 - Lata Mangeshkar"
           "Lonely"
           "Words"
           "Heaven"
           "It's Only Love"
           "When You Love Someone"
           "10.EVERYTHING I DO"
           "In The End"
           "It's My Life"
           "04.SUMMER OF '69"
           "So Happy Together"
           "Mangal Bhairav"
           "Mangal Bhairav2"
           "Raga Durgawati: Alap"
           "Raga Durgawati: Gat in teen tal"
           "Raga Durgawati: Drut gat in teental"
           "Raga Mishra Shivaranjani: Alap"
           "Raga Mishra Shivaranjani: Dhun in dadra tal"
           "01 KHUDA JAANE"
           "Track 02"
           "Track 06"
           "Maula Mere Lele Meri Jaan"
           "Track 11"
           "06 TERI UMEED TERA INTZAR"
           "suna"
           "Udit & Alka"
           "01 KYON KI ITNA PYAR"
           "05Layi Vi Na Gayee"
           "Track 04"
           "JAB KOI BAAT BIGAD JAAYE"
           "13 LAGI AAJ SAWAN KI"
           "Jee Karda - www.Songs.PK"
           "14 SATYAM SHIVAM SUNDRAM"
           "Track 1"
           "Main Agar Kahoon"
           "19 TUJH MEIN RAB DIKHTA HAI ("
           "20 to chaloon"
           "21 Tadap Tadap"
           "22 aina tenu pyar"
           "line in track 20"
           "25 Aaja Sohneya"
           "26 SAJJAN  RUSS  GAYE"
           "27 DIL TAN PAGAL HAI"
           "MUSIC PLANET KALLI BEH KE SOCHIN"
           "Teri Ore - www.Songs.PK"
           "Kaise Mujhe - www.Songs.PK"
           "Guzarish - www.Songs.PK"
           "01 DEKHA HAI PEHLI BAAR"
           "02 TUMSE MILNE KI TAMMANA"
           "03 BAHUT PYAR KARTE (F)"
           "04 JEYEN TO JEYEN KAISE"
           "05 TU SAYAR HAI"
           "Track 06"
           "07 MERA DIL BHI KITNA"
           "Track 08"
           "09 BAHUT PYAR KARTE (M)"
           "01CHHOTI CHHOTI RAATEIN"
           "SIVA"
           "FARIYAAD"
           "04DEKHTE HI DEKHTE"
           "05MERI DUNIYA MEIN"
           "BOOMBARA"
           "07DAAROO VICH PYAAR"
           "BIN"
           "RU"
           "10CHHOTI CHHOTI RAATEIN PART2"
           "11PYAAR HUM KO HONE LAGA"
           "12MERI DUNIYA MEIN"
           "O...Saya - www.Songs.PK"
           "Riots - www.Songs.PK"
           "Mausam & Escape - www.Songs.PK"
           "Paper Planes - www.Songs.PK"
           "Paper Planes (DFA Remix) - www.Songs.PK"
           "Ringa Ringa - www.Songs.PK"
           "Liquid Dance - www.Songs.PK"
           "Latika's Theme - www.Songs.PK"
           "Aaj Ki Raat - www.Songs.PK"
           "Millionaire - www.Songs.PK"
           "Gangsta Blues - www.Songs.PK"
           "Dreams On Fire - www.Songs.PK"
           "Jai Ho - www.Songs.PK"
           "Aakhnkho Mein Jal Raha Hai"
           "Din Kuch Aise Guzarta"
           "Ek Parvaz Dikhayi Di Hai"
           "Speaks"
           "Speeak"
           "Speaks"
           "Haat Chhute bhi To"
           "Ik Purana Mausam Lauta"
           "Shaam Se aankhmein Nami Si ha"
           "Woh Khat Ke Purze Uda Rahatha"
           "Zindage yun Hui Basar Tanha"
           "01 TOH PHIR AAO MUSTAFA ZAHID"
           "01 ZARA SA"
           "01Kya Mujhe Pyaar Hai"
           "01Teri Yaadon Mein"
           "01Tu Hi Meri Shab Hai"
           "Aadat"
           "JUDAI"
           "Track 2"
           "02 PEHLI NAZAR MEIN"
           "02 TERA MERA RISHTA MUSTAFA Z"
           "Tu Meri Dost Hain - Songs.PK"
           "Bheegi"
           "02ChalChale"
           "Bin"
           "03 JAANE TU MERA KYA HAI"
           "Track 3"
           "03Tu Jo Nahin"
           "Track 4"
           "9. TU MERI JAAN HAIN"
           "a01 ek din teri"
           "Track 04"
           "01. KYON KI ITNA PYAR"
           "thoda sa pyaar hua"
           "EK LADKI KO DEKHA TO"
           "03. DIL KE BADLE SANAM"
           "Jugni"
           "Aa Bhi Ja Aa"
           "aadat"
           "Track 01"
           "Kuch Is Tarah (Mp3HunGama.Com)"
           "Track 12"
           "Dekho Maine Dekha"
           "chaha hai tujhko"
           "Chalo Tumko Lekar Chale @ Mp3Hungama.com"
           "choti choti raatein"
           "Tere Bin - Rabbi Shergill"
           "DEKHA TUJHE TO"
           "03 dil de diya hai"
           "dil..."
           "Track 1"
           "HUM DUM SUNIYO RE                              "
           "HUM HAIN RAHI PYAR KE - KASH"
           "HUM HAIN RAHI PYAR KE - WOH M"
           "humko sirf tumse pyaar..."
           "INTEHA HO GAYI INTEZAAR KI"
           "1Is tarah aashiqi ka"
           "Dil To Bachcha Hai - www.Songs.PK"
           "Track 01"
           "Tera Saath Hai Kitna Pyara"
           "Jadu hai Nasha Hai @ Mp3Hungama.com"
           "Track 05"
           "Pehla Nasha"
           "11 kyon kisi ko"
           "kyon ke itna pyar "
           "Leja Leja"
           "Main Jahaan Rahoon"
           "Mauja Hi Mauja - [Songs.PK]"
           "Maula Mere Le Le Meri Jaan - [Songs.PK]"
           "Maula Mere Maula"
           "MERA DIL BHI KITNA - K SANU &"
           "MITRAN DI CHHATRI"
           "pehla nasha"
           "PYAR SE MERI TARAF"
           "Behene De - www.Songs.PK"
           "Bulla Ki Jaana"
           "Jaane Kaise - Songs.PK"
           "Bluffmaster (2005) - 04 - Right Here Right Now"
           "Saagar Jaise Ankhon"
           "BUHUT PYAR KARTE"
           "Musafirak13"
           "SUCH KEH RAHA HAI"
           "tera chehra"
           "Tere Bin "
           "Track  1"
           "Tumse Milna"
           "Tune Jo Na Kaha - www.Songs.PK"
           "Woh Pehli Baar"
           "Ya Rabba [DJLUV]"
           "zara zara"
           "Zindagi Bangae Ho Tum"
           "Aaj Kal Tere Mere Pyar Ke"
           "Main Shair To Nahin"
           "Chabi Kho Jaye"
           "Akele hain chale aao"
           "An Evening In Paris"
           "Mere Man Ki Ganga - www.songs.pk"
           "Chithi Aai Hai - Pankaj Udhas"
           "DIl KI Aawaz Bhi Sun"
           "Dost Dost Na Raha -www.songs.pk"
           "Duniya Na Bhaaye - Basant Bahaar 1956 - Mohammed Rafi"
           "hai preet jahan ki reet"
           "hamne jafa na sikhi"
           "Har Dil Jo Pyar Karega - www.songs.pk"
           "Hum Bewafa Hargiz Na The"
           "Hum Tum Se Judaa Ho Ke"
           "huye hum jin ke liye"
           "Kasie Kahin Hum"
           "kya hua tera wada"
           "Suhana Safar Aur Yeh"
           "MANZILEN APNI JAGAH"
           "Huzur Is Kadar"
           "Mere Dosti Mera Pyar"
           "Milan (1965) - Aaj Dil Pe Koi"
           "Nain Lad Jai Hai [From Ganga Jumna]"
           "Aaj Mausam Bada Be-Iman Hai [From Loafer]"
           "khuda"
           "Akele hain chale aao{Rafi}"
           "Ek tha gul aur ek thi bulbul"
           "Mujhe Buddah Mil Gaya -www.songs.pk"
           "Mujhe Ishq Hai Tujhe Se"
           "O Meri Sharmilee"
           "Aye Meri Zohra Jabeen"
           "Aye Mere pyare watan"
           "Tu pyar ka sagar hai"
           "Zindagi Ki Na Toote"
           "Zihale Masti"
           "Jab Hum Jawan Honge"
           "Hum Bane Tum Bane"
           "Chahe Lakh Tufan"
           "Dekho Maine Dekha"
           "Hum Tum Dono Milke"
           "Mere Pyar Ki Umar"
           "Teri Yaad Aayee"
           "Pyaar Kiya Nahin Jata"
           "Aankhon Mein Kajal Hai"
           "Mera Pyar Bhi Tu Hai - Saathi"
           "Bhanvare Ne Khilaya"
           "Mere Saathi Jivan Saathi"
           "Kya Khoob Lagti Ho - Dharmatma"
           "Humrahi Mere Humrahi"
           "Janam Janam Ka Saath"
           "Hum To Tere Aashiq - Farz"
           "Paani Re Paani - Shor"
           "Main Hoon Pyar Tera [Teesri Manzil]"
           "Phool Tumhe Bheja"
           "hum tumhe chahte hain"
           "Jeevan Se Bhari Teri"
           "Jo Tumko Ho Pasand"
           "Sau Baar Janam Leinge"
           "TU PYAR KA SAGAR HAI"
           "Dil Cheez Kya Hai"
           "Wada Karo"
           "Wadiyan Mera Daman [From Abhilasha]"
           "Yaad na jaye"
           "yaadon ki baarat nikli hai"
           "Yeh Mera Prem Patra - www.songs.pk"
           "YEH DIL NA HOTA BECHARA  "
           "Track 01"
           "01SAJJAN RUS GAYE"
           "02 botalan sharab diyan"
           "02 mundiya tu bach ke"
           "Mehfil"
           "Ae Jo Seeli Seeli Aundi Ae Hawa"
           "ik aisi ladki thi"
           "KOI"
           "3 DHOL NEW"
           "Track 1"
           "Dil Ta Pagal"
           "01_ISHQE_DI_MAAR"
           "01"
           "NAAG JAZZY B"
           "SAPNE MAIN MILTE HAIN SATYA"
           "Tum Saath Ho - Songspk.LINK"
           "Boond Boond - MyMp3Song.com"
           "12 Saal (DjPunjab.CoM)"
           "Aise Na Mujhe Tum Dekho (Armaan Malik) Full Song"
           "Mere Sapno Ki Rani Kab - www.hotmentos.com"
           "Att Goriye"
           "Jaguar (feat. Bohemia) (DJJOhAL.Com)"
           "Baliye (Laung Gawacha) (Mr-Jatt.com)"
           "Bapu Zimidar (RoyalJatt.Com)"
           "BILAL SAEED -ADHI ADHI RAAT (DjPunjab.CoM)"
           "2 Number"
           "Black Suit (RoyalJatt.Com)"
           "Blow (RoyalJatt.Com)"
           "Bolo Har Har Har (Mr-Jatt.com)"
           "Breakup Party - Yo Yo Honey Singh (Ft. Leo) - ApnaFunz.Com"
           "Brown Boi (feat. Bling Singh)"
           "Chupke Se - Saathiya (RoyalJatt.Com)"
           "Chura Liya Hai Tumne Jo Dil Ko (RoyalJatt.Com)"
           "Dil Cheez Tujhe Dedi(Mr-Jatt.com)"
           "Halka Halka Suroor (Nusrat Fateh Ali Khan Cover)"
           "Ford V s Ford (RoyalJatt.Com)"
           "Ambarsariya - www.DJMaza.Com"
           "Horn Blow (RaagJatt.Com)"
           "Hulara (RoyalJatt.Com)"
           "Jatt Sikka (RoyalJatt.Com)"
           "Jugni @ Mp3HunGama.Com"
           "Jutti Kasuri - iPendu.com"
           "Khaab(Mr-Jatt.com)"
           " (DJJOhAL.Com)"
           "Laung Gawacha (Mr-Jatt.com)"
           "Look    ::www.RAAG.ME::"
           "Mainu Single Rehna - PagalWorld.com"
           "Mere Mehboob Qayamat Hogi (RoyalJatt.Com)"
           "Munda Iphone Warga (RoyalJatt.Com)"
           "O Re Piya"
           "One Dream(Mr-Jatt.com)"
           "Outfit - Guru Randhawa (RaagTune.Com)"
           "Patola (RoyalJatt.Com)"
           "Dilko - www.Songs.PK"
           "Roop Tera Mastana (Aradhana)    ::www.RAAG.ME::"
           "Sapna Jahan - MyMp3Song.Com"
           "tinka tinka"
           "Tu Hai Ki Nahi [Mixmp3.In]"
           "Zara Zara"
           "Zulfa - (Ft Dr.Zeus) (RoyalJatt.Com)" ]

map_choices =     { "Tera Mera Pyar Amar" : "https://drj1.000webhostapp.com/tera.mp3" ,
                    "Tujhse Naraz Nahi Zindagi" : "https://drj1.000webhostapp.com/tujhse_naraaz_nahin_zindagi__male__-_masoom_songs_-__naseeruddin_shah_-_jugal_hansraj__-_filmigaane.mp3" ,
                    "Tere Bina Besuaadi lage ye ratiyan" : "https://drj1.000webhostapp.com/bina.mp3" ,
                    "01 Radha nam sang brij 84 kos" : "https://drj1.000webhostapp.com/01_Radha_nam_sang_brij_84_kosh_yatr.mp3" ,
                    "01 SURAJ KI GARMI SE" : "https://drj1.000webhostapp.com/01_SURAJ_KI_GARMI_SE.mp3" ,
                    "04 RAAM NAAM SE TUMNE BANDE" : "https://drj1.000webhostapp.com/04_RAAM_NAAM_SE_TUMNE_BANDE.mp3" ,
                    "06 KUCHH PAL KI ZINDAGI" : "https://drj1.000webhostapp.com/06_KUCHH_PAL_KI_ZINDAGI.mp3" ,
                    "22 BHALA KISI KA KAR NA SAKO" : "https://drj1.000webhostapp.com/22_BHALA_KISI_KA_KAR_NA_SAKO_TO.mp3" ,
                    "Sunder Kand(Mzc.in)" : "https://drj1.000webhostapp.com/_mzc_Sunder_Kand_www.mzc.in_.mp3" ,
                    "Hanuman Ji Ki Aarti" : "https://drj1.000webhostapp.com/Hanuman_Ji_Ki_Aarti.mp3" ,
                    "He Ram He Ram" : "https://drj1.000webhostapp.com/He_Ram_He_Ram.mp3" ,
                    "Jai Jai Hanuman Gunsai" : "https://drj1.000webhostapp.com/Jai_Jai_Hanuman_Gunsai.mp3" ,
                    "Kabir Amritvani - 1" : "https://drj1.000webhostapp.com/KabirAmritvani-1.mp3" ,
                    "Kabir Amritvani - 2" : "https://drj1.000webhostapp.com/KabirAmritvani-2.mp3" ,
                    "Manavta_ke_mann_mandir_mein" : "https://drj1.000webhostapp.com/Manavta_ke_mann_mandir_mein.mp3" ,
                    "Bandaa Re - www.Songs.PK" : "https://drj1.000webhostapp.com/moko_kaha_dundhat_hain_bande.mp3" ,
                    "Om Jagdish Hare" : "https://drj1.000webhostapp.com/Om_Jagdish_Hare___Fmw11.com.mp3" ,
                    "Track01" : "https://drj1.000webhostapp.com/PEERTEREJANDI.mp3" ,
                    "Sunder Kand(Mzc.in)" : "https://drj1.000webhostapp.com/Sunder_Kand.mp3" ,
                    "Asha Bhosle" : "https://drj1.000webhostapp.com/Asha_Bhosle.mp3" ,
                    "Dr.Balamuralikrishna" : "https://drj1.000webhostapp.com/Balamuralikrishna.mp3" ,
                    "Pt.Ajoy Chakrabarty with Kaushiki Chakrabarty" : "https://drj1.000webhostapp.com/Chakrabarty.mp3" ,
                    "Pt.Hari Prasad Chaurasia" : "https://drj1.000webhostapp.com/Hari_Prasad.mp3" ,
                    "Hariharan" : "https://drj1.000webhostapp.com/Hariharan.mp3" ,
                    "Lata Mangeshkar wav" : "https://drj1.000webhostapp.com/Lata_Mangeshkar.mp3" ,
                    "Maa Tujhe Salaam" : "https://drj1.000webhostapp.com/Maa_Tujhe_Salaam.mp3" ,
                    "Mile sur mera tumhara" : "https://drj1.000webhostapp.com/Mile_Sur_Mera_Tumhara.mp3" ,
                    "National Anthem collective instrumental version" : "https://drj1.000webhostapp.com/National_instrumental.mp3" ,
                    "National Anthem collective vocal version wav" : "https://drj1.000webhostapp.com/National_vocal.mp3" ,
                    " Vande Mataram '98 - Lata Mangeshkar" : "https://drj1.000webhostapp.com/Vande98_Lata_Mangeshkar.mp3" ,
                    "Lonely" : "https://drj1.000webhostapp.com/Akon_-_Lonely.mp3" ,
                    "Words" : "https://drj1.000webhostapp.com/Boyzone-Words.mp3" ,
                    "Heaven" : "https://drj1.000webhostapp.com/Brian_adams_-_Heaven.mp3" ,
                    "It's Only Love" : "https://drj1.000webhostapp.com/Bryan_Adams_-_It_s_Only_Love.mp3" ,
                    "When You Love Someone" : "https://drj1.000webhostapp.com/Bryan_Adams_-_When_You_Love_Someone.mp3" ,
                    "10.EVERYTHING I DO" : "https://drj1.000webhostapp.com/EVERYTHING_I_DO.mp3" ,
                    "In The End" : "https://drj1.000webhostapp.com/in_the_end.mp3" ,
                    "It's My Life" : "https://drj1.000webhostapp.com/It_s_my_life.mp3" ,
                    "04.SUMMER OF '69" : "https://drj1.000webhostapp.com/SUMMER_OF__69.mp3" ,
                    "So Happy Together" : "https://drj1.000webhostapp.com/the_turtles_-_so_happy_together.mp3" ,
                    "Mangal Bhairav" : "https://drj1.000webhostapp.com/Mangal_Bhairav.mp3" ,
                    "Mangal Bhairav2" : "https://drj1.000webhostapp.com/Mangal_Bhairav2.mp3" ,
                    "Raga Durgawati: Alap" : "https://drj1.000webhostapp.com/PHC_01_Raga_Durgawati-_Alap.mp3" ,
                    "Raga Durgawati: Gat in teen tal" : "https://drj1.000webhostapp.com/PHC_02_Raga_Durgawati-_Gat_in_teen_tal.mp3" ,
                    "Raga Durgawati: Drut gat in teental" : "https://drj1.000webhostapp.com/PHC_03_Raga_Durgawati-_Drut_gat_in_teental.mp3" ,
                    "Raga Mishra Shivaranjani: Alap" : "https://drj1.000webhostapp.com/PHC_04_Raga_Mishra_Shivaranjani-_Alap.mp3" ,
                    "Raga Mishra Shivaranjani: Dhun in dadra tal" : "https://drj1.000webhostapp.com/PHC_05_Raga_Mishra_Shivaranjani-_Dhun_in_dadra_tal.mp3" ,
                    "01 KHUDA JAANE" : "https://drj1.000webhostapp.com/01_KHUDA_JAANE.mp3" ,
                    "Track 02" : "https://drj1.000webhostapp.com/02_TUM_SE_HI.mp3" ,
                    "Track 06" : "https://drj1.000webhostapp.com/03_Chaha_Hay_Tumko.mp3" ,
                    "Maula Mere Lele Meri Jaan" : "https://drj1.000webhostapp.com/04_Maula_Mere_Lele_Meri_Jaan.mp3" ,
                    "Track 11" : "https://drj1.000webhostapp.com/05_Ham_Aapke.mp3" ,
                    "06 TERI UMEED TERA INTZAR" : "https://drj1.000webhostapp.com/06_TERI_UMEED_TERA_INTZAR.mp3" ,
                    "suna" : "https://drj1.000webhostapp.com/07_suna.mp3" ,
                    "Udit & Alka" : "https://drj1.000webhostapp.com/08_Tere_Naam_-_Udit_&_Alka.mp3" ,
                    "01 KYON KI ITNA PYAR" : "https://drj1.000webhostapp.com/09_KYON_KI_ITNA_PYAR.mp3" ,
                    "05Layi Vi Na Gayee" : "https://drj1.000webhostapp.com/10_Layi_Vi_Na_Gayee.mp3" ,
                    "Track 04" : "https://drj1.000webhostapp.com/11_Sab_Kuchh_Bhula_Diya.mp3" ,
                    "JAB KOI BAAT BIGAD JAAYE" : "https://drj1.000webhostapp.com/12_JURM_=_JAB_KOI_BAAT_BIGAD_JAAYE.mp3" ,
                    "13 LAGI AAJ SAWAN KI" : "https://drj1.000webhostapp.com/13_LAGI_AAJ_SAWAN_KI.mp3" ,
                    "Jee Karda - www.Songs.PK" : "https://drj1.000webhostapp.com/14_JEE_KARDA.mp3" ,
                    "14 SATYAM SHIVAM SUNDRAM" : "https://drj1.000webhostapp.com/14_SATYAM_SHIVAM_SUNDRAM.mp3" ,
                    "Track 1" : "https://drj1.000webhostapp.com/15_CHAND_SIFARISH.mp3" ,
                    "Main Agar Kahoon" : "https://drj1.000webhostapp.com/18_Main_Agar_Kahoon_-_plateau.mp3" ,
                    "19 TUJH MEIN RAB DIKHTA HAI (" : "https://drj1.000webhostapp.com/19_TUJH_MEIN_RAB_DIKHTA_HAI__ROOP_KUMAR_RATHOD_.mp3" ,
                    "20 to chaloon" : "https://drj1.000webhostapp.com/20_to_chaloon.mp3" ,
                    "21 Tadap Tadap" : "https://drj1.000webhostapp.com/21_Tadap_Tadap.mp3" ,
                    "22 aina tenu pyar" : "https://drj1.000webhostapp.com/22_aina_tenu_pyar.mp3" ,
                    "line in track 20" : "https://drj1.000webhostapp.com/23_AIVEN_RUSIA_NA_KER_MERI.mp3" ,
                    "25 Aaja Sohneya" : "https://drj1.000webhostapp.com/25_Aaja_Sohneya.mp3" ,
                    "26 SAJJAN  RUSS  GAYE" : "https://drj1.000webhostapp.com/26_SAJJAN__RUSS__GAYE.mp3" ,
                    "27 DIL TAN PAGAL HAI" : "https://drj1.000webhostapp.com/27_DIL_TAN_PAGAL_HAI.mp3" ,
                    "MUSIC PLANET KALLI BEH KE SOCHIN" : "https://drj1.000webhostapp.com/28_KALLI_BEH_KE_SOCHIN.mp3" ,
                    "Teri Ore - www.Songs.PK" : "https://drj1.000webhostapp.com/29_TERI_ORE.mp3" ,
                    "Kaise Mujhe - www.Songs.PK" : "https://drj1.000webhostapp.com/30_KAISE_MUJHE.mp3" ,
                    "Guzarish - www.Songs.PK" : "https://drj1.000webhostapp.com/31_GUZARISH.mp3" ,
                    "01 DEKHA HAI PEHLI BAAR" : "https://drj1.000webhostapp.com/01_DEKHA_HAI_PEHLI_BAAR.mp3" ,
                    "02 TUMSE MILNE KI TAMMANA" : "https://drj1.000webhostapp.com/02_TUMSE_MILNE_KI_TAMMANA.mp3" ,
                    "03 BAHUT PYAR KARTE (F)" : "https://drj1.000webhostapp.com/03_BAHUT_PYAR_KARTE__F_.mp3" ,
                    "04 JEYEN TO JEYEN KAISE" : "https://drj1.000webhostapp.com/04_JEYEN_TO_JEYEN_KAISE.mp3" ,
                    "05 TU SAYAR HAI" : "https://drj1.000webhostapp.com/05_TU_SAYAR_HAI.mp3" ,
                    "Track 06" : "https://drj1.000webhostapp.com/06_PEHLI_BAAR_MILE_HAIN.mp3" ,
                    "07 MERA DIL BHI KITNA" : "https://drj1.000webhostapp.com/07_MERA_DIL_BHI_KITNA.mp3" ,
                    "Track 08" : "https://drj1.000webhostapp.com/08_JEYE_TO_JIYE_KAISE__M_.mp3" ,
                    "09 BAHUT PYAR KARTE (M)" : "https://drj1.000webhostapp.com/09_BAHUT_PYAR_KARTE__M_.mp3" ,
                    "01CHHOTI CHHOTI RAATEIN" : "https://drj1.000webhostapp.com/01CHHOTI_CHHOTI_RAATEIN.mp3" ,
                    "SIVA" : "https://drj1.000webhostapp.com/02THUMARE_SIVA.mp3" ,
                    "FARIYAAD" : "https://drj1.000webhostapp.com/03KOI_FARIYAAD.mp3" ,
                    "04DEKHTE HI DEKHTE" : "https://drj1.000webhostapp.com/04DEKHTE_HI_DEKHTE.mp3" ,
                    "05MERI DUNIYA MEIN" : "https://drj1.000webhostapp.com/05MERI_DUNIYA_MEIN.mp3" ,
                    "BOOMBARA" : "https://drj1.000webhostapp.com/06ZOOM_BOOMBARA.mp3" ,
                    "07DAAROO VICH PYAAR" : "https://drj1.000webhostapp.com/07DAAROO_VICH_PYAAR.mp3" ,
                    "BIN" : "https://drj1.000webhostapp.com/08TUM_BIN.mp3" ,
                    "RU" : "https://drj1.000webhostapp.com/09SURU_RU.mp3" ,
                    "10CHHOTI CHHOTI RAATEIN PART2" : "https://drj1.000webhostapp.com/10CHHOTI_CHHOTI_RAATEIN_PART2.mp3" ,
                    "11PYAAR HUM KO HONE LAGA" : "https://drj1.000webhostapp.com/11PYAAR_HUM_KO_HONE_LAGA.mp3" ,
                    "12MERI DUNIYA MEIN" : "https://drj1.000webhostapp.com/12MERI_DUNIYA_MEIN.mp3" ,
                    "O...Saya - www.Songs.PK" : "https://drj1.000webhostapp.com/01_O.._SAYA.mp3" ,
                    "Riots - www.Songs.PK" : "https://drj1.000webhostapp.com/02_RIOTS.mp3" ,
                    "Mausam & Escape - www.Songs.PK" : "https://drj1.000webhostapp.com/03_MAUSAM_&_ESCAPE.mp3" ,
                    "Paper Planes - www.Songs.PK" : "https://drj1.000webhostapp.com/04_PAPER_PLANES.mp3" ,
                    "Paper Planes (DFA Remix) - www.Songs.PK" : "https://drj1.000webhostapp.com/05_PAPER_PLANES_REMIX.mp3" ,
                    "Ringa Ringa - www.Songs.PK" : "https://drj1.000webhostapp.com/06_RINGA_RINGA.mp3" ,
                    "Liquid Dance - www.Songs.PK" : "https://drj1.000webhostapp.com/07_LIQUID_A_THEME.mp3" ,
                    "Latika's Theme - www.Songs.PK" : "https://drj1.000webhostapp.com/08_LATIKA_S_THEME.mp3" ,
                    "Aaj Ki Raat - www.Songs.PK" : "https://drj1.000webhostapp.com/09_AAJ_KI_RAAT.mp3" ,
                    "Millionaire - www.Songs.PK" : "https://drj1.000webhostapp.com/10_MILLIONAIRE.mp3" ,
                    "Gangsta Blues - www.Songs.PK" : "https://drj1.000webhostapp.com/11_GANGSTA_BLUE.mp3" ,
                    "Dreams On Fire - www.Songs.PK" : "https://drj1.000webhostapp.com/12_DREAMS_ON_FIRE.mp3" ,
                    "Jai Ho - www.Songs.PK" : "https://drj1.000webhostapp.com/13_JAI_HO.mp3" ,
                    "Aakhnkho Mein Jal Raha Hai" : "https://drj1.000webhostapp.com/Aakhnkho_Mein_Jal_Raha_Hai.mp3" ,
                    "Din Kuch Aise Guzarta" : "https://drj1.000webhostapp.com/Din_Kuch_Aise_Guzarta.mp3" ,
                    "Ek Parvaz Dikhayi Di Hai" : "https://drj1.000webhostapp.com/Ek_Parvaz_Dikhayi_Di_Hai.mp3" ,
                    "Speaks" : "https://drj1.000webhostapp.com/Guljar_Speaks.mp3" ,
                    "Speeak" : "https://drj1.000webhostapp.com/Guljar_Speeak.mp3" ,
                    "Speaks" : "https://drj1.000webhostapp.com/Gulzaar_Speaks.mp3" ,
                    "Haat Chhute bhi To" : "https://drj1.000webhostapp.com/Haat_Chhute_bhi_To_.mp3" ,
                    "Ik Purana Mausam Lauta" : "https://drj1.000webhostapp.com/Ik_Purana_Mausam_Lauta.mp3" ,
                    "Shaam Se aankhmein Nami Si ha" : "https://drj1.000webhostapp.com/Shaam_Se_aankhmein_Nami_Si_hai.mp3" ,
                    "Woh Khat Ke Purze Uda Rahatha" : "https://drj1.000webhostapp.com/Woh_Khat_Ke_Purze_Uda_Rahatha.mp3" ,
                    "Zindage yun Hui Basar Tanha" : "https://drj1.000webhostapp.com/Zindage_yun_Hui_Basar_Tanha.mp3" ,
                    "01 TOH PHIR AAO MUSTAFA ZAHID" : "https://drj1.000webhostapp.com/01_TOH_PHIR_AAO_MUSTAFA_ZAHID.mp3" ,
                    "01 ZARA SA" : "https://drj1.000webhostapp.com/01_ZARA_SA.mp3" ,
                    "01Kya Mujhe Pyaar Hai" : "https://drj1.000webhostapp.com/01Kya_Mujhe_Pyaar_Hai.mp3" ,
                    "01Teri Yaadon Mein" : "https://drj1.000webhostapp.com/01Teri_Yaadon_Mein.mp3" ,
                    "01Tu Hi Meri Shab Hai" : "https://drj1.000webhostapp.com/01Tu_Hi_Meri_Shab_Hai.mp3" ,
                    "Aadat" : "https://drj1.000webhostapp.com/02_Aadat.mp3" ,
                    "JUDAI" : "https://drj1.000webhostapp.com/02_JUDAI.mp3" ,
                    "Track 2" : "https://drj1.000webhostapp.com/02_MERE_HATH_MEIN.mp3" ,
                    "02 PEHLI NAZAR MEIN" : "https://drj1.000webhostapp.com/02_PEHLI_NAZAR_MEIN.mp3" ,
                    "02 TERA MERA RISHTA MUSTAFA Z" : "https://drj1.000webhostapp.com/02_TERA_MERA_RISHTA_MUSTAFA_ZAHID.mp3" ,
                    "Tu Meri Dost Hain - Songs.PK" : "https://drj1.000webhostapp.com/02_TU_MERI_DOST_HAI.mp3" ,
                    "Bheegi" : "https://drj1.000webhostapp.com/02Bheegi_Bheegi.mp3" ,
                    "02ChalChale" : "https://drj1.000webhostapp.com/02ChalChale.mp3" ,
                    "Bin" : "https://drj1.000webhostapp.com/02Tere_Bin.mp3" ,
                    "03 JAANE TU MERA KYA HAI" : "https://drj1.000webhostapp.com/03_JAANE_TU_MERA_KYA_HAI.mp3" ,
                    "Track 3" : "https://drj1.000webhostapp.com/03_MAIN_JAHAAN_RAHOON_RAHAT_FATEH.mp3" ,
                    "03Tu Jo Nahin" : "https://drj1.000webhostapp.com/03Tu_Jo_Nahin.mp3" ,
                    "Track 4" : "https://drj1.000webhostapp.com/04_YAHI_HOTA_PYAAR.mp3" ,
                    "9. TU MERI JAAN HAIN" : "https://drj1.000webhostapp.com/9._TU_MERI_JAAN_HAIN.mp3" ,
                    "a01 ek din teri" : "https://drj1.000webhostapp.com/a01_ek_din_teri.mp3" ,
                    "Track 04" : "https://drj1.000webhostapp.com/KYA_PYAR_KAROGE_04.mp3" ,
                    "01. KYON KI ITNA PYAR" : "https://drj1.000webhostapp.com/01._KYON_KI_ITNA_PYAR.mp3" ,
                    "thoda sa pyaar hua" : "https://drj1.000webhostapp.com/01Thoda_sa_pyar_hua_hai.mp3" ,
                    "EK LADKI KO DEKHA TO" : "https://drj1.000webhostapp.com/03_EK_LADKI_KO_DEKHA_TO_.mp3" ,
                    "03. DIL KE BADLE SANAM" : "https://drj1.000webhostapp.com/03._DIL_KE_BADLE_SANAM.mp3" ,
                    "Jugni" : "https://drj1.000webhostapp.com/09Jugni.mp3" ,
                    "Aa Bhi Ja Aa" : "https://drj1.000webhostapp.com/Aa_Bhi_Ja_Aa.mp3" ,
                    "aadat" : "https://drj1.000webhostapp.com/aadat.mp3" ,
                    "Track 01" : "https://drj1.000webhostapp.com/Andekhi_anjaani.mp3" ,
                    "Kuch Is Tarah (Mp3HunGama.Com)" : "https://drj1.000webhostapp.com/Atif_Aslam_-_Kuch_Is_Tarah.mp3" ,
                    "Track 12" : "https://drj1.000webhostapp.com/Bahut_Pyar_Karte_Hain.mp3" ,
                    "Dekho Maine Dekha" : "https://drj1.000webhostapp.com/Best_Love_Songs_Compilation_Vol3_1980_-_1995_-_Love_Story_-_Dekho_Maine_Dekha.mp3" ,
                    "chaha hai tujhko" : "https://drj1.000webhostapp.com/Chaha_hai_tujhko.mp3" ,
                    "Chalo Tumko Lekar Chale @ Mp3Hungama.com" : "https://drj1.000webhostapp.com/Chalo_Tumko_Lekar_Chale__Mp3Hungama.com_.mp3" ,
                    "choti choti raatein" : "https://drj1.000webhostapp.com/choti_raatein.mp3" ,
                    "Tere Bin - Rabbi Shergill" : "https://drj1.000webhostapp.com/dehli_heights2_www.songs.pk_.mp3" ,
                    "DEKHA TUJHE TO" : "https://drj1.000webhostapp.com/dekha_tujhe_toh.mp3" ,
                    "03 dil de diya hai" : "https://drj1.000webhostapp.com/Dil_de_diya_hai.mp3" ,
                    "dil..." : "https://drj1.000webhostapp.com/diwana_dil....mp3" ,
                    "Track 1" : "https://drj1.000webhostapp.com/Do_Dil_Mil_Rahe_Hai__1_.mp3" ,
                    "HUM DUM SUNIYO RE                              " : "https://drj1.000webhostapp.com/HUM_DUM_SUNIYO_RE_________________________.mp3" ,
                    "HUM HAIN RAHI PYAR KE - KASH" : "https://drj1.000webhostapp.com/HUM_HAIN_RAHI_PYAR_KE_-_KASH_KOI_LADKA_-_K_SANU_&_ALKA_MP5.mp3" ,
                    "HUM HAIN RAHI PYAR KE - WOH M" : "https://drj1.000webhostapp.com/HUM_HAIN_RAHI_PYAR_KE_-_WOH_MERI_NEEND_-_SADHNA_MP5.mp3" ,
                    "humko sirf tumse pyaar..." : "https://drj1.000webhostapp.com/humko_sirf_tumse_pyaar....mp3" ,
                    "INTEHA HO GAYI INTEZAAR KI" : "https://drj1.000webhostapp.com/imtehan_ho_gayi.mp3" ,
                    "1Is tarah aashiqi ka" : "https://drj1.000webhostapp.com/Is_tarah_aashiqi_ka_.mp3" ,
                    "Dil To Bachcha Hai - www.Songs.PK" : "https://drj1.000webhostapp.com/ishqiya01_www.songs.pk_.mp3" ,
                    "Track 01" : "https://drj1.000webhostapp.com/JAADU_HAI_NASHA_HAI.mp3" ,
                    "Tera Saath Hai Kitna Pyara" : "https://drj1.000webhostapp.com/JAANBA~1.mp3" ,
                    "Jadu hai Nasha Hai @ Mp3Hungama.com" : "https://drj1.000webhostapp.com/Jadu_hai_Nasha_Hai__Mp3Hungama.com_.mp3" ,
                    "Track 05" : "https://drj1.000webhostapp.com/Jeeye_To_Jeeye_Kaise.mp3" ,
                    "Pehla Nasha" : "https://drj1.000webhostapp.com/Jo_Jeeta_Wohi_Sikandar_Pehla_Nasha.mp3" ,
                    "11 kyon kisi ko" : "https://drj1.000webhostapp.com/kyon_kisi_ko_.mp3" ,
                    "kyon ke itna pyar " : "https://drj1.000webhostapp.com/kyun_itna_pyar_tumse.mp3" ,
                    "Leja Leja" : "https://drj1.000webhostapp.com/leja_re-ustad_and_.....mp3" ,
                    "Main Jahaan Rahoon" : "https://drj1.000webhostapp.com/Main_Jahaan_Rahoon_-_Rahat_Fateh_Ali_Khan_And_Krishna.mp3" ,
                    "Mauja Hi Mauja - [Songs.PK]" : "https://drj1.000webhostapp.com/Mauja_hi_mauja.mp3" ,
                    "Maula Mere Le Le Meri Jaan - [Songs.PK]" : "https://drj1.000webhostapp.com/Maula_Mere_Le_Le_Meri_Jaan.mp3" ,
                    "Maula Mere Maula" : "https://drj1.000webhostapp.com/Maula_Mere_Maularoop_Kumar_Rathod.mp3" ,
                    "MERA DIL BHI KITNA - K SANU &" : "https://drj1.000webhostapp.com/Mera_Dil_Bhi_Kitna_Pagal_Hain.mp3" ,
                    "MITRAN DI CHHATRI" : "https://drj1.000webhostapp.com/Mitra_Ki_Chatri.mp3" ,
                    "pehla nasha" : "https://drj1.000webhostapp.com/pehla_nasha.mp3" ,
                    "PYAR SE MERI TARAF" : "https://drj1.000webhostapp.com/Pyar_se_meri_taraf.mp3" ,
                    "Behene De - www.Songs.PK" : "https://drj1.000webhostapp.com/raavan02_www.songs.pk_.mp3" ,
                    "Bulla Ki Jaana" : "https://drj1.000webhostapp.com/Rabbi-BullaKi.mp3" ,
                    "Jaane Kaise - Songs.PK" : "https://drj1.000webhostapp.com/raqeeb01_www.songs.pk_.mp3" ,
                    "Bluffmaster (2005) - 04 - Right Here Right Now" : "https://drj1.000webhostapp.com/Right_Here_Right_Now.mp3" ,
                    "Saagar Jaise Ankhon" : "https://drj1.000webhostapp.com/Saagar_Jaise_Ankhon_Wali.mp3" ,
                    "BUHUT PYAR KARTE" : "https://drj1.000webhostapp.com/saajan_bahu_t_pyar_karte_hai.mp3" ,
                    "Musafirak13" : "https://drj1.000webhostapp.com/Saaki_Musafir.mp3" ,
                    "SUCH KEH RAHA HAI" : "https://drj1.000webhostapp.com/SUCH_KEH_RAHA_HAI.mp3" ,
                    "tera chehra" : "https://drj1.000webhostapp.com/tera_chehra-adnan_sami.mp3" ,
                    "Tere Bin " : "https://drj1.000webhostapp.com/Tere_Bin_.mp3" ,
                    "Track  1" : "https://drj1.000webhostapp.com/to_fir_aayo.mp3" ,
                    "Tumse Milna" : "https://drj1.000webhostapp.com/tumse_milna.mp3" ,
                    "Tune Jo Na Kaha - www.Songs.PK" : "https://drj1.000webhostapp.com/Tune_Jo_Na_Kaha.mp3" ,
                    "Woh Pehli Baar" : "https://drj1.000webhostapp.com/Woh_Pehli_Baar.mp3" ,
                    "Ya Rabba [DJLUV]" : "https://drj1.000webhostapp.com/ya_rabba_-_kailash_kher.mp3" ,
                    "zara zara" : "https://drj1.000webhostapp.com/Zara_zara.mp3" ,
                    "Zindagi Bangae Ho Tum" : "https://drj1.000webhostapp.com/ZINDIGI_BAN_GAYE_HO_TUM.mp3" ,
                    "Aaj Kal Tere Mere Pyar Ke" : "https://drj1.000webhostapp.com/01_Aaj_Kal_Tere_Mere_Pyar_Ke.mp3" ,
                    "Main Shair To Nahin" : "https://drj1.000webhostapp.com/01_Main_Shair_To_Nahin__Papuyaar.com_.mp3" ,
                    "Chabi Kho Jaye" : "https://drj1.000webhostapp.com/02_Chabi_Kho_Jaye__Papuyaar.com_.mp3" ,
                    "Akele hain chale aao" : "https://drj1.000webhostapp.com/Akele_Hain_Chale_Aao.mp3" ,
                    "An Evening In Paris" : "https://drj1.000webhostapp.com/an_evening_in_paris.mp3" ,
                    "Mere Man Ki Ganga - www.songs.pk" : "https://drj1.000webhostapp.com/bol_radha_bol.mp3" ,
                    "Chithi Aai Hai - Pankaj Udhas" : "https://drj1.000webhostapp.com/Chithi_Aai_Hai_-_Pankaj_Udhas.mp3" ,
                    "DIl KI Aawaz Bhi Sun" : "https://drj1.000webhostapp.com/Dil_Ki_Aawaz_Bhi_Sun.mp3" ,
                    "Dost Dost Na Raha -www.songs.pk" : "https://drj1.000webhostapp.com/dost_dost_na_raha.mp3" ,
                    "Duniya Na Bhaaye - Basant Bahaar 1956 - Mohammed Rafi" : "https://drj1.000webhostapp.com/DuniyaNaBhaaye-BasantBahaar.mp3" ,
                    "hai preet jahan ki reet" : "https://drj1.000webhostapp.com/Hai_Preet_Jahan_Ki_Reet___Fmw11.com.mp3" ,
                    "hamne jafa na sikhi" : "https://drj1.000webhostapp.com/Hamne_Jafa_Na_Ki_Thi.mp3" ,
                    "Har Dil Jo Pyar Karega - www.songs.pk" : "https://drj1.000webhostapp.com/har_dil_jo_pyar_karega.mp3" ,
                    "Hum Bewafa Hargiz Na The" : "https://drj1.000webhostapp.com/Hum_Bewafa_Hargiz_Na_The_-_Kishore_Kumar_-_Shaalimaar.mp3" ,
                    "Hum Tum Se Judaa Ho Ke" : "https://drj1.000webhostapp.com/Hum_Tum_Se_Judaa_Ho_Ke.mp3" ,
                    "huye hum jin ke liye" : "https://drj1.000webhostapp.com/Huye_Hum_Jinke_Liye_Barbad.mp3" ,
                    "Kasie Kahin Hum" : "https://drj1.000webhostapp.com/Kasie_Kahin_Hum.mp3" ,
                    "kya hua tera wada" : "https://drj1.000webhostapp.com/kya_hua_tera_wada.mp3" ,
                    "Suhana Safar Aur Yeh" : "https://drj1.000webhostapp.com/Madhumati_Suhana_Safar_Aur_Yeh.mp3" ,
                    "MANZILEN APNI JAGAH" : "https://drj1.000webhostapp.com/MANZILEN_APNI_JAGAH.mp3" ,
                    "Huzur Is Kadar" : "https://drj1.000webhostapp.com/Masoom_Huzur_Is_Kadar.mp3" ,
                    "Mere Dosti Mera Pyar" : "https://drj1.000webhostapp.com/Mere_Dosti_Mera_Pyar.mp3" ,
                    "Milan (1965) - Aaj Dil Pe Koi" : "https://drj1.000webhostapp.com/Milan__1965__-_Aaj_Dil_Pe_Koi___Mp3HunGama.Com.mp3" ,
                    "Nain Lad Jai Hai [From Ganga Jumna]" : "https://drj1.000webhostapp.com/23_nain_lad_jai_hai_to_manwa_ma_.mp3" ,
                    "Aaj Mausam Bada Be-Iman Hai [From Loafer]" : "https://drj1.000webhostapp.com/16_Aaj_mausam_bada_be-iman_hai.mp3" ,
                    "khuda" : "https://drj1.000webhostapp.com/02Affoo_khuda.mp3" ,
                    "Akele hain chale aao{Rafi}" : "https://drj1.000webhostapp.com/03Akele_hain_chale_aao.mp3" ,
                    "Ek tha gul aur ek thi bulbul" : "https://drj1.000webhostapp.com/05Ek_tha_gul_aur_ek_thi_bulbul.mp3" ,
                    "Mujhe Buddah Mil Gaya -www.songs.pk" : "https://drj1.000webhostapp.com/mujhe_buddha_mil_gaya.mp3" ,
                    "Mujhe Ishq Hai Tujhe Se" : "https://drj1.000webhostapp.com/Mujhe_Ishq_Hai_Tujhe_Se___Mp3HunGama.Com.mp3" ,
                    "O Meri Sharmilee" : "https://drj1.000webhostapp.com/O_Meri_Sharmilee___Mp3HunGama.Com.mp3" ,
                    "Aye Meri Zohra Jabeen" : "https://drj1.000webhostapp.com/Aye_Meri_Zohra_Jabeen_-_Waqt.mp3" ,
                    "Aye Mere pyare watan" : "https://drj1.000webhostapp.com/Aye_Mere_Pyare_Watan_-_Kabuliwala.mp3" ,
                    "Tu pyar ka sagar hai" : "https://drj1.000webhostapp.com/Tu_Pyar_Ka_Sagar_Hai_-_Seema.mp3" ,
                    "Zindagi Ki Na Toote" : "https://drj1.000webhostapp.com/002_Kranti_-_Zindagi_Ki_Na_Toote.mp3" ,
                    "Zihale Masti" : "https://drj1.000webhostapp.com/004._Ghulami_-_Zihale_Masti.mp3" ,
                    "Jab Hum Jawan Honge" : "https://drj1.000webhostapp.com/006._Betaab_-_Jab_Hum_Jawan_Honge.mp3" ,
                    "Hum Bane Tum Bane" : "https://drj1.000webhostapp.com/008._Ek_Duuje_Ke_Liye_-_Hum_Bane_Tum_Bane.mp3" ,
                    "Chahe Lakh Tufan" : "https://drj1.000webhostapp.com/010._Pyar_Jhukta_Nahin_-_Chahe_Lakh_Tufan.mp3" ,
                    "Dekho Maine Dekha" : "https://drj1.000webhostapp.com/012._Love_Story_-_Dekho_Maine_Dekha.mp3" ,
                    "Hum Tum Dono Milke" : "https://drj1.000webhostapp.com/014._Lava_-_Hum_Tum_Dono_Milke.mp3" ,
                    "Mere Pyar Ki Umar" : "https://drj1.000webhostapp.com/016_Waaris_-_Mere_Pyar_Ki_Umar.mp3" ,
                    "Teri Yaad Aayee" : "https://drj1.000webhostapp.com/018_Love_Story_-_Teri_Yaad_Aayee.mp3" ,
                    "Pyaar Kiya Nahin Jata" : "https://drj1.000webhostapp.com/022._Woh_7_Din_-_Pyaar_Kiya_Nahin_Jata.mp3" ,
                    "Aankhon Mein Kajal Hai" : "https://drj1.000webhostapp.com/024_Doosra_Aadmi_-_Aankhon_Mein_Kajal_Hai.mp3" ,
                    "Mera Pyar Bhi Tu Hai - Saathi" : "https://drj1.000webhostapp.com/025_SAATHI_-_MERA_PYAR_BHI_TU_HAI.mp3" ,
                    "Bhanvare Ne Khilaya" : "https://drj1.000webhostapp.com/026_Prem_Rog_-_Bhanvare_Ne_Khilaya.mp3" ,
                    "Mere Saathi Jivan Saathi" : "https://drj1.000webhostapp.com/028_Baazi_-_Mere_Saathi_Jivan_Saathi.mp3" ,
                    "Kya Khoob Lagti Ho - Dharmatma" : "https://drj1.000webhostapp.com/029_Kya_khoob_lagti_ho.mp3" ,
                    "Humrahi Mere Humrahi" : "https://drj1.000webhostapp.com/030_Do_Dilon_Ki_Dastan_-_Humrahi_Mere_Humrahi.mp3" ,
                    "Janam Janam Ka Saath" : "https://drj1.000webhostapp.com/032._Bheegi_Palken_-_Janam_Janam_Ka_Saath.mp3" ,
                    "Hum To Tere Aashiq - Farz" : "https://drj1.000webhostapp.com/074_Hum_To_Tere_Aashiq_Hain.mp3" ,
                    "Paani Re Paani - Shor" : "https://drj1.000webhostapp.com/083_Paani_Re_Paani.mp3" ,
                    "Main Hoon Pyar Tera [Teesri Manzil]" : "https://drj1.000webhostapp.com/087_Aaja_Aaja_Main_Hoon_Pyar_Tera.mp3" ,
                    "Phool Tumhe Bheja" : "https://drj1.000webhostapp.com/Phool_Tumhe_Bheja___Mp3HunGama.com.mp3" ,
                    "hum tumhe chahte hain" : "https://drj1.000webhostapp.com/Qurbani-HumTumheChahteHainAise.mp3" ,
                    "Jeevan Se Bhari Teri" : "https://drj1.000webhostapp.com/Safar_Jeevan_Se_Bhari_Teri.mp3" ,
                    "Jo Tumko Ho Pasand" : "https://drj1.000webhostapp.com/Safar_Jo_Tumko_Ho_Pasand.mp3" ,
                    "Sau Baar Janam Leinge" : "https://drj1.000webhostapp.com/Sau_Baar_Janam_Leinge.mp3" ,
                    "TU PYAR KA SAGAR HAI" : "https://drj1.000webhostapp.com/TU_PYAR_KA_SAGAR_HAI.mp3" ,
                    "Dil Cheez Kya Hai" : "https://drj1.000webhostapp.com/Umrao_Jaan_Dil_Cheez_Kya_Hai.mp3" ,
                    "Wada Karo" : "https://drj1.000webhostapp.com/Waada_Karon_Ki_Tum_Nahi.mp3" ,
                    "Wadiyan Mera Daman [From Abhilasha]" : "https://drj1.000webhostapp.com/Wadiyan_Mera_Daman.mp3" ,
                    "Yaad na jaye" : "https://drj1.000webhostapp.com/Yaad_Na_Jaaye.mp3" ,
                    "yaadon ki baarat nikli hai" : "https://drj1.000webhostapp.com/yadoon_ki_barat.mp3" ,
                    "Yeh Mera Prem Patra - www.songs.pk" : "https://drj1.000webhostapp.com/ye_mera_prem_patra.mp3" ,
                    "YEH DIL NA HOTA BECHARA  " : "https://drj1.000webhostapp.com/YEH_DIL_NA_HOTA_BECHARA__.mp3" ,
                    "Track 01" : "https://drj1.000webhostapp.com/01_-_ishqey_di_maar.mp3" ,
                    "01SAJJAN RUS GAYE" : "https://drj1.000webhostapp.com/01SAJJAN_RUS_GAYE.mp3" ,
                    "02 botalan sharab diyan" : "https://drj1.000webhostapp.com/02_botalan_sharab_diyan_.mp3" ,
                    "02 mundiya tu bach ke" : "https://drj1.000webhostapp.com/02_mundiya_tu_bach_ke_.mp3" ,
                    "Mehfil" : "https://drj1.000webhostapp.com/08_Mehfil.mp3" ,
                    "Ae Jo Seeli Seeli Aundi Ae Hawa" : "https://drj1.000webhostapp.com/1naseebo5_www.songs..mp3" ,
                    "ik aisi ladki thi" : "https://drj1.000webhostapp.com/2_mp3pk.com_.mp3" ,
                    "KOI" : "https://drj1.000webhostapp.com/2__KOI_AAYA_APNA_KAM_CHHODKE.mp3" ,
                    "3 DHOL NEW" : "https://drj1.000webhostapp.com/2_YE_CHHORI_MARENGI.mp3" ,
                    "Track 1" : "https://drj1.000webhostapp.com/de_de_geda.mp3" ,
                    "Dil Ta Pagal" : "https://drj1.000webhostapp.com/dil_ta_pagal_hai.mp3" ,
                    "01_ISHQE_DI_MAAR" : "https://drj1.000webhostapp.com/Dj_songs_-_01_ISHQE_DI_MAAR.mp3" ,
                    "01" : "https://drj1.000webhostapp.com/mitra_di_chhatri_to.mp3" ,
                    "NAAG JAZZY B" : "https://drj1.000webhostapp.com/NAAG_JAZZY_B.mp3" ,
                    "SAPNE MAIN MILTE HAIN SATYA" : "https://drj1.000webhostapp.com/SAPNE_MAIN_MILTE_HAIN_SATYA.mp3" ,
                    "Tum Saath Ho - Songspk.LINK" : "https://drj1.000webhostapp.com/03_-_Tamasha_-_Tum_Saath_Ho__Songspk.LINK_.mp3" ,
                    "Boond Boond - MyMp3Song.com" : "https://drj1.000webhostapp.com/04_-_Boond_Boond_MyMp3Song.mp3" ,
                    "12 Saal (DjPunjab.CoM)" : "https://drj1.000webhostapp.com/12_Saal_-_www.DjPunjab.Com.mp3" ,
                    "Aise Na Mujhe Tum Dekho (Armaan Malik) Full Song" : "https://drj1.000webhostapp.com/Aise_Na_Mujhe_Tum_Dekho__Armaan_Malik__Full_Song.mp3" ,
                    "Mere Sapno Ki Rani Kab - www.hotmentos.com" : "https://drj1.000webhostapp.com/Aradhana-Mere_Sapno_Ki_Rani_Kab.mp3" ,
                    "Att Goriye" : "https://drj1.000webhostapp.com/Att_Goriye-_RaagJatt.mp3" ,
                    "Jaguar (feat. Bohemia) (DJJOhAL.Com)" : "https://drj1.000webhostapp.com/AUD-20150220-WA0001.mp3" ,
                    "Baliye (Laung Gawacha) (Mr-Jatt.com)" : "https://drj1.000webhostapp.com/Baliye__Laung_Gawacha_-_Mr-Jatt.com_.mp3" ,
                    "Bapu Zimidar (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Bapu_Zimidar-Jassi_Gill_www.Mp3MaD.Com_.mp3" ,
                    "BILAL SAEED -ADHI ADHI RAAT (DjPunjab.CoM)" : "https://drj1.000webhostapp.com/BILAL_SAEED_-ADHI_ADHI_RAAT__DjPunjab.Com_.mp3" ,
                    "2 Number" : "https://drj1.000webhostapp.com/Bilal_Saeed-2_Number.mp3" ,
                    "Black Suit (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Black_Suit-Preet_Harpal-www.Mp3Mad.Com.mp3" ,
                    "Blow (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Blow-Kesha_www.mp3" ,
                    "Bolo Har Har Har (Mr-Jatt.com)" : "https://drj1.000webhostapp.com/Bolo_Har_Har_Har-_Mr-Jatt.com_.mp3" ,
                    "Breakup Party - Yo Yo Honey Singh (Ft. Leo) - ApnaFunz.Com" : "https://drj1.000webhostapp.com/Breakup_Party_-_Yo_Yo_Honey_Singh_Ft.mp3" ,
                    "Brown Boi (feat. Bling Singh)" : "https://drj1.000webhostapp.com/Brown_Boi__feat._Bling_Singh_-_RaagJatt.com_.mp3" ,
                    "Chupke Se - Saathiya (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Chupke_Se_-_Saathiya-Various_www.mp3" ,
                    "Chura Liya Hai Tumne Jo Dil Ko (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/chura_liya.mp3" ,
                    "Dil Cheez Tujhe Dedi(Mr-Jatt.com)" : "https://drj1.000webhostapp.com/Dil_Cheez_Tujhe_Dedi-_Mr-Jatt.com_.mp3" ,
                    "Halka Halka Suroor (Nusrat Fateh Ali Khan Cover)" : "https://drj1.000webhostapp.com/farhan-saeed-halka-halka-suroor-koolmuzone.mp3" ,
                    "Ford V s Ford (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Ford_V_s_Ford-Shivjot_www.mp3" ,
                    "Ambarsariya - www.DJMaza.Com" : "https://drj1.000webhostapp.com/Fukrey_-_Ambarsariya__DJMaza_.mp3" ,
                    "Horn Blow (RaagJatt.Com)" : "https://drj1.000webhostapp.com/Horn_Blow__RaagJatt.com_.mp3" ,
                    "Hulara (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Hulara-J_Star_www.mp3" ,
                    "Jatt Sikka (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Jatt_Sikka-Sheera_Jasvir_www.mp3" ,
                    "Jugni @ Mp3HunGama.Com" : "https://drj1.000webhostapp.com/Jugni___Mp3HunGama.Com.mp3" ,
                    "Jutti Kasuri - iPendu.com" : "https://drj1.000webhostapp.com/Jutti_Kasuri-Harshdeep_Kaur_iPendu.com_.mp3" ,
                    "Khaab(Mr-Jatt.com)" : "https://drj1.000webhostapp.com/Khaab-_Mr-Jatt.com_.mp3" ,
                    " (DJJOhAL.Com)" : "https://drj1.000webhostapp.com/Laden_-_Jassi_Gill___DJOJ_.mp3" ,
                    "Laung Gawacha (Mr-Jatt.com)" : "https://drj1.000webhostapp.com/Laung_Gawacha-_Mr-Jatt.com_.mp3" ,
                    "Look    ::www.RAAG.ME::" : "https://drj1.000webhostapp.com/Look-Roshan_Prince__Raag.Me__.mp3" ,
                    "Mainu Single Rehna - PagalWorld.com" : "https://drj1.000webhostapp.com/Mainu_Single_Rehna__Dr_Zeus_Rajveer_n_Fateh__320Kbps.mp3" ,
                    "Mere Mehboob Qayamat Hogi (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Mere_Mehboob_Qayamat_Hogi-Kishore_Kumar_www.mp3" ,
                    "Munda Iphone Warga (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Munda_Iphone_Warga-A-Kay_www.Mp3MaD.Com_.mp3" ,
                    "O Re Piya" : "https://drj1.000webhostapp.com/o_re_piya.mp3" ,
                    "One Dream(Mr-Jatt.com)" : "https://drj1.000webhostapp.com/One_Dream-_Mr-Jatt.com_.mp3" ,
                    "Outfit - Guru Randhawa (RaagTune.Com)" : "https://drj1.000webhostapp.com/Outfit_320___Raag.Me__.mp3" ,
                    "Patola (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Patola-Guru_Randhawa-Bohemia-www.Mp3Mad.Com.mp3" ,
                    "Dilko - www.Songs.PK" : "https://drj1.000webhostapp.com/rhtdm02_www.songs.pk_.mp3" ,
                    "Roop Tera Mastana (Aradhana)    ::www.RAAG.ME::" : "https://drj1.000webhostapp.com/Roop_Tera_Mastana__Aradhana_-Kishore_Kumar__Raag.Me__.mp3" ,
                    "Sapna Jahan - MyMp3Song.Com" : "https://drj1.000webhostapp.com/Sapna_Jahan_MyMp3Song.Com_.mp3" ,
                    "tinka tinka" : "https://drj1.000webhostapp.com/Tinka_tinka.mp3" ,
                    "Tu Hai Ki Nahi [Mixmp3.In]" : "https://drj1.000webhostapp.com/Tu_Hai_Ki_Nahi_Roy_.mp3" ,
                    "Zara Zara" : "https://drj1.000webhostapp.com/Zara_Zara-Rahna_hai_tere_dil_mein_001.mp3" ,
                    "Zulfa - (Ft Dr.Zeus) (RoyalJatt.Com)" : "https://drj1.000webhostapp.com/Zulfa_-__Ft_Dr.Zeus_-Jaz_Dhami-www.Mp3Mad.Com.mp3" }


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    input_data = str(req.get("result").get("resolvedQuery"))
    choice_val = process.extract(input_data, choices, limit=1)
    choice_song_path = map_choices[choice_val]
    print(input_data)
    print(choice_val)
    data = input_data
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))

    speech = "Response is fantastic " 
    print("Response:")
    print(speech)

    return {
        "speech": data,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
