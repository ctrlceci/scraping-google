import requests
from bs4 import BeautifulSoup
import pandas as pd

import re
import time
import json

# pip install requests beautifulsoup4 pandas openpyxl

re_tel_cel = '\(\d{2}\)\s?(9?\d{4}|\d{4})-\d{4}'

planilha_xlsx = pd.read_excel('./empresas.xlsx')

empresas = planilha_xlsx['Empresa'].tolist()

novos_dados = pd.DataFrame(columns=['Empresa', 'Telefone'])

for index, empresa in enumerate(empresas):
    print(f'Buscando empresa {empresa}...')
    
    response = requests.get(f'https://www.google.com/search?q={empresa}')

    if response.status_code != 200:
        with open(f'./info/empresa_{index}.json', 'w') as file:
            dados = { "empresa": empresa, "status_code": response.status_code, "headers": response.headers.__dict__}
            json.dump(dados, file, default=str)
        break

    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.find('div', class_='Gx5Zad xpd EtOod pkphOe')

    if not main_content:
        novos_dados.loc[index] = [empresa, '']
        continue

    telefone_content = main_content.find('div', class_='AVsepf u2x1Od')
    if not telefone_content:
        novos_dados.loc[index] = [empresa, '']
        continue

    telefone_content = telefone_content.text

    celular = re.search(re_tel_cel, telefone_content)
    if not celular:
        novos_dados.loc[index] = [empresa, '']
        continue

    novos_dados.loc[index] = [empresa, celular.group()]
    print(f'{empresa}: {celular.group()}')

    time.sleep(1)

novos_dados.to_excel('./empresas_com_telefone.xlsx', index=False)