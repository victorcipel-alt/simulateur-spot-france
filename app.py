import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Simulateur SPOT France", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJECTION CSS PERSONNALISÉ (Clone Design HTML) ---
st.markdown("""
<style>
    /* Variables et Background */
    :root {
        --bg-main: #0D1110;
        --bg-darker: #0B0D0C;
        --card-bg: #161B1A;
        --accent-primary: #ADFF2F;
        --text-main: #FFFFFF;
    }
    
    .stApp {
        background: radial-gradient(circle at top left, var(--bg-main), var(--bg-darker));
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }
    
    /* Cacher les headers Streamlit par défaut */
    header { visibility: hidden; }
    
    /* Metrics Styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(173,255,47,0.1) 0%, rgba(122,204,30,0.1) 100%);
        border: 1px solid rgba(173,255,47,0.3);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(173,255,47,0.05);
    }
    div[data-testid="metric-container"] > div > div > div {
        color: var(--text-main) !important;
    }
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-weight: 600;
        font-size: 1rem;
    }

    /* Boutons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important;
        padding: 8px 24px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #ADFF2F !important;
        box-shadow: 0 0 10px rgba(173, 255, 47, 0.2) !important;
    }
    
    /* Sidebar Focus */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE (Pour les boutons Aléatoires) ---
if 'demand' not in st.session_state:
    st.session_state.demand = 55000

PRODUCER_CONFIGS = [
    {
        'id': 'sunPower', 'name': 'SunPower', 'color': '#FFD700',
        'portfolio': [ {'type': 'Solaire', 'price_range': [0, 0], 'default_vol': 2500, 'default_price': 0} ]
    },
    {
        'id': 'ecoStream', 'name': 'EcoStream', 'color': '#2BD9AF',
        'portfolio': [
            {'type': 'Hydro (Fil de l\'eau)', 'price_range': [10, 20], 'default_vol': 4000, 'default_price': 10},
            {'type': 'Éolien', 'price_range': [0, 0], 'default_vol': 2000, 'default_price': 0}
        ]
    },
    {
        'id': 'megaCorp', 'name': 'MegaCorp', 'color': '#A28CFF',
        'portfolio': [
            {'type': 'Nucléaire', 'price_range': [30, 45], 'default_vol': 45000, 'default_price': 35},
            {'type': 'Éolien', 'price_range': [0, 0], 'default_vol': 1000, 'default_price': 0},
            {'type': 'Charbon', 'price_fixed': 120, 'default_vol': 1500, 'default_price': 120},
            {'type': 'Fioul', 'price_fixed': 150, 'default_vol': 2000, 'default_price': 150},
            {'type': 'Gaz (CCGT)', 'price_fixed': 500, 'default_vol': 5000, 'default_price': 500},
            {'type': 'Secours (TAC)', 'price_fixed': 3000, 'default_vol': 1500, 'default_price': 3000}
        ]
    },
    {
        'id': 'hydroFlex', 'name': 'HydroFlex', 'color': '#3B82F6',
        'portfolio': [
            {'type': 'Hydro (Lacs)', 'price_range': [60, 90], 'default_vol': 8000, 'default_price': 75},
            {'type': 'Gaz (Pointe)', 'price_fixed': 500, 'default_vol': 4000, 'default_price': 500}
        ]
    }
]

if 'provider_vols' not in st.session_state:
    st.session_state.provider_vols = {}
    st.session_state.provider_prices = {}
    for p in PRODUCER_CONFIGS:
        for a in p['portfolio']:
            st.session_state.provider_vols[f"{p['id']}_{a['type']}"] = a['default_vol']
            st.session_state.provider_prices[f"{p['id']}_{a['type']}"] = a['default_price']

# --- BOUTONS ALÉATOIRES (Callables) ---
def random_demand():
    st.session_state.demand = random.randint(40000, 85000)

def random_orders():
    for p in PRODUCER_CONFIGS:
        for a in p['portfolio']:
            k_vol = f"{p['id']}_{a['type']}"
            k_px = f"{p['id']}_{a['type']}"
            
            # Prix aléatoire
            pmin, pmax = a.get('price_range', [a.get('price_fixed', 0), a.get('price_fixed', 0)])
            st.session_state.provider_prices[k_px] = random.uniform(pmin, pmax) if pmin != pmax else pmin
            
            # Volume aléatoire
            if a['type'] == 'Solaire':
                vol = random.randint(1000, 4000)
            elif a['type'] == 'Éolien' and p['id'] == 'ecoStream':
                vol = random.randint(1000, 3000)
            elif a['type'] == 'Éolien' and p['id'] == 'megaCorp':
                vol = random.randint(500, 1500)
            elif a['type'] == 'Nucléaire':
                vol = random.randint(40000, 50000)
            elif 'Hydro' in a['type']:
                vol = int(a['default_vol'] * random.uniform(0.9, 1.05))
            else:
                variation = a['default_vol'] * 0.2
                vol = int(a['default_vol'] + random.uniform(-variation, variation))
            
            # Pannes aléatoires
            if a['type'] in ['Charbon', 'Fioul', 'Gaz (CCGT)'] and random.random() < 0.1:
                vol = 0
                
            st.session_state.provider_vols[k_vol] = vol

# --- LAYOUT PRINCIPAL ---
st.title("⚡ Simulateur SPOT France")
st.markdown("Formation du prix d'équilibre (Mécanisme **Pay-as-Clear**)")

col_main, col_side = st.columns([2.5, 1], gap="large")

# --- SIDEBAR (Carnet d'Ordres & Inputs) ---
with st.sidebar:
    st.header("1. Demande Réseau")
    c1, c2 = st.columns([2, 1])
    d_input = c1.number_input("Volume (MW)", min_value=0, value=st.session_state.demand, step=500, key="dem_input_ui")
    if d_input != st.session_state.demand:
        st.session_state.demand = d_input
        
    c2.button("🎲 Aléatoire", on_click=random_demand, use_container_width=True, key="btn_rand_dem")
    
    st.markdown("---")
    c_ord1, c_ord2 = st.columns([2, 1])
    c_ord1.header("2. Carnet d'Ordres")
    c_ord2.button("🎲 Aléatoire", on_click=random_orders, use_container_width=True, key="btn_rand_ord")
    
    active_orders = []
    
    for provider in PRODUCER_CONFIGS:
        with st.expander(f"🏢 {provider['name']}", expanded=False):
            st.markdown(f"<div style='height:4px; width:100%; background:{provider['color']}; margin-bottom:10px; border-radius:2px;'></div>", unsafe_allow_html=True)
            for asset in provider['portfolio']:
                k_vol = f"{provider['id']}_{asset['type']}"
                k_px = f"{provider['id']}_{asset['type']}"
                
                c_vol, c_px = st.columns(2)
                vol_val = c_vol.number_input(
                    f"{asset['type']} (MW)", 
                    min_value=0, 
                    value=st.session_state.provider_vols[k_vol], 
                    step=100,
                    key=f"ui_vol_{k_vol}"
                )
                
                is_fixed = 'price_fixed' in asset
                px_val = c_px.number_input(
                    f"Prix (€)", 
                    min_value=0.0, 
                    value=float(st.session_state.provider_prices[k_px]), 
                    step=1.0, 
                    disabled=is_fixed,
                    key=f"ui_px_{k_px}"
                )
                
                st.session_state.provider_vols[k_vol] = vol_val
                if not is_fixed: st.session_state.provider_prices[k_px] = px_val
                
                if vol_val > 0:
                    active_orders.append({
                        'Fournisseur': provider['name'],
                        'Couleur': provider['color'],
                        'Type': asset['type'],
                        'Volume (MW)': vol_val,
                        'Prix (€/MWh)': float(px_val if not is_fixed else asset['price_fixed'])
                    })

# --- MOTEUR PANDAS ---
demand_active = st.session_state.demand

if not active_orders:
    st.warning("Aucun producteur actif.")
    st.stop()

df = pd.DataFrame(active_orders)
dff = df.sort_values(by='Prix (€/MWh)', ascending=True).reset_index(drop=True)
dff['Volume Cumulé (MW)'] = dff['Volume (MW)'].cumsum()

total_supply = dff['Volume (MW)'].sum()
is_shortage = demand_active > total_supply

if is_shortage:
    clearing_price = 3000
    clearing_volume = total_supply
else:
    cleared = dff[dff['Volume Cumulé (MW)'] >= demand_active]
    clearing_price = cleared.iloc[0]['Prix (€/MWh)']
    clearing_volume = demand_active

# --- AFFICHAGE MAIN CONTENT ---
with col_side:
    st.markdown("### 📊 Résultats SPOT (J-1)")
    
    if is_shortage:
        st.metric("Prix d'Équilibre", "MAX (3000 €)", delta="Pénurie Réseau", delta_color="inverse")
    else:
        st.metric("Prix d'Équilibre", f"{clearing_price:,.2f} €/MWh")
        
    st.metric("Volume Échangé", f"{clearing_volume:,.0f} MW")
    st.metric("Capacité Disponible", f"{total_supply:,.0f} MW")
    
    st.markdown("---")
    st.markdown("### Mix Énergétique")
    
    # Mix Chart (Donut)
    df_mix = df.groupby(['Fournisseur', 'Couleur'])['Volume (MW)'].sum().reset_index()
    fig_mix = go.Figure(data=[go.Pie(
        labels=df_mix['Fournisseur'], 
        values=df_mix['Volume (MW)'],
        hole=.7,
        marker_colors=df_mix['Couleur'],
        textinfo='none'
    )])
    fig_mix.update_layout(
        showlegend=True, 
        template="plotly_dark", 
        margin=dict(t=0, b=0, l=0, r=0),
        height=250,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1)
    )
    st.plotly_chart(fig_mix, use_container_width=True)

with col_main:
    st.markdown("### Courbe d'Ordres (Merit Order)")
    
    x_hv = [0] + dff['Volume Cumulé (MW)'].tolist()
    y_hv = [dff.iloc[0]['Prix (€/MWh)']] + dff['Prix (€/MWh)'].tolist()

    fig = go.Figure()

    # Offre (Escalier)
    fig.add_trace(go.Scatter(
        x=x_hv, y=y_hv, mode='lines', line_shape='hv',
        name="Offre", fill='tozeroy', fillcolor='rgba(255, 255, 255, 0.05)',
        line=dict(color='#FFFFFF', width=2)
    ))

    # Demande (Verticale)
    max_p = max(500, clearing_price + 100)
    fig.add_trace(go.Scatter(
        x=[demand_active, demand_active],
        y=[0, max_p],
        mode='lines',
        name="Demande",
        line=dict(color='#ADFF2F', width=2, dash='dash')
    ))

    fig.update_layout(
        xaxis_title="Volume Cumulé (MW)", yaxis_title="Prix (€/MWh)",
        template="plotly_dark", hovermode="x unified",
        margin=dict(l=0, r=0, t=10, b=40),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Simulateur SPOT France", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJECTION CSS PERSONNALISÉ (Clone Design HTML) ---
st.markdown("""
<style>
    /* Variables et Background */
    :root {
        --bg-main: #0D1110;
        --bg-darker: #0B0D0C;
        --card-bg: #161B1A;
        --accent-primary: #ADFF2F;
        --text-main: #FFFFFF;
    }
    
    .stApp {
        background: radial-gradient(circle at top left, var(--bg-main), var(--bg-darker));
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }
    
    /* Cacher les headers Streamlit par défaut */
    header { visibility: hidden; }
    
    /* Metrics Styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(173,255,47,0.1) 0%, rgba(122,204,30,0.1) 100%);
        border: 1px solid rgba(173,255,47,0.3);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(173,255,47,0.05);
    }
    div[data-testid="metric-container"] > div > div > div {
        color: var(--text-main) !important;
    }
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-weight: 600;
        font-size: 1rem;
    }

    /* Boutons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important;
        padding: 8px 24px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #ADFF2F !important;
        box-shadow: 0 0 10px rgba(173, 255, 47, 0.2) !important;
    }
    
    /* Sidebar Focus */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE (Pour les boutons Aléatoires) ---
if 'demand' not in st.session_state:
    st.session_state.demand = 55000

PRODUCER_CONFIGS = [
    {
        'id': 'sunPower', 'name': 'SunPower', 'color': '#FFD700',
        'portfolio': [ {'type': 'Solaire', 'price_range': [0, 0], 'default_vol': 2500, 'default_price': 0} ]
    },
    {
        'id': 'ecoStream', 'name': 'EcoStream', 'color': '#2BD9AF',
        'portfolio': [
            {'type': 'Hydro (Fil de l\'eau)', 'price_range': [10, 20], 'default_vol': 4000, 'default_price': 10},
            {'type': 'Éolien', 'price_range': [0, 0], 'default_vol': 2000, 'default_price': 0}
        ]
    },
    {
        'id': 'megaCorp', 'name': 'MegaCorp', 'color': '#A28CFF',
        'portfolio': [
            {'type': 'Nucléaire', 'price_range': [30, 45], 'default_vol': 45000, 'default_price': 35},
            {'type': 'Éolien', 'price_range': [0, 0], 'default_vol': 1000, 'default_price': 0},
            {'type': 'Charbon', 'price_fixed': 120, 'default_vol': 1500, 'default_price': 120},
            {'type': 'Fioul', 'price_fixed': 150, 'default_vol': 2000, 'default_price': 150},
            {'type': 'Gaz (CCGT)', 'price_fixed': 500, 'default_vol': 5000, 'default_price': 500},
            {'type': 'Secours (TAC)', 'price_fixed': 3000, 'default_vol': 1500, 'default_price': 3000}
        ]
    },
    {
        'id': 'hydroFlex', 'name': 'HydroFlex', 'color': '#3B82F6',
        'portfolio': [
            {'type': 'Hydro (Lacs)', 'price_range': [60, 90], 'default_vol': 8000, 'default_price': 75},
            {'type': 'Gaz (Pointe)', 'price_fixed': 500, 'default_vol': 4000, 'default_price': 500}
        ]
    }
]

if 'provider_vols' not in st.session_state:
    st.session_state.provider_vols = {}
    st.session_state.provider_prices = {}
    for p in PRODUCER_CONFIGS:
        for a in p['portfolio']:
            st.session_state.provider_vols[f"{p['id']}_{a['type']}"] = a['default_vol']
            st.session_state.provider_prices[f"{p['id']}_{a['type']}"] = a['default_price']

# --- BOUTONS ALÉATOIRES (Callables) ---
def random_demand():
    st.session_state.demand = random.randint(40000, 85000)

def random_orders():
    for p in PRODUCER_CONFIGS:
        for a in p['portfolio']:
            k_vol = f"{p['id']}_{a['type']}"
            k_px = f"{p['id']}_{a['type']}"
            
            # Prix aléatoire
            pmin, pmax = a.get('price_range', [a.get('price_fixed', 0), a.get('price_fixed', 0)])
            st.session_state.provider_prices[k_px] = random.uniform(pmin, pmax) if pmin != pmax else pmin
            
            # Volume aléatoire
            if a['type'] == 'Solaire':
                vol = random.randint(1000, 4000)
            elif a['type'] == 'Éolien' and p['id'] == 'ecoStream':
                vol = random.randint(1000, 3000)
            elif a['type'] == 'Éolien' and p['id'] == 'megaCorp':
                vol = random.randint(500, 1500)
            elif a['type'] == 'Nucléaire':
                vol = random.randint(40000, 50000)
            elif 'Hydro' in a['type']:
                vol = int(a['default_vol'] * random.uniform(0.9, 1.05))
            else:
                variation = a['default_vol'] * 0.2
                vol = int(a['default_vol'] + random.uniform(-variation, variation))
            
            # Pannes aléatoires
            if a['type'] in ['Charbon', 'Fioul', 'Gaz (CCGT)'] and random.random() < 0.1:
                vol = 0
                
            st.session_state.provider_vols[k_vol] = vol

# --- LAYOUT PRINCIPAL ---
st.title("⚡ Simulateur SPOT France")
st.markdown("Formation du prix d'équilibre (Mécanisme **Pay-as-Clear**)")

col_main, col_side = st.columns([2.5, 1], gap="large")

# --- SIDEBAR (Carnet d'Ordres & Inputs) ---
with st.sidebar:
    st.header("1. Demande Réseau")
    c1, c2 = st.columns([2, 1])
    d_input = c1.number_input("Volume (MW)", min_value=0, value=st.session_state.demand, step=500, key="dem_input_ui")
    if d_input != st.session_state.demand:
        st.session_state.demand = d_input
        
    c2.button("🎲 Aléatoire", on_click=random_demand, use_container_width=True, key="btn_rand_dem")
    
    st.markdown("---")
    c_ord1, c_ord2 = st.columns([2, 1])
    c_ord1.header("2. Carnet d'Ordres")
    c_ord2.button("🎲 Aléatoire", on_click=random_orders, use_container_width=True, key="btn_rand_ord")
    
    active_orders = []
    
    for provider in PRODUCER_CONFIGS:
        with st.expander(f"🏢 {provider['name']}", expanded=False):
            st.markdown(f"<div style='height:4px; width:100%; background:{provider['color']}; margin-bottom:10px; border-radius:2px;'></div>", unsafe_allow_html=True)
            for asset in provider['portfolio']:
                k_vol = f"{provider['id']}_{asset['type']}"
                k_px = f"{provider['id']}_{asset['type']}"
                
                c_vol, c_px = st.columns(2)
                vol_val = c_vol.number_input(
                    f"{asset['type']} (MW)", 
                    min_value=0, 
                    value=st.session_state.provider_vols[k_vol], 
                    step=100,
                    key=f"ui_{k_vol}"
                )
                
                is_fixed = 'price_fixed' in asset
                px_val = c_px.number_input(
                    f"Prix (€)", 
                    min_value=0.0, 
                    value=float(st.session_state.provider_prices[k_px]), 
                    step=1.0, 
                    disabled=is_fixed,
                    key=f"ui_{k_px}"
                )
                
                st.session_state.provider_vols[k_vol] = vol_val
                if not is_fixed: st.session_state.provider_prices[k_px] = px_val
                
                if vol_val > 0:
                    active_orders.append({
                        'Fournisseur': provider['name'],
                        'Couleur': provider['color'],
                        'Type': asset['type'],
                        'Volume (MW)': vol_val,
                        'Prix (€/MWh)': float(px_val if not is_fixed else asset['price_fixed'])
                    })

# --- MOTEUR PANDAS ---
demand_active = st.session_state.demand

if not active_orders:
    st.warning("Aucun producteur actif.")
    st.stop()

df = pd.DataFrame(active_orders)
dff = df.sort_values(by='Prix (€/MWh)', ascending=True).reset_index(drop=True)
dff['Volume Cumulé (MW)'] = dff['Volume (MW)'].cumsum()

total_supply = dff['Volume (MW)'].sum()
is_shortage = demand_active > total_supply

if is_shortage:
    clearing_price = 3000
    clearing_volume = total_supply
else:
    cleared = dff[dff['Volume Cumulé (MW)'] >= demand_active]
    clearing_price = cleared.iloc[0]['Prix (€/MWh)']
    clearing_volume = demand_active

# --- AFFICHAGE MAIN CONTENT ---
with col_side:
    st.markdown("### 📊 Résultats SPOT (J-1)")
    
    if is_shortage:
        st.metric("Prix d'Équilibre", "MAX (3000 €)", delta="Pénurie Réseau", delta_color="inverse")
    else:
        st.metric("Prix d'Équilibre", f"{clearing_price:,.2f} €/MWh")
        
    st.metric("Volume Échangé", f"{clearing_volume:,.0f} MW")
    st.metric("Capacité Disponible", f"{total_supply:,.0f} MW")
    
    st.markdown("---")
    st.markdown("### Mix Énergétique")
    
    # Mix Chart (Donut)
    df_mix = df.groupby(['Fournisseur', 'Couleur'])['Volume (MW)'].sum().reset_index()
    fig_mix = go.Figure(data=[go.Pie(
        labels=df_mix['Fournisseur'], 
        values=df_mix['Volume (MW)'],
        hole=.7,
        marker_colors=df_mix['Couleur'],
        textinfo='none'
    )])
    fig_mix.update_layout(
        showlegend=True, 
        template="plotly_dark", 
        margin=dict(t=0, b=0, l=0, r=0),
        height=250,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1)
    )
    st.plotly_chart(fig_mix, use_container_width=True)

with col_main:
    st.markdown("### Courbe d'Ordres (Merit Order)")
    
    x_hv = [0] + dff['Volume Cumulé (MW)'].tolist()
    y_hv = [dff.iloc[0]['Prix (€/MWh)']] + dff['Prix (€/MWh)'].tolist()

    fig = go.Figure()

    # Offre (Escalier)
    fig.add_trace(go.Scatter(
        x=x_hv, y=y_hv, mode='lines', line_shape='hv',
        name="Offre", fill='tozeroy', fillcolor='rgba(255, 255, 255, 0.05)',
        line=dict(color='#FFFFFF', width=2)
    ))

    # Demande (Verticale)
    max_p = max(500, clearing_price + 100)
    fig.add_trace(go.Scatter(
        x=[demand_active, demand_active],
        y=[0, max_p],
        mode='lines',
        name="Demande",
        line=dict(color='#ADFF2F', width=2, dash='dash')
    ))

    fig.update_layout(
        xaxis_title="Volume Cumulé (MW)", yaxis_title="Prix (€/MWh)",
        template="plotly_dark", hovermode="x unified",
        margin=dict(l=0, r=0, t=10, b=40),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

