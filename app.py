import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor, XGBClassifier
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Título principal do aplicativo
st.title("OKIAR 360º")

# Sidebar com título e seleção de aba
st.sidebar.title("OKIAR 360º")
aba_selecionada = st.sidebar.selectbox("Selecione a aba", ["MMM SIMULADOR", "MMM Media Behavior", "BRAIN", "MERIDIO", "MMX", "UXM", "FLAG"])

# Texto explicativo
st.sidebar.write("**SUITE MODULAR E ALWAYS ON DE PLANEJAMENTO INTEGRADO DE MENSURAÇÃO DE MARKETING.**")
st.sidebar.write("GUIDANCE DE MARCA E PRODUTO, AUDITORIA DE ROI E SUPORTE NA DEFINIÇÃO DE BUDGETS E PRIORIDADES DO MARKETING.")

# Definindo os canais e investimentos iniciais
investimentos_iniciais = {
    "Google Ads": 100,
    "Meta Ads": 100,
    "Out of Home": 50,
    "Rádio": 75,
    "TV Paga": 150,
    "TV Aberta": 200,
    "Influenciadores": 120
}

# Função para calcular métricas com base nos investimentos
def calcular_metricas(investimentos):
    acessos = sum(investimentos.values()) * 0.5
    leads = acessos * 0.3
    vendas = leads * 0.1
    return acessos, leads, vendas

# Valores de referência para o cálculo das mudanças percentuais
valor_base_acessos = 300
valor_base_leads = 100
valor_base_vendas = 10

# Parte 1:  MMM
if aba_selecionada == "MMM SIMULADOR":
    st.header("Simulador Marketing Mix Modeling")

    # Bloco Inicial: KPIs Principais
    st.subheader("Principais KPIs de Mídia")
    col1, col2, col3, col4 = st.columns(4)

    investimento_total = sum(investimentos_iniciais.values())
    roi_geral = 120.5  # ROI Geral fictício inicial em %
    roi_online = 130.2  # ROI Online fictício inicial em %
    roi_offline = 110.3  # ROI Offline fictício inicial em %

    with col1:
        st.metric(label="Investimento Total (mil R$)", value=f"{investimento_total:.0f}", delta="",
                  delta_color="off")
    with col2:
        st.metric(label="ROI Geral de Marketing", value=f"{roi_geral:.1f}%", delta="",
                  delta_color="off")
    with col3:
        st.metric(label="ROI Online", value=f"{roi_online:.1f}%", delta="",
                  delta_color="off")
    with col4:
        st.metric(label="ROI Offline", value=f"{roi_offline:.1f}%", delta="",
                  delta_color="off")

    # Bloco 1: Alocação de Investimento por Canal
    st.subheader("Alocação de Investimento por Canal")
    col1, col2, col3 = st.columns(3)

    investimentos = {}
    with col1:
        investimentos["Google Ads"] = st.slider("Google Ads (mil R$)", 0, 500, investimentos_iniciais["Google Ads"])
        investimentos["Meta Ads"] = st.slider("Meta Ads (mil R$)", 0, 500, investimentos_iniciais["Meta Ads"])
        investimentos["Out of Home"] = st.slider("Out of Home (mil R$)", 0, 500, investimentos_iniciais["Out of Home"])
    with col2:
        investimentos["Rádio"] = st.slider("Rádio (mil R$)", 0, 500, investimentos_iniciais["Rádio"])
        investimentos["TV Paga"] = st.slider("TV Paga (mil R$)", 0, 500, investimentos_iniciais["TV Paga"])
    with col3:
        investimentos["TV Aberta"] = st.slider("TV Aberta (mil R$)", 0, 500, investimentos_iniciais["TV Aberta"])
        investimentos["Influenciadores"] = st.slider("Influenciadores (mil R$)", 0, 500, investimentos_iniciais["Influenciadores"])

    # Bloco 2: Simulação de Resultados
    st.subheader("Simulação de Resultados")
    acessos, leads, vendas = calcular_metricas(investimentos)

    col1, col2, col3 = st.columns(3)
    col1.metric("Acessos", f"{acessos:.0f}", f"{(acessos / valor_base_acessos - 1) * 100:.0f}%", delta_color="normal")
    col2.metric("Leads", f"{leads:.0f}", f"{(leads / valor_base_leads - 1) * 100:.0f}%", delta_color="normal")
    col3.metric("Vendas", f"{vendas:.0f}", f"{(vendas / valor_base_vendas - 1) * 100:.0f}%", delta_color="normal")

    # Bloco 3: ROI MIX Marketing com mudança entre matriz e pesos
    st.subheader("ROI Mix Marketing")
    matriz_ou_pesos = st.radio("Selecione a visualização:", ("Matrix", "Pesos"))

    if matriz_ou_pesos == "Matrix":
        fig_matrix = go.Figure()
        fig_matrix.add_trace(go.Scatter(
            x=[30, 15, 25, 35, 20, 40, 45],
            y=[0.5, 0.8, 1.0, 1.3, 0.6, 1.5, 1.8],
            mode='markers+text',
            text=list(investimentos.keys()),
            textposition="top center",
            marker=dict(size=[v * 0.1 for v in investimentos.values()], color='red')
        ))
        fig_matrix.update_layout(title="Distribuição de ROI por Canal", xaxis_title="Investimento (%)", yaxis_title="Peso no Resultado")
        st.plotly_chart(fig_matrix)

    else:
        fig_pesos = go.Figure(go.Bar(
            x=list(investimentos.values()),
            y=list(investimentos.keys()),
            orientation='h',
            marker=dict(color="red")
        ))
        fig_pesos.update_layout(title="Pesos dos Canais de Mídia")
        st.plotly_chart(fig_pesos)

# Parte 2: Media Behavior
elif aba_selecionada == "MMM Media Behavior":
    st.header("Comportamento de Mídia")

    # Inicialização da variável investimentos com valores padrão
    investimentos = {
        "Google Ads": 100,
        "Meta Ads": 100,
        "Out of Home": 50,
        "Rádio": 75,
        "TV Paga": 150,
        "TV Aberta": 200,
        "Influenciadores": 120
    }

    # Curva de resposta de mídia com ponto de investimento
    st.subheader("Curva de Resposta de Mídia")
    canal_selecionado = st.selectbox("Selecione o Canal de Mídia", options=list(investimentos.keys()))

    # Definindo a curva de resposta (modelo em três fases)
    x = np.linspace(0, 500, 500)
    y = np.piecewise(x, [x < 100, (x >= 100) & (x < 300), x >= 300],
                     [lambda x: 0.5 * x / 100, lambda x: x * 0.01 + 0.5, lambda x: 3])

    # Gráfico da curva de resposta com ponto de investimento destacado
    fig_resposta = go.Figure()
    fig_resposta.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Curva de Resposta"))
    fig_resposta.add_trace(go.Scatter(
        x=[investimentos[canal_selecionado]],
        y=[y[int(investimentos[canal_selecionado])]],  # Convertendo índice para acessar a curva
        mode="markers", marker=dict(color="red", size=10), name="Investimento Atual"
    ))
    fig_resposta.update_layout(
        title=f"Curva de Resposta para {canal_selecionado}",
        xaxis_title="Investimento",
        yaxis_title="Efeito"
    )
    st.plotly_chart(fig_resposta)

    # Gráfico de Vendas Previstas vs. Realizadas
    st.subheader("Previsto vs. Realizado")
    datas = pd.date_range(start="2023-01-01", periods=12, freq="M")
    vendas_previstas = np.sin(np.linspace(0, 3 * np.pi, 12)) * 200 + 1000
    vendas_reais = vendas_previstas + np.random.normal(0, 50, 12)

    fig_previsto_realizado = go.Figure()
    fig_previsto_realizado.add_trace(go.Scatter(x=datas, y=vendas_previstas, mode='lines', name='Vendas Previstas'))
    fig_previsto_realizado.add_trace(go.Scatter(x=datas, y=vendas_reais, mode='lines+markers', name='Vendas Reais'))
    fig_previsto_realizado.update_layout(
        title="Vendas Previstas vs. Realizadas",
        xaxis_title="Mês",
        yaxis_title="Vendas"
    )
    st.plotly_chart(fig_previsto_realizado)


elif aba_selecionada == "BRAIN":
    st.header("SUAS AÇÕES IMPACTAM A MARCA? QUAL A IMPORTÂNCIA DE BRANDING PARA O NEGÓCIO?")

    # Bloco Inicial: KPIs de Marca
    st.subheader("Principais KPIs de Marca")
    col1, col2, col3, col4 = st.columns(4)

    kpi_lembranca = 75.2
    kpi_consideracao = 60.5
    kpi_brand_equity = 85.0
    kpi_brand_impact_index = 45.3  # Percentual médio de impacto da marca

    with col1:
        st.metric("Lembrança", f"{kpi_lembranca:.1f}%")
    with col2:
        st.metric("Consideração", f"{kpi_consideracao:.1f}%")
    with col3:
        st.metric("Brand Equity", f"{kpi_brand_equity:.1f}%")
    with col4:
        st.metric("Brand Impact Index", f"{kpi_brand_impact_index:.1f}%")

    # Bloco de Top of Mind
    st.subheader("Top of Mind do Mercado")
    top_of_mind_data = {
        "Marca 1": 32,
        "Marca 2": 27,
        "Marca 3": 20,
        "Marca 4": 15,
        "Marca 5": 6
    }
    fig_top_of_mind = go.Figure(go.Bar(
        x=list(top_of_mind_data.values()),
        y=list(top_of_mind_data.keys()),
        orientation='h',
        marker=dict(color="red")
    ))
    fig_top_of_mind.update_layout(title="Top of Mind", xaxis_title="%", yaxis_title="Marcas")
    st.plotly_chart(fig_top_of_mind)

    # Bloco de Funis de Marca
    st.subheader("Funis de Marca")
    funil_data = {
        "Marca 1": [85, 60, 45],
        "Marca 2": [75, 55, 35],
        "Marca 3": [70, 50, 30],
        "Marca 4": [65, 45, 25]
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    for marca, col in zip(funil_data.keys(), [col1, col2, col3, col4]):
        funil = funil_data[marca]
        fig_funil = go.Figure(go.Bar(
            x=funil,  # Lembrança, Consideração, Preferência
            y=["Lembrança", "Consideração", "Preferência"],
            orientation='h',
            marker=dict(color=["#ff9999", "#ff6666", "#ff3333"]),
            text=[f"{val}%" for val in funil],
            textposition='inside'
        ))
        fig_funil.update_layout(
            title=f"Funil de {marca}",
            xaxis=dict(showticklabels=False),  # Remove ticks do eixo x para visualização simplificada
            yaxis=dict(autorange="reversed", showline=False, showticklabels=True),
            bargap=0.4,
            height=300
        )
        col.plotly_chart(fig_funil)


    # Radar de Atributos Comparando 3 Marcas
    st.subheader("Comparação de Atributos de Marca")
    marcas = ["Marca 1", "Marca 2", "Marca 3"]
    atributos_radar = ["Qualidade", "Inovação", "Confiabilidade", "Disponibilidade", "Atendimento", "Preço", "Sustentabilidade", "Design"]
    valores_marca_1 = [8, 6, 7, 5, 9, 4, 6, 7]
    valores_marca_2 = [7, 7, 6, 6, 8, 5, 5, 6]
    valores_marca_3 = [6, 8, 5, 7, 7, 6, 4, 5]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=valores_marca_1, theta=atributos_radar, fill='toself', name='Marca 1'))
    fig_radar.add_trace(go.Scatterpolar(r=valores_marca_2, theta=atributos_radar, fill='toself', name='Marca 2'))
    fig_radar.add_trace(go.Scatterpolar(r=valores_marca_3, theta=atributos_radar, fill='toself', name='Marca 3'))
    fig_radar.update_layout(title="Radar de Atributos de Marca", polar=dict(radialaxis=dict(visible=True, range=[0, 10])))
    st.plotly_chart(fig_radar)

    # Matriz de Performance e Importância de Atributos
    st.subheader("Matriz de Importância vs. Performance")
    importancia = [8, 7, 9, 5, 6, 4, 7, 8]
    performance = [6, 8, 7, 4, 5, 3, 8, 7]
    fig_matriz = go.Figure()
    fig_matriz.add_trace(go.Scatter(
        x=importancia, y=performance, mode='markers+text', text=atributos_radar, textposition="top center",
        marker=dict(size=12, color="red")
    ))
    fig_matriz.update_layout(title="Importância vs. Performance dos Atributos", xaxis_title="Importância", yaxis_title="Performance")
    st.plotly_chart(fig_matriz)

    # Gráfico de Impacto de Marca em Resultados de Negócio
    st.subheader("Impacto da Marca nos Resultados de Negócio")
    resultados_negocio = ["Abertura de Conta", "Uso do Aplicativo", "Adoção de Crédito", "Investimentos"]
    impacto_marca = [0.65, 0.7, 0.5, 0.6]  # Valores fictícios de R quadrado

    fig_impacto = go.Figure(go.Bar(
        x=impacto_marca,
        y=resultados_negocio,
        orientation='h',
        marker=dict(color="red")
    ))
    fig_impacto.update_layout(title="Impacto da Marca (R²) nos Resultados de Negócio", xaxis_title="Impacto (R²)", yaxis_title="Resultado de Negócio")
    st.plotly_chart(fig_impacto)


# Parte MERIDIO: Segmentação e Personas
elif aba_selecionada == "MERIDIO":
    st.header("QUAIS AS PERSONAS NO SEU MERCADO E QUAIS AS ALAVANCAS DE CONSUMO?")
    
    # Bloco de seleção de personas
    st.subheader("Personas")
    cluster_selecionado = st.multiselect(
        "Selecione um ou dois clusters para visualizar", 
        ["Cluster A", "Cluster B", "Cluster C", "Cluster D"]
    )

    # Descrições de cada cluster
    descricoes_clusters = {
        "Cluster A": "Alta Renda A: Consumidores focados em investimentos robustos e personalizados. Valorizam atendimento premium e acesso rápido a produtos de crédito.",
        "Cluster B": "Alta Renda B: Investidores conservadores que preferem produtos de baixo risco. Valorizam segurança e estabilidade.",
        "Cluster C": "Mass Market A: Focados em construção de patrimônio com produtos acessíveis. Importante para eles é a facilidade de uso e diversidade de canais.",
        "Cluster D": "Mass Market B: Consumidores de renda média interessados em crédito rápido e soluções práticas. Valorizam o custo-benefício."
    }
    verbatim_clusters = {
        "Cluster A": "“Quero soluções rápidas e exclusivas para meus investimentos.”",
        "Cluster B": "“Prefiro segurança e estabilidade nas minhas escolhas.”",
        "Cluster C": "“Preciso de uma plataforma acessível e prática para crescer.”",
        "Cluster D": "“Opções de crédito acessível são o que mais busco.”"
    }

    # Exibe a descrição do cluster e verbatim se um único cluster for selecionado
    if len(cluster_selecionado) == 1:
        st.write(f"**Descrição do {cluster_selecionado[0]}**")
        st.write(descricoes_clusters[cluster_selecionado[0]])
        st.write(f"*Verbatim:* {verbatim_clusters[cluster_selecionado[0]]}")
    
    # Bloco de seleção de tópicos para visualizar gráficos
    st.subheader("Tópicos de Interesse")
    topico_selecionado = st.selectbox(
        "Selecione um tópico para visualizar",
        ["Quais critérios mais importantes na hora de abrir uma conta?", 
         "Quais são os produtos mais buscados?",
         "Quais são as alavancas de principalidade?",
         "Quantas contas a pessoa tem aberta entre digitais e tradicionais?"]
    )

    # Dados fictícios para os gráficos de cada tópico
    dados_topicos = {
        "Quais critérios mais importantes na hora de abrir uma conta?": {
            "Acessibilidade": [80, 70, 60, 75],
            "Segurança": [90, 85, 70, 80],
            "Atendimento": [85, 65, 60, 70],
        },
        "Quais são os produtos mais buscados?": {
            "Investimentos": [95, 90, 50, 45],
            "Crédito": [60, 65, 85, 80],
            "Poupança": [40, 50, 75, 70],
        },
        "Quais são as alavancas de principalidade?": {
            "Programas de Fidelidade": [70, 55, 60, 65],
            "Benefícios de Conta": [85, 80, 75, 70],
            "Facilidade de Uso": [90, 85, 80, 75],
        },
        "Quantas contas a pessoa tem aberta entre digitais e tradicionais?": {
            "Digitais": [1.5, 1.2, 2.0, 1.8],
            "Tradicionais": [1.8, 1.5, 1.0, 0.9],
        }
    }
    
    # Exibição dos gráficos
    if topico_selecionado and cluster_selecionado:
        st.subheader(f"Resultados para: {topico_selecionado}")

        # Preparar os dados para visualização de clusters
        dados_topico = dados_topicos[topico_selecionado]
        clusters_indices = {"Cluster A": 0, "Cluster B": 1, "Cluster C": 2, "Cluster D": 3}

        fig = go.Figure()

        # Gráfico de barras para visualização de até dois clusters selecionados
        for cluster in cluster_selecionado:
            indice = clusters_indices[cluster]
            valores = [dados_topico[fator][indice] for fator in dados_topico]
            fig.add_trace(go.Bar(
                x=list(dados_topico.keys()), 
                y=valores, 
                name=cluster
            ))

        fig.update_layout(
            title=f"Análise do Tópico: {topico_selecionado}",
            xaxis_title="Fatores",
            yaxis_title="Pontuação",
            barmode='group'
        )
        st.plotly_chart(fig)

# Parte MMX: Satisfação e Modelo de Equação Estrutural
elif aba_selecionada == "MMX":
    st.header("QUAIS AS ALAVANCAS DE LEALDADE E MONETIZAÇÃO NO SEU MERCADO?")

    # Bloco de métricas gerais de satisfação
    st.subheader("Métricas Gerais de Satisfação")
    col1, col2, col3, col4, col5 = st.columns(5)

    # Valores fictícios para os scores de satisfação
    satisfacao = 88
    nps = 72
    score_qualidade = 85
    score_facilidade = 78
    score_valor = 82

    # Exibindo as métricas principais em blocos
    with col1:
        st.metric(label="Satisfação", value=f"{satisfacao}%")
    with col2:
        st.metric(label="NPS", value=f"{nps}")
    with col3:
        st.metric(label="Qualidade", value=f"{score_qualidade}")
    with col4:
        st.metric(label="Facilidade", value=f"{score_facilidade}")
    with col5:
        st.metric(label="Valor", value=f"{score_valor}")

    # Bloco de evolução das métricas em ondas
    st.subheader("Evolução das Métricas por Onda")
    ondas = ["Onda 1", "Onda 2", "Onda 3"]
    evolucao_qualidade = [80, 83, 85]
    evolucao_facilidade = [75, 76, 78]
    evolucao_valor = [78, 80, 82]

    fig_evolucao = go.Figure()
    fig_evolucao.add_trace(go.Scatter(x=ondas, y=evolucao_qualidade, mode="lines+markers", name="Qualidade", line=dict(color="red")))
    fig_evolucao.add_trace(go.Scatter(x=ondas, y=evolucao_facilidade, mode="lines+markers", name="Facilidade", line=dict(color="blue")))
    fig_evolucao.add_trace(go.Scatter(x=ondas, y=evolucao_valor, mode="lines+markers", name="Valor", line=dict(color="yellow")))
    fig_evolucao.update_layout(title="Evolução das Métricas por Onda", xaxis_title="Onda", yaxis_title="Pontuação")
    st.plotly_chart(fig_evolucao)

    # Bloco de prioridades e retorno
    st.subheader("Prioridades e Retorno")

    col1, col2 = st.columns(2)

    # Matriz de performance e importância dos fatores
    with col1:
        st.write("Matriz de Performance vs. Importância dos Fatores")
        fatores = ["Atendimento", "Disponibilidade", "Personalização", "Interfaces", "Processos", "Omnichannel", "Custo Benefício", "Competitividade", "Benefícios"]
        performance = [0.6, 0.8, 0.75, 0.9, 0.7, 0.85, 0.65, 0.6, 0.8]
        importancia = [0.7, 0.85, 0.9, 0.75, 0.8, 0.7, 0.9, 0.65, 0.8]
        fig_matriz = go.Figure()
        fig_matriz.add_trace(go.Scatter(
            x=performance, y=importancia, mode='markers+text', text=fatores, textposition="top center",
            marker=dict(size=12, color="purple")
        ))
        fig_matriz.update_layout(title="Performance vs. Importância", xaxis_title="Performance", yaxis_title="Importância")
        st.plotly_chart(fig_matriz)

    # Gráfico de R-quadrado dos constructos para resultados específicos
    with col2:
        st.write("Impacto da Satisfação em Resultados Estratégicos")
        resultados = ["Abertura de Conta", "Uso do App", "Crédito", "Investimentos"]
        r_quadrado = [0.8, 0.65, 0.7, 0.6]
        fig_rquadrado = go.Figure(go.Bar(
            x=r_quadrado, y=resultados, orientation='h', marker=dict(color="green")
        ))
        fig_rquadrado.update_layout(title="R² da Satisfação por Resultado", xaxis_title="Impacto (R²)", yaxis_title="Resultados")
        st.plotly_chart(fig_rquadrado)

elif aba_selecionada == "UXM":
    st.header("COMO DEVE SER A EXPERIÊNCIA DIGITAL DO SEU CLIENTE E O QUANTO ISSO IMPORTA?")

    # Seletor de ondas
    onda_selecionada = st.multiselect("Selecione uma ou mais ondas", ["Onda 1 - Q1", "Onda 2 - Q2", "Onda 3 - Q3", "Onda 4 - Q4"], ["Onda 1 - Q1"])
    
    # Dados fictícios para as ondas
    dados_ondas = {
        "Onda 1 - Q1": {"Usabilidade": 70, "CX": 65, "Engajamento": 75, "Tecnologia": 85, "Utilidade": 80, "UX Equity": 77},
        "Onda 2 - Q2": {"Usabilidade": 75, "CX": 68, "Engajamento": 78, "Tecnologia": 88, "Utilidade": 82, "UX Equity": 79},
        "Onda 3 - Q3": {"Usabilidade": 80, "CX": 70, "Engajamento": 80, "Tecnologia": 90, "Utilidade": 85, "UX Equity": 81},
        "Onda 4 - Q4": {"Usabilidade": 82, "CX": 72, "Engajamento": 83, "Tecnologia": 92, "Utilidade": 88, "UX Equity": 83},
    }
    
    # Verificar se apenas uma onda foi selecionada para exibir os blocos de KPIs
    if len(onda_selecionada) == 1:
        st.subheader("Visão Geral")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        valores = dados_ondas[onda_selecionada[0]]
        col1.metric("Usabilidade", f"{valores['Usabilidade']}")
        col2.metric("CX", f"{valores['CX']}")
        col3.metric("Engajamento", f"{valores['Engajamento']}")
        col4.metric("Tecnologia", f"{valores['Tecnologia']}")
        col5.metric("Utilidade", f"{valores['Utilidade']}")
        col6.metric("UX Equity", f"{valores['UX Equity']}")
    else:
        st.subheader("Evolução dos Constructos")
        ondas = [onda.split(" - ")[0] for onda in onda_selecionada]
        
        fig_evolucao = go.Figure()
        for constructo in ["Usabilidade", "CX", "Engajamento", "Tecnologia", "Utilidade", "UX Equity"]:
            valores_constructo = [dados_ondas[onda][constructo] for onda in onda_selecionada]
            fig_evolucao.add_trace(go.Scatter(x=ondas, y=valores_constructo, mode="lines+markers", name=constructo,
                                              line=dict(dash="dash" if constructo != "UX Equity" else "solid")))
        fig_evolucao.update_layout(title="Evolução dos Constructos", xaxis_title="Onda", yaxis_title="Pontuação")
        st.plotly_chart(fig_evolucao)

    # Seletor de visão para abas ou telas
    visao = st.radio("Selecione a visão", ["Visão Geral", "Abas", "Telas"])
    
    # Dados fictícios para abas e telas
    dados_abas = {
        "Home": {"Usabilidade": 78, "CX": 70, "Engajamento": 75, "Tecnologia": 85, "Utilidade": 82},
        "Produtos": {"Usabilidade": 76, "CX": 72, "Engajamento": 74, "Tecnologia": 86, "Utilidade": 83},
        "Suporte": {"Usabilidade": 74, "CX": 68, "Engajamento": 73, "Tecnologia": 82, "Utilidade": 80},
        "Conta": {"Usabilidade": 77, "CX": 69, "Engajamento": 76, "Tecnologia": 87, "Utilidade": 81},
    }
    
    dados_telas = {
        "Tela A": {"Usabilidade": 80, "CX": 74, "Engajamento": 78, "Tecnologia": 88, "Utilidade": 85},
        "Tela B": {"Usabilidade": 75, "CX": 70, "Engajamento": 76, "Tecnologia": 84, "Utilidade": 80},
        "Tela C": {"Usabilidade": 78, "CX": 72, "Engajamento": 77, "Tecnologia": 86, "Utilidade": 82},
    }

    if visao in ["Abas", "Telas"]:
        # Selecionar abas ou telas para comparação
        itens = list(dados_abas.keys()) if visao == "Abas" else list(dados_telas.keys())
        selecao = st.multiselect(f"Selecione {visao} para Comparação", itens)
        
        if len(onda_selecionada) == 1:
            # Exibir gráfico radar para comparação de uma única onda
            fig_radar = go.Figure()
            for item in selecao:
                valores = dados_abas[item] if visao == "Abas" else dados_telas[item]
                fig_radar.add_trace(go.Scatterpolar(
                    r=list(valores.values()),
                    theta=list(valores.keys()),
                    fill='toself',
                    name=item
                ))
            fig_radar.update_layout(title=f"Comparação de {visao}")
            st.plotly_chart(fig_radar)
        elif len(selecao) == 1:
            # Exibir gráfico de evolução se mais de uma onda for selecionada e apenas uma aba/tela for selecionada
            item = selecao[0]
            valores_constructos = {constructo: [dados_abas[item][constructo] if visao == "Abas" else dados_telas[item][constructo] for onda in onda_selecionada] for constructo in ["Usabilidade", "CX", "Engajamento", "Tecnologia", "Utilidade"]}
            
            fig_evolucao_constructo = go.Figure()
            for constructo, valores in valores_constructos.items():
                fig_evolucao_constructo.add_trace(go.Scatter(x=ondas, y=valores, mode="lines+markers", name=constructo))
            fig_evolucao_constructo.update_layout(title=f"Evolução de Constructos para {item} nas Ondas Selecionadas", xaxis_title="Onda", yaxis_title="Pontuação")
            st.plotly_chart(fig_evolucao_constructo)

    # Bloco de matriz de prioridades de UX
    st.subheader("Matriz de Prioridades de UX")
    fatores = ["Facilidade", "Clareza", "Acessibilidade", "Atendimento", "Resolução", "Eficiência", "Diversão", "Interação", "Personalização"]
    importancia_fatores = [0.75, 0.6, 0.8, 0.7, 0.85, 0.9, 0.65, 0.7, 0.9]
    performance_fatores = [0.7, 0.65, 0.75, 0.85, 0.8, 0.88, 0.68, 0.6, 0.8]

    fig_matriz_ux = go.Figure()
    fig_matriz_ux.add_trace(go.Scatter(
        x=performance_fatores,
        y=importancia_fatores,
        mode='markers+text',
        text=fatores,
        textposition="top center",
        marker=dict(size=12, color="purple")
    ))
    fig_matriz_ux.update_layout(title="Performance vs. Importância dos Fatores de UX", xaxis_title="Performance", yaxis_title="Importância")
    st.plotly_chart(fig_matriz_ux)

    # Bloco final: Retorno de UX para o Negócio
    st.subheader("Retorno de UX para o Negócio")
    resultados = ["Contratação de Crédito", "Uso do App", "Principalidade", "NPS", "Branding", "Investimentos"]
    impacto_ux_equity = [0.7, 0.65, 0.8, 0.75, 0.6, 0.85]

    fig_retorno_ux = go.Figure(go.Bar(
        x=impacto_ux_equity,
        y=resultados,
        orientation='h',
        marker=dict(color="green"),
        text=[f"{val:.0%}" for val in impacto_ux_equity],
        textposition="outside"
    ))
    fig_retorno_ux.update_layout(title="Impacto do UX Equity em Resultados Estratégicos", xaxis_title="Impacto (R²)", yaxis_title="Resultados")
    st.plotly_chart(fig_retorno_ux)

# Parte UXM: Modelo de UX e Retorno de Experiência
elif aba_selecionada == "UXM":
    st.header("COMO DEVE SER A EXPERIÊNCIA DIGITAL DO SEU CLIENTE E O QUANTO ISSO IMPORTA?")

    # Seletor de ondas
    onda_selecionada = st.multiselect("Selecione uma ou mais ondas", ["Onda 1 - Q1", "Onda 2 - Q2", "Onda 3 - Q3", "Onda 4 - Q4"], ["Onda 1 - Q1"])

    # Dados fictícios com variações entre ondas e itens
    dados_ondas = {
        "Onda 1 - Q1": {"Usabilidade": 72, "CX": 68, "Engajamento": 75, "Tecnologia": 83, "Utilidade": 78, "UX Equity": 76},
        "Onda 2 - Q2": {"Usabilidade": 74, "CX": 69, "Engajamento": 77, "Tecnologia": 84, "Utilidade": 80, "UX Equity": 78},
        "Onda 3 - Q3": {"Usabilidade": 76, "CX": 70, "Engajamento": 79, "Tecnologia": 87, "Utilidade": 81, "UX Equity": 79},
        "Onda 4 - Q4": {"Usabilidade": 79, "CX": 72, "Engajamento": 82, "Tecnologia": 89, "Utilidade": 84, "UX Equity": 81},
    }
    
    # Exibir KPIs se apenas uma onda for selecionada
    if len(onda_selecionada) == 1:
        st.subheader("Visão Geral")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        valores = dados_ondas[onda_selecionada[0]]
        col1.metric("Usabilidade", f"{valores['Usabilidade']}")
        col2.metric("CX", f"{valores['CX']}")
        col3.metric("Engajamento", f"{valores['Engajamento']}")
        col4.metric("Tecnologia", f"{valores['Tecnologia']}")
        col5.metric("Utilidade", f"{valores['Utilidade']}")
        col6.metric("UX Equity", f"{valores['UX Equity']}")
    else:
        st.subheader("Evolução dos Constructos")
        ondas = [onda.split(" - ")[0] for onda in onda_selecionada]
        fig_evolucao = go.Figure()
        
        for constructo in ["Usabilidade", "CX", "Engajamento", "Tecnologia", "Utilidade", "UX Equity"]:
            valores_constructo = [dados_ondas[onda][constructo] for onda in onda_selecionada]
            fig_evolucao.add_trace(go.Scatter(x=ondas, y=valores_constructo, mode="lines+markers", name=constructo,
                                              line=dict(dash="dash" if constructo != "UX Equity" else "solid")))
        fig_evolucao.update_layout(title="Evolução dos Constructos", xaxis_title="Onda", yaxis_title="Pontuação")
        st.plotly_chart(fig_evolucao)

    # Seletor de visão para abas ou telas
    visao = st.radio("Selecione a visão", ["Visão Geral", "Abas", "Telas"])

    # Dados variáveis para abas e telas com variações por onda
    dados_abas = {
        "Onda 1 - Q1": {
            "Home": {"Usabilidade": 74, "CX": 68, "Engajamento": 77, "Tecnologia": 83, "Utilidade": 78},
            "Produtos": {"Usabilidade": 71, "CX": 67, "Engajamento": 75, "Tecnologia": 80, "Utilidade": 76},
            "Suporte": {"Usabilidade": 72, "CX": 65, "Engajamento": 73, "Tecnologia": 79, "Utilidade": 74},
            "Conta": {"Usabilidade": 73, "CX": 66, "Engajamento": 76, "Tecnologia": 82, "Utilidade": 77}
        },
        "Onda 2 - Q2": {
            "Home": {"Usabilidade": 76, "CX": 69, "Engajamento": 78, "Tecnologia": 84, "Utilidade": 79},
            "Produtos": {"Usabilidade": 73, "CX": 68, "Engajamento": 76, "Tecnologia": 82, "Utilidade": 78},
            "Suporte": {"Usabilidade": 71, "CX": 67, "Engajamento": 74, "Tecnologia": 80, "Utilidade": 76},
            "Conta": {"Usabilidade": 75, "CX": 69, "Engajamento": 77, "Tecnologia": 83, "Utilidade": 80}
        },
        "Onda 3 - Q3": {
            "Home": {"Usabilidade": 78, "CX": 71, "Engajamento": 80, "Tecnologia": 85, "Utilidade": 81},
            "Produtos": {"Usabilidade": 74, "CX": 70, "Engajamento": 78, "Tecnologia": 83, "Utilidade": 79},
            "Suporte": {"Usabilidade": 73, "CX": 68, "Engajamento": 76, "Tecnologia": 82, "Utilidade": 78},
            "Conta": {"Usabilidade": 77, "CX": 70, "Engajamento": 79, "Tecnologia": 86, "Utilidade": 82}
        },
        "Onda 4 - Q4": {
            "Home": {"Usabilidade": 80, "CX": 73, "Engajamento": 82, "Tecnologia": 87, "Utilidade": 83},
            "Produtos": {"Usabilidade": 76, "CX": 72, "Engajamento": 80, "Tecnologia": 85, "Utilidade": 81},
            "Suporte": {"Usabilidade": 75, "CX": 70, "Engajamento": 78, "Tecnologia": 84, "Utilidade": 80},
            "Conta": {"Usabilidade": 79, "CX": 74, "Engajamento": 81, "Tecnologia": 88, "Utilidade": 84}
        }
    }
    
    dados_telas = {
        "Onda 1 - Q1": {
            "Login": {"Usabilidade": 72, "CX": 66, "Engajamento": 74, "Tecnologia": 81, "Utilidade": 77},
            "Dashboard": {"Usabilidade": 73, "CX": 67, "Engajamento": 75, "Tecnologia": 82, "Utilidade": 78},
            "Transações": {"Usabilidade": 71, "CX": 65, "Engajamento": 73, "Tecnologia": 80, "Utilidade": 76}
        },
        "Onda 2 - Q2": {
            "Login": {"Usabilidade": 74, "CX": 67, "Engajamento": 76, "Tecnologia": 82, "Utilidade": 78},
            "Dashboard": {"Usabilidade": 75, "CX": 68, "Engajamento": 77, "Tecnologia": 83, "Utilidade": 79},
            "Transações": {"Usabilidade": 72, "CX": 66, "Engajamento": 74, "Tecnologia": 81, "Utilidade": 77}
        },
        "Onda 3 - Q3": {
            "Login": {"Usabilidade": 76, "CX": 69, "Engajamento": 78, "Tecnologia": 84, "Utilidade": 80},
            "Dashboard": {"Usabilidade": 77, "CX": 70, "Engajamento": 79, "Tecnologia": 85, "Utilidade": 81},
            "Transações": {"Usabilidade": 75, "CX": 68, "Engajamento": 76, "Tecnologia": 83, "Utilidade": 79}
        },
        "Onda 4 - Q4": {
            "Login": {"Usabilidade": 78, "CX": 72, "Engajamento": 81, "Tecnologia": 86, "Utilidade": 83},
            "Dashboard": {"Usabilidade": 79, "CX": 73, "Engajamento": 82, "Tecnologia": 87, "Utilidade": 84},
            "Transações": {"Usabilidade": 77, "CX": 70, "Engajamento": 78, "Tecnologia": 85, "Utilidade": 81}
        }
    }

    if visao in ["Abas", "Telas"]:
    # Define itens como abas ou telas, com base na escolha do usuário
        itens = list(dados_abas["Onda 1 - Q1"].keys()) if visao == "Abas" else list(dados_telas["Onda 1 - Q1"].keys())
        selecao = st.multiselect(f"Escolha uma {visao.lower()}", itens)

    if len(onda_selecionada) == 1:
        # Se apenas uma onda é selecionada, mostrar gráfico radar para comparação de itens
        dados_selecionados = dados_abas if visao == "Abas" else dados_telas
        fig_radar = go.Figure()
        for item in selecao:
            valores = dados_selecionados[onda_selecionada[0]][item]
            fig_radar.add_trace(go.Scatterpolar(
                r=list(valores.values()),
                theta=list(valores.keys()),
                fill='toself',
                name=item
            ))
        fig_radar.update_layout(title=f"Comparação de {visao} - {onda_selecionada[0]}", polar=dict(radialaxis=dict(visible=True, range=[60, 90])))
        st.plotly_chart(fig_radar)

    elif len(selecao) == 1:
        # Se várias ondas são selecionadas mas apenas um item (aba ou tela), mostrar evolução dos constructos
        item = selecao[0]
        dados_selecionados = dados_abas if visao == "Abas" else dados_telas
        ondas = [onda.split(" - ")[0] for onda in onda_selecionada]
        
        # Preparar dados para evolução dos constructos ao longo das ondas
        valores_constructos = {
            constructo: [dados_selecionados[onda][item][constructo] for onda in onda_selecionada] 
            for constructo in ["Usabilidade", "CX", "Engajamento", "Tecnologia", "Utilidade"]
        }

        fig_evolucao_constructo = go.Figure()
        for constructo, valores in valores_constructos.items():
            fig_evolucao_constructo.add_trace(go.Scatter(
                x=ondas,
                y=valores,
                mode="lines+markers",
                name=constructo,
                line=dict(shape='linear')
            ))
        fig_evolucao_constructo.update_layout(title=f"Evolução dos Constructos para {item} nas Ondas Selecionadas", xaxis_title="Onda", yaxis_title="Pontuação")
        st.plotly_chart(fig_evolucao_constructo)

    # Bloco de matriz de prioridades de UX
    st.subheader("Matriz de Prioridades de UX")
    fatores = ["Facilidade", "Clareza", "Acessibilidade", "Atendimento", "Resolução", "Eficiência", "Diversão", "Interação", "Personalização"]
    importancia_fatores = [0.72, 0.6, 0.85, 0.68, 0.9, 0.88, 0.67, 0.7, 0.88]
    performance_fatores = [0.7, 0.63, 0.8, 0.83, 0.78, 0.85, 0.7, 0.66, 0.84]

    fig_matriz_ux = go.Figure()
    fig_matriz_ux.add_trace(go.Scatter(
        x=performance_fatores,
        y=importancia_fatores,
        mode='markers+text',
        text=fatores,
        textposition="top center",
        marker=dict(size=12, color="purple")
    ))
    fig_matriz_ux.update_layout(title="Performance vs. Importância dos Fatores de UX", xaxis_title="Performance", yaxis_title="Importância")
    st.plotly_chart(fig_matriz_ux)

    # Bloco final: Retorno de UX para o Negócio
    st.subheader("Retorno de UX para o Negócio")
    resultados = ["Contratação de Crédito", "Uso do App", "Principalidade", "NPS", "Branding", "Investimentos"]
    impacto_ux_equity = [0.7, 0.65, 0.8, 0.75, 0.6, 0.85]

    fig_retorno_ux = go.Figure(go.Bar(
        x=impacto_ux_equity,
        y=resultados,
        orientation='h',
        marker=dict(color="green"),
        text=[f"{val:.0%}" for val in impacto_ux_equity],
        textposition="outside"
    ))
    fig_retorno_ux.update_layout(title="Impacto do UX Equity em Resultados Estratégicos", xaxis_title="Impacto (R²)", yaxis_title="Resultados")
    st.plotly_chart(fig_retorno_ux)

# Parte FLAG: LTV MODELING
elif aba_selecionada == "FLAG":
    st.header("FLAG - Previsão de LTV & ROAS VBB")
    def format_with_zeros(x, pos):
        return f'{int(x):,}'.replace(",", ".")
    df = pd.read_csv("digital_wallet_ltv_dataset.csv")
    plt.style.use('fivethirtyeight')
    sns.set_context("poster", font_scale=0.5)
    
    df_novo = df.copy()
    app_usage_map = {'Daily': 30, 'Weekly': 4, 'Monthly': 1}
    income_level_map = {'Low': 1, 'Middle': 5, 'High': 10}

    df_novo['app_usage_numerico'] = df_novo['App_Usage_Frequency'].map(app_usage_map)
    df_novo['income_level_numerico'] = df_novo['Income_Level'].map(income_level_map)
    df_novo.drop(['App_Usage_Frequency', 'Income_Level'], axis=1, inplace=True)

    location_map = {'Urban': 3, 'Suburban': 2, 'Rural': 1}
    df_novo['location_numerico'] = df_novo['Location'].map(location_map)
    df_novo.drop(['Location'], axis=1, inplace=True)

    ltv_mean_by_payment = df_novo.groupby("Preferred_Payment_Method")["LTV"].mean().reset_index()
    ltv_mean_by_payment = ltv_mean_by_payment.sort_values(by="LTV", ascending=False).reset_index(drop=True)
    ltv_mean_by_payment["payment_score"] = range(len(ltv_mean_by_payment), 0, -1)

    df_novo = df_novo.merge(ltv_mean_by_payment[['Preferred_Payment_Method', 'payment_score']], 
                            on='Preferred_Payment_Method', how='left')
    df_novo.rename(columns={'payment_score': 'payment_score_per_client'}, inplace=True)
    df_novo.drop(columns=['Preferred_Payment_Method'], inplace=True)

    features = df_novo.drop(['Customer_ID', 'LTV'], axis=1)
    target = df_novo['LTV']

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features) #normalizando

    optimal_k = 5
    num_clusters = 5
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df_novo['cluster_label'] = kmeans.fit_predict(df_novo.drop(columns=['Customer_ID', 'LTV']))

    cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=df_novo.columns.drop(['Customer_ID', 'LTV', 'cluster_label']))
    cluster_summary = df_novo.drop(columns=['Customer_ID']).groupby('cluster_label').agg(['mean', 'median', 'std'])
    cluster_summary.columns = ['_'.join(col).strip() for col in cluster_summary.columns.values]

    features = df_novo.drop(columns=['Customer_ID', 'cluster_label', 'LTV'])
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(features)
    df_novo['PCA_1'] = pca_components[:, 0]
    df_novo['PCA_2'] = pca_components[:, 1]
    cluster_models = {}
    cluster_metrics = {}
    clustered_predictions = []

    # Selecionando uma distribuição para o GLM (Gamma geralmente é adequada para valores contínuos como o LTV)
    for cluster in df_novo['cluster_label'].unique():
        # Subconjunto dos dados para o cluster atual
        cluster_data = df_novo[df_novo['cluster_label'] == cluster]
        X = cluster_data.drop(columns=['Customer_ID', 'cluster_label', 'LTV'])
        y = cluster_data['LTV']
        
        # Adicionando uma constante para o intercepto
        X = sm.add_constant(X)

        # Ajustando o modelo GLM com distribuição Gamma
        glm_model = sm.GLM(y, X, family=sm.families.Gamma())
        glm_results = glm_model.fit()

        # Guardando o modelo e as métricas
        cluster_models[cluster] = glm_results
        cluster_metrics[cluster] = {
            "AIC": glm_results.aic,
            "Pseudo R-squared": glm_results.prsquared if hasattr(glm_results, 'prsquared') else None,
            "Coefficients": glm_results.params
        }

        # Realizando previsões para o cluster atual
        cluster_predictions = glm_results.predict(X)
        clustered_predictions.extend(cluster_predictions)

    evaluation_metrics = {}

    for cluster in df_novo['cluster_label'].unique():
        # Dados do cluster
        cluster_data = df_novo[df_novo['cluster_label'] == cluster]
        X_cluster = sm.add_constant(cluster_data.drop(columns=['Customer_ID', 'cluster_label', 'LTV']))
        y_cluster = cluster_data['LTV']
        
        # Previsão para o cluster usando o modelo específico do cluster
        predictions = cluster_models[cluster].predict(X_cluster)
        
        # Cálculo de métricas de erro
        mae = mean_absolute_error(y_cluster, predictions)
        mse = mean_squared_error(y_cluster, predictions)
        rmse = np.sqrt(mse)

        evaluation_metrics[cluster] = {
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse
        }

    glm_models = {}

    for cluster in df_novo['cluster_label'].unique():
        # Filter data for the current cluster
        cluster_data = df_novo[df_novo['cluster_label'] == cluster]
        
        # Add a constant column to the cluster_data DataFrame
        cluster_data['const'] = 1  # This line is crucial for fixing the KeyError
        
        # Define independent variables for the GLM model
        X = cluster_data[['const', 'PCA_1', 'PCA_2', 'Age', 'Total_Transactions',
                          'Avg_Transaction_Value', 'Max_Transaction_Value', 'Min_Transaction_Value',
                          'Total_Spent', 'Active_Days', 'Last_Transaction_Days_Ago',
                          'Loyalty_Points_Earned', 'Referral_Count', 'Cashback_Received',
                          'Support_Tickets_Raised', 'Issue_Resolution_Time',
                          'Customer_Satisfaction_Score', 'app_usage_numerico',
                          'income_level_numerico', 'location_numerico', 'payment_score_per_client']]
        y = cluster_data['LTV']
        
        # Fit the GLM model with a Gamma distribution
        model = sm.GLM(y, X, family=sm.families.Gamma()).fit()
        
        # Store the trained model in the dictionary
        glm_models[cluster] = model

    # Função para aplicar previsões usando os modelos GLM por cluster
    def apply_predictions(data, glm_models):
        predicted_ltv_values = []
        
        # Iterar por cada linha do df para aplicar o modelo correspondente ao cluster
        for _, row in data.iterrows():
            cluster = row['cluster_label']
            model = glm_models[cluster]
            
            # Define os dados da linha para previsão com as colunas usadas no treino
            row_for_prediction = row[['const', 'PCA_1', 'PCA_2', 'Age', 'Total_Transactions',
                                      'Avg_Transaction_Value', 'Max_Transaction_Value', 'Min_Transaction_Value',
                                      'Total_Spent', 'Active_Days', 'Last_Transaction_Days_Ago',
                                      'Loyalty_Points_Earned', 'Referral_Count', 'Cashback_Received',
                                      'Support_Tickets_Raised', 'Issue_Resolution_Time',
                                      'Customer_Satisfaction_Score', 'app_usage_numerico',
                                      'income_level_numerico', 'location_numerico', 'payment_score_per_client']]
            
            # Calcula a previsão e adiciona à lista
            predicted_ltv = model.predict(row_for_prediction)[0]
            predicted_ltv_values.append(predicted_ltv)
        
        # Adiciona as previsões ao dataframe original
        data['conversion_value'] = predicted_ltv_values
        return data

    # Adiciona a constante para previsões
    df_novo['const'] = 1

    # Aplicar previsões ao df_novo e salvar em `conversion_value`
    df_novo = apply_predictions(df_novo, glm_models)

    avg_conversion_per_cluster_income = df_novo.groupby(['cluster_label', 'income_level_numerico'])['conversion_value'].mean().reset_index()

    cluster_names = {2: 'Alto-Potencial', 4: 'Bons-Clientes', 1: 'Medianos', 3: 'Clientes-Ruins', 0: 'Muito-Ruins'}
    income_names = {10: 'Alta Renda', 5: 'Mass Market Medium', 1: 'Mass Market Low'}

    df_novo['cluster_label'] = df_novo['cluster_label'].map(cluster_names)
    df_novo['income_level_numerico'] = df_novo['income_level_numerico'].map(income_names)


    df_novo['conversion_value'] = df_novo['conversion_value'] / 50

    def format_with_currency(x, pos):
        return f'R${int(x):,}'.replace(",", ".")

    avg_conversion_per_cluster_income = df_novo.groupby(['cluster_label', 'income_level_numerico'])['conversion_value'].mean().reset_index()

    # Subbloco de KPIs
    st.subheader("KPIs de Performance")
    
    # Filtros (apenas ilustrativos)
    st.write("### Filtros")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_selecionada = st.date_input("Selecione a data", [])
    with col2:
        regioes = st.multiselect("Selecione a(s) Região(ões)", ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"])
    with col3:
        plataformas = st.multiselect("Selecione a(s) Plataforma(s)", ["Google Ads", "Meta"])
    
    # Seleção de KPIs para exibir no gráfico de linhas
    kpis_selecionados = st.multiselect("Selecione os KPIs para o gráfico de linhas", ["ROAS", "Taxa de Conversão", "CPC", "LTV Médio"])

    # Gráfico de KPIs selecionados ao longo de 6 meses
    if kpis_selecionados:
        # Dados fictícios para visualização
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        dados_kpis = {
            "ROAS": [1.2, 1.4, 1.3, 1.5, 1.6, 1.4],
            "Taxa de Conversão": [0.03, 0.04, 0.035, 0.038, 0.04, 0.042],
            "CPC": [0.5, 0.45, 0.48, 0.46, 0.44, 0.43],
            "LTV Médio": [200, 220, 210, 230, 240, 225]
        }
        
        fig_kpis = go.Figure()
        for kpi in kpis_selecionados:
            fig_kpis.add_trace(go.Scatter(x=meses, y=dados_kpis[kpi], mode="lines+markers", name=kpi))
        
        fig_kpis.update_layout(
            title="KPIs de Performance (últimos 6 meses)",
            xaxis_title="Meses",
            yaxis_title="Valor",
            legend_title="KPI"
        )
        st.plotly_chart(fig_kpis)

    # Subbloco de Integridade de Conectores
    st.subheader("Integridade de Conectores")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.success("Google Ads")
    with col2:
        st.success("Meta")
    with col3:
        st.success("HubSpot")
    with col4:
        st.success("Azure")

    # Subbloco de Modelo de LTV Core
    st.subheader("Modelo de LTV Core")
    
    # Exibição da Acurácia (dados fictícios)
    col1, col2, col3 = st.columns(3)
    col1.metric("Acurácia - Mês 1", "80%")
    col2.metric("Acurácia - Mês 2", "85%")
    col3.metric("Acurácia - Mês 3", "83%")
    col1.metric("Acurácia - Mês 4", "86%")
    col2.metric("Acurácia - Mês 5", "82%")
    col3.metric("Acurácia - Mês 6", "89%")

    # Gráfico de "Conversion Value" por Clusters usando Plotly
    st.subheader("Conversion Value Próximos 180 dias vs Cluster")
    
    # Convertendo os dados para gráfico
    avg_conversion_per_cluster_income['income_level_numerico'] = avg_conversion_per_cluster_income['income_level_numerico'].map({
        'Alta Renda': 'Alta Renda',
        'Mass Market Medium': 'Média Renda',
        'Mass Market Low': 'Baixa Renda'
    })

    fig_conversion = px.bar(
        avg_conversion_per_cluster_income,
        x='cluster_label',
        y='conversion_value',
        color='income_level_numerico',
        title='Conversion Value próximos 180 dias vs Cluster & Renda',
        labels={
            'cluster_label': 'Cluster',
            'conversion_value': 'Conversion Value Médio (R$)',
            'income_level_numerico': 'Renda'
        },
        text='conversion_value'
    )
    fig_conversion.update_traces(texttemplate="R$ %{text:.2s}", textposition="outside")
    fig_conversion.update_layout(
        yaxis_tickformat="R$",
        xaxis_title="Cluster",
        yaxis_title="Conversion Value Médio",
        legend_title="Nível de Renda",
        height=500
    )

    st.plotly_chart(fig_conversion)
