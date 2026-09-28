import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

# 타이틀
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    "1년간 박스오피스 10위권에 든 영화(216편)의 데이터를 활용하여 장르별 분포와"
    " 다양한 관계를 시각화한 도감입니다."
)


# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
  url = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"
  df = pd.read_csv(url)

  # 장르 컬럼 전처리: 세로막대 기호(|)로 여러 개 적힌 경우 첫 번째 장르만 추출
  if "genre" in df.columns:
    df["genre"] = df["genre"].apply(
        lambda x: str(x).split("|")[0].strip() if pd.notnull(x) else "기타"
    )
  return df


# 데이터 불러오기
try:
  df = load_data()
except Exception as e:
  st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
  st.stop()

# 데이터 미리보기 (선택 사항)
with st.expander("원본 데이터 확인하기"):
  st.dataframe(df.head())

# --- 첫 번째 그래프: 장르별 영화 편수 도넛 그래프 ---
st.header("1. 장르별 영화 편수 분포")
st.markdown(
    "박스오피스 10위권에 든 영화들의 주요 장르별 편수와 전체 비율을"
    " 보여줍니다."
)

if "genre" in df.columns:
  genre_counts = df["genre"].value_counts().reset_index()
  genre_counts.columns = ["genre", "count"]

  # Plotly 도넛 그래프 생성
  fig_genre = px.pie(
      genre_counts,
      names="genre",
      values="count",
      hole=0.4,  # 도넛 형태 지정
      labels={"genre": "장르", "count": "편수"},
  )

  # 마우스 오버 시 편수와 비율이 명확히 보이도록 설정
  fig_genre.update_traces(
      textinfo="percent+label", hoverinfo="label+value+percent"
  )
  fig_genre.update_layout(margin=dict(t=30, b=30, l=30, r=30))

  st.plotly_chart(fig_genre, use_container_width=True)
else:
  st.warning("데이터에 'genre' 열이 존재하지 않습니다.")

# '이 그래프로 알 수 있는 것' 구역
st.markdown("---")
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "• 박스오피스 상위권에 진입하는 영화 중 가장 비중이 높은 주력 장르가"
    " 무엇인지 한눈에 파악할 수 있습니다.\n• 특정 장르가 시장에서"
    " 편중되어 있는지, 혹은 다양한 장르가 골고루 분포해 있는지 비율을 통해"
    " 확인할 수 있습니다."
)
