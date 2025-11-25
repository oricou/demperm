"""
Encryption service for E2E encrypted messaging.
Uses AES-256 for content encryption and RSA-2048 for key encryption.
"""
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import os


class EncryptionService:
    """Service for E2E message encryption."""
    
    @staticmethod
    def generate_rsa_keypair():
        """
        Generate RSA-2048 key pair for a user.
        
        Returns:
            Tuple of (private_key_pem, public_key_pem)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem.decode('utf-8'), public_pem.decode('utf-8')
    
    @staticmethod
    def encrypt_message(content: str, sender_public_key: str, receiver_public_key: str) -> dict:
        """
        Encrypt a message with E2E encryption.
        
        Args:
            content: Message content to encrypt
            sender_public_key: Sender's RSA public key (PEM format)
            receiver_public_key: Receiver's RSA public key (PEM format)
            
        Returns:
            Dictionary with encrypted_content, encryption_key_sender, encryption_key_receiver
        """
        # Generate random AES-256 key
        aes_key = os.urandom(32)  # 256 bits
        iv = os.urandom(16)  # 128 bits
        
        # Encrypt content with AES-256
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad content to AES block size (16 bytes)
        content_bytes = content.encode('utf-8')
        padding_length = 16 - (len(content_bytes) % 16)
        padded_content = content_bytes + bytes([padding_length] * padding_length)
        
        encrypted_content = encryptor.update(padded_content) + encryptor.finalize()
        
        # Combine IV and encrypted content
        encrypted_data = iv + encrypted_content
        encrypted_content_b64 = base64.b64encode(encrypted_data).decode('utf-8')
        
        # Encrypt AES key with sender's public key
        sender_pub_key = serialization.load_pem_public_key(
            sender_public_key.encode('utf-8'),
            backend=default_backend()
        )
        encrypted_key_sender = sender_pub_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Encrypt AES key with receiver's public key
        receiver_pub_key = serialization.load_pem_public_key(
            receiver_public_key.encode('utf-8'),
            backend=default_backend()
        )
        encrypted_key_receiver = receiver_pub_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return {
            'encrypted_content': encrypted_content_b64,
            'encryption_key_sender': base64.b64encode(encrypted_key_sender).decode('utf-8'),
            'encryption_key_receiver': base64.b64encode(encrypted_key_receiver).decode('utf-8'),
        }
    
    @staticmethod
    def decrypt_message(encrypted_content: str, encrypted_key: str, private_key: str) -> str:
        """
        Decrypt a message.
        
        Args:
            encrypted_content: Base64-encoded encrypted content
            encrypted_key: Base64-encoded encrypted AES key
            private_key: User's RSA private key (PEM format)
            
        Returns:
            Decrypted message content
        """
        # Load private key
        priv_key = serialization.load_pem_private_key(
            private_key.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        
        # Decrypt AES key
        encrypted_key_bytes = base64.b64decode(encrypted_key)
        aes_key = priv_key.decrypt(
            encrypted_key_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt content
        encrypted_data = base64.b64decode(encrypted_content)
        iv = encrypted_data[:16]
        encrypted_content_bytes = encrypted_data[16:]
        
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        padded_content = decryptor.update(encrypted_content_bytes) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_content[-1]
        content = padded_content[:-padding_length]
        
        return content.decode('utf-8')

