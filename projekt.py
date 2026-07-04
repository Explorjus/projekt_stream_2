import streamlit as st
import yt_dlp
import os

st.write("Witaj w yt_downloader")

link = st.text_input("Wklej link")

# !!! WYBIERZ SWOJĄ PRZEGLĄDARKĘ !!!
# Dostępne opcje: 'chrome', 'safari', 'firefox', 'edge', 'brave'
MOJA_PRZEGLADARKA = ['chrome', 'safari'] 

nazwa_pliku = None

if link:
    try:
        opcje_info = {
            'extractor_args': {'youtube': {'player_client': ['web', 'ios']}},
            # PRZEKAZUJEMY CIASTECZKA DO SPRAWDZENIA INFO
            'cookiesfrombrowser': (MOJA_PRZEGLADARKA,), 
        }
        with yt_dlp.YoutubeDL(opcje_info) as ydl:
            info = ydl.extract_info(link, download=False)
            tytul_filmu = info.get('title', 'video')
            bezpieczny_tytul = "".join([c for c in tytul_filmu if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            nazwa_pliku = f"{bezpieczny_tytul}.mp4"
    except Exception as e:
        st.error(f"Nie udało się pobrać informacji o filmie: {e}")
        st.stop()

if 'pobrane' not in st.session_state:
    st.session_state.pobrane = False

if st.button("Przygotuj film do pobrania"):
    if not link:
        st.warning("Wklej link najpierw")
    else:
        with st.spinner("Pobieranie i przygotowywanie... Może to chwilę potrwać."):
            ustawienia = {
                'format': 'best',
                'outtmpl': nazwa_pliku,
                'extractor_args': {'youtube': {'player_client': ['web', 'mweb', 'ios']}},
                'nocheckcertificate': True,
                # PRZEKAZUJEMY CIASTECZKA DO WŁAŚCIWEGO POBIERANIA
                'cookiesfrombrowser': (MOJA_PRZEGLADARKA,), 
            }
            try:
                with yt_dlp.YoutubeDL(ustawienia) as pobieranie:
                    pobieranie.download([link])
                st.session_state.pobrane = True
                st.success("Film jest gotowy do pobrania na Twój komputer!")
            except Exception as e:
                st.error(f"Wystąpił błąd podczas pobierania: {e}")
                st.session_state.pobrane = False
                if nazwa_pliku and os.path.exists(nazwa_pliku):
                    os.remove(nazwa_pliku)

if st.session_state.pobrane and nazwa_pliku and os.path.exists(nazwa_pliku):
    with open(nazwa_pliku, "rb") as file:
        kliknieto = st.download_button(
            label="Zapisz plik na swoim komputerze 📥",
            data=file.read(),
            file_name=nazwa_pliku,
            mime="video/mp4"
        )
        if kliknieto:
            os.remove(nazwa_pliku)
            st.session_state.pobrane = False
            st.rerun()