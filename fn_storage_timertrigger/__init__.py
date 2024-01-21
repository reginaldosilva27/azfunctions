import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = func.FunctionApp()

def main(myTimer: func.TimerRequest) -> None:
    logging.warning(f">>>>> >>>>> <<<<< <<<<<")
    logging.warning('>>>>> Baixando Blob.')
    blob = BlobClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=saflatdatalake;AccountKey=qHGDsICR1cyxB6Yf/+/EMkc12Tpm5eUM3qQWq/nwfV0lhzk9LDrD/0uxMo396B4S+Swm0WhBj4D/+ASt5lPVvw==;EndpointSuffix=core.windows.net','datalake','azurefunction/hello.txt')

    data = blob.download_blob()
    result = str(data.readall())
    count = int(result.split(',')[1].replace("'",""))
    logging.warning(f">>>>> Dados baixados: {result}")
    logging.warning(f">>>>> Count: {count}")

    logging.warning('>>>>> Atualizando Blob.')
    count = count+1
    data = f"helloworld,{count}"
    blob.upload_blob(data=data,overwrite=True)
    logging.info('>>>>> Blob Atualizado.')
