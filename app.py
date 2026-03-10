import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Simulateur SPOT France", page_icon="⚡", layout="wide")

st.title("⚡ Simulateur SPOT France - Merit Order")
st.markdown("Simulation didactique du mécanisme de formation des prix **SPOT en France** (Day-Ahead) selon le modèle **Pay-as-Clear**.")

# --- Données des Fournisseurs ---
PRODUCER_CONFIGS = [
    {
        'id': 'sunPower', 'name': 'SunPower', 'color': '#FFD700',
        'portfolio': [
            {'type': 'Solaire', 'price_fixed': 0, 'default_volume': 2500}
        ]
    },
    {
        'id': 'ecoStream', 'name': 'EcoStream', 'color': '#2BD9AF',
        'portfolio': [
            {'type': 'Hydro (Fil de l\'eau)', 'price_range': [10, 20], 'default_volume': 4000, 'default_price': 10},
            {'type': 'Éolien', 'price_fixed': 0, 'default_volume': 2000}
        ]
    },
    {
        'id': 'megaCorp', 'name': 'MegaCorp', 'color': '#A28CFF',
        'portfolio': [
            {'type': 'Nucléaire', 'price_range': [30, 45], 'default_volume': 45000, 'default_price': 35},
            {'type': 'Éolien', 'price_fixed': 0, 'default_volume': 1000},
            {'type': 'Charbon', 'price_fixed': 120, 'default_volume': 1500},
            {'type': 'Fioul', 'price_fixed': 150, 'default_volume': 2000},
            {'type': 'Gaz (CCGT)', 'price_fixed': 500, 'default_volume': 5000},
            {'type': 'Secours (TAC)', 'price_fixed': 3000, 'default_volume': 1500}
        ]
    },
    {
        'id': 'hydroFlex', 'name': 'HydroFlex', 'color': '#3B82F6',
        'portfolio': [
            {'type': 'Hydro (Lacs)', 'price_range': [60, 90], 'default_volume': 8000, 'default_price': 75},
            {'type': 'Gaz (Pointe)', 'price_fixed': 500, 'default_volume': 4000}
        ]
    }
]

# --- UI Sidebar ---
st.sidebar.header("Réglages du Marché")
demand = st.sidebar.number_input("Demande Globale (MW)", min_value=0, value=55000, step=1000)

st.sidebar.markdown("---")
st.sidebar.header("Carnet d'Ordres (Producteurs)")

orders = []

for provider in PRODUCER_CONFIGS:
    with st.sidebar.expander(provider['name'], expanded=False):
        for asset in provider['portfolio']:
            st.markdown(f"**{asset['type']}**")
            col1, col2 = st.columns(2)
            
            # Volume
            vol = col1.number_input(
                "Vol (MW)", 
                min_value=0, 
                value=asset['default_volume'], 
                step=100, 
                key=f"vol_{provider['id']}_{asset['type']}"
            )
            
            # Price
            if 'price_fixed' in asset:
                price = asset['price_fixed']
                col2.number_input(
                    "Prix (€)", 
                    value=float(price), 
                    disabled=True, 
                    key=f"px_{provider['id']}_{asset['type']}"
                )
            else:
                default_p = float(asset.get('default_price', asset['price_range'][0]))
                price = col2.number_input(
                    "Prix (€)", 
                    min_value=0.0, 
                    value=default_p, 
                    step=1.0, 
                    key=f"px_{provider['id']}_{asset['type']}"
                )
            
            if vol > 0:
                orders.append({
                    'Fournisseur': provider['name'],
                    'Couleur': provider['color'],
                    'Type': asset['type'],
                    'Volume (MW)': vol,
                    'Prix (€/MWh)': price
                })

# --- Order Book Processing (Pandas) ---
if not orders:
    st.warning("Le carnet d'ordres est complètement vide.")
    st.stop()

df = pd.DataFrame(orders)
# Tri (Merit Order)
dff = df.sort_values(by='Prix (€/MWh)', ascending=True).reset_index(drop=True)
# Calcul Cumulé
dff['Volume Cumulé (MW)'] = dff['Volume (MW)'].cumsum()

# --- Moteur de Clearing ---
total_supply = dff['Volume (MW)'].sum()
clearing_price = 0
clearing_volume = 0
is_shortage = False

if demand > total_supply:
    clearing_price = 3000
    clearing_volume = total_supply
    is_shortage = True
else:
    # Intersection
    cleared_df = dff[dff['Volume Cumulé (MW)'] >= demand]
    if not cleared_df.empty:
        clearing_price = cleared_df.iloc[0]['Prix (€/MWh)']
        clearing_volume = demand

# --- Affichage des Métriques ---
st.markdown("### Résultats du Marché (Clearing)")
col1, col2, col3 = st.columns(3)

if is_shortage:
    col1.metric("Prix d'Équilibre", "MAX (Pénurie)", delta="Capacité Insuffisante", delta_color="inverse")
else:
    col1.metric("Prix d'Équilibre", f"{clearing_price:,.2f} €/MWh")

col2.metric("Volume Échangé", f"{clearing_volume:,.0f} MW")
col3.metric("Capacité Totale Disponible", f"{total_supply:,.0f} MW")

st.markdown("---")

# --- Graphique Plotly (Merit Order) ---
st.markdown("### Graphique Merit Order")

# On génère les points en escalier (x=Volume, y=Prix)
x_hv = [0] + dff['Volume Cumulé (MW)'].tolist()
y_hv = [dff.iloc[0]['Prix (€/MWh)']] + dff['Prix (€/MWh)'].tolist()

fig = go.Figure()

# Courbe d'Offre (escalier h-v)
fig.add_trace(go.Scatter(
    x=x_hv, 
    y=y_hv,
    mode='lines',
    line_shape='hv', # Graphique en escalier natif
    name="Offre (Centrales)",
    fill='tozeroy',
    fillcolor='rgba(162, 140, 255, 0.2)',
    line=dict(color='#A28CFF', width=2)
))

# Demande (Ligne verticale pointillée)
max_p = max(500, clearing_price * 1.5)
fig.add_trace(go.Scatter(
    x=[demand, demand],
    y=[0, max_p],
    mode='lines',
    name="Demande",
    line=dict(color='#ADFF2F', width=3, dash='dash')
))

fig.update_layout(
    xaxis_title="Volume Cumulé (MW)",
    yaxis_title="Prix (€/MWh)",
    template="plotly_dark",
    hovermode="x unified",
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# --- Tableau des Données ---
with st.expander("Voir les données brutes de la journée (Carnet Aplatit)"):
    st.dataframe(
        dff[['Fournisseur', 'Type', 'Volume (MW)', 'Prix (€/MWh)', 'Volume Cumulé (MW)']], 
        use_container_width=True
    )
