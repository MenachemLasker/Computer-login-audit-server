from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def create_keys():
    # יצירת זוג מפתחות RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # ייצוא המפתח הפרטי
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # ייצוא המפתח הפומבי
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


# פונקציה לפענוח נתונים מוצפנים
def decrypt(encrypted_data):
    # פענוח הנתונים באמצעות המפתח הפרטי והגדרות ה-padding
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    original_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_data

# נניח ש-encrypted_data הוא המידע המוצפן שקיבלנו
# decrypted_data = decrypt(encrypted_data)
# print(decrypted_data)
import socket
from cryptography.hazmat.primitives import serialization

def send_public_key(socket, public_key_path):
    # טעינת המפתח הציבורי מקובץ
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=None
        )

    # ייצוא המפתח הציבורי לבייטים
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # שליחת המפתח הציבורי דרך הסוקט
    socket.sendall(public_key_bytes)

# דוגמה לשימוש בפונקציה:
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('hostname', port))
# send_public_key(s, 'public_key.pem')