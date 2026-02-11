import streamlit as st
import math
from datetime import date, timedelta

# ==============================================================================
# 1. KONFIGURASI HALAMAN & CSS
# ==============================================================================
st.set_page_config(
    page_title="Temen Tani: Smart Farming Assistant",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan profesional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7d32; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #1b5e20; }
    .highlight { font-weight: bold; color: #2e7d32; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DATABASE AGRO-TEKNOLOGI LENGKAP (Buah, Sayur, Rempah)
# ==============================================================================
# Struktur: "Nama": {"jarak": (Baris, Antar_Baris), "hari_panen": int, "desc": "..."}

DATABASE = {
    "🍎 Buah-buahan (Fruits)": {
        "Dataran Rendah (Lowland)": {
            "Semangka": {"jarak": (1.0, 1.5), "hari_panen": 75, "desc": "Butuh sinar matahari penuh, tanah berpasir."},
            "Melon": {"jarak": (0.7, 0.6), "hari_panen": 65, "desc": "Gunakan lanjaran/tali, rentan jamur di musim hujan."},
            "Pepaya Calina": {"jarak": (2.5, 2.5), "hari_panen": 210, "desc": "Panen pertama umur 7 bulan, produktif hingga 2 tahun."},
            "Nanas": {"jarak": (0.5, 0.5), "hari_panen": 365, "desc": "Tahan lahan kering, pH asam (4.5-5.5) oke."},
            "Mangga": {"jarak": (8.0, 8.0), "hari_panen": 1095, "desc": "Jangka panjang. Panen optimal mulai tahun ke-3."},
            "Durian": {"jarak": (10.0, 10.0), "hari_panen": 1825, "desc": "Raja buah. Butuh ruang akar luas & drainase sempurna."},
            "Alpukat": {"jarak": (5.0, 6.0), "hari_panen": 1095, "desc": "Tidak tahan genangan air, butuh tanah gembur."}
        },
        "Dataran Tinggi (Highland)": {
            "Apel": {"jarak": (3.0, 4.0), "hari_panen": 1460, "desc": "Butuh suhu dingin ekstrem untuk pembuahan."},
            "Jeruk Keprok": {"jarak": (4.0, 4.0), "hari_panen": 1095, "desc": "Sangat cocok di ketinggian 700-1200 mdpl."},
            "Strawberry": {"jarak": (0.3, 0.4), "hari_panen": 60, "desc": "Wajib mulsa plastik, butuh penyiraman rutin."},
            "Leci": {"jarak": (6.0, 6.0), "hari_panen": 1095, "desc": "Tanaman subtropis yang butuh musim dingin kering."}
        }
    },
    "🥦 Sayur-mayur (Vegetables)": {
        "Dataran Rendah (Lowland)": {
            "Cabai Merah": {"jarak": (0.5, 0.6), "hari_panen": 90, "desc": "Komoditas inflasi. Perhatikan hama patek/antraknosa."},
            "Tomat": {"jarak": (0.5, 0.6), "hari_panen": 70, "desc": "Butuh kalsium tinggi agar buah tidak pecah."},
            "Terong": {"jarak": (0.7, 0.6), "hari_panen": 60, "desc": "Panen berkali-kali, butuh air cukup."},
            "Kangkung": {"jarak": (0.1, 0.1), "hari_panen": 25, "desc": "Panen super cepat (20-25 hari). Cashflow harian."},
            "Bayam": {"jarak": (0.1, 0.1), "hari_panen": 25, "desc": "Sensitif terhadap genangan air berlebih."},
            "Kacang Panjang": {"jarak": (0.4, 0.4), "hari_panen": 45, "desc": "Butuh lanjaran tinggi, panen setiap 2 hari."}
        },
        "Dataran Tinggi (Highland)": {
            "Wortel": {"jarak": (0.1, 0.2), "hari_panen": 90, "desc": "Tanah harus gembur tanpa batu agar umbi lurus."},
            "Kubis/Kol": {"jarak": (0.5, 0.5), "hari_panen": 75, "desc": "Butuh suhu sejuk untuk membentuk krop padat."},
            "Kentang": {"jarak": (0.3, 0.7), "hari_panen": 100, "desc": "Guludan harus tinggi, hindari tanah liat."},
            "Brokoli": {"jarak": (0.5, 0.5), "hari_panen": 60, "desc": "Nilai jual tinggi, panen sebelum bunga mekar."}
        }
    },
    "🍂 Rempah-rempah (Spices/Herbs)": {
        "Dataran Rendah (Lowland)": {
            "Jahe Gajah": {"jarak": (0.4, 0.5), "hari_panen": 270, "desc": "Pasar ekspor tinggi. Panen rimpang tua 9 bulan."},
            "Kunyit": {"jarak": (0.4, 0.5), "hari_panen": 240, "desc": "Tanaman obat dasar. Tahan naungan."},
            "Lengkuas": {"jarak": (0.6, 0.6), "hari_panen": 300, "desc": "Sangat tahan banting, minim perawatan."},
            "Lada (Perdu)": {"jarak": (1.5, 1.5), "hari_panen": 730, "desc": "Emas hitam. Butuh tiang panjat atau sistem perdu."},
            "Serai Wangi": {"jarak": (1.0, 1.0), "hari_panen": 90, "desc": "Panen daun untuk minyak atsiri setiap 3 bulan."}
        },
        "Dataran Tinggi (Highland)": {
            "Cengkeh": {"jarak": (8.0, 8.0), "hari_panen": 1825, "desc": "Investasi jangka panjang. Panen raya 2 tahun sekali."},
            "Kapulaga": {"jarak": (1.5, 1.5), "hari_panen": 540, "desc": "High Value! Tanam di bawah tegakan pohon (Agroforestri)."},
            "Pala": {"jarak": (9.0, 9.0), "hari_panen": 2190, "desc": "Rempah asli Indonesia. Bernilai ekonomi sangat tinggi."},
            "Kayu Manis": {"jarak": (3.0, 3.0), "hari_panen": 2555, "desc": "Panen kulit batang, butuh waktu 6-8 tahun."}
        }
    }
}

# ==============================================================================
# 3. SIDEBAR & INPUT USER
# ==============================================================================
with st.sidebar:
    st.title("🌾 Temen Tani Pro")
    st.write("Sistem Perencanaan Lahan Presisi")
    
    # Input Kategori
    kategori = st.selectbox("1. Pilih Komoditas", list(DATABASE.keys()))
    elevasi = st.selectbox("2. Elevasi/Lokasi", list(DATABASE[kategori].keys()))
    tanaman_list = list(DATABASE[kategori][elevasi].keys())
    pilihan_tanaman = st.selectbox("3. Pilih Tanaman", tanaman_list)
    
    st.markdown("---")
    st.write("📐 **Dimensi Lahan**")
    panjang = st.number_input("Panjang Lahan (meter)", min_value=1.0, value=20.0, step=1.0)
    lebar = st.number_input("Lebar Lahan (meter)", min_value=1.0, value=10.0, step=1.0)
    
    st.markdown("---")
    tgl_tanam = st.date_input("📅 Tanggal Mulai Tanam", date.today())

# ==============================================================================
# 4. LOGIKA PERHITUNGAN (ENGINE)
# ==============================================================================
data_tanaman = DATABASE[kategori][elevasi][pilihan_tanaman]
jarak_baris = data_tanaman["jarak"][0] # Jarak dalam baris
jarak_antar_baris = data_tanaman["jarak"][1] # Jarak antar baris

# Hitung Populasi (Menggunakan Floor untuk realitas lapangan)
jml_baris = math.floor(lebar / jarak_antar_baris)
jml_tanaman_per_baris = math.floor(panjang / jarak_baris)
total_bibit = jml_baris * jml_tanaman_per_baris

# Hitung Efisiensi
luas_total = panjang * lebar
luas_terpakai = total_bibit * (jarak_baris * jarak_antar_baris)
sisa_lahan = luas_total - luas_terpakai
efisiensi = (luas_terpakai / luas_total) * 100

# Hitung Panen
hari_panen = data_tanaman["hari_panen"]
tgl_panen = tgl_tanam + timedelta(days=hari_panen)

# ==============================================================================
# 5. DASHBOARD UTAMA (OUTPUT)
# ==============================================================================
st.title(f"Analisis Budidaya: {pilihan_tanaman}")
st.markdown(f"**Kategori:** {kategori} | **Lokasi:** {elevasi}")

# Baris 1: Metric Utama
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bibit", f"{total_bibit} Batang", help="Jumlah maksimal bibit yang muat")
col2.metric("Formasi Tanam", f"{jml_baris} x {jml_tanaman_per_baris}", help="Baris x Kolom")
col3.metric("Estimasi Panen", f"{tgl_panen.strftime('%d %b %Y')}", help="Perkiraan tanggal panen pertama")
col4.metric("Efisiensi Lahan", f"{efisiensi:.1f}%", f"Sisa: {sisa_lahan:.1f} m²")

# Baris 2: Visualisasi & Detail
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📋 Spesifikasi Teknis")
    st.info(f"""
    * **Jarak Tanam Ideal:** {jarak_baris}m (Jarak Tanam) x {jarak_antar_baris}m (Jarak Baris)
    * **Masa Tunggu Panen:** {hari_panen} Hari ({round(hari_panen/30, 1)} Bulan)
    * **Catatan Ahli:** {data_tanaman['desc']}
    """)

    

with c2:
    st.subheader("🧪 Analisis pH Tanah")
    ph_tanah = st.slider("Input pH Tanah Anda", 0.0, 14.0, 6.5, step=0.1)
    
    if ph_tanah < 5.5:
        st.error("⚠️ **Tanah ASAM**")
        st.write("Tanaman sulit menyerap nutrisi.")
        st.write("👉 **Solusi:** Taburkan Kapur Dolomit 2-3 minggu sebelum tanam.")
    elif 5.5 <= ph_tanah <= 7.5:
        st.success("✅ **Tanah IDEAL**")
        st.write("Kondisi optimal untuk penyerapan nutrisi.")
        st.write("👉 **Solusi:** Pertahankan dengan pupuk organik.")
    else:
        st.warning("⚠️ **Tanah BASA**")
        st.write("Rawan kekurangan unsur mikro (Besi/Mangan).")
        st.write("👉 **Solusi:** Berikan Sulfur atau pupuk ZA.")

# ==============================================================================
# 6. FOOTER
# ==============================================================================
st.markdown("---")
st.caption("© 2024 Temen Tani Pro | International Agriculture Assistant | Developed with Python Streamlit")
