import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Título principal do aplicativo
st.title("Simulador de Marketing Mix Modeling")

# Sidebar com título e seleção de aba
st.sidebar.title("OKIAR 360º")
aba_selecionada = st.sidebar.selectbox("Selecione a aba", ["MMM", "Media Behavior", "BRAIN", "MERIDIO", "MMX", "UXM"])

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
if aba_selecionada == "MMM":
    st.header("Dashboard de Marketing Mix Modeling")

    # Bloco Inicial: KPIs Principais
    st.subheader("Principais KPIs de Marketing")
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
elif aba_selecionada == "Media Behavior":
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


# Aba 3: BRAIN
elif aba_selecionada == "BRAIN":
    st.header("MARCA, CAMPANHAS & INFLUÊNCIA")

    # Matriz de performance por importância
    st.subheader("O que a marca é e precisa ser")
    atributos = ["Qualidade", "Inovação", "Confiabilidade", "Disponibilidade", "Atendimento", "Preço", "Sustentabilidade", "Design"]
    importancia = [8, 7, 9, 5, 6, 4, 7, 8]
    performance = [6, 8, 7, 4, 5, 3, 8, 7]

    fig_matriz = go.Figure()
    fig_matriz.add_trace(go.Scatter(
        x=importancia, y=performance, mode='markers+text', text=atributos, textposition="top center",
        marker=dict(size=12, color="red")
    ))
    fig_matriz.update_layout(title="Matriz de Importância vs. Performance", xaxis_title="Importância", yaxis_title="Performance")
    st.plotly_chart(fig_matriz)

    # Gráfico de radar para impacto de influenciadores
    st.subheader("Importância de Influência nos Atributos de Marca")
    atributos_radar = ["Qualidade", "Inovação", "Confiabilidade", "Disponibilidade", "Atendimento", "Preço", "Sustentabilidade", "Design"]
    influencia = [6, 7, 8, 6, 5, 6, 7, 8]
    geral = [5, 6, 6, 4, 4, 5, 6, 6]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=influencia, theta=atributos_radar, fill='toself', name='Influência'))
    fig_radar.add_trace(go.Scatterpolar(r=geral, theta=atributos_radar, fill='toself', name='Geral'))
    fig_radar.update_layout(title="Impacto de Influência vs. Geral")
    st.plotly_chart(fig_radar)

    # Gráfico de avaliação de eficiência de influenciadores
    st.subheader("Eficiência de Influência")
    eficiencia = {"Autenticidade": 7, "Adequação": 8, "Relevância": 6, "Endossamento": 7}
    fig_eficiencia = go.Figure(go.Bar(
        x=list(eficiencia.keys()), y=list(eficiencia.values()), marker=dict(color="red")
    ))
    fig_eficiencia.update_layout(title="Avaliação de Influência por Métrica")
    st.plotly_chart(fig_eficiencia)

# Parte MERIDIO: Segmentação e Personas
elif aba_selecionada == "MERIDIO":
    st.header("MERIDIO - Segmentação e Personas")
    
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
    st.header("MMX - Satisfação e Tracking Estrutural")

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

# Parte UXM: Modelo de UX e Retorno de Experiência
elif aba_selecionada == "UXM":
    st.header("UXM - Avaliação da Experiência do Usuário")

    # Bloco inicial: Diagnóstico da Qualidade de Experiência
    st.subheader("Diagnóstico da Qualidade da Experiência")
    
    # Constructos principais com valores fictícios de avaliação
    constructos = ["Usabilidade", "CX", "Engajamento", "Tecnologia", "Utilidade"]
    pontuacoes_constructos = [80, 75, 78, 85, 82]
    ux_equity = 77  # Valor da UX Equity como métrica de norte (north star metric)

    # Exibindo gráfico de barras para os constructos
    fig_constructos = go.Figure(go.Bar(
        x=constructos,
        y=pontuacoes_constructos,
        marker=dict(color="orange")
    ))
    fig_constructos.add_shape(
        type="line", x0=-0.5, x1=4.5, y0=ux_equity, y1=ux_equity,
        line=dict(color="red", dash="dash"), name="UX Equity"
    )
    fig_constructos.update_layout(title="Qualidade da Experiência por Constructo", yaxis_title="Pontuação")
    st.plotly_chart(fig_constructos)
    st.write("**Nota**: A linha pontilhada representa a métrica UX Equity.")

    # Botões de visão geral, abas e telas
    visao = st.radio("Selecione a visão", ["Visão Geral", "Abas", "Telas"])

    # Dados detalhados para visão geral e abas
    if visao == "Visão Geral":
        st.write("**Visão Geral da Qualidade no Aplicativo**")
        st.plotly_chart(fig_constructos)

    elif visao == "Abas":
        aba_selecionada = st.selectbox("Selecione a Aba para Comparação", ["Home", "Produtos", "Suporte", "Conta"])
        
        # Gráfico de radar comparativo para os constructos por aba
        fig_radar_abas = go.Figure()
        for aba in ["Home", "Produtos", "Suporte", "Conta"]:
            fig_radar_abas.add_trace(go.Scatterpolar(
                r=[np.random.uniform(70, 90) for _ in constructos],
                theta=constructos,
                fill='toself',
                name=aba
            ))
        fig_radar_abas.update_layout(title=f"Comparação dos Constructos - {aba_selecionada}")
        st.plotly_chart(fig_radar_abas)

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
        marker=dict(color="green")
    ))
    fig_retorno_ux.update_layout(title="Impacto do UX Equity em Resultados Estratégicos", xaxis_title="Impacto (R²)", yaxis_title="Resultados")
    st.plotly_chart(fig_retorno_ux)
