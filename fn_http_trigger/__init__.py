import json
import logging
import azure.functions as func
import psycopg2

host = "srvpostgresql-datainaction.postgres.database.azure.com"
dbname = "cepbrasil"
user = "adminpostgresql"
password = "xxxxxx"
sslmode = "require"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning("Http disparado")

    param_value = req.params.get('cep')

    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    logging.warning("Connection established")

    if param_value is not None:
        cursor.execute(f"select to_jsonb(t) from (select \
        a.name as Cidade, b.name as Estado,b.initials as Sigla, postal_code as CEP, address as Endereco, e.name as Bairro \
        from cities a \
        inner join states b on a.state_id = b.id \
        left join address_searchs d on a.id = d.city_id \
        left join districts e on d.district_id = e.id \
        where postal_code = '{param_value}') t;")

        rows = cursor.fetchall()

        if len(rows) > 0:
            for row in rows:
                contentJson = json.dumps(row, ensure_ascii=False, indent=4)
                logging.warning(contentJson)
                #logging.warning(">>>> Cidade: %s, Estado: %s, Sigla: %s, CEP: %s, Endereco: %s, Barrio: %s" %(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]) , str(row[5])))
                return func.HttpResponse(
                  contentJson
                 ,status_code=200
                )
        else:
            return func.HttpResponse(
                 f"##### CEP NÃO encontrado #####",
                 status_code=204
                 ) 
    else:
        return func.HttpResponse(
                 f"##### Nenhum CEP informado #####",
                 status_code=404
        )
