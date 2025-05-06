import pandas as pd

import pandas as pd

# Lê o CSV com os dados dos pilotos
df = pd.read_csv("classificacao_pilotos_2025_miami.csv")

points_table = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]


# Mostra os pilotos e seus números
print("Pilotos disponíveis:")
for _, row in df.iterrows():
    print(f"{row['Número']:>2} - {row['Piloto']}")

# Input do usuário
num = int(input("\nEscolha o número do piloto: "))
posicao = int(input("Digite a posição final na corrida (1-20): "))

# Filtra piloto pelo número
piloto_row = df[df['Número'] == num]

if piloto_row.empty:
    print("❌ Número de piloto não encontrado.")
else:
    piloto = piloto_row.iloc[0]['Piloto']
    pontos_atuais = piloto_row.iloc[0]['Pontos']
    pontos_corrida = points_table[posicao - 1] if posicao <= 10 else 0
    total = pontos_atuais + pontos_corrida

    print(f"\n🏁 Piloto: {piloto}")
    print(f"Posição na corrida: P{posicao} → {pontos_corrida} pontos")
    print(f"Total acumulado: {total} pontos")

# Mostra equipes únicas
equipes = df['Equipe'].unique()

print("Equipes disponíveis:")
for equipe in equipes:
    print("-", equipe)

# Escolha da equipe
equipe = input("\nDigite o nome da equipe: ")

# Filtra pilotos dessa equipe
pilotos_equipe = df[df['Equipe'] == equipe]

if len(pilotos_equipe) != 2:
    print("❌ Não foi possível identificar dois pilotos para essa equipe.")
else:
    print("\nPilotos da equipe", equipe)
    for _, row in pilotos_equipe.iterrows():
        print(f"{row['Número']} - {row['Piloto']}")

    # Input de posições
    pos1 = int(input("\nDigite a posição final do primeiro piloto (1-20): "))
    pos2 = int(input("Digite a posição final do segundo piloto (1-20): "))

    pontos1 = points_table[pos1 - 1] if pos1 <= 10 else 0
    pontos2 = points_table[pos2 - 1] if pos2 <= 10 else 0

    pontos_atuais = pilotos_equipe['Pontos'].sum()
    pontos_corrida = pontos1 + pontos2
    total = pontos_atuais + pontos_corrida

    print(f"\n🏁 Equipe: {equipe}")
    print(f"Pontos na corrida: {pontos_corrida} ({pontos1} + {pontos2})")
    print(f"Total acumulado no campeonato: {total} pontos")