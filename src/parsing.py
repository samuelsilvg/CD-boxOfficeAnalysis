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

    # Tratando valores monetários antes de salvar:
    df['domestic_bo'] = moneyParser(df['domestic_bo'])
    df['estreia_bilheteria'] = moneyParser(df['estreia_bilheteria'])
    df['semana_2'] = moneyParser(df['semana_2'])
    df['semana_3'] = moneyParser(df['semana_3'])
    df['semana_4'] = moneyParser(df['semana_4'])

    print(df.info())
    df.to_csv('data/raw/tabela_tratada.csv', index=False)