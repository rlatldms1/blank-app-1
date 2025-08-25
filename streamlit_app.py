import streamlit as st
import requests

# 🔑 API 키 (OMDb만 필요)
OMDB_API_KEY = "여기에_OMDb_API_KEY"
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"

st.set_page_config(page_title="책 & 영화 검색 서비스", page_icon="📚🎬", layout="centered")

st.title("📚 책 & 🎬 영화 검색기")

query = st.text_input("🔎 책/영화 제목을 입력하세요")
search_type = st.radio("검색할 대상", ["책", "영화"])

if st.button("검색하기"):
    if search_type == "책":
        params = {"q": query, "maxResults": 1}
        res = requests.get(GOOGLE_BOOKS_API, params=params)
        data = res.json()

        if "items" in data:
            book = data["items"][0]["volumeInfo"]
            st.subheader(book.get("title", "제목 없음"))
            st.write("✍️ 저자:", ", ".join(book.get("authors", ["정보 없음"])))

            if "imageLinks" in book and "thumbnail" in book["imageLinks"]:
                st.image(book["imageLinks"]["thumbnail"], caption="책 표지")

            # 줄거리 접기
            raw_desc = book.get("description", "")
            with st.expander("📖 줄거리 더보기"):
                st.write(raw_desc if raw_desc else "줄거리 없음")

            if "infoLink" in book:
                st.markdown(f"[📕 책 구매/정보 링크]({book['infoLink']})")
        else:
            st.warning("검색 결과가 없습니다.")

    elif search_type == "영화":
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={query}"
        res = requests.get(url)
        data = res.json()

        if data.get("Response") == "True":
            st.subheader(data["Title"])
            st.write(f"📅 개봉년도: {data.get('Year', 'N/A')}")
            st.write(f"⭐ 평점: {data.get('imdbRating', 'N/A')}/10")

            if data.get("Poster") and data["Poster"] != "N/A":
                st.image(data["Poster"], caption="영화 포스터")

            # 줄거리 접기
            raw_plot = data.get("Plot", "")
            with st.expander("🎬 줄거리 더보기"):
                st.write(raw_plot if raw_plot else "줄거리 없음")

            st.markdown(f"[🎥 IMDb에서 보기](https://www.imdb.com/title/{data['imdbID']}/)")
        else:
            st.warning("검색 결과가 없습니다.")
