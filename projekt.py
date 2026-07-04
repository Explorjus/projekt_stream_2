import streamlit as st
import yt_dlp
import os

st.write("Witaj w yt_downloader")

link = st.text_input("Wklej link")

# Lista przeglądarek, które program przetestuje po kolei
LISTA_PRZEGLADAREK = ['chrome', 'safari', 'firefox', 'edge'] 

nazwa_pliku = None

# Zmienna pomocnicza, w której zapiszemy przeglądarkę, która zadziałała
if 'dzialajaca_przegladarka' not in st.session_state:
    st.session_state.dzialajaca_przegladarka = None

if link:
    info = None
    # Pętla for przechodzi po kolei przez każdą przeglądarkę z listy
    for przegladarka in LISTA_PRZEGLADAREK:
        try:
            opcje_info = {
                'extractor_args': {'youtube': {'player_client': ['web', 'ios']}},
                # Przekazujemy pojedynczy tekst w krotce, np. ('chrome',)
                'cookiesfrombrowser': (przegladarka,), 
            }
            with yt_dlp.YoutubeDL(opcje_info) as ydl:
                info = ydl.extract_info(link, download=False)
                tytul_filmu = info.get('title', 'video')
                bezpieczny_tytul = "".join([c for c in tytul_filmu if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                nazwa_pliku = f"{bezpieczny_tytul}.mp4"
                
                # Sukces! Zapisujemy, która przeglądarka zadziałała i przerywamy pętlę
                st.session_state.dzialajaca_przegladarka = przegladarka
                break
        except Exception:
            # Jeśli ta przeglądarka wywali błąd, ignorujemy go i pętla idzie do następnej
            continue

    # Jeśli pętla się skończyła, a zmienna 'info' dalej jest pusta, to znaczy że żadna przeglądarka nie zadziałała
    if not info:
        st.error("Nie udało się pobrać informacji o filmie. Żadna z przeglądarek nie dostarczyła poprawnych ciasteczek. Upewnij się, że jesteś zalogowany na YouTube w Chrome lub Safari.")
        st.stop()

if 'pobrane' not in st.session_state:
    st.session_state.pobrane = False

if st.button("Przygotuj film do pobrania"):
    if not link:
        st.warning("Wklej link najpierw")
    else:
        with st.spinner("Pobieranie i przygotowywanie... Może to chwilę potrwać."):
            # Używamy tej przeglądarki, która zadziałała w kroku powyżej
            uzyj_przegladarki = st.session_state.dzialajaca_przegladarka
            
            ustawienia = {
                'format': 'best',
                'outtmpl': nazwa_pliku,
                'extractor_args': {'youtube': {'player_client': ['web', 'mweb', 'ios']}},
                'nocheckcertificate': True,
                'cookiesfrombrowser': (uzyj_przegladarki,), 
            }
            try:
                with yt_dlp.YoutubeDL(ustawienia) as pobieranie:
                    pobieranie.download([link])
                st.session_state.pobrane = True
                st.success(f"Film przygotowany przy użyciu ciasteczek z: {uzyj_przegladarki}!")
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