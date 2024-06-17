# trigger_lambda
Repositorio para ajudar quem precisa aprender a fazer um gatilho com S3 na lambda AWS

O repositorio é para auxiliar em sua criação de gatilho s3 para lambda, o nivel de conhecimento com AWS é iniciante e com algumas leituras vai ser fácil de fazer um teste.

Primeiro de permissão IAM para seu EC2 a politica ja existe é somente atrelar a sua instancia, caso não tenha a role criada vai ser necessario criar uma role com a policy ssm, eu utilizei a AmazonSSMFullAccess. Garanta tambem que a role do EC2 tenha permissão no s3 que vai fazer a copia do arquivo, eu deixei no arquivo lieracao_s3.json um exemplo que eu usei, mas pode tambem utilizar o AmazonS3FullAccess ( não recomendado)

![roleIAM](img/roleIMA.png)
