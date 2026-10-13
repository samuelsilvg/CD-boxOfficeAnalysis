import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


def createFolders(ano):
    '''Cria pastas necessarias caso elas ainda nâo existam.'''
    caminho_world = f'data/raw/{ano}/world'
    caminho_movies = f'data/raw/{ano}/movies'
    os.makedirs(caminho_world, exist_ok=True)
    os.makedirs(caminho_movies, exist_ok=True)


def createDriver():
    '''Cria o driver padrão do Selenium com Chromium.'''

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Navegador invisível
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    return driver


def getTNMovieTable(driver, ano):
    url = f'https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/released-in-{ano}'
    lista_tabela = []

    try:
        driver.get(url)
        time.sleep(5)

        linhas = driver.find_elements(By.XPATH, '//table//tr')
        for linha in linhas[1:]:
            lista_linha = []
        
            link_filme = linha.find_element(By.XPATH, './td[2]//a').get_attribute('href')
            data_filme = linha.find_element(By.XPATH, './td[3]').get_attribute('textContent').replace('\xa0', ' ')
            genero_filme = linha.find_element(By.XPATH, './td[5]').get_attribute('textContent')

            lista_linha.append(link_filme)
            lista_linha.append(data_filme)
            lista_linha.append(genero_filme)

            lista_tabela.append(lista_linha)

        return lista_tabela
            
    except Exception as e:
        print(f'getTNMoviesLinks::Ocorreu um erro: {e}')


def getTNMovieWData(driver, link):
    try:
        driver.get(link)
        time.sleep(3)

        linhas_tabela_dados = driver.find_elements(By.XPATH, '(//div[@id="box_office_chart"]//table)[4]//tr//td[3]')

        # Inicializa todas as semanas como None por segurança
        tk2, tk3, tk4 = None, None, None
        
        # Verifica se a tabela possui elementos suficientes antes de acessar os índices
        if len(linhas_tabela_dados) > 1:
            tk2 = linhas_tabela_dados[1].text # - Arrecadação no segundo fim de semana doméstico
        if len(linhas_tabela_dados) > 2:
            tk3 = linhas_tabela_dados[2].text # - Arrecadação no terceiro fim de semana doméstico
        if len(linhas_tabela_dados) > 3:
            tk4 = linhas_tabela_dados[3].text # - Arrecadação no quarto fim de semana doméstico

        return tk2, tk3, tk4
        
    except Exception as e:
        print(f'getTNMovieWData::Ocorreu um erro: {e}')
        return None, None, None
    
    
def getTNMovieInfo(driver, link):
    try:
        driver.get(link)
        time.sleep(3)

        lista_info = []

        # Inicializando como None para lidar com erros de coleta
        nome_filme = None
        estreia_bilheteria = None
        tn_legs = None
        domestic_share = None
        domestic_bo = None
        rating = None
        tempo = None
        producao = None
        wk2, wk3, wk4 = None, None, None

        # - Nome do filme
        nome_filme = driver.find_element(By.XPATH, '(//h1)[1]').text
        
        linhas_tabela_metricas = driver.find_elements(By.XPATH, '//div[@id="summary"]//table[1]//tr')
        for linha in linhas_tabela_metricas:
            colunas = linha.find_elements(By.TAG_NAME, 'td')

            # - Estreia da bilheteria doméstica
            if colunas[0].text == 'Opening Weekend:':
                estreia_bilheteria = colunas[1].text.split(' ')[0]
            
            # - Legs TheNumbers
            elif colunas[0].text == 'Legs:':
                tn_legs = colunas[1].text.split(' ')[0]

            # - Relação bilheteria doméstica/total (domestic share)
            elif colunas[0].text == 'Domestic Share:':
                domestic_share = colunas[1].text.split(' ')[0]

            # - Bilheteria doméstica total (ajustada pela inflação)
            elif colunas[0].text == 'Infl. Adj. Dom. BO':
                domestic_bo = colunas[1].text


        linhas_tabela_detalhes = driver.find_elements(By.XPATH, '//div[@id="summary"]//table[2]//tr')
        for linha in linhas_tabela_detalhes:
            colunas = linha.find_elements(By.TAG_NAME, 'td')

            # - MPA Rating (classificação indicativa do USA)
            if colunas[0].text == 'MPA Rating:':
                rating = colunas[1].text.split(' ')[0]

            # - Duração do filme (em minutos)
            elif colunas[0].text == 'Running Time:':
                tempo = colunas[1].text.split(' ')[0]

            # - Método de produção (live action ou animação, por exemplo)
            elif colunas[0].text == 'Production Method:':
                producao = colunas[1].text

        data_url = link + '#domestic'

        # - Arrecadação de cada fim de semana doméstico sem reajuste da inflação
        wk2, wk3, wk4 = getTNMovieWData(driver, data_url)
        
        # - Legs BOM (calculado em código)
        #bom_legs = domestic_bo / estreia_bilheteria

        lista_info.append(nome_filme)
        lista_info.append(tn_legs)
        lista_info.append(domestic_share)
        lista_info.append(domestic_bo)
        lista_info.append(rating)
        lista_info.append(tempo)
        lista_info.append(producao)

        lista_info.append(estreia_bilheteria)
        lista_info.append(wk2)
        lista_info.append(wk3)
        lista_info.append(wk4)

        return lista_info
        
    except Exception as e:
        print(f'getTNMovieInfo::Ocorreu um erro: {e}')



if __name__ == '__main__':
    # Cria pastas de data necessarias:
    caminho_raw = 'data/raw'
    caminho_processed = 'data/processed'
    os.makedirs(caminho_raw, exist_ok=True)
    os.makedirs(caminho_raw, exist_ok=True)

    createFolders(2026)
    driver = createDriver()

    print('-' * 50)
    print('W E B  S C R A P E R  |  The Numbers')
    print('-' * 50)
    
    print('> Buscando dados da tabela: ', end=' ')
    movies_table_2026 = getTNMovieTable(driver, 2026)
    print('SUCESSO!')

    colunas = ['link', 'date', 'genre']

    # Salvando dados:
    print('> Salvando dados da tabela: ', end=' ')
    df = pd.DataFrame(movies_table_2026)
    df.columns = colunas
    df.to_csv('data/raw/tabela.csv', index=False)
    print('SUCESSO!')
    print('-' * 50)

    item_colunas = ['nome', 'tn_legs', 'domestic_share', 'domestic_bo', 'rating', 'tempo', 'producao', 
                    'estreia_bilheteria', 'semana_2', 'semana_3', 'semana_4']
    
    # Coletando dados de cada filme:
    lista_movie_info = []
    
    for i in range(len(df['link'])):
            print(f'Extraindo filme {i+1:03d}/{len(df['link']):03d}: ', end=' ')
            movie_info = getTNMovieInfo(driver, df['link'][i])
            
            if movie_info:
                lista_movie_info.append(movie_info)
                print('SUCESSO!')
            else:
                print('FALHA (Ignorado).')
    
    
    '''
    # Testando com filme especifico:
        movie_info = movie_info = getTNMovieInfo(driver, df['link'][47])
        if movie_info:
            print('deu boa')
            lista_movie_info.append(movie_info)
        else:
            print('nn deu boa')
    '''
    

    print('-' * 50)

    # Salvado dados das infos dos filmes:
    print('> Salvando dados dos filmes: ', end=' ')
    df_info = pd.DataFrame(lista_movie_info, columns=item_colunas)
    df_info.to_csv('data/raw/tabela_info.csv', index=False)
    print('Dados salvos!')

    print('-' * 50)