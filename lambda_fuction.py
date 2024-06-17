import boto3
import json
import time

def lambda_handler(event, context):
    # Inicializando clientes do S3 e SSM
    s3_client = boto3.client('s3')
    ssm_client = boto3.client('ssm')

    # Nome do bucket S3 de onde queremos copiar o arquivo .txt
    bucket_name = 'trigger-s3-lambda'  # Substitua pelo nome do seu bucket S3

    # Listar objetos no bucket S3
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix='',
    )

    # Filtrar apenas arquivos com extensão .txt e encontrar o mais recente
    txt_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.txt')]
    if txt_files:
        latest_txt_file = max(txt_files, key=lambda x: response['Contents'][txt_files.index(x)]['LastModified'])
        
        # Construir o caminho completo do arquivo no S3
        s3_file_path = f's3://{bucket_name}/{latest_txt_file}'

        # Comando para copiar o arquivo do S3 para /tmp na instância EC2 via SSM
        command = f"aws s3 cp {s3_file_path} /tmp/"

        # Enviar comando via SSM para a instância EC2
        response_ssm = ssm_client.send_command(
            InstanceIds=['id bucket'],  # Substitua pelo ID da sua instância EC2
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': [command]},
        )

        # Capturar Command ID
        command_id = response_ssm['Command']['CommandId']

        # Tentar obter o resultado do comando após um curto intervalo de tempo
        time.sleep(10)  # Esperar 10 segundos para dar tempo de executar o comando
        output = None
        for _ in range(3):  # Tentar até 3 vezes
            output = ssm_client.get_command_invocation(
                CommandId=command_id,
                InstanceId='id bucket'  # Substitua pelo ID da sua instância EC2
            )
            if output['Status'] in ['Pending', 'InProgress']:  # Se o comando ainda estiver em andamento, esperar mais um pouco
                time.sleep(10)
            else:
                break

        if output and output['Status'] == 'Success':
            return {
                'statusCode': 200,
                'body': json.dumps(f'Arquivo {latest_txt_file} copiado com sucesso para /tmp!')
            }
        else:
            return {
                'statusCode': 500,
                'body': 'Falha ao copiar o arquivo.'
            }
    else:
        return {
            'statusCode': 404,
            'body': 'Nenhum arquivo .txt encontrado no bucket.'
        }
