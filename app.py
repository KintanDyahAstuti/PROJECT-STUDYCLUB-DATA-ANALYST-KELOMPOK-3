"""Dashboard Game Online Favorit Indonesia 2026
Jalankan dengan:  streamlit run app.py
"""
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Game Online Favorit Indonesia 2026", page_icon="🕹️", layout="wide")

# ====================== Konstanta ======================
BASE = Path(__file__).parent
INK, SOFT, PAPER, MUTED, RULE, ACCENT = "#1B1A17", "#3B4252", "#F6F1E7", "#6B665C", "#D9D2C3", "#C8372D"
WARNA = {
    "Mobile Legends": "#C8372D", "Free Fire": "#E2A03F", "Roblox": "#2E6F6A", "PUBG": "#26405E",
    "Candy Crush Saga": "#B4577B", "FIFA Mobile": "#6E8B3D", "Minecraft": "#8A6B4B", "Lainnya": "#BDB6A6",
}
SUMBER_URL = "https://data.goodstats.id/statistic/game-online-favorit-pengguna-internet-indonesia-2026-mobile-legends-teratas-udfO8"
# Keterangan metodologi dan konteks berasal dari halaman sumber yang sama (GoodStats Data, 11 Juni 2026)
RESPONDEN, PROVINSI = 8700, 38
INTERNET_JUTA, POPULASI_JUTA, PENETRASI = 235.26, 287.88, 81.72


def idn(x, d=1):
    """Format angka gaya Indonesia: 1.234,5"""
    return f"{x:,.{d}f}".replace(",", "§").replace(".", ",").replace("§", ".")


# ====================== Gaya ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"], .stMarkdown, label { font-family: 'IBM Plex Sans', sans-serif; }
.block-container { max-width: 1060px; padding-top: 2.2rem; padding-bottom: 4rem; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.title { font: 700 1.25rem 'Fraunces', serif; margin: 0 0 .2rem; padding: 0; color: #1B1A17; }
.kicker { font: 500 .85rem 'IBM Plex Mono', monospace; color: #C8372D; margin-bottom: .6rem; }
.headline { font: 700 clamp(2rem, 4.6vw, 3.5rem)/1.04 'Fraunces', serif; letter-spacing: -.02em; margin: 0 0 1rem; max-width: 20ch; }
.standfirst { font-size: 1.12rem; line-height: 1.55; color: #3d3a33; max-width: 62ch; margin: 0 0 1.6rem; }
.figs { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); border-top: 2px solid #1B1A17; border-bottom: 1px solid #D9D2C3; margin-bottom: 1rem; }
.fig { padding: 16px 18px 16px 0; }
.fig + .fig { padding-left: 18px; border-left: 1px solid #D9D2C3; }
.fig b { display: block; font: 700 2.3rem/1.1 'Fraunces', serif; }
.fig span { color: #6B665C; font-size: .88rem; }

.sec { display: flex; align-items: baseline; gap: 14px; border-top: 2px solid #1B1A17; margin: 3rem 0 .6rem; padding-top: .7rem; }
.sec .n { font: 500 .9rem 'IBM Plex Mono', monospace; color: #C8372D; }
.sec h2 { font: 700 1.7rem/1.2 'Fraunces', serif; margin: 0; padding: 0; letter-spacing: -.01em; }
.lede { color: #4a463d; max-width: 64ch; margin: 0 0 1rem; line-height: 1.55; }
.cap { color: #6B665C; font-size: .84rem; line-height: 1.5; margin-top: .4rem; max-width: 70ch; }

.duel { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin: 1rem 0 .4rem; }
.duel .nm { font: 600 1.05rem 'IBM Plex Sans'; }
.duel .num { font: 700 3.4rem/1.05 'Fraunces', serif; }
.duel .est { color: #6B665C; font-size: .85rem; margin-top: 4px; }
.track { height: 10px; background: #E4DCCB; margin-top: 10px; }
.track i { display: block; height: 100%; }
.verdict { border-top: 1px solid #D9D2C3; border-bottom: 1px solid #D9D2C3; padding: 12px 0; margin: 14px 0 4px; font-size: 1.05rem; }

.key { list-style: none; padding: 0; margin: 0; }
.key li { display: flex; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid #D9D2C3; font-size: .95rem; }
.key .sw { width: 14px; height: 14px; flex: none; }
.key .v { margin-left: auto; font: 500 .9rem 'IBM Plex Mono', monospace; color: #3d3a33; }
.focus { font: 500 1.35rem/1.3 'Fraunces', serif; margin-top: 18px; }

.notes { padding-left: 1.2rem; max-width: 66ch; line-height: 1.6; }
.notes li { margin-bottom: .55rem; }
.src li { margin-bottom: .4rem; }
@media (max-width: 640px) { .duel { grid-template-columns: 1fr; } .fig + .fig { border-left: 0; padding-left: 0; } }
</style>
""", unsafe_allow_html=True)


def tema(chart):
    """Gaya grafik Altair seragam dengan halaman."""
    return (chart.configure(background="transparent", font="IBM Plex Sans")
            .configure_view(stroke=None)
            .configure_axis(labelColor=MUTED, titleColor=MUTED, gridColor="#E4DCCB", domainColor=RULE,
                            tickColor=RULE, labelFontSize=12, titleFontSize=12))


def section(no, judul, lede=""):
    st.markdown(f'<div class="sec"><span class="n">{no}</span><h2>{judul}</h2></div>'
                + (f'<p class="lede">{lede}</p>' if lede else ""), unsafe_allow_html=True)


def caption(teks):
    st.markdown(f'<p class="cap">{teks}</p>', unsafe_allow_html=True)


# ====================== Data ======================
def cari_csv():
    for p in (BASE / "game_favorit_clean.csv", BASE / "data" / "game_favorit_clean.csv",
              BASE / "data" / "game_2026_clean.csv"):
        if p.exists():
            return p
    return None


@st.cache_data
def muat(path):
    d = pd.read_csv(path).rename(columns={"persen": "persentase"})
    d["game"] = d["game"].astype(str).str.strip()
    d["persentase"] = pd.to_numeric(d["persentase"], errors="coerce")
    return d.dropna(subset=["game", "persentase"]).drop_duplicates("game")[["game", "persentase"]]


def kelompok(p):
    return "Besar (>20%)" if p > 20 else "Menengah (5-20%)" if p >= 5 else "Kecil (<5%)"


csv_path = cari_csv()
if csv_path is None:
    st.error("File game_favorit_clean.csv tidak ditemukan. Letakkan di folder yang sama dengan app.py.")
    st.stop()

semua = muat(csv_path)
game = (semua[semua.game != "Lainnya"].sort_values("persentase", ascending=False).reset_index(drop=True))
game["peringkat"] = game.index + 1
game["kumulatif"] = game.persentase.cumsum().round(1)
game["kelompok"] = game.persentase.map(kelompok)
game["kum_label"] = game.kumulatif.map(idn)
lainnya = semua[semua.game == "Lainnya"].persentase.sum()
top, kedua = game.iloc[0], game.iloc[1]
top3 = game.persentase.head(3).sum()

# ====================== Kepala halaman ======================
dari10 = int(round(top.persentase / 10))
st.markdown(f"""
<h1 class="title">Dashboard Analisis Game Terpopuler di Indonesia 2026</h1>
<div class="kicker">Survei APJII 2026 · data dari GoodStats Data</div>
<h1 class="headline">{dari10} dari 10 gamer online di Indonesia paling sering memainkan {top.game}</h1>
<p class="standfirst">{kedua.game} menyusul dengan {idn(kedua.persentase)}%, lalu {game.iloc[2].game} dengan
{idn(game.iloc[2].persentase)}%. Tiga game teratas menguasai {idn(top3)}% jawaban responden. Jelajahi datanya di bawah.</p>
<div class="figs">
  <div class="fig"><b>{idn(top.persentase)}%</b><span>pangsa {top.game}, terbesar di daftar</span></div>
  <div class="fig"><b>{idn(top.persentase / kedua.persentase, 2)}×</b><span>dibanding {kedua.game}</span></div>
  <div class="fig"><b>{idn(top3)}%</b><span>dikuasai tiga game teratas</span></div>
  <div class="fig"><b>{idn(RESPONDEN, 0)}</b><span>responden di {PROVINSI} provinsi</span></div>
</div>
""", unsafe_allow_html=True)

# ====================== 01 Peringkat ======================
section("01", "Peringkat game online", "Persentase pengguna internet yang bermain game online dan paling sering memainkan game tersebut.")

c1, c2, c3 = st.columns([2.2, 1, 1.2])
semua_kel = ["Besar (>20%)", "Menengah (5-20%)", "Kecil (<5%)"]
pilih_kel = c1.multiselect("Kelompok game", semua_kel, default=semua_kel)
tampil_lain = c2.toggle("Sertakan “Lainnya”", value=False)
urut = c3.radio("Urutkan", ["Terbesar", "A–Z"], horizontal=True)

view = game[game.kelompok.isin(pilih_kel)][["game", "persentase", "kelompok"]].copy()
if tampil_lain:
    view = pd.concat([view, pd.DataFrame([{"game": "Lainnya", "persentase": lainnya, "kelompok": "Gabungan"}])])

if view.empty:
    st.info("Tidak ada game yang cocok dengan filter. Pilih minimal satu kelompok.")
else:
    view["label"] = view.persentase.map(lambda v: f"{idn(v)}%")
    view["warna"] = view.game.map(lambda g: ACCENT if g == top.game else ("#BDB6A6" if g == "Lainnya" else SOFT))
    urutan = (view.sort_values("persentase", ascending=False).game.tolist() if urut == "Terbesar"
              else sorted(view.game))
    hover = alt.selection_point(on="mouseover", fields=["game"], clear="mouseout")
    dasar = alt.Chart(view).encode(y=alt.Y("game:N", sort=urutan, title=None,
                                           axis=alt.Axis(labelFontSize=14, labelColor=INK, ticks=False,
                                                         domain=False, labelPadding=8, labelLimit=220)))
    bar = dasar.mark_bar(size=26).encode(
        x=alt.X("persentase:Q", title=None, scale=alt.Scale(domain=[0, float(view.persentase.max()) * 1.16]),
                axis=alt.Axis(format=".0f", labelExpr="datum.value + '%'", tickCount=5)),
        color=alt.Color("warna:N", scale=None),
        opacity=alt.condition(hover, alt.value(1), alt.value(.5)),
        tooltip=[alt.Tooltip("game:N", title="Game"), alt.Tooltip("persentase:Q", title="Persentase (%)", format=".1f"),
                 alt.Tooltip("kelompok:N", title="Kelompok")],
    ).add_params(hover)
    teks = dasar.mark_text(align="left", dx=7, font="IBM Plex Mono", fontSize=13, fontWeight=500, color=INK).encode(
        x="persentase:Q", text="label:N")
    st.altair_chart(tema(alt.layer(bar, teks).properties(height=44 * len(view) + 20)), width="stretch")
    caption("Arahkan kursor ke batang untuk melihat detail. Warna merah menandai game dengan pangsa terbesar.")

# ====================== 02 Seratus gamer ======================
section("02", "Kalau ada 100 gamer online…",
        "Satu kotak mewakili satu dari 100 gamer. Pilih sebuah game untuk menyorotnya.")


def alokasi_100(d):
    """Bulatkan persentase ke 100 kotak dengan metode sisa terbesar."""
    p = d.persentase / d.persentase.sum() * 100
    n = np.floor(p).astype(int)
    kurang = 100 - int(n.sum())
    n.loc[(p - n).sort_values(ascending=False).index[:kurang]] += 1
    return n


waf = pd.concat([game[["game", "persentase"]], pd.DataFrame([{"game": "Lainnya", "persentase": lainnya}])], ignore_index=True)
waf["kotak"] = alokasi_100(waf)
sel_opsi = ["Semua game"] + waf.game.tolist()
kolom_w, kolom_k = st.columns([1.1, 1])
with kolom_k:
    sorot = st.selectbox("Sorot game", sel_opsi, label_visibility="collapsed")
cells = []
for _, r in waf.iterrows():
    cells += [{"game": r.game, "persen": r.persentase} for _ in range(int(r.kotak))]
cells = pd.DataFrame(cells)
cells["x"], cells["y"] = cells.index % 10, cells.index // 10
cells["op"] = np.where((sorot == "Semua game") | (cells.game == sorot), 1.0, 0.14)
waffle = (alt.Chart(cells).mark_rect(stroke=PAPER, strokeWidth=3, cornerRadius=3)
          .encode(x=alt.X("x:O", axis=None), y=alt.Y("y:O", axis=None, sort="ascending"),
                  color=alt.Color("game:N", scale=alt.Scale(domain=list(WARNA), range=list(WARNA.values())), legend=None),
                  opacity=alt.Opacity("op:Q", scale=None),
                  tooltip=[alt.Tooltip("game:N", title="Game"), alt.Tooltip("persen:Q", title="Persentase (%)", format=".1f")])
          .properties(width=340, height=340))
with kolom_w:
    st.altair_chart(tema(waffle), width="content")
with kolom_k:
    daftar = "".join(
        f'<li style="opacity:{1 if sorot in ("Semua game", r.game) else .35}"><span class="sw" style="background:{WARNA.get(r.game, "#888")}"></span>'
        f'{r.game}<span class="v">{int(r.kotak)} kotak · {idn(r.persentase)}%</span></li>' for _, r in waf.iterrows())
    st.markdown(f'<ul class="key">{daftar}</ul>', unsafe_allow_html=True)
    if sorot != "Semua game":
        r = waf[waf.game == sorot].iloc[0]
        st.markdown(f'<div class="focus">Dari 100 gamer online, sekitar {int(r.kotak)} paling sering memainkan {sorot}.</div>',
                    unsafe_allow_html=True)
caption(f"Pembulatan memakai metode sisa terbesar agar jumlah kotak tepat 100. Total persentase asli {idn(semua.persentase.sum())}% "
        "karena pembulatan dari sumber.")

# ====================== 03 Adu dua game ======================
section("03", "Adu dua game", "Pilih dua game dan bandingkan pangsanya secara langsung.")
nama = game.game.tolist()
d1, d2 = st.columns(2)
a = d1.selectbox("Game pertama", nama, index=0)
b = d2.selectbox("Game kedua", nama, index=1)
if a == b:
    st.info("Pilih dua game yang berbeda.")
else:
    ra, rb = game[game.game == a].iloc[0], game[game.game == b].iloc[0]
    besar, kecil = (ra, rb) if ra.persentase >= rb.persentase else (rb, ra)
    mx = float(game.persentase.max())

    def sisi(r):
        return (f'<div><div class="nm">{r.game}</div><div class="num" style="color:{WARNA.get(r.game, INK)}">{idn(r.persentase)}%</div>'
                f'<div class="track"><i style="width:{r.persentase / mx * 100:.1f}%;background:{WARNA.get(r.game, INK)}"></i></div>'
                f'<div class="est">peringkat {r.peringkat} · kelompok {r.kelompok}</div></div>')

    st.markdown(f'<div class="duel">{sisi(ra)}{sisi(rb)}</div>'
                f'<div class="verdict"><b>{besar.game}</b> unggul <b>{idn(besar.persentase - kecil.persentase)} poin</b>, '
                f'atau {idn(besar.persentase / kecil.persentase, 2)}× pangsa {kecil.game}.</div>', unsafe_allow_html=True)
    caption("Lebar batang dihitung terhadap pangsa terbesar di daftar.")

# ====================== 04 Konsentrasi ======================
section("04", "Seberapa terkonsentrasi pasarnya?",
        "Batang menunjukkan pangsa tiap game, garis menunjukkan akumulasinya dari peringkat teratas.")
idx80 = int(game.index[game.kumulatif >= 80][0])
par = alt.Chart(game).encode(x=alt.X("game:N", sort=game.game.tolist(), title=None, axis=alt.Axis(labelAngle=0, labelLimit=170, labelFontSize=12, labelColor=INK)))
p_bar = par.mark_bar(color=SOFT, size=34).encode(y=alt.Y("persentase:Q", title="Persentase (%)", scale=alt.Scale(domain=[0, 100])),
                                                 tooltip=[alt.Tooltip("game:N", title="Game"), alt.Tooltip("persentase:Q", title="Persentase (%)", format=".1f")])
p_line = par.mark_line(color=ACCENT, strokeWidth=3, point=alt.OverlayMarkDef(color=ACCENT, size=70)).encode(
    y="kumulatif:Q", tooltip=[alt.Tooltip("game:N", title="Game"), alt.Tooltip("kumulatif:Q", title="Kumulatif (%)", format=".1f")])
p_lbl = par.mark_text(dy=-14, font="IBM Plex Mono", fontSize=12, color=ACCENT, fontWeight=500).encode(y="kumulatif:Q", text="kum_label:N")
p_80 = alt.Chart(pd.DataFrame({"y": [80]})).mark_rule(strokeDash=[5, 4], color=MUTED).encode(y="y:Q")
st.altair_chart(tema(alt.layer(p_bar, p_80, p_line, p_lbl).properties(height=360)), width="stretch")
caption("Garis putus-putus menandai 80%.")

kel = (game.groupby("kelompok").agg(Jumlah=("game", "count"), Total=("persentase", "sum"), Game=("game", lambda s: ", ".join(s)))
       .reindex(semua_kel).reset_index().rename(columns={"kelompok": "Kelompok"}))
kel["Total"] = kel.Total.round(1)
kel["label"] = kel.Total.map(lambda v: f"{idn(v)}%")
kiri, kanan = st.columns([1, 1])
with kiri:
    st.markdown("**Total pangsa per kelompok**")
    kb = alt.Chart(kel).encode(y=alt.Y("Kelompok:N", sort=semua_kel, title=None, axis=alt.Axis(ticks=False, domain=False, labelColor=INK, labelFontSize=13, labelLimit=180)))
    kbar = kb.mark_bar(color=SOFT, size=22).encode(x=alt.X("Total:Q", title=None, axis=None, scale=alt.Scale(domain=[0, 80])),
                                                     tooltip=[alt.Tooltip("Kelompok:N"), alt.Tooltip("Jumlah:Q", title="Jumlah game"), alt.Tooltip("Total:Q", title="Total (%)", format=".1f")])
    ktxt = kb.mark_text(align="left", dx=6, font="IBM Plex Mono", fontSize=12, color=INK).encode(x="Total:Q", text="label:N")
    st.altair_chart(tema(alt.layer(kbar, ktxt).properties(height=150)), width="stretch")
with kanan:
    st.markdown("**Anggota tiap kelompok**")
    st.dataframe(kel[["Kelompok", "Jumlah", "Game"]], hide_index=True, width="stretch")
caption("Kelompok dibuat dari persentase: Besar (>20%), Menengah (5–20%), Kecil (<5%).")

gap = (game.persentase.shift(1) - game.persentase).iloc[1:]       # jarak ke peringkat di atasnya
ketat = int(gap.idxmin())
besar_tot = kel.Total[0]; kecil_tot = kel.Total[2]
catatan = [
    f"Tiga game teratas menguasai <b>{idn(top3)}%</b>. Akumulasi melewati 80% pada game ke-{idx80 + 1}, "
    f"yaitu {game.game[idx80]} (<b>{idn(game.kumulatif[idx80])}%</b>).",
    f"Jarak peringkat 1 ke 2 sebesar <b>{idn(top.persentase - kedua.persentase)} poin</b>, sedangkan peringkat 3 ke 4 hanya "
    f"<b>{idn(game.persentase[2] - game.persentase[3])} poin</b>.",
    f"Dua game kelompok Besar menguasai <b>{idn(besar_tot)}%</b>, sedangkan dua game kelompok Kecil hanya <b>{idn(kecil_tot)}%</b>, "
    f"lebih kecil dari kategori “Lainnya” ({idn(lainnya)}%).",
    f"Selisih terkecil ada antara {game.game[ketat - 1]} dan {game.game[ketat]}: <b>{idn(gap[ketat])} poin</b>, lebih kecil dari margin of error ±1,1%.",
]
st.markdown("**Catatan dari data**")
st.markdown('<ol class="notes">' + "".join(f"<li>{c}</li>" for c in catatan) + "</ol>", unsafe_allow_html=True)

# ====================== 05 Kesimpulan ======================
section("05", "Kesimpulan dan rekomendasi", "Jawaban atas pertanyaan analisis, berdasarkan data pada dashboard ini.")
k1, k2 = st.columns(2)
with k1:
    st.markdown("**Insight**")
    st.markdown(f"""<ol class="notes">
<li><b>Mobile Legends menjadi game favorit nomor 1 dengan 40.5%.</li>
<li><b>Dua game teratas menguasai 64.7% dari seluruh pilihan.</li>
<li><b>Dua game berada di bawah 5% (FIFA Mobile, Minecraft), artinya pasarnya sangat terkonsentrasi di beberapa game besar.</li>
</ol>""", unsafe_allow_html=True)
with k2:
    st.markdown("**Rekomendasi** (interpretasi penyusun)")
    st.markdown(f"""<ol class="notes">
<li><b>Pemasar dan pengembang:</b> kolaborasi dengan {top.game} dan {kedua.game} menjangkau pemain terbanyak ({idn(besar_tot)}%), tetapi persaingannya paling berat.</li>
<li><b>Game menengah:</b> {game.game[2]}, {game.game[3]}, dan {game.game[4]} terpaut relatif dekat ({idn(game.persentase[2] - game.persentase[3])} dan {idn(game.persentase[3] - game.persentase[4])} poin), jadi peluang naik peringkat lebih realistis lewat diferensiasi daripada mengejar dua teratas.</li>
<li><b>Pembaca data:</b> jangan menyimpulkan urutan dari selisih di bawah ±1,1 poin. Analisis lanjutan butuh data demografi, durasi bermain, dan tren antar tahun.</li>
</ol>""", unsafe_allow_html=True)


# ====================== 06 Tentang data ======================
section("06", "Tentang data")
st.markdown(f"""
<ul class="src">
<li><b>Sumber data:</b> <a href="{SUMBER_URL}">Game Online Favorit Pengguna Internet Indonesia 2026</a>, GoodStats Data (11 Juni 2026),
berdasarkan Survei Penetrasi Internet Indonesia 2026 yang dirilis APJII (<a href="https://survei.apjii.or.id/">survei.apjii.or.id</a>).</li>
<li><b>Metodologi survei:</b> 1 Februari–15 Maret 2026, {idn(RESPONDEN, 0)} responden WNI berusia minimal 13 tahun di {PROVINSI} provinsi, wawancara langsung,
multistage random sampling, margin of error ±1,1%.</li>
<li><b>Konteks:</b> {idn(INTERNET_JUTA, 2)} juta pengguna internet dari {idn(POPULASI_JUTA, 2)} juta penduduk (penetrasi {idn(PENETRASI, 2)}%).</li>
<li><b>Lisensi:</b> tidak ada lisensi terbuka. Hak cipta ada pada GoodStats/APJII
(<a href="https://goodstats.id/page/aturan">aturan GoodStats</a>). Dipakai untuk keperluan belajar dengan mencantumkan sumber.</li>
<li><b>Keterbatasan:</b> hanya 8 baris ringkasan tanpa data responden. Margin of error ±1,1% berlaku untuk seluruh sampel, sedangkan pangsa game
dihitung dari subset pemain sehingga ketidakpastiannya lebih besar. Kelompok (Besar, Menengah, Kecil) adalah pengelompokan penyusun dashboard.</li>
</ul>
""", unsafe_allow_html=True)

tabel = semua.sort_values("persentase", ascending=False).copy()
tabel["kelompok"] = tabel.apply(lambda r: "Gabungan" if r.game == "Lainnya" else kelompok(r.persentase), axis=1)
with st.expander("Lihat dan unduh data bersih"):
    st.dataframe(tabel, hide_index=True, width="stretch", column_config={
        "game": "Game", "kelompok": "Kelompok",
        "persentase": st.column_config.ProgressColumn("Persentase (%)", min_value=0, max_value=50, format="%.1f")})
    st.download_button("Unduh CSV", tabel.to_csv(index=False).encode("utf-8"), "game_favorit_2026.csv", "text/csv")