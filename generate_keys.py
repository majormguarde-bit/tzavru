
import base64
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

def generate_vapid_keys():
    # Generate an EC private key using the SECP256R1 curve
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    
    # Get the public key from the private key
    public_key = private_key.public_key()
    
    # Extract the private bytes (uncompressed, for pywebpush)
    # VAPID private keys are just the 32-byte private scalar
    private_bytes = private_key.private_numbers().private_value.to_bytes(32, 'big')
    private_key_b64 = base64.urlsafe_b64encode(private_bytes).decode('utf-8').strip('=')
    
    # Extract the public bytes in X9.62 uncompressed format
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    public_key_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').strip('=')

    print("\n--- СГЕНЕРИРОВАННЫЕ КЛЮЧИ VAPID ---")
    print(f"VAPID_PUBLIC_KEY={public_key_b64}")
    print(f"VAPID_PRIVATE_KEY={private_key_b64}")
    print("----------------------------------\n")
    print("Добавьте эти строки в ваш файл .env на хостинге.")
    print("Или в конфигурацию приложения.")

if __name__ == "__main__":
    generate_vapid_keys()
