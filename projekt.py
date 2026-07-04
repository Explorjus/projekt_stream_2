import streamlit as st
import yt_dlp
import os

st.write("Witaj w yt_downloader")

link = st.text_input("Wklej link")

nazwa_pliku = None

if link:
    try:
        # Dodajemy udawanie przeglądarki już na etapie sprawdzania informacji
        opcje_info = {
            'extractor_args': {'youtube': {'player_client': ['web', 'ios']}},
            # 'cookiesfrombrowser': ('safari',), # Odkomentuj (usuń #) i zmień na 'chrome' lub 'firefox' jeśli to nie zadziała
        }
        with yt_dlp.YoutubeDL(opcje_info) as ydl:
            info = ydl.extract_info(link, download=False)
            tytul_filmu = info.get('title', 'video')
            # Usuwamy z tytułu znaki, które mogą psuć nazwy plików w systemie
            bezpieczny_tytul = "".join([c for c in tytul_filmu if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            nazwa_pliku = f"{bezpieczny_tytul}.mp4"
    except Exception as e:
        st.error(f"Nie udało się pobrać informacji o filmie: {e}")
        st.stop()

# Używamy st.session_state, żeby Streamlit pamiętał, że plik został już przygotowany
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
                # Drastyczna zmiana klientów + ignorowanie błędów certyfikatów
                'extractor_args': {'youtube': {'player_client': ['web', 'mweb', 'ios']}},
                'nocheckcertificate': True,
                # W razie ciągłego błędu 403, odkomentuj poniższą linię (usuń #):
                # 'cookiesfrombrowser': ('safari',), # wpisz tu przeglądarkę z której korzystasz np. 'chrome', 'firefox'
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

# Jeśli plik się pobrał na serwer, pokazujemy zielony przycisk do zapisu na dysku
if st.session_state.pobrane and nazwa_pliku and os.path.exists(nazwa_pliku):
    with open(nazwa_pliku, "rb") as file:
        kliknieto = st.download_button(
            label="Zapisz plik na swoim komputerze 📥",
            data=file.read(),
            file_name=nazwa_pliku,
            mime="video/mp4"
        )
        # Po kliknięciu przycisku przez użytkownika, sprzątamy plik
        if kliknieto:
            os.remove(nazwa_pliku)
            st.session_state.pobrane = False
            st.rerun()