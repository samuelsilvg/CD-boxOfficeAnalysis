import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def getTablesURL(url, mode):
    '''Retorna a primeira ou todas as tabelas HTML de uma URL.'''
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        site = BeautifulSoup(resposta.text, 'html.parser')
        
        if mode == 'first':
            tabela = site.find('table')
            return tabela
        
        elif mode == 'all':
            lista_tabelas = site.find_all('table')
            return lista_tabelas
    else:
        raise Exception('getTablesURL :: erro ao obter tabela/tabelas.')
        

def WSWorldwideBoxOffice(ano):
    '''Extrai os dados com base em um ano e gera um dataset.'''

    url = f"https://www.boxofficemojo.com/year/world/{ano}/"

    dados = []
    lista_links = []
    colunas_nomes = ['Rank', 'Release Group', 'Worldwide', 'Domestic', 'Domestic_%', 'Foreign', 'Foreign_%']

    tabela = getTablesURL(url, 'first')

    # Gerando o dataset:
    if tabela == None:
        raise Exception('erro na extracao da tabela.')
    else:
        for linha in tabela.find_all('tr'):
            colunas = linha.find_all('td')
            if colunas:
                valores = [col.text.strip() for col in colunas]

                tag_a = colunas[1].find('a')
                if tag_a and tag_a.has_attr('href'):
                    link = tag_a['href']
                    link_completo = f"https://www.boxofficemojo.com{link}"
                    lista_links.append(link_completo)

                dados.append(valores)

        df = pd.DataFrame(dados)
        df.columns = colunas_nomes
        df['data_links'] = lista_links

        df.to_csv(f'data/raw/{ano}/world/worldwide_box_{ano}.csv', index=False)
        return df
    

def WSMovieBoxOffice(url):
    '''Retorna tabelas individuais de um filme.'''

    dados = []
    colunas_nomes = ['Market', 'Release_Date', 'Opening', 'Gross']

    lista_tabelas = getTablesURL(url, 'all')

    if lista_tabelas == None:
            raise Exception('erro na extracao da tabela.')
    else:
        for tabela in lista_tabelas:
            for linha in tabela.find_all('tr'):
                colunas = linha.find_all('td')
                if colunas:
                    valores = [col.text.strip() for col in colunas]    
                    dados.append(valores)

        df = pd.DataFrame(dados)
        df.columns = colunas_nomes
        return df


def getBoxOfficeYear(ano):
    '''Extrai informações do top global e 
    de filmes individuais com base no ano.'''

    print(f'> Obtendo o rank global dos filmes de {ano}: ')
    worldwide_box_2026_df = WSWorldwideBoxOffice(ano)

    print(f'> Obtendo as tabelas de cada filme do rank de {ano}: ')
    for index, row in worldwide_box_2026_df.iterrows():
        movie_rank = row['Rank']
        movie_info_df = WSMovieBoxOffice(row['data_links'])
        movie_info_df.to_csv(f'data/raw/{ano}/movies/{movie_rank}.csv', index=False)

        time.sleep(1.5)

    print(f'> Tabelas salvas em CSV com sucesso em data/raw/{ano}!')



if __name__ == '__main__':
    # Usando como exemplo o ano de 2026
    getBoxOfficeYear(2026)

    