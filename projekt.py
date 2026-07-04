import streamlit as st
import yt_dlp
import os

st.write("Witaj w yt_downloader")
link = st.text_input("Wklej link")

if st.button("Pobierz film"):
    if link:
        st.write("Pobieranie...")
        ustawienia = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
        }

        try:
            with yt_dlp.YoutubeDL(ustawienia) as pobieranie:
                pobieranie.download([link])
            st.success("Film pobrano")
        except Exception as e:
            st.error(f"Wystąpił błąd: {str(e)}")
    else:
        st.warning("Wklej poprawny link")




