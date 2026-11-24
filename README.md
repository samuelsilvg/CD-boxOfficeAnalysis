# boxOfficeAnalysis | Trabalho Final de Ciência dos Dados
Repositório para o trabalho final da disciplina de Ciência dos Dados :: UFCI-MG

## como instalar dependências
instale dependências através do seguinte comando, se necessário:

```
pip install -r requirements.txt
```

## estrutura do repositório:
```
.
├── data
│   ├── processed
│   │   └── tabela_tratada.csv
│   └── raw
│       ├── tabela_dados_completos.csv
│       └── tabela_links.csv
├── LICENSE
├── notebooks
│   ├── analise_dataset.ipynb
│   ├── analise_P1.ipynb
│   ├── analise_P2.ipynb
│   ├── analise_P3.ipynb
│   └── analise_P4.ipynb
├── README.md
└── src
    ├── data_scraping.py
    └── parsing.py
```
___
- `data/` armazena os arquivos .csv de coleta em `raw/` e a base de dados tratada em `processed/`;
- `notebooks/` possui arquivos .ipynb para análise exploratória dos dados coletados e tratados;
- `src/` possui os scripts Python utilizados no projeto: `data_scraping.py` realiza a raspagem de dados do site _The Numbers_, e `parsing.py` realiza o pré-processamento e tratamento da base de dados coletada

## pipleine de reprodução do trabalho:
- para reproduzir os mesmos resultados do trabalho, apenas execute os scripts da pasta `notebooks/`, ou execute `parsing.py` para os dados que já estão no `data/raw/` deste repositório.

## pipeline de execução recomendado para novas coletas:
Para refazer as coletas e tratar os dados, execute os seguintes comandos:
```
python -m src/data_parsing.py
python -m src/parsing.py
```

Para analisar os resultados, execute os .ipynb da pasta `notebooks/` na ordem em que preferir.

