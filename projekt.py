import streamlit as st
import yt_dlp
import os

st.write("Witaj w yt_downloader")

link = st.text_input("Wklej link")

nazwa_pliku = None

if link:
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(link, download=False)
            tytul_filmu = info.get('title', 'video')
            nazwa_pliku = f"{tytul_filmu}.mp4"
    except Exception as e:
        st.error(f"Nie udało się pobrać informacji o filmie: {e}")
        st.stop()

if st.button("Przygotuj film do pobrania"):
    if not link:
        st.warning("Wklej link najpierw")
    else:
        with st.spinner("Pobieranie i przygotowywanie"):
            ustawienia = {
                'format': 'best',
                'outtmpl': nazwa_pliku,
                'extractor_args': {'youtube': {'player_client': ['ios', 'web', 'android']}},
            }
            try:
                with yt_dlp.YoutubeDL(ustawienia) as pobieranie:
                    pobieranie.download([link])

                with open(nazwa_pliku, "rb") as file:
                    st.download_button(
                        label="Zapisz plik na swoim komputerze",
                        data=file.read(),
                        file_name=nazwa_pliku,
                        mime="video/mp4"
                    )
                st.success("Film jest gotowy")

                os.remove(nazwa_pliku)

            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")
                if nazwa_pliku and os.path.exists(nazwa_pliku):
                    os.remove(nazwa_pliku)
else:
    st.info("Wklej link")
