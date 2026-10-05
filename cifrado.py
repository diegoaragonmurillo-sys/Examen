import boto3, base64
from cryptography.fernet import Fernet

kms = boto3.client('kms', region_name='us-east-1')
KEY_ID = 'alias/tu-llave-kms' # Reemplaza por tu Key ID o Alias de KMS

def cifrar(msj):
    # 1. Obtener Data Key de KMS y preparar llave plana
    res = kms.generate_data_key(KeyId=KEY_ID, KeySpec='AES_256')
    key_plana = base64.urlsafe_b64encode(res['Plaintext'])
    
    # 2. Cifrar mensaje y armar el sobre digital
    msj_cifrado = Fernet(key_plana).encrypt(msj.encode()).decode()
    sobre = {
        'msj': msj_cifrado,
        'key_cifrada': base64.b64encode(res['CiphertextBlob']).decode()
    }
    
    # 3. Destruir la llave plana
    del key_plana, res
    return sobre

def descifrar(sobre):
    # 1. Pedir a KMS descifrar la llave guardada en el sobre
    blob = base64.b64decode(sobre['key_cifrada'])
    key_plana = base64.urlsafe_b64encode(kms.decrypt(CiphertextBlob=blob)['Plaintext'])
    
    # 2. Descifrar el mensaje
    msj = Fernet(key_plana).decrypt(sobre['msj'].encode()).decode()
    return msj, key_plana.decode()

# --- PRUEBA ---
sobre = cifrar("Mensaje Secreto")
print("Sobre Digital:", sobre)

msj_revelado, key_revelada = descifrar(sobre)
print("Mensaje descifrado:", msj_revelado)
print("Llave plana usada:", key_revelada)
