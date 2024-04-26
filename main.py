import streamlit as st
import pandas as pd
import numpy as np
import duckdb

st.set_page_config(
    page_title="Data Cloud Summit 2024",
    page_icon="❄",
    layout="wide",
    initial_sidebar_state="auto",
)

'Data Cloud Summit 24'
'### セッション検索アプリ❄️'
st.caption('''
セッションの日本語検索アプリ。  
時点データなので、実際のセッション時間等はリンク先を確認してください。
''')

df = pd.read_csv(r'./data_cloud_summit.csv')
en_toggle = st.sidebar.toggle('English')

if en_toggle:
    df = duckdb.sql(
        '''
        select
            code,
            title,
            session_type,
            session_tracks,
            -- strftime(date, '%Y-%m-%d') as date,
            date,
            time_from,
            time_to,
            right( '00' || hour_from || '時', 3) as hour_from,
            description,
            session_id,
            url
        from df
        order by date, time_from, session_tracks_ja
        '''
        ).df()
else:
    df = duckdb.sql(
        '''
        select
            code,
            title_ja as title,
            session_type,
            session_tracks_ja as session_tracks,
            -- strftime(date, '%Y-%m-%d') as date,
            date,
            time_from,
            time_to,
            right( '00' || hour_from || '時', 3) as hour_from,
            description_ja as description,
            session_id,
            url
        from df
        order by date, time_from, session_tracks_ja
        '''
        ).df()


st.sidebar.markdown('''
## 検索条件
プルダウン内に直接入力もできます。
''')
select_session_tracks = st.sidebar.selectbox(
    '分類',
    np.insert(df['session_tracks'].sort_values().unique(), 0, 'すべて'),
)
select_date = st.sidebar.selectbox(
    '日付',
    np.insert(df['date'].sort_values().unique(), 0, 'すべて'),
)
select_hour = st.sidebar.selectbox(
    '開始時間帯',
    np.insert(df['hour_from'].sort_values().unique(), 0, 'すべて'),
)
select_session_type = st.sidebar.selectbox(
    'セッション種別',
    np.insert(df['session_type'].sort_values().unique(), 0, 'すべて'),
)
input_search = st.sidebar.text_input(
    '検索',
    placeholder='Like'
)


if select_session_tracks != 'すべて':
    df = df[df["session_tracks"] == select_session_tracks]
if select_date != 'すべて':
    df = df[df["date"] == select_date]
if select_session_type != 'すべて':
    df = df[df["session_type"] == select_session_type]
if select_hour != 'すべて':
    df = df[df["hour_from"] == select_hour]
if input_search != '':
    cond_code = df["code"].str.contains(input_search, case=False)
    cond_title = df["title"].str.contains(input_search, case=False)
    cond_session_type = df["session_type"].str.contains(input_search, case=False)
    cond_session_tracks = df["session_tracks"].str.contains(input_search, case=False)
    cond_date = df["date"].str.contains(input_search, case=False)
    cond_description = df["description"].str.contains(input_search, case=False)
    cond = cond_code | cond_title | cond_session_type | cond_session_tracks | cond_date | cond_description
    df = df[cond]

st.sidebar.markdown(f'''
---
## 検索結果
### {df.shape[0]}件
''')

df_display = df[['code', 'title', 'session_type', 'session_tracks', 'date', 'time_from', 'time_to', 'description', 'url']]
st.dataframe(df_display,
            column_config={
                "code": st.column_config.Column(
                    "CODE",
                ),
                "title": st.column_config.Column(
                    "タイトル",
                ),
                "session_type": st.column_config.Column(
                    "セッション種別",
                ),
                "session_tracks": st.column_config.Column(
                    "分類",
                ),
                "date": st.column_config.DateColumn(
                    "日付",
                    format="MM/DD",
                ),
                "time_from": st.column_config.DatetimeColumn(
                    "開始時刻",
                    format="HH:mm",
                ),
                "time_to": st.column_config.DatetimeColumn(
                    "終了時刻",
                    format="HH:mm",
                ),
                "description": st.column_config.Column(
                    "説明",
                ),
                "url": st.column_config.LinkColumn(
                    "リンク",
                    display_text="❄️",
                ),
            },
             height=700,
             hide_index=True,
             )

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@100..900&display=swap" rel="stylesheet">
    <style>
    body,div,h1,h2,h3,h4,h5,p, input{
        font-family: "Noto Sans JP", "Segoe UI", "游ゴシック体", YuGothic, "游ゴシック Medium", "Yu Gothic Medium", sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
