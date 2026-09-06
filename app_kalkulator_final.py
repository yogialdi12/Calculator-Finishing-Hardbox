
import streamlit as st

st.set_page_config(
    page_title="Kalkulator Biaya Box - Bungkust.id",
    page_icon="📦",
    layout="wide"
)

# --- CSS ADAPTIF LIGHT & DARK MODE + BRANDING BUNGKUST.ID ---
st.markdown("""
    <style>
    /* Styling dasar adaptif tema Light / Dark mode */
    :root {
        --brand-orange: #FF6B00;
        --brand-navy: #1E293B;
    }
    
    /* Header Container */
    .header-container {
        text-align: center;
        padding: 10px 0px 20px 0px;
        border-bottom: 2px solid var(--brand-orange);
        margin-bottom: 25px;
    }
    
    .brand-logo-text {
        font-size: 32px;
        font-weight: 800;
        color: var(--brand-orange) !important;
        letter-spacing: 1px;
        margin: 0;
        padding: 0;
    }
    
    .brand-subtitle {
        font-size: 16px;
        font-weight: 500;
        color: var(--text-color);
        opacity: 0.85;
        margin-top: 5px;
    }
    
    .brand-company {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-color);
        opacity: 0.65;
    }
    
    /* Summary Card Styling */
    .summary-card {
        background-color: rgba(255, 107, 0, 0.08);
        border-left: 5px solid var(--brand-orange);
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0px;
    }
    
    /* Footer Styling */
    .footer-container {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid rgba(128, 128, 128, 0.2);
    }
    
    .footer-brand {
        font-size: 15px;
        font-weight: 700;
        color: var(--brand-orange) !important;
    }
    
    .footer-credit {
        font-size: 13px;
        font-style: italic;
        color: var(--text-color);
        opacity: 0.75;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER BUNGKUST.ID (TANPA LOGO) ---
st.markdown("""
    <div class="header-container">
        <div class="brand-logo-text">Bungkust.id</div>
        <div class="brand-company">PT BUNGKUST KEMASAN INDONESIA</div>
        <div class="brand-subtitle">Kalkulator Biaya Finishing Hardbox</div>
    </div>
""", unsafe_allow_html=True)

def get_category_dim(p, l):
    max_dim = max(p, l)
    if max_dim <= 15: return 15
    elif max_dim <= 20: return 20
    elif max_dim <= 30: return 30
    elif max_dim <= 40: return 40
    elif max_dim <= 50: return 50
    else: return 60

def get_category_box(p, l, t):
    dim_cat = get_category_dim(p, l)
    if t <= 5: t_cat = 15
    elif t <= 10: t_cat = 20
    elif t <= 15: t_cat = 30
    elif t <= 20: t_cat = 40
    elif t <= 30: t_cat = 50
    else: t_cat = 60
    return max(dim_cat, t_cat)

def calc_cost(qty_input, price_per_pcs):
    return qty_input * price_per_pcs

# --- PRICING DICTIONARIES ---
price_lapis_dalam = {15: 300, 20: 400, 30: 500, 40: 600, 50: 700, 60: 1000}
price_lapis_luar = {15: 600, 20: 800, 30: 1000, 40: 1200, 50: 1400, 60: 2000}
price_board = {15: 200, 20: 250, 30: 300, 40: 500, 50: 700, 60: 1000}
price_board_mall = {15: 1000, 20: 1250, 30: 1500, 40: 1750, 50: 2000, 60: 2500}
price_assembly = {15: 300, 20: 500, 30: 700, 40: 900, 50: 1100, 60: 1500}
price_qc = {15: 100, 20: 200, 30: 300, 40: 400, 50: 500, 60: 600}
price_aksesoris = {"Pita": 500, "Mata ayam": 250, "Magnet": 100, "Handel": 500, "Custom": 1000}

with st.sidebar:
    st.header("⚙️ Pengaturan Qty")
    
    qty_order = st.number_input("Qty Order (Pesanan Bersih)", min_value=1, value=100)
    st.caption("Digunakan sebagai pembagi HPP per pcs.")
    
    st.divider()
    
    qty_lapisan = st.number_input("Qty untuk Lapisan (Global)", min_value=1, value=110)
    st.caption("Default Qty untuk Lapis Dalam & Lapis Luar.")
    
    st.divider()
    
    qty_board = st.number_input("Qty untuk Board & Lainnya (Sudah + Insheet)", min_value=1, value=100)
    st.caption("Mengalikan biaya Board, Assembly, QC, Aksesoris, & Mall.")

# --- 1. LAPIS DALAM ---
st.header("1. Lapis Dalam")
num_ld = st.number_input("Berapa lapisan dalam yang ingin dimasukkan?", min_value=0, value=1, step=1)
total_ld = 0

for i in range(int(num_ld)):
    st.markdown(f"**Lapis Dalam ke-{i+1}**")
    col1, col2 = st.columns(2)
    with col1:
        p = st.number_input(f"Panjang Lapis Dalam {i+1} (cm)", min_value=0.0, value=25.0, key=f"ld_p_{i}")
    with col2:
        l = st.number_input(f"Lebar Lapis Dalam {i+1} (cm)", min_value=0.0, value=35.0, key=f"ld_l_{i}")
    
    use_custom_qty_ld = st.checkbox(f"Gunakan Qty Custom untuk Lapis Dalam {i+1}?", key=f"ld_check_{i}")
    if use_custom_qty_ld:
        current_qty_ld = st.number_input(f"Qty Custom Lapis Dalam {i+1}", min_value=1, value=qty_lapisan, key=f"ld_custom_qty_{i}")
    else:
        current_qty_ld = qty_lapisan
        
    cat = get_category_dim(p, l)
    harga = price_lapis_dalam[cat]
    subtotal = calc_cost(current_qty_ld, harga)
    total_ld += subtotal
    st.write(f"👉 Kategori: **{cat}x{cat}** | Biaya/pcs: **Rp {harga:,}** | Subtotal: **Rp {subtotal:,}** (Dikali {current_qty_ld} pcs)")

st.info(f"**Total Keseluruhan Lapis Dalam: Rp {total_ld:,}**")
st.divider()

# --- 2. LAPIS LUAR ---
st.header("2. Lapis Luar")
num_ll = st.number_input("Berapa lapisan luar yang ingin dimasukkan?", min_value=0, value=1, step=1)
total_ll = 0

for i in range(int(num_ll)):
    st.markdown(f"**Lapis Luar ke-{i+1}**")
    col1, col2 = st.columns(2)
    with col1:
        p = st.number_input(f"Panjang Lapis Luar {i+1} (cm)", min_value=0.0, value=39.0, key=f"ll_p_{i}")
    with col2:
        l = st.number_input(f"Lebar Lapis Luar {i+1} (cm)", min_value=0.0, value=45.0, key=f"ll_l_{i}")
    
    use_custom_qty_ll = st.checkbox(f"Gunakan Qty Custom untuk Lapis Luar {i+1}?", key=f"ll_check_{i}")
    if use_custom_qty_ll:
        current_qty_ll = st.number_input(f"Qty Custom Lapis Luar {i+1}", min_value=1, value=qty_lapisan, key=f"ll_custom_qty_{i}")
    else:
        current_qty_ll = qty_lapisan
        
    cat = get_category_dim(p, l)
    harga = price_lapis_luar[cat]
    subtotal = calc_cost(current_qty_ll, harga)
    total_ll += subtotal
    st.write(f"👉 Kategori: **{cat}x{cat}** | Biaya/pcs: **Rp {harga:,}** | Subtotal: **Rp {subtotal:,}** (Dikali {current_qty_ll} pcs)")

st.info(f"**Total Keseluruhan Lapis Luar: Rp {total_ll:,}**")
st.divider()

# --- 3. PEMBENTUKAN BOARD ---
st.header("3. Pembentukan Board")
num_board = st.number_input("Berapa ukuran pembentukan board yang ingin dimasukkan?", min_value=0, value=1, step=1)
total_board = 0

for i in range(int(num_board)):
    st.markdown(f"**Board ke-{i+1}**")
    col1, col2 = st.columns(2)
    with col1:
        p = st.number_input(f"Panjang Board {i+1} (cm)", min_value=0.0, value=30.0, key=f"b_p_{i}")
    with col2:
        l = st.number_input(f"Lebar Board {i+1} (cm)", min_value=0.0, value=30.0, key=f"b_l_{i}")
    
    cat = get_category_dim(p, l)
    harga = price_board[cat]
    subtotal = calc_cost(qty_board, harga)
    total_board += subtotal
    st.write(f"👉 Kategori: **{cat}x{cat}** | Biaya/pcs: **Rp {harga:,}** | Subtotal: **Rp {subtotal:,}** (Dikali {qty_board} pcs)")

st.info(f"**Total Keseluruhan Pembentukan Board: Rp {total_board:,}**")
st.divider()

# --- 4 & 6. ASSEMBLY DAN QC ---
st.header("4 & 6. Assembly & QC Packing")
st.write("Masukkan ukuran Box Jadi (Panjang, Lebar, Tinggi)")
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    box_p = st.number_input("Panjang Box (cm)", min_value=0.0, value=20.0)
with col_a2:
    box_l = st.number_input("Lebar Box (cm)", min_value=0.0, value=20.0)
with col_a3:
    box_t = st.number_input("Tinggi Box (cm)", min_value=0.0, value=10.0)

cat_box = get_category_box(box_p, box_l, box_t)
harga_ass = price_assembly[cat_box]
total_ass = calc_cost(qty_board, harga_ass)

harga_qc = price_qc[cat_box]
total_qc = calc_cost(qty_board, harga_qc)

st.write(f"**Kategori Ukuran Box Assembly & QC: {cat_box}**")
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.info(f"**Total Biaya Assembly:** Rp {total_ass:,} (Biaya/pcs: Rp {harga_ass:,} | Dikali {qty_board} pcs)")
with col_res2:
    st.info(f"**Total Biaya QC & Packing:** Rp {total_qc:,} (Biaya/pcs: Rp {harga_qc:,} | Dikali {qty_board} pcs)")

st.divider()

# --- 5. PEMASANGAN AKSESORIS ---
st.header("5. Pemasangan Aksesoris")
num_acc = st.number_input("Berapa jenis aksesoris yang ingin dimasukkan?", min_value=0, value=1, step=1)
total_acc = 0

for i in range(int(num_acc)):
    st.markdown(f"**Aksesoris ke-{i+1}**")
    col1, col2 = st.columns(2)
    with col1:
        acc_type = st.selectbox(f"Jenis Aksesoris {i+1}", list(price_aksesoris.keys()), key=f"acc_type_{i}")
    with col2:
        acc_freq = st.number_input(f"Jumlah/Frekuensi per Box (misal: 2 magnet)", min_value=1, value=1, key=f"acc_freq_{i}")
    
    harga_satuan = price_aksesoris[acc_type]
    subtotal_acc_pcs = harga_satuan * acc_freq
    subtotal_acc_total = calc_cost(qty_board, subtotal_acc_pcs)
    total_acc += subtotal_acc_total
    
    st.write(f"👉 Jenis: **{acc_type}** ({acc_freq} buah/box) | Biaya total/pcs: **Rp {subtotal_acc_pcs:,}** | Subtotal: **Rp {subtotal_acc_total:,}** (Dikali {qty_board} pcs)")

st.info(f"**Total Keseluruhan Aksesoris: Rp {total_acc:,}**")
st.divider()

# --- 7. BIAYA MALL (JIKA QTY DIBAWAH 200 PCS) ---
st.header("7. Biaya Mall (Khusus Qty di Bawah 200 pcs)")
total_mall = 0

if qty_board < 200:
    st.warning(f"⚠️ Qty Board & Lainnya ({qty_board} pcs) berada **di bawah 200 pcs**, sehingga biaya Mall diaktifkan otomatis.")
    num_mall = st.number_input("Berapa ukuran mall yang ingin dimasukkan?", min_value=0, value=1, step=1)
    
    for i in range(int(num_mall)):
        st.markdown(f"**Mall ke-{i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            p = st.number_input(f"Panjang Mall {i+1} (cm)", min_value=0.0, value=30.0, key=f"mall_p_{i}")
        with col2:
            l = st.number_input(f"Lebar Mall {i+1} (cm)", min_value=0.0, value=30.0, key=f"mall_l_{i}")
        
        cat = get_category_dim(p, l)
        harga_mall = price_board_mall[cat]
        subtotal_mall = calc_cost(qty_board, harga_mall)
        total_mall += subtotal_mall
        st.write(f"👉 Kategori: **{cat}x{cat}** | Biaya Mall/pcs: **Rp {harga_mall:,}** | Subtotal: **Rp {subtotal_mall:,}** (Dikali {qty_board} pcs)")
    
    st.info(f"**Total Keseluruhan Biaya Mall: Rp {total_mall:,}**")
else:
    st.success(f"✅ Qty Board & Lainnya ({qty_board} pcs) **sudah mencapai atau lebih dari 200 pcs**, sehingga Biaya Mall otomatis **tidak ada (0)**.")

st.divider()

# --- GRAND TOTAL ---
grand_total = total_ld + total_ll + total_board + total_ass + total_qc + total_acc + total_mall

st.header("Ringkasan Biaya")
st.success(f"**GRAND TOTAL KESELURUHAN (Semua Proses): Rp {grand_total:,}**")
if qty_order > 0:
    grand_total_per_pcs = grand_total / qty_order
    st.warning(f"**Harga Pokok per Pcs Jadi (Dibagi Qty Order {qty_order} pcs): Rp {grand_total_per_pcs:,.2f}**")

# --- FOOTER & CREDIT ADAPTIF ---
st.markdown("""
    <div class="footer-container">
        <p class="footer-brand">
            Bungkust.id - Packaging Production Management
        </p>
        <p class="footer-credit">
            Designed & Developed by Prayogi Aldiansyah Saputra
        </p>
    </div>
""", unsafe_allow_html=True)
