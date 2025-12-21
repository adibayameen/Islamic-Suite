import streamlit as st
import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from streamlit_geolocation import streamlit_geolocation
st.set_page_config(page_title="Islam Suite", layout="wide")

st.markdown("""
    <style>
    /* -------------------------------
    Google Fonts
    --------------------------------*/
    @import url('https://fonts.googleapis.com/css2?family=Hafs&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

    /* -------------------------------
    Global Font
    --------------------------------*/
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    /* -------------------------------
    SIDEBAR – SOFT NAVY
    --------------------------------*/
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0B3558,
            #0E4A6B,
            #11698E
        ) !important;

        border-right: 1px solid #7FB9D455;
        padding: 0px !important;
        color: #EAF4FB !important;
    }

    /* Sidebar Titles */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #EAF4FB !important;
        font-weight: 600;
    }

    /* Labels: Select a Feature / Choose Surah / Choose Reciter */
    [data-testid="stSidebar"] label {
        color: #D9ECF7 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        margin-bottom: 6px;
    }

    /* -------------------------------
    DROPDOWN (THEME MATCHED)
    --------------------------------*/
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background: #E3F0F8 !important;   /* light navy tint */
        border-radius: 10px !important;
        border: 1px solid #7FB9D4AA !important;
    }

    /* Dropdown Text */
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #0B3558 !important;
        font-weight: 500;
    }

    /* Hover / Focus */
    [data-testid="stSidebar"] [data-baseweb="select"]:hover {
        box-shadow: 0 0 0 1px #7FB9D4AA;
    }

    /* Dropdown menu (options list) */
    [data-testid="stSidebar"] ul {
        background: #D6EAF5 !important;
        border-radius: 10px;
    }

    [data-testid="stSidebar"] li {
        color: #0B3558 !important;
    }

    [data-testid="stSidebar"] li:hover {
        background: #BFDFF1 !important;
    }

    /* -------------------------------
    ARABIC TEXT
    --------------------------------*/
    .arabic-text {
        font-family: 'Hafs', serif !important;
        direction: rtl;
        background: #EDF6FC;
        padding: 18px;
        border-radius: 18px;
        font-size: 26px;
        color: #0B3558;
        line-height: 1.8;
        text-align: right;
    }

    /* -------------------------------
    URDU TEXT
    --------------------------------*/
    .urdu-text {
        font-family: 'Noto Nastaliq Urdu', serif !important;
        direction: rtl;
        background: #EDF6FC;
        padding: 18px;
        border-radius: 18px;
        font-size: 26px;
        color: #0B3558;
        line-height: 1.8;
        text-align: right;
    }

    /* -------------------------------
    ENGLISH TEXT
    --------------------------------*/
    .english-text {
        background: #EDF6FC;
        padding: 16px;
        border-radius: 14px;
        font-size: 18px;
        color: #0B3558;
        line-height: 1.6;
    }

    /* -------------------------------
    LAYOUT
    --------------------------------*/
    .block-container {
        padding-top: 1.5rem !important;
    }

    /* -------------------------------
    Audio Player
    --------------------------------*/
    audio {
        width: 100%;
        margin: 6px 0 16px 0;
    }
    /* ===============================
    DROPDOWN BOX (CLOSED STATE)
    =============================== */

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #CFE6F3 !important;   /* soft navy blue */
        border-radius: 10px !important;
        border: 1.5px solid #5FA3C6 !important;
    }

    /* Text inside dropdown box */
    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] div {
        color: #0B3558 !important;
        font-weight: 500 !important;
    }

    /* Hover effect */
    [data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
        background-color: #C3DFF0 !important;
    }

    /* Focus (when clicked) */
    [data-testid="stSidebar"] [data-baseweb="select"]:focus-within > div {
        box-shadow: 0 0 0 2px #5FA3C655 !important;
    }
    /* -------------------------------
   GET TAFSEER BUTTON (SIDEBAR)
    --------------------------------*/
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, #8ED1FC, #4DA3D9) !important;
        color: #0B3558 !important;
        border-radius: 14px !important;
        padding: 10px 22px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.18);
        transition: all 0.3s ease-in-out;
    }

    /* Hover */
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #4DA3D9, #1E88C8) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(0, 0, 0, 0.28);
    }

    /* Disabled state (image jaisa) */
    section[data-testid="stSidebar"] div.stButton > button:disabled {
        background: #E3F2FD !important;
        color: #90A4AE !important;
        box-shadow: none !important;
        cursor: not-allowed;
    }
    /* -------------------------------
    Full Surah / Ayah-wise Radio Buttons Box
    --------------------------------*/
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        background: #CFE6F3 !important;
        padding: 12px;
        border-radius: 12px;
        margin-top: 10px;
    }

    /* Text attempt (won't work due to inline style) */
    section[data-testid="stSidebar"] div[role="radiogroup"] div[class*="css"] span {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

 
    </style>
""", unsafe_allow_html=True)



def load_json(path):
    full_path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.exists(full_path):
        st.error(f"File not found: {path}")
        return {}
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)

st.title("Islam Suite")
st.sidebar.title(" Islam Suite Menu")


menu=st.sidebar.selectbox("Select a Feature",["Quran with Audio","Quran Tafseer","Hadiths","Duas","Kalimas","99 Names Of Allah","99 Names Of Prophet Muhammad","Prayer Time","Qibla Direction","Namaz Steps","Rakats","Wudu Steps","Ghusl Steps","Zakat Calculator"])
if menu == "Quran with Audio":
    st.header("Quran with Audio")
    surah_data = requests.get("https://quranapi.pages.dev/api/surah.json").json()
    surah_list = [
    f"{i+1} | {s['surahNameArabicLong']} | {s['surahName']}"
    for i, s in enumerate(surah_data)
    ]

    selected_surah = st.sidebar.selectbox("Select Surah", surah_list)
    surah_num = int(selected_surah.split("|")[0].strip())


    reciters = {
        "Mishary Rashid Al Afasy": "1",
        "Abu Bakr Al Shatri": "2",
        "Nasser Al Qatami": "3",
        "Yasser Al Dosari": "4",
        "Hani Ar Rifai": "5"
    }
    reciter_name = st.sidebar.selectbox(" Choose Reciter", list(reciters.keys()))
    reciter_id = reciters[reciter_name]

    data = requests.get(f"https://quranapi.pages.dev/api/{surah_num}.json").json()

    arabic_verses = data.get("arabic1", [])
    urdu_verses = data.get("urdu", [])
    english_verses = data.get("english", [])

    st.header(f"{data['surahName']} - {data['surahNameArabic']}")

    # Arabic
    st.subheader("**Arabic**")
    for ayah in arabic_verses:
        st.markdown(f"<p class='arabic-text'>{ayah}</p>", unsafe_allow_html=True)

    st.markdown("---")
    # Urdu
    st.subheader("**Urdu Translation**")
    for ayah in urdu_verses:
        st.markdown(f"<p class='urdu-text'>{ayah}</p>", unsafe_allow_html=True)

    st.markdown("---")
    # English
    st.subheader("**English Translation**")
    for ayah in english_verses:
        st.markdown(f"<p class='english-text'>{ayah}</p>", unsafe_allow_html=True)

    st.markdown("---")
    # Audio
    st.subheader(f"Recitation by {reciter_name}")
    audio_data = requests.get(f"https://quranapi.pages.dev/api/audio/{surah_num}.json").json()
    if reciter_id in audio_data:
        st.audio(audio_data[reciter_id]["url"])
    else:
        st.warning("Audio not available for this reciter.")

elif menu == "Quran Tafseer":
 
    
    surah_data = requests.get("https://quranapi.pages.dev/api/surah.json").json()

    surah_list = [
        f"{i+1} | {s['surahNameArabicLong']} | {s['surahName']}"
        for i, s in enumerate(surah_data)
    ]

    selected_surah = st.sidebar.selectbox("Select Surah", surah_list)

    surah_num = int(selected_surah.split("|")[0].strip())
    surah_name_ar = selected_surah.split("|")[1].strip()

    authors = ["Ibn Kathir", "Maarif Ul Quran", "Tazkirul Quran"]
    author = st.sidebar.selectbox("Choose Tafseer Author", authors)

    view_option = st.sidebar.radio("View Tafseer", ["Full Surah", "Ayah-wise"])

    st.subheader(f"Surah {surah_num} | {surah_name_ar} | Tafseer by {author}")

    def fetch_full_tafsir(surah):
        url = f"https://quranapi.pages.dev/api/tafsir/{surah}.json"
        data = requests.get(url).json()

        tafsirs = []
        for group in data.get("tafsirs", []):
            for t in group:
                if isinstance(t, dict) and t.get("author") == author:
                    tafsirs.append(t)
        return tafsirs


    def fetch_ayah_tafsir(surah, ayah):
        url = f"https://quranapi.pages.dev/api/tafsir/{surah}_{ayah}.json"
        data = requests.get(url).json()

        for t in data.get("tafsirs", []):
            if isinstance(t, dict) and t.get("author") == author:
                return t.get("content")
        return None

    author_tafsirs = fetch_full_tafsir(surah_num)

    if not author_tafsirs:
        st.warning("Tafseer not available for this author.")
    else:
        if view_option == "Full Surah":
            if "ayah" in author_tafsirs[0]:
                for t in author_tafsirs:
                    st.markdown(f"**Ayah {t['ayah']}**")
                    st.write(t.get("content", ""))
                    st.divider()
            else:
                st.write(author_tafsirs[0].get("content", "Tafseer not available"))

        else:
            surah_info = requests.get(
                f"https://quranapi.pages.dev/api/{surah_num}.json"
            ).json()

            total_ayah = surah_info["totalAyah"]

            ayah_number = st.sidebar.selectbox(
                "Select Ayah",
                list(range(1, total_ayah + 1))
            )

            tafsir_text = fetch_ayah_tafsir(surah_num, ayah_number)

            if tafsir_text:
                st.subheader(f"Ayah {ayah_number} Tafseer")
                st.write(tafsir_text)
            else:
                st.warning("Ayah-wise tafseer not available.")

        
elif menu == "Hadiths":
    st.header("Hadiths")
    HADITH_API_KEY = st.secrets["HADITH_API_KEY"]
    try:
        response = requests.get(f"https://hadithapi.com/api/books?apiKey={HADITH_API_KEY}")
        books = response.json().get("books", [])
        books_list = [f"{b['bookName']} | {b['bookSlug']}" for b in books]
    except:
        st.error("Failed to fetch Hadith books")
        st.stop()

    bookName = st.sidebar.selectbox("Choose a Book", books_list)
    book_slug = bookName.split("|")[1].strip()
    try:
        responsechapter = requests.get(f"https://hadithapi.com/api/{book_slug}/chapters?apiKey={HADITH_API_KEY}")
        bookchapter = responsechapter.json().get("chapters", [])
        bookschapterlist = [f"{c['chapterNumber']} | {c['chapterEnglish']} | {c['chapterArabic']}" for c in bookchapter]
    except:
        st.error("Failed to fetch chapters")
        st.stop()

    bookchapterName = st.sidebar.selectbox("choose a chapter", bookschapterlist)
    chapter_number = int(bookchapterName.split("|")[0].strip())

    try:
        hadith_response = requests.get(
            f"https://hadithapi.com/public/api/hadiths?apiKey={HADITH_API_KEY}&book={book_slug}&chapter={chapter_number}&paginate=100000"
        )
        hadiths = hadith_response.json().get("hadiths", {}).get("data", [])
    except:
        st.error("Failed to fetch hadiths")
        st.stop()

    for h in hadiths:
        st.header(f"{h['hadithNumber']}")
        st.subheader(f"{h['englishNarrator']}")
        st.write(f"**Arabic:** {h.get('hadithArabic','-')}")
        st.write(f"**English:** {h.get('hadithEnglish','-')}")
        st.write(f"**Urdu:** {h.get('hadithUrdu','-')}")
        st.markdown("---")

elif menu == "Duas":
    data = load_json("data/duas.json")
    st.header("Important Duas")
    duas_list = data.get("duas")
    total = len(duas_list)
    col1, col2 = st.sidebar.columns(2)
    start_input = col1.number_input("Start", min_value=0 ,max_value=total, value=0)
    end_input = col2.number_input("End", min_value=0 ,max_value=total, value=10)   
    if start_input > end_input:
        st.sidebar.error("Start value cannot be greater than End Value") 
    start, end = st.sidebar.slider(
        "Select Range",
        0,total ,
        (int(start_input),int(end_input))
    )
    start_input = start
    end_input = end
    for i in range(start, end ):
        dua = duas_list[i]
        st.subheader(dua.get("title"))
        st.write("**Arabic:**", dua.get("arabic"))
        st.write("**English:**", dua.get("translation_en"))
        st.write("**Urdu:**", dua.get("translation_ur"))
        st.markdown("---")
elif menu == "Kalimas":
    data = load_json("data/kalimas.json")
    st.header("Six Kalimas")
    kalimas_list = data.get("kalimas")
    kalima_names = [k.get("title") for k in kalimas_list]
    selected = st.sidebar.selectbox("Select Kalima", kalima_names)
    kalima = next((k for k in kalimas_list if k.get("title") == selected), None)
    if kalima:
        st.subheader(kalima.get("name"))
        st.write("**Arabic:**", kalima.get("arabic"))
        st.markdown("---")
        st.write("**English:**", kalima.get("translation_en"))
        st.markdown("---")
        st.write("**Urdu:**", kalima.get("translation_ur"))
        st.markdown("---")
    else:
        st.warning("Kalima not found!")
elif menu == "99 Names Of Allah":
    st.header("99 Names Of Allah")
    response = requests.get("https://api.aladhan.com/v1//asmaAlHusna")
    names = response.json()["data"]
    total_names = len(names)
    col1, col2 = st.sidebar.columns(2)
    Start_input = col1.number_input("Start", min_value=0 ,max_value=total_names, value=0)
    End_input = col2.number_input("End", min_value=0 ,max_value=total_names, value=10)  
    if Start_input > End_input:
        st.sidebar.error("Start value cannot be greater than End Value") 
    Start, End = st.sidebar.slider(
        "Select Range",
        0,total_names ,
        (int(Start_input),int(End_input))
    )
    for A in range(Start, End ):
        item = names[A]
        st.header(f"{item['number']}")
        st.write(f"**Arabic:** {item['name']}")
        st.write(f"**English:** {item['transliteration']}")
        st.write(f"**Translation:** {item['en']['meaning']}")
elif menu == "99 Names Of Prophet Muhammad":
    data = load_json("data/prophets.json")
    st.header("99 Names Of Prophet Muhammad")

    pnames_list = data.get("prophet_names")
    total = len(pnames_list)

    col1, col2 = st.sidebar.columns(2)
    Start_input = col1.number_input("Start", min_value=0 ,max_value=total, value=0)
    End_input = col2.number_input("End", min_value=0 ,max_value=total, value=10)   

    if Start_input > End_input:
        st.sidebar.error("Start value cannot be greater than End Value") 

    start, end = st.sidebar.slider(
        "Select Range",
        0, total,
        (int(Start_input), int(End_input))
    )
    for i in range(start, end):
        pname = pnames_list[i]
        st.subheader(f"{pname.get('number')}")
        st.write(f"**Arabic:** {pname.get('arabic')}")
        st.write(f"**English:** {pname.get('name_en')}")
        st.write(f"**Translation:** {pname.get('description_en')}")
        st.markdown("---")
elif menu == "Prayer Time":
    st.header("Prayer Time")
    def convert_to_12hr(time_str):
        return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")
    method_mapping = {
        "Muslim World League": 3,
        "Islamic Society of North America (ISNA)": 2,
        "Egyptian General Authority of Survey": 5,
        "Umm Al-Qura University, Makkah": 4,
        "University of Islamic Sciences, Karachi": 1,
        "Institute of Geophysics, University of Tehran": 7,
        "Shia Ithna-Ashari, Leva Institute, Qum": 0,
        "Gulf Region": 8,
        "Kuwait": 9,
        "Qatar": 10,
        "Majlis Ugama Islam Singapura, Singapore": 11,
        "Union Organization Islamic de France": 12,
        "Diyanet İşleri Başkanlığı, Turkey (experimental)": 13,
        "Spiritual Administration of Muslims of Russia": 14,
        "Moonsighting Committee Worldwide (Moonsighting.com)": 15,
        "Jabatan Kemajuan Islam Malaysia (JAKIM)": 17,
        "Tunisia": 18,
        "Algeria": 19,
        "Kementerian Agama Republik Indonesia": 20,
        "Morocco": 21,
        "Comunidade Islamica de Lisboa": 22,
        "Ministry of Awqaf, Islamic Affairs and Holy Places, Jordan": 23,
    }
    method = st.sidebar.selectbox("Select Calculation Method",list(method_mapping.keys()))
    month = st.sidebar.selectbox("Select Month", list(range(1, 13)))
    year = st.sidebar.number_input("Enter Year", min_value=2000, max_value=2100, value=datetime.now().year)
    country = st.sidebar.text_input("Enter Country (e.g.,PK)")
    state = st.sidebar.text_input("Enter State (e.g., Sindh)")
    city = st.sidebar.text_input("Enter City (e.g., Karachi)")
    if st.button("Generate Prayer Calender"):
        if not country or not state or not city:
            st.warning("Please enter country, state, and city!")
        else:
            try:
                start_date = datetime(year, month, 1)
                if month == 12:
                    end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
                else:
                    end_date = datetime(year, month +1, 1) - timedelta(days=1)
                dates_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
                prayer_data = []
                method_number = method_mapping[method]
                for date in dates_list:
                    date_str = date.strftime("%d-%m-%Y")
                    url = f"https://api.aladhan.com/v1/timingsByCity/{date_str}?city={city}&country={country}&state={state}&method={method_number}"
                    response = requests.get(url)
                    data = response.json()
                    if data['code'] == 200:
                        timings = data['data']['timings']
                        prayer_data.append({
                            "Date": date_str,
                            "Fajr": convert_to_12hr(timings["Fajr"]),
                            "Dhuhr": convert_to_12hr(timings["Dhuhr"]),
                            "Asr": convert_to_12hr(timings["Asr"]),
                            "Maghrib": convert_to_12hr(timings["Maghrib"]),
                            "Isha": convert_to_12hr(timings["Isha"]),
                        })
                    else:
                        prayer_data.append({
                            "Date": date_str,
                            "Fajr": "-",
                            "Dhuhr": "-",
                            "Asr": "-",
                            "Maghrib": "-",
                            "Isha": "-"
                        })
                df = pd.DataFrame(prayer_data)
                st.subheader(f"Prayer Calender for {city}, {state}, {country} - {start_date.strftime('%B %Y')}")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error: {e}")
elif menu == "Qibla Direction":
    st.header("Qibla Direction")
    loc = streamlit_geolocation()
    if not loc:
        st.warning("Waiting for location... Please allow location access or enter manually")
        lat = st.number_input("Latitude", value=0.0)
        lon = st.number_input("Longitude", value=0.0)
        if lat == 0.0 and lon == 0.0:
            st.stop()
    else:
        lat = loc["latitude"]
        lon = loc["longitude"]
        st.success(f"Your Location Detected:\nLatitude: {lat}\nLongitude: {lon}")
    data_url = f"https://api.aladhan.com/v1/qibla/{lat}/{lon}"
    response = requests.get(data_url)
    def get_compass_direction(angle):
        directions = [
            "North", "North-East", "East", "South-East",
            "South", "South-West", "West", "North-West"
        ]
        ix = round(angle / 45) % 8
        return directions[ix]
    if response.status_code == 200:
        data = response.json()['data']
        qibla_angle = data['direction']
        direction_name = get_compass_direction(qibla_angle)
        st.subheader("Qibla Direction Info")
        st.write(f"**Amgle from North:** {qibla_angle:.2f} **Direction:** {direction_name}")
        compass_url = f"https://api.aladhan.com/v1/qibla/{lat}/{lon}/compass/500"
        st.image(compass_url, caption=f"Qibla Compass ({direction_name})")
    else:
        st.error("Failed to fetch Qibla data")
        st.experimental_rerun()
elif menu == "Zakat Calculator":
    ZAKAT_API_KEY = st.secrets["ZAKAT_API_KEY"]
    st.header("Live Zakat Calculator")
    st.markdown("Calculate your zakat based on **Gold, Silver, Cash, Business, and Other assests** using live Nisab values from Islam Suite.")
    currency = st.sidebar.selectbox(
        "Select Currency",
        ["USD","AED","AFN","ALL","AMD","ANG","AOA","ARS","AUD","AWG","AZN","BAM","BBD","BDT","BGN","BHD","BIF","BMD","BND","BOB","BRL","BSD","BTN","BWP","BYN","BZD","CAD","CDF","CHF","CLF","CLP","CNH","CNY","COP","CRC","CUP","CVE","CZK","DJF","DKK","DOP","DZD","EGP","ERN","ETB","EUR","FJD","FKP","FOK","GBP","GEL","GGP","GHS","GIP","GMD","GNF","GTQ","GYD","HKD","HNL","HRK","HTG","HUF","IDR","ILS","IMP","INR","IQD","IRR","ISK","JEP","JMD","JOD","JPY","KES","KGS","KHR","KID","KMF","KRW","KWD","KYD","KZT","LAK","LBP","LKR","LRD","LSL","LYD","MAD","MDL","MGA","MKD","MMK","MNT","MOP","MRU","MUR","MVR","MWK","MXN","MYR","MZN","NAD","NGN","NIO","NOK","NPR","NZD","OMR","PAB","PEN","PGK","PHP","PKR","PLN","PYG","QAR","RON","RSD","RUB","RWF","SAR","SBD","SCR","SDG","SEK","SGD","SHP","SLE","SLL","SOS","SRD","SSP","STN","SYP","SZL","THB","TJS","TMT","TND","TOP","TRY","TTD","TVD","TWD","TZS","UAH","UGX","UYU","UZS","VES","VND","VUV","WST","XAF","XCD","XCG","XDR","XOF","XPF","YER","ZAR","ZMW","ZWL"])
    unit = "g"
    try:
        Api = f"https://islamicapi.com/api/v1/zakat-nisab/?standard=classical&currency={currency}&unit={unit}&api_key={ZAKAT_API_KEY}"
        response = requests.get(Api)
        data = response.json()["data"]
        gold_nisab = data["nisab_thresholds"]["gold"]["nisab_amount"]
        silver_nisab = data["nisab_thresholds"]["silver"]["nisab_amount"]
        zakat_rate = float(data["zakat_rate"].replace("%",""))/100
        st.info(f"Gold Nisab: {gold_nisab} {currency}")
        st.info(f"Silver Nisab: {silver_nisab} {currency}")
        st.info(f"Zakat Rate: {data['zakat_rate']}")
    except Exception as e:
        st.error(f"Nisab Fetch Error: {e}")
        gold_nisab = silver_nisab = None
        zakat_rate = 0.025
    st.header("Enter Your Assests")
    col1, col2 = st.columns(2)
    with col1:
        gold_amount = st.number_input(f"Gold ({unit})", min_value=0.0)
        gold_price = st.number_input(f"Gold Price Per {unit} ({currency})", min_value=0.0)
        silver_amount = st.number_input(f"Silver ({unit})", min_value=0.0)
        silver_price = st.number_input(f"Silver Price Per {unit} ({currency})", min_value=0.0)
    with col2:
        cash =  st.number_input(f"Cash / Bank ({currency})", min_value=0.0)
        business_assets = st.number_input(f"Business Assests ({currency})", min_value=0.0)
        other_assets = st.number_input(f"Other Assests ({currency})", min_value=0.0)
    gold_value = gold_amount * gold_price
    silver_value = silver_amount * silver_price
    total_assests = gold_value + silver_value + cash + business_assets +other_assets
    st.markdown(f"Total Assests: **{round(total_assests,2)} {currency}**")
    if st.button("Calculate Zakat"):
        if gold_nisab is None:
            st.error("Nisab Not Fetched.")
        else:
            nisab = min(gold_nisab, silver_nisab)
            if total_assests >= nisab:
                zakat = total_assests * zakat_rate
                st.success(f"Zakat is obligatory: **{round(zakat,2)} {currency}**")
            else:
                st.warning("!Your wealth is below the Nisab — Zakat is not obligatory.")
elif  menu == "Namaz Steps":
    data = load_json("data/namaz.json")
    st.header("Namaz steps")
    for N in data.get("namaz_recitations"):
        st.subheader(N.get("step"))
        st.write("**Arabic:**", N.get("arabic"))
        st.write("**English:**", N.get("english"))
        st.write("**Urdu:**", N.get("urdu"))
        st.markdown("---")
elif menu == "Wudu Steps":
    data = load_json("data/wudu.json")
    st.header("Wudu Steps")
    for w in data.get("wudu_steps"):
        st.subheader(w.get("step"))
        st.write("**Detail:**", w.get("action"))
        st.write("**Urdu:**", w.get("description_ur"))
        st.write("**English:**", w.get("description_en"))
        st.markdown("---")
elif menu == "Ghusl Steps":
    data = load_json("data/ghusl.json")
    st.header("Ghusl Steps")
    for g in data.get("ghusl_steps"):
        st.subheader(g.get("step_number"))
        st.write("**Detail:**",g.get("title"))
        st.write("**Urdu:**",g.get("description_ur"))
        st.write("**English:**",g.get("description_en"))
        st.markdown("---")
elif menu == "Rakats":
    data = load_json("data/rakats.json")
    st.header("Rakats Information")
    rakats_list = data.get("prayer_rakats")
    rakats_names = [r.get("prayer") for r in rakats_list]
    selected = st.sidebar.selectbox("Select Namaz", rakats_names)
    rakats = next((r for r in rakats_list if r.get("prayer") == selected), None)
    if rakats:
        st.subheader(rakats.get("prayer"))
        for r in rakats.get("rakats"):
            st.write(f"**Rakats:** {r.get('type')} - {r.get('count')}")
            st.write("**English:**", r.get("description_en"))
            st.write("**Urdu:**", r.get("description_ur"))
            st.markdown("---")
    else:
        st.warning("Rakats not found!")

st.markdown('---')
st.markdown('<div class="small-muted">Developed By Adeeba Yameen Sheikh  </div>', unsafe_allow_html=True)
