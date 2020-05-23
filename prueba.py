import boto3

client = boto3.client(
    's3',
    aws_access_key_id='ASIA5IDOZ467MW3SOINK',
    aws_secret_access_key='vvDH6oNWKYjnuq3q44gRUsuKFhT1odwQSWJ7MlzF'
)

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

x = input('presione cualquier tecla para continuar')