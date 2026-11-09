import pandas as pd

def moneyParser(serie):
    serie_limpa = (
        serie
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
    )
    
    return pd.to_numeric(serie_limpa, errors='coerce')

if __name__ == '__main__':
    df = pd.read_csv('data/raw/tabela_dados_completos.csv')

    # Tratando string de valores monetários:
    df['domestic_bo'] = moneyParser(df['domestic_bo'])
    df['domestic_bo_original'] = moneyParser(df['domestic_bo_original'])
    df['estreia_bilheteria'] = moneyParser(df['estreia_bilheteria'])
    df['semana_2'] = moneyParser(df['semana_2'])
    df['semana_3'] = moneyParser(df['semana_3'])
    df['semana_4'] = moneyParser(df['semana_4'])

    # Normalizar domestic share:
    if 'domestic_share' in df.columns:
        df['domestic_share'] = (
            df['domestic_share']
            .astype(str)
            .str.replace('%', '', regex=False)
            .str.strip()
        )
        df['domestic_share'] = pd.to_numeric(df['domestic_share'], errors='coerce')
        df['domestic_share'] = (df['domestic_share'] / 100).round(3)

    # Tratar erros no rating:
    if 'rating' in df.columns:
        df['rating'] = (df['rating']
                   .astype(str)
                   .str.replace('\n', ' ', regex=False)
                   .str.strip()
                   .str.split()
                   .str[0]
        )

    # Reajustando a inflação dos dados semanais:
    fator_inflacao = df['domestic_bo'] / df['domestic_bo_original']
    fator_inflacao = fator_inflacao.fillna(1.0)
    colunas_semanais = ['estreia_bilheteria', 'semana_2', 'semana_3', 'semana_4']

    for col in colunas_semanais:
        if col in df.columns:
            df[col] = (df[col] * fator_inflacao).round(2)

    print(df.info())
    df.to_csv('data/processed/tabela_tratada.csv', index=False)