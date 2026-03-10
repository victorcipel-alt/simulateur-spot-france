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

# --- INJECTION CSS PERSONNALISÉ ---
st.markdown("""
<style>
    :root {
        --bg-main: #0D1110;
        --bg-darker: #0B0D0C;
        --card-bg: #161B1A;
        --accent-primary: #ADFF2F;
        --accent-tertiary: #2BD9AF;
    }
    
    .stApp {
        background: radial-gradient(circle at top left, var(--bg-main), var(--bg-darker));
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    header { visibility: hidden; }
    
    /* Metrics Styling (Résultats SPOT): fond transparent, texte blanc, encadré vert */
    div[data-testid="metric-container"] {
        background-color: transparent !important;
        border: 2px solid #ADFF2F !important;
        border-radius: 8px !important;
        padding: 15px !important;
        box-shadow: 0 4px 15px rgba(173,255,47,0.1) !important;
    }
    div[data-testid="metric-container"] > div {
        color: #FFFFFF !important;
    }
    div[data-testid="metric-container"] > div > div {
        color: #FFFFFF !important;
    }
    div[data-testid="metric-container"] > div > div > div {
        color: #FFFFFF !important;
    }
    div[data-testid="metric-container"] label {
        color: #FFFFFF !important;
        font-weight: bold;
        font-size: 1.1rem;
    }

    /* Boutons personnalisés (Ajustés pour ne pas déborder dans la sidebar) */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        transition: all 0.3s ease;
        padding-top: 5px;
        padding-bottom: 5px;
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: #ADFF2F;
        color: #ADFF2F;
    }

    #btn-guide > button {
        background: var(--accent-tertiary) !important;
        color: black !important;
        border: none !important;
        font-weight: bold;
    }
    
    /* Sidebar Focus */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- DONNÉES DES FOURNISSEURS ---
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

# --- INIT SESSION STATE ---
if 'ui_demande_globale' not in st.session_state:
    st.session_state.ui_demande_globale = 55000

for p in PRODUCER_CONFIGS:
    for a in p['portfolio']:
        k_vol = f"vol_{p['id']}_{a['type']}"
        k_px = f"px_{p['id']}_{a['type']}"
        if k_vol not in st.session_state:
            st.session_state[k_vol] = a['default_vol']
        if k_px not in st.session_state:
            st.session_state[k_px] = float(a.get('default_price', a.get('price_fixed', 0)))

# --- FONCTIONS CALLABLES (Boutons Aléatoires) ---
# Pour que les boutons Streamlit mettent à jour les Inputs, 
# la fonction doit modifier directement les variables du session_state liées aux `key=` des widgets.
def random_demand():
    st.session_state.ui_demande_globale = random.randint(40000, 85000)

def random_orders():
    for p in PRODUCER_CONFIGS:
        for a in p['portfolio']:
            k_vol = f"vol_{p['id']}_{a['type']}"
            k_px = f"px_{p['id']}_{a['type']}"
            
            pmin, pmax = a.get('price_range', [a.get('price_fixed', 0), a.get('price_fixed', 0)])
            st.session_state[k_px] = float(random.uniform(pmin, pmax) if pmin != pmax else pmin)
            
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
            
            if a['type'] in ['Charbon', 'Fioul', 'Gaz (CCGT)'] and random.random() < 0.1:
                vol = 0
                
            st.session_state[k_vol] = int(vol)

# --- HEADER & GUIDE MODAL ---
c_title, c_btn = st.columns([5, 1])
with c_title:
    st.title("⚡ Simulateur SPOT France")
    st.markdown("Formation du prix d'équilibre (Mécanisme **Pay-as-Clear**)")

with c_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("❓ Guide d'emploi", use_container_width=True):
        st.session_state.show_guide = not st.session_state.get('show_guide', False)

if st.session_state.get('show_guide', False):
    st.info("""
    **Bienvenue ! Ce site simule de façon interactive le mécanisme de formation des prix SPOT en France (marché Day-Ahead).**

    **Comment utiliser l'interface ?**
    1. **Gérer la Demande :** Saisissez manuellement un volume à gauche, ou cliquez sur "Scénario Aléatoire" pour simuler une consommation réaliste (du creux d'été à la pointe d'hiver).
    2. **Observer l'Offre :** Le carnet d'ordres liste les centrales à droite. Cliquez sur "Ordres Aléatoires" (icône tournante) pour simuler la disponibilité des énergies au quotidien (panne nucléaire, fort vent, etc).
    3. **Analyser le Prix (Clearing) :** Le graphique Merit Order se met à jour en direct. Le marché empile les offres de la moins chère (Solaire/Éolien) à la plus chère (Gaz/Secours). Le croisement avec la demande détermine le Prix d'Équilibre.
    4. **Tester des cas extrêmes :** Modifiez manuellement le volume (MW) ou le prix proposé (€) de n'importe quelle énergie du carnet d'ordres pour manipuler la courbe économique.
    
    **La Méthode Pay-as-Clear**
    C'est la règle européenne : l'outil empile les vendeurs en commençant par les Énergies Renouvelables (proposées à 0€ et prioritaires) jusqu'à ce que la demande soit couverte. Le prix marginal de la toute dernière centrale électrique allumée fixe le prix au mégawatt pour tout le monde ce jour-là.
    """)

# --- LAYOUT PRINCIPAL ---
col_main, col_side = st.columns([2.5, 1], gap="large")

# --- SIDEBAR (Carnet d'Ordres & Inputs) ---
with st.sidebar:
    st.header("1. Demande Réseau")
    st.number_input("Volume (MW)", min_value=0, step=500, key="ui_demande_globale")
    st.button("🎲 Demande Aléatoire", on_click=random_demand, use_container_width=True)
    
    st.markdown("---")
    st.header("2. Carnet d'Ordres")
    st.button("🎲 Ordres Aléatoires", on_click=random_orders, use_container_width=True)
    
    active_orders = []
    
    for provider in PRODUCER_CONFIGS:
        with st.expander(f"🏢 {provider['name']}", expanded=True if provider['id'] == 'sunPower' else False):
            st.markdown(f"<div style='height:4px; width:100%; background:{provider['color']}; margin-bottom:10px; border-radius:2px;'></div>", unsafe_allow_html=True)
            for asset in provider['portfolio']:
                k_vol = f"vol_{provider['id']}_{asset['type']}"
                k_px = f"px_{provider['id']}_{asset['type']}"
                
                c_vol, c_px = st.columns(2)
                vol_val = c_vol.number_input(f"{asset['type']} (MW)", min_value=0, step=100, key=k_vol)
                px_val = c_px.number_input(f"Prix (€)", min_value=0.0, step=1.0, disabled=('price_fixed' in asset), key=k_px)
                
                if vol_val > 0:
                    active_orders.append({
                        'Fournisseur': provider['name'],
                        'Couleur': provider['color'],
                        'Type': asset['type'],
                        'Volume (MW)': vol_val,
                        'Prix (€/MWh)': float(px_val)
                    })

# --- MOTEUR PANDAS ---
demand_active = st.session_state.ui_demande_globale

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
    if not cleared.empty:
        clearing_price = cleared.iloc[0]['Prix (€/MWh)']
    else:
        clearing_price = 0
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
    
    # Mix Chart (Donut) sur fond blanc
    df_mix = df.groupby(['Fournisseur', 'Couleur'])['Volume (MW)'].sum().reset_index()
    fig_mix = go.Figure(data=[go.Pie(
        labels=df_mix['Fournisseur'], 
        values=df_mix['Volume (MW)'],
        hole=.6,
        marker_colors=df_mix['Couleur'],
        textfont=dict(color="black"),
    )])
    fig_mix.update_layout(
        showlegend=True, 
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(color="black"))
    )

    st.markdown("""<div style="background-color: white; padding: 10px; border-radius: 12px; border: 1px solid #ADFF2F;">""", unsafe_allow_html=True)
    st.plotly_chart(fig_mix, use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)

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
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

