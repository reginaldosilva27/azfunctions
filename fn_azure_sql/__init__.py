import json
import logging
import azure.functions as func
import requests
from azure.functions.decorators.core import DataType

def main(changes, retornoCEP: func.Out[func.SqlRow]):
    # Usando o binfing de input chamado 'changes' para encapusular as mudanças recebidas do SQL Server
    rows = json.loads(changes)
    logging.warning("SQL Changes: %s", rows)

    #Extraindo os dados de dentro do JSON
    cep = rows[0]["Item"]["cep"]
    cpf = rows[0]["Item"]["cpf"]

    logging.warning("cep: %s",cep)
    logging.warning("cpf: %s",cpf)

    # chamando a API de CEP para buscar as informações
    url = f"https://demofunctionappstorage.azurewebsites.net/api/fn_http_trigger?cep={str(cep)}"
    response = requests.get(
        url = url
    )

    logging.warning("Status Code:  %s", str(response.status_code))
    logging.warning(str(json.dumps(json.loads(response.content),indent=4)))

    # formarando nossos dados com o retorno da API pra gravar no SQL Server
    newCEP = {
        "cpf": cpf,
        "cep": json.loads(response.content)[0]["cep"],
        "sigla": json.loads(response.content)[0]["sigla"],
        "bairro": json.loads(response.content)[0]["bairro"],
        "estado": json.loads(response.content)[0]["cidade"],
        "cidade": json.loads(response.content)[0]["estado"],
        "endereco": json.loads(response.content)[0]["endereco"]
    }
    # Usando o binding de output para gravar no SQL Server as informações
    row = func.SqlRow(newCEP)
    retornoCEP.set(row)
    logging.warning("GRAVADO COM SUCESSO")
