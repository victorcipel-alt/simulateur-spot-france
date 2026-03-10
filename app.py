<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulateur SPOT France - Merit Order</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* --- Styles Fusionnés (styles.css + Ajustements responsive & Modale) --- */
         :root {
            /* Couleurs principales */
            --bg-main: #0D1110;
            --bg-darker: #0B0D0C;
            --card-bg: #161B1A;
            --glass-bg: rgba(22, 27, 26, 0.6);
            --glass-border: rgba(255, 255, 255, 0.05);

            /* Accents */
            --accent-primary: #ADFF2F;
            --accent-primary-hover: #98e624;
            --accent-secondary: #A28CFF;
            --accent-tertiary: #2BD9AF;

            /* Typographie */
            --text-main: #FFFFFF;
            --text-muted: #94A3B8;
            --text-dark: #000000;

            /* Géométrie */
            --radius-lg: 24px;
            --radius-md: 16px;
            --radius-sm: 8px;
            --radius-full: 9999px;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at top left, var(--bg-main), var(--bg-darker));
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            line-height: 1.5;
        }

        /* --- Layout --- */
        .app-container {
            display: grid;
            grid-template-columns: 1fr 400px;
            height: 100vh;
            gap: 24px;
            padding: 24px;
        }

        /* --- Main Content --- */
        .main-content {
            display: flex;
            flex-direction: column;
            gap: 24px;
            overflow-y: auto;
            padding-right: 8px;
        }
        .main-content::-webkit-scrollbar { width: 6px; }
        .main-content::-webkit-scrollbar-thumb {
            background: var(--card-bg);
            border-radius: var(--radius-full);
        }

        .header { display: flex; flex-direction: column; gap: 16px; }
        h1 { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; }
        h2 { font-size: 20px; font-weight: 600; }
        h3 { font-size: 18px; font-weight: 600; }
        .subtitle { font-size: 14px; color: var(--text-muted); }

        /* Chips */
        .filter-chips { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
        .chip {
            padding: 10px 20px;
            border-radius: var(--radius-full);
            background: var(--card-bg);
            color: var(--text-muted);
            border: 1px solid var(--glass-border);
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        .chip:hover { color: var(--text-main); background: rgba(255, 255, 255, 0.05); }
        .chip.active {
            background: var(--accent-primary);
            color: var(--text-dark);
            border-color: var(--accent-primary);
            box-shadow: 0 4px 15px rgba(173, 255, 47, 0.15);
        }
        .chip.btn-info {
            background: var(--accent-tertiary);
            color: var(--text-dark);
            border-color: var(--accent-tertiary);
            font-weight: 700;
            padding: 10px 24px;
            box-shadow: 0 4px 15px rgba(43, 217, 175, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
            transform: translateY(0);
        }
        .chip.btn-info:hover {
            background: #20c29b;
            color: var(--text-dark);
            transform: translateY(-2px);
        }

        /* Cards */
        .overlay-card {
            background: var(--card-bg);
            border-radius: var(--radius-lg);
            padding: 24px;
            border: 1px solid var(--glass-border);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .chart-section {
            flex: 1;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .chart-header { margin-bottom: 20px; flex-shrink: 0; }
        .chart-container { flex: 1; position: relative; width: 100%; min-height: 0; }
        .bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }

        /* Demand Section */
        .header-flex { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px;}
        .btn-secondary {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-main);
            border: 1px solid var(--glass-border);
            padding: 8px 16px;
            border-radius: var(--radius-full);
            font-size: 13px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .btn-secondary:hover { background: rgba(255, 255, 255, 0.1); }
        
        .input-group label { display: block; margin-bottom: 8px; color: var(--text-muted); font-size: 14px; }
        .input-wrapper { position: relative; display: flex; align-items: center; }
        .input-wrapper input {
            width: 100%;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--glass-border);
            color: var(--text-main);
            font-size: 24px;
            font-weight: 600;
            padding: 16px;
            border-radius: var(--radius-md);
            outline: none;
            font-family: inherit;
            transition: border-color 0.2s;
        }
        .input-wrapper input:focus { border-color: var(--accent-primary); }
        .input-wrapper .unit { position: absolute; right: 16px; color: var(--text-muted); font-weight: 500; }

        .demand-stats { display: flex; gap: 16px; margin-top: 20px; }
        .stat-item { background: rgba(0, 0, 0, 0.2); padding: 12px; border-radius: var(--radius-sm); flex: 1; }
        .stat-item .label { display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }
        .stat-item .value { font-size: 14px; font-weight: 600; }

        .mix-section { display: flex; flex-direction: column; }
        .donut-placeholder { flex: 1; position: relative; display: flex; align-items: center; justify-content: center; min-height: 200px; }

        /* --- Right Panel --- */
        .right-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .clearing-widget {
            background: linear-gradient(135deg, var(--accent-primary) 0%, #7acc1e 100%);
            border-radius: var(--radius-lg);
            padding: 24px;
            color: var(--text-dark);
            box-shadow: 0 10px 25px rgba(173, 255, 47, 0.15);
        }
        .clearing-widget h3 { margin-bottom: 16px; opacity: 0.8; }
        .price-display { display: flex; align-items: baseline; gap: 8px; margin-bottom: 16px; }
        .price-value { font-size: 48px; font-weight: 800; letter-spacing: -1px; line-height: 1; }
        .price-unit { font-size: 20px; font-weight: 600; opacity: 0.8; }
        .volume-display {
            display: flex;
            justify-content: space-between;
            background: rgba(0, 0, 0, 0.1);
            padding: 12px 16px;
            border-radius: var(--radius-md);
            font-weight: 500;
            font-size: 14px;
        }

        /* Carnet d'Ordres */
        .order-book { flex: 1; display: flex; flex-direction: column; min-height: 0;}
        .btn-icon {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);
            color: var(--text-main);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background 0.2s;
        }
        .btn-icon:hover { background: rgba(255, 255, 255, 0.1); }
        .transactions-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            overflow-y: auto;
            padding-right: 4px;
        }
        .producer-item {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid transparent;
            border-radius: var(--radius-md);
            padding: 16px;
            transition: border-color 0.2s;
        }
        .producer-item:hover { border-color: var(--glass-border); }
        .producer-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
        .producer-color { width: 12px; height: 12px; border-radius: 50%; }
        .producer-name { font-weight: 600; font-size: 15px; }
        
        .portfolio-card { padding: 12px 16px; }
        .portfolio-assets {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 8px;
            padding-top: 12px;
            border-top: 1px solid var(--glass-border);
        }
        .asset-row { display: flex; justify-content: space-between; align-items: center; padding: 4px 0; transition: all 0.3s; }
        .asset-row.inactive { opacity: 0.4; filter: grayscale(80%); }
        .asset-type { font-size: 13px; color: var(--text-main); font-weight: 500; flex: 1; }
        
        .asset-inputs { display: flex; gap: 8px; flex: 2; justify-content: flex-end; }
        .small-input-wrapper { position: relative; display: flex; align-items: center; width: 80px; }
        .small-input-wrapper input {
            width: 100%;
            background: var(--bg-darker);
            border: 1px solid var(--glass-border);
            color: var(--text-main);
            padding: 6px 24px 6px 8px;
            border-radius: var(--radius-sm);
            font-size: 12px;
            outline: none;
            transition: border-color 0.2s;
            text-align: right;
        }
        .small-input-wrapper input:focus { border-color: var(--accent-primary); }
        .unit-xs { position: absolute; right: 6px; font-size: 10px; color: var(--text-muted); pointer-events: none; }

        /* --- Modal --- */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: var(--card-bg);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 30px;
            width: 90%;
            max-width: 600px;
            color: var(--text-main);
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            position: relative;
        }
        .guide-scroll {
            max-height: 60vh;
            overflow-y: auto;
            padding-right: 15px;
        }
        .guide-scroll::-webkit-scrollbar { width: 6px; }
        .guide-scroll::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: var(--radius-full); }
        .guide-scroll h3 { color: var(--text-main); margin: 20px 0 10px 0; font-size: 16px; border-bottom: 1px solid var(--glass-border); padding-bottom: 5px; }
        .guide-list { list-style: none; padding-left: 0; }
        .guide-list li {
            margin-bottom: 15px;
            color: var(--text-muted);
            font-size: 14px;
            line-height: 1.5;
            padding-left: 20px;
            position: relative;
        }
        .guide-list li::before {
            content: "•";
            color: var(--accent-tertiary);
            position: absolute;
            left: 0;
            font-weight: bold;
        }
        .guide-list li strong { color: var(--text-main); }
        .modal-content h2 { margin-bottom: 15px; color: var(--accent-tertiary); font-size: 24px; }
        .modal-content p { margin-bottom: 15px; color: var(--text-muted); font-size: 15px; line-height: 1.6; }
        .close-modal {
            color: var(--text-muted);
            position: absolute;
            right: 20px;
            top: 20px;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }
        .close-modal:hover { color: #fff; }

        /* --- Responsiveness Mobile --- */
        @media (max-width: 1000px) {
            .app-container {
                grid-template-columns: 1fr;
                height: auto;
                min-height: 100vh;
                overflow-y: visible; /* La page scroll naturellement */
            }
            .right-panel {
                grid-column: 1 / -1;
            }
            .bottom-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="app-container">
        <!-- Main Content (Left Column) -->
        <main class="main-content">
            <header class="header">
                <h1>Spot Market Dashboard</h1>
                <div class="filter-chips">
                    <button class="chip active">J-1 (Day-Ahead)</button>
                    <button id="btn-info" class="chip btn-info">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                        Guide d'emploi
                    </button>
                </div>
            </header>

            <section class="chart-section overlay-card">
                <div class="chart-header">
                    <h2>Merit Order</h2>
                </div>
                <div class="chart-container">
                    <canvas id="meritOrderChart"></canvas>
                </div>
            </section>

            <div class="bottom-grid">
                <!-- Demande Control Panel -->
                <section class="demand-section overlay-card">
                    <div class="header-flex">
                        <h2>Demande</h2>
                        <button id="btn-random-demand" class="btn-secondary" aria-label="Générer une demande aléatoire">
                            Scénario Aléatoire
                        </button>
                    </div>
                    
                    <div class="input-group">
                        <label for="demand-input">Volume demandé (MW)</label>
                        <div class="input-wrapper">
                            <input type="number" id="demand-input" value="55000" min="0" step="100">
                            <span class="unit">MW</span>
                        </div>
                    </div>
                    
                    <div class="demand-stats">
                        <div class="stat-item">
                            <span class="label">Pointe Hiver</span>
                            <span class="value">~75 000 MW</span>
                        </div>
                        <div class="stat-item">
                            <span class="label">Creux Été</span>
                            <span class="value">~35 000 MW</span>
                        </div>
                    </div>
                </section>
                
                <!-- Résumé des producteurs -->
                <section class="mix-section overlay-card">
                    <h2>Mix Énergétique</h2>
                    <div class="donut-placeholder">
                        <canvas id="mixChart"></canvas>
                    </div>
                </section>
            </div>
        </main>

        <!-- Right Panel (Glassmorphism) -->
        <aside class="right-panel glass-panel">
            <div class="clearing-widget">
                <h3>Marché Cleared</h3>
                <div class="price-display">
                    <span class="price-value" id="clearing-price">--</span>
                    <span class="price-unit">€/MWh</span>
                </div>
                <div class="volume-display">
                    <span class="volume-label">Volume Total:</span>
                    <span class="volume-value" id="clearing-volume">-- MW</span>
                </div>
            </div>

            <div class="order-book">
                <div class="header-flex">
                    <h3>Carnet d'Ordres</h3>
                    <button id="btn-random-orders" class="btn-icon" aria-label="Ordres Aléatoires">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 2v6h-6M3 12a9 9 0 102.6-6.7L2 8M3 22v-6h6M21 12a9 9 0 10-2.6 6.7L22 16" /></svg>
                    </button>
                </div>
                
                <div id="producers-list" class="transactions-list">
                    <!-- Producer Items will be generated by JS -->
                </div>
            </div>
        </aside>
    </div>

    <!-- About Modal -->
    <div id="aboutModal" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <h2>Guide d'emploi du Simulateur</h2>
            <div class="guide-scroll">
                <p>Bienvenue ! Ce site simule de façon interactive le mécanisme de formation des prix <strong>SPOT en France</strong> (marché Day-Ahead).</p>
                
                <h3>Comment utiliser l'interface ?</h3>
                <ul class="guide-list">
                    <li><strong>1. Gérer la Demande :</strong> Saisissez manuellement un volume à gauche, ou cliquez sur <em>"Scénario Aléatoire"</em> pour simuler une consommation réaliste (du creux d'été à la pointe d'hiver).</li>
                    <li><strong>2. Observer l'Offre :</strong> Le carnet d'ordres liste les centrales à droite. Cliquez sur <em>"Ordres Aléatoires"</em> (icône tournante) pour simuler la disponibilité des énergies au quotidien (panne nucléaire, fort vent, etc).</li>
                    <li><strong>3. Analyser le Prix (Clearing) :</strong> Le graphique Merit Order se met à jour en direct. Le marché empile les offres de la moins chère (Solaire/Éolien) à la plus chère (Gaz/Secours). Le croisement avec la demande détermine le <strong>Prix d'Équilibre</strong>.</li>
                    <li><strong>4. Tester des cas extrêmes :</strong> Modifiez manuellement le volume (MW) ou le prix proposé (€) de n'importe quelle énergie du carnet d'ordres pour manipuler la courbe économique.</li>
                </ul>

                <h3>La Méthode Pay-as-Clear</h3>
                <p>C'est la règle européenne : l'outil empile les vendeurs en commençant par les Énergies Renouvelables (proposées à 0€ et prioritaires) jusqu'à ce que la demande soit couverte. Le <strong>prix marginal</strong> de la toute dernière centrale électrique allumée fixe le prix au mégawatt pour tout le monde ce jour-là.</p>
            </div>
            <button id="close-modal-btn" class="btn-secondary" style="margin-top: 25px; width: 100%; border-color: var(--accent-tertiary); color: var(--accent-tertiary); font-weight: bold; font-size: 16px; padding: 14px;">Jouer avec le simulateur</button>
        </div>
    </div>

    <!-- Script Inline Massif -->
    <script>
        /**
         * Simulateur SPOT France - Moteur Javascript
         */

        // Configuration des producteurs (Système 100% Local - 4 Fournisseurs)
        const producerConfigs = [
            {
                id: 'sunPower', name: 'SunPower', color: '#FFD700',
                portfolio: [
                    { type: 'Solaire', priceRange: [0, 0], defaultVolume: 2500, defaultPrice: 0 }
                ]
            },
            {
                id: 'ecoStream', name: 'EcoStream', color: '#2BD9AF',
                portfolio: [
                    { type: 'Hydro (Fil de l\'eau)', priceRange: [10, 20], defaultVolume: 4000, defaultPrice: 10 },
                    { type: 'Éolien', priceRange: [0, 0], defaultVolume: 2000, defaultPrice: 0 }
                ]
            },
            {
                id: 'megaCorp', name: 'MegaCorp', color: '#A28CFF',
                portfolio: [
                    { type: 'Nucléaire', priceRange: [30, 45], defaultVolume: 45000, defaultPrice: 35 },
                    { type: 'Éolien', priceRange: [0, 0], defaultVolume: 1000, defaultPrice: 0 },
                    { type: 'Charbon', priceRange: [120, 120], defaultVolume: 1500, defaultPrice: 120 },
                    { type: 'Fioul', priceRange: [150, 150], defaultVolume: 2000, defaultPrice: 150 },
                    { type: 'Gaz (CCGT)', priceRange: [500, 500], defaultVolume: 5000, defaultPrice: 500 },
                    { type: 'Secours (TAC)', priceRange: [3000, 3000], defaultVolume: 1500, defaultPrice: 3000 }
                ]
            },
            {
                id: 'hydroFlex', name: 'HydroFlex', color: '#3B82F6',
                portfolio: [
                    { type: 'Hydro (Lacs)', priceRange: [60, 90], defaultVolume: 8000, defaultPrice: 75 },
                    { type: 'Gaz (Pointe)', priceRange: [500, 500], defaultVolume: 4000, defaultPrice: 500 }
                ]
            }
        ];

        let orders = producerConfigs.map(p => ({
            id: p.id,
            name: p.name,
            color: p.color,
            portfolio: p.portfolio.map(asset => ({
                type: asset.type,
                volume: asset.defaultVolume,
                price: asset.defaultPrice
            }))
        }));

        let currentDemand = 55000;
        let clearingResult = { price: 0, volume: 0 };

        const domElements = {
            demandInput: document.getElementById('demand-input'),
            btnRandomDemand: document.getElementById('btn-random-demand'),
            btnRandomOrders: document.getElementById('btn-random-orders'),
            producersList: document.getElementById('producers-list'),
            clearingPrice: document.getElementById('clearing-price'),
            clearingVolume: document.getElementById('clearing-volume')
        };

        let meritOrderChart = null;
        let mixChart = null;

        function getFlattenedOrderBook(producerOrders) {
            let globalOrders = [];
            producerOrders.forEach(provider => {
                provider.portfolio.forEach(asset => {
                    if (asset.volume > 0) {
                        globalOrders.push({
                            providerName: provider.name,
                            providerColor: provider.color,
                            type: asset.type,
                            volume: asset.volume,
                            price: asset.price
                        });
                    }
                });
            });
            return globalOrders.sort((a, b) => a.price - b.price);
        }

        function calculateClearingPrice(demand, producerOrders) {
            const sortedOrders = getFlattenedOrderBook(producerOrders);
            let cumulativeVolume = 0;
            let clearingPrice = 0;
            let clearingVolume = 0;
            
            const totalSupply = sortedOrders.reduce((sum, order) => sum + order.volume, 0);

            if (demand > totalSupply) {
                return { price: 3000, volume: totalSupply, isShortage: true, sortedOrders };
            }

            for (const order of sortedOrders) {
                cumulativeVolume += order.volume;
                if (cumulativeVolume >= demand) {
                    clearingPrice = order.price;
                    clearingVolume = demand;
                    break;
                }
            }

            return { price: clearingPrice, volume: clearingVolume, isShortage: false, sortedOrders };
        }

        function updateUI() {
            clearingResult = calculateClearingPrice(currentDemand, orders);
            
            domElements.clearingPrice.textContent = clearingResult.isShortage ? "MAX" : clearingResult.price.toFixed(2);
            domElements.clearingVolume.textContent = clearingResult.volume.toLocaleString('fr-FR') + " MW";
            
            if (clearingResult.isShortage) {
                domElements.clearingPrice.style.color = "#FF0000";
            } else {
                domElements.clearingPrice.style.color = "var(--text-dark)";
            }

            updateMeritOrderChart();
            updateMixChart();
        }

        function renderOrderBook() {
            domElements.producersList.innerHTML = '';
            
            orders.forEach((provider, providerIndex) => {
                const item = document.createElement('div');
                item.className = 'producer-item portfolio-card';
                
                let htmlContent = `
                    <div class="producer-header">
                        <div class="producer-color" style="background-color: ${provider.color}"></div>
                        <span class="producer-name">${provider.name}</span>
                    </div>
                    <div class="portfolio-assets">
                `;
                
                provider.portfolio.forEach((asset, assetIndex) => {
                    const isZero = asset.volume === 0;
                    htmlContent += `
                        <div class="asset-row ${isZero ? 'inactive' : ''}">
                            <span class="asset-type">${asset.type}</span>
                            <div class="asset-inputs">
                                <div class="small-input-wrapper">
                                    <input type="number" data-pindex="${providerIndex}" data-aindex="${assetIndex}" data-field="volume" value="${asset.volume}" min="0">
                                    <span class="unit-xs">MW</span>
                                </div>
                                <div class="small-input-wrapper">
                                    <input type="number" data-pindex="${providerIndex}" data-aindex="${assetIndex}" data-field="price" value="${asset.price}" min="0" step="0.1">
                                    <span class="unit-xs">€</span>
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                htmlContent += `</div>`;
                item.innerHTML = htmlContent;
                domElements.producersList.appendChild(item);
            });

            const inputs = domElements.producersList.querySelectorAll('input');
            inputs.forEach(input => {
                input.addEventListener('change', (e) => {
                    const pIndex = e.target.getAttribute('data-pindex');
                    const aIndex = e.target.getAttribute('data-aindex');
                    const field = e.target.getAttribute('data-field');
                    
                    orders[pIndex].portfolio[aIndex][field] = parseFloat(e.target.value) || 0;
                    
                    if (field === 'volume') {
                        const assetRow = e.target.closest('.asset-row');
                        if (orders[pIndex].portfolio[aIndex].volume === 0) {
                            assetRow.classList.add('inactive');
                        } else {
                            assetRow.classList.remove('inactive');
                        }
                    }
                    updateUI();
                });
            });
        }

        function initCharts() {
            Chart.defaults.color = '#94A3B8';
            Chart.defaults.font.family = 'Inter';

            const ctxMerit = document.getElementById('meritOrderChart').getContext('2d');
            meritOrderChart = new Chart(ctxMerit, {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Offre (Merit Order)',
                        data: [],
                        borderColor: '#ffffff',
                        borderWidth: 2,
                        stepped: true,
                        fill: true,
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        pointRadius: 0
                    },
                    {
                        label: 'Demande',
                        data: [],
                        borderColor: '#ADFF2F',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { intersect: false, mode: 'index' },
                    scales: {
                        x: { type: 'linear', title: { display: true, text: 'Volume Cumulé (MW)' }, min: 0 },
                        y: { title: { display: true, text: 'Prix (€/MWh)' }, min: 0, suggestedMax: 500 }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#94A3B8',
                                usePointStyle: true,
                                generateLabels: function(chart) {
                                    const original = Chart.defaults.plugins.legend.labels.generateLabels(chart);
                                    original.forEach(label => {
                                        if (label.text === 'Demande') {
                                             label.pointStyle = 'line';
                                             label.lineWidth = 2;
                                             label.lineDash = [5, 5];
                                             label.strokeStyle = '#ADFF2F';
                                        } else {
                                             label.pointStyle = 'rectRounded';
                                        }
                                    });
                                    return original;
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `${context.dataset.label}: ${context.parsed.y} €/MWh á ${context.parsed.x} MW`;
                                }
                            }
                        }
                    }
                }
            });

            const ctxMix = document.getElementById('mixChart').getContext('2d');
            mixChart = new Chart(ctxMix, {
                type: 'doughnut',
                data: {
                    labels: orders.map(o => o.name),
                    datasets: [{
                        data: orders.map(o => o.volume),
                        backgroundColor: orders.map(o => o.color),
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%',
                    plugins: {
                        legend: { position: 'right', labels: { color: '#ffffff', boxWidth: 12 } }
                    }
                }
            });
        }

        function updateMeritOrderChart() {
            if (!meritOrderChart) return;

            const { sortedOrders } = clearingResult;
            const offerData = [{x: 0, y: sortedOrders[0]?.price || 0}];
            let cumulativeVol = 0;
            
            sortedOrders.forEach(order => {
                cumulativeVol += order.volume;
                offerData.push({ x: cumulativeVol, y: order.price });
                const nextOrderIndex = sortedOrders.indexOf(order) + 1;
                if (nextOrderIndex < sortedOrders.length) {
                     offerData.push({ x: cumulativeVol, y: sortedOrders[nextOrderIndex].price });
                }
            });

            const maxPrice = Math.max(500, clearingResult.price + 100);
            const demandData = [
                { x: currentDemand, y: 0 },
                { x: currentDemand, y: maxPrice }
            ];

            meritOrderChart.data.datasets[0].data = offerData;
            meritOrderChart.data.datasets[1].data = demandData;
            meritOrderChart.options.scales.x.max = Math.max(currentDemand * 1.2, cumulativeVol * 1.1);
            meritOrderChart.update();
        }

        function updateMixChart() {
            if (!mixChart) return;
            const providerVolumes = orders.map(provider => {
                return provider.portfolio.reduce((sum, asset) => sum + asset.volume, 0);
            });
            mixChart.data.datasets[0].data = providerVolumes;
            mixChart.data.datasets[0].backgroundColor = orders.map(o => o.color);
            mixChart.data.labels = orders.map(o => o.name);
            mixChart.update();
        }

        function generateRandomDemand() {
            currentDemand = Math.floor(Math.random() * (85000 - 40000 + 1)) + 40000;
            domElements.demandInput.value = currentDemand;
            updateUI();
        }

        function generateRandomOrders() {
            orders.forEach((provider, pIndex) => {
                const config = producerConfigs[pIndex];
                
                provider.portfolio.forEach((asset, aIndex) => {
                    const assetConfig = config.portfolio[aIndex];
                    
                    const priceMin = assetConfig.priceRange[0];
                    const priceMax = assetConfig.priceRange[1];
                    if (priceMin === priceMax) {
                        asset.price = priceMin;
                    } else {
                        asset.price = parseFloat((Math.random() * (priceMax - priceMin) + priceMin).toFixed(2));
                    }
                    
                    if (assetConfig.type === 'Solaire') {
                        asset.volume = Math.floor(Math.random() * (4000 - 1000 + 1)) + 1000;
                    } else if (assetConfig.type === 'Éolien' && provider.id === 'ecoStream') {
                        asset.volume = Math.floor(Math.random() * (3000 - 1000 + 1)) + 1000;
                    } else if (assetConfig.type === 'Éolien' && provider.id === 'megaCorp') {
                        asset.volume = Math.floor(Math.random() * (1500 - 500 + 1)) + 500;
                    } else if (assetConfig.type === 'Nucléaire') {
                        asset.volume = Math.floor(Math.random() * (50000 - 40000 + 1)) + 40000;
                    } else if (assetConfig.type.includes('Hydro')) {
                        asset.volume = Math.floor(assetConfig.defaultVolume * (Math.random() * 0.15 + 0.9));
                    } else {
                        const volVariation = assetConfig.defaultVolume * 0.2;
                        asset.volume = Math.floor(assetConfig.defaultVolume + (Math.random() * volVariation * 2 - volVariation));
                    }
                    
                    if (['Charbon', 'Fioul', 'Gaz (CCGT)'].includes(assetConfig.type) && Math.random() < 0.1) {
                        asset.volume = 0;
                    }
                });
            });
            
            renderOrderBook();
            updateUI();
        }

        // Configuration du Modal d'Information
        function setupModal() {
            const modal = document.getElementById('aboutModal');
            const btnInfo = document.getElementById('btn-info');
            const spanClose = document.getElementsByClassName('close-modal')[0];
            const btnClose = document.getElementById('close-modal-btn');

            btnInfo.onclick = function() { modal.style.display = 'flex'; }
            
            function closeModal() { modal.style.display = 'none'; }
            spanClose.onclick = closeModal;
            btnClose.onclick = closeModal;

            window.onclick = function(event) {
                if (event.target == modal) { modal.style.display = 'none'; }
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            domElements.demandInput.addEventListener('input', (e) => {
                currentDemand = parseFloat(e.target.value) || 0;
                updateUI();
            });
            domElements.btnRandomDemand.addEventListener('click', generateRandomDemand);
            domElements.btnRandomOrders.addEventListener('click', generateRandomOrders);

            setupModal();
            renderOrderBook();
            initCharts();
            updateUI();
        });
    </script>
</body>
</html>
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
                vol_val = c_vol.number_input(f"{asset['type']} (MW)", min_value=0, value=st.session_state.provider_vols[k_vol], step=100)
                
                is_fixed = 'price_fixed' in asset
                px_val = c_px.number_input(f"Prix (€)", min_value=0.0, value=float(st.session_state.provider_prices[k_px]), step=1.0, disabled=is_fixed)
                
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

