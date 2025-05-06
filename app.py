import pandas as pd
import streamlit as st

# Carrega os dados do CSV
df = pd.read_csv("classificacao_pilotos_2025_miami.csv")

# Tabela de pontos da F1 (top 10)
points_table = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

# Configuração do Streamlit
st.set_page_config(page_title="Simulador de Pontuação F1", layout="centered")
st.title("🏎️ Simulador de Pontuação da Fórmula 1")

# Abas para Piloto, Construtor e Comparação de Equipes
aba_piloto, aba_construtor, aba_comparacao = st.tabs(["👤 Piloto", "🏢 Construtor", "📊 Comparação de Equipes"])

# 🏎️ Seção Piloto
with aba_piloto:
    st.subheader("Simulador de Pontuação por Piloto")

    # Criando uma lista que combina número e nome
    pilotos_com_numeros = [f"{row['Número']} - {row['Piloto']}" for _, row in df.iterrows()]

    # Escolha do primeiro piloto
    escolha_piloto_1 = st.selectbox("Escolha o primeiro piloto:", pilotos_com_numeros)
    num_piloto_1 = int(escolha_piloto_1.split(" - ")[0])
    pilotos_restantes = [piloto for piloto in pilotos_com_numeros if int(piloto.split(" - ")[0]) != num_piloto_1]

    # Escolha da posição do primeiro piloto
    posicoes_disponiveis = list(range(1, 21))
    posicao_piloto_1 = st.selectbox(f"Qual foi a posição do piloto {escolha_piloto_1} na corrida?", posicoes_disponiveis)

    # Remover a posição escolhida para o primeiro piloto da lista de posições disponíveis para o segundo piloto
    posicoes_disponiveis.remove(posicao_piloto_1)

    # Escolha do segundo piloto
    escolha_piloto_2 = st.selectbox("Escolha o segundo piloto:", pilotos_restantes)
    num_piloto_2 = int(escolha_piloto_2.split(" - ")[0])

    # Escolha da posição do segundo piloto (garante que a posição já escolhida não será duplicada)
    posicao_piloto_2 = st.selectbox(f"Qual foi a posição do piloto {escolha_piloto_2} na corrida?", posicoes_disponiveis)

    # Obter dados dos pilotos
    piloto_row_1 = df[df["Número"] == num_piloto_1]
    piloto_row_2 = df[df["Número"] == num_piloto_2]

    if piloto_row_1.empty or piloto_row_2.empty:
        st.error("❌ Piloto(s) não encontrados.")
    else:
        piloto_1 = piloto_row_1.iloc[0]["Piloto"]
        pontos_atuais_1 = piloto_row_1.iloc[0]["Pontos"]
        pontos_corrida_1 = points_table[posicao_piloto_1 - 1] if posicao_piloto_1 <= 10 else 0
        total_1 = pontos_atuais_1 + pontos_corrida_1

        piloto_2 = piloto_row_2.iloc[0]["Piloto"]
        pontos_atuais_2 = piloto_row_2.iloc[0]["Pontos"]
        pontos_corrida_2 = points_table[posicao_piloto_2 - 1] if posicao_piloto_2 <= 10 else 0
        total_2 = pontos_atuais_2 + pontos_corrida_2

        st.markdown(f"### 🏁 Resultado para os pilotos escolhidos")
        st.write(f"- **{piloto_1}** (Número {num_piloto_1})")
        st.write(f"  - Posição na corrida: P{posicao_piloto_1} → {pontos_corrida_1} pontos")
        st.write(f"  - Total acumulado: **{total_1} pontos**")

        st.write(f"- **{piloto_2}** (Número {num_piloto_2})")
        st.write(f"  - Posição na corrida: P{posicao_piloto_2} → {pontos_corrida_2} pontos")
        st.write(f"  - Total acumulado: **{total_2} pontos**")

# 🏢 Seção Construtor
with aba_construtor:
    st.subheader("Simulador de Pontuação por Construtor")

    equipe = st.selectbox("Escolha a equipe:", df["Equipe"].unique())
    pilotos_equipe = df[df["Equipe"] == equipe]

    if len(pilotos_equipe) != 2:
        st.error("❌ Não foi possível identificar dois pilotos para essa equipe.")
    else:
        st.markdown(f"### 🏁 Pilotos da equipe **{equipe}**")

        piloto_1 = pilotos_equipe.iloc[0]
        piloto_2 = pilotos_equipe.iloc[1]

        st.write(f"- **{piloto_1['Piloto']}** (Número {piloto_1['Número']})")
        st.write(f"- **{piloto_2['Piloto']}** (Número {piloto_2['Número']})")

        posicoes_disponiveis = list(range(1, 21))

        # Escolha da posição do primeiro piloto
        posicao_1 = st.selectbox(
            f"Posição final do {piloto_1['Piloto']}:",
            posicoes_disponiveis,
            key=f"posicao_1_{equipe}"
        )

        # Remove a posição escolhida pelo primeiro piloto da lista do segundo
        posicoes_para_segundo = [p for p in posicoes_disponiveis if p != posicao_1]

        # Escolha da posição do segundo piloto, com exclusão
        posicao_2 = st.selectbox(
            f"Posição final do {piloto_2['Piloto']}:",
            posicoes_para_segundo,
            key=f"posicao_2_{equipe}"
        )

        pontos_1 = points_table[posicao_1 - 1] if posicao_1 <= 10 else 0
        pontos_2 = points_table[posicao_2 - 1] if posicao_2 <= 10 else 0

        pontos_atuais = pilotos_equipe["Pontos"].sum()
        pontos_corrida = pontos_1 + pontos_2
        total = pontos_atuais + pontos_corrida

        st.markdown(f"### 🏁 Resultado para a equipe **{equipe}**")
        st.write(f"- Pontos na corrida: **{pontos_corrida}** ({pontos_1} + {pontos_2})")
        st.write(f"- Total acumulado no campeonato: **{total} pontos**")

with aba_comparacao:
    st.subheader("Comparação de Pontuação entre duas Equipes")

    equipe_1 = st.selectbox("Escolha a primeira equipe:", df["Equipe"].unique())

    equipes_disponiveis = df["Equipe"].unique()
    equipes_disponiveis = equipes_disponiveis[equipes_disponiveis != equipe_1]

    equipe_2 = st.selectbox("Escolha a segunda equipe:", equipes_disponiveis)

    pilotos_equipe_1 = df[df["Equipe"] == equipe_1]
    pilotos_equipe_2 = df[df["Equipe"] == equipe_2]

    if len(pilotos_equipe_1) != 2 or len(pilotos_equipe_2) != 2:
        st.error("❌ Cada equipe deve ter exatamente 2 pilotos.")
    else:
        st.markdown(f"### 🏁 Escolha as posições para as equipes **{equipe_1}** e **{equipe_2}**")

        posicoes_disponiveis = list(range(1, 21))

        # Equipe 1
        posicao_1_eq1 = st.selectbox(
            f"Posição do piloto 1 da equipe {equipe_1} ({pilotos_equipe_1.iloc[0]['Piloto']}):",
            posicoes_disponiveis
        )

        posicoes_restantes_eq1 = [p for p in posicoes_disponiveis if p != posicao_1_eq1]
        posicao_2_eq1 = st.selectbox(
            f"Posição do piloto 2 da equipe {equipe_1} ({pilotos_equipe_1.iloc[1]['Piloto']}):",
            posicoes_restantes_eq1
        )

        # Equipe 2
        posicoes_restantes_eq2 = [p for p in posicoes_disponiveis if p not in [posicao_1_eq1, posicao_2_eq1]]
        posicao_1_eq2 = st.selectbox(
            f"Posição do piloto 1 da equipe {equipe_2} ({pilotos_equipe_2.iloc[0]['Piloto']}):",
            posicoes_restantes_eq2
        )

        posicoes_restantes_eq2_final = [p for p in posicoes_restantes_eq2 if p != posicao_1_eq2]
        posicao_2_eq2 = st.selectbox(
            f"Posição do piloto 2 da equipe {equipe_2} ({pilotos_equipe_2.iloc[1]['Piloto']}):",
            posicoes_restantes_eq2_final
        )

        # Calcula pontuações
        pontos_1_eq1 = points_table[posicao_1_eq1 - 1] if posicao_1_eq1 <= 10 else 0
        pontos_2_eq1 = points_table[posicao_2_eq1 - 1] if posicao_2_eq1 <= 10 else 0
        pontos_1_eq2 = points_table[posicao_1_eq2 - 1] if posicao_1_eq2 <= 10 else 0
        pontos_2_eq2 = points_table[posicao_2_eq2 - 1] if posicao_2_eq2 <= 10 else 0

        pontos_atuais_eq1 = pilotos_equipe_1["Pontos"].sum()
        pontos_atuais_eq2 = pilotos_equipe_2["Pontos"].sum()

        total_eq1 = pontos_atuais_eq1 + pontos_1_eq1 + pontos_2_eq1
        total_eq2 = pontos_atuais_eq2 + pontos_1_eq2 + pontos_2_eq2

        st.markdown(f"### 🏁 Resultado para as equipes **{equipe_1}** e **{equipe_2}**")

        st.write(f"- **{equipe_1}**: {pontos_atuais_eq1} (atuais) + {pontos_1_eq1} + {pontos_2_eq1} = **{total_eq1} pontos**")
        st.write(f"- **{equipe_2}**: {pontos_atuais_eq2} (atuais) + {pontos_1_eq2} + {pontos_2_eq2} = **{total_eq2} pontos**")

        if total_eq1 > total_eq2:
            st.success(f"A **{equipe_1}** está à frente com **{total_eq1} pontos**, uma diferença de **{total_eq1 - total_eq2} pontos**.")
        elif total_eq2 > total_eq1:
            st.success(f"A **{equipe_2}** está à frente com **{total_eq2} pontos**, uma diferença de **{total_eq2 - total_eq1} pontos**.")
        else:
            st.info(f"As equipes estão empatadas com **{total_eq1} pontos**.")
