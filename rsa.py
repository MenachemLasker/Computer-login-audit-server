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


def load_key(key_path):
    with open(key_path, "rb") as f:
        key_bytes = f.read()

    # פירוק המפתח הציבורי
    key = serialization.load_key(
        key_bytes,
        backend=default_backend()
    )

    return key
def decrypt_message(encrypted_text, private_key):
    # פירוק המפתח הפרטי
    private_key = serialization.load_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )

    # יצירת פונקציית פענוח
    decryptor = private_key.decryptor()

    # פענוח הטקסט המוצפן
    try:
        decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
    except Exception as e:
        print(f"שגיאה בפענוח הטקסט: {e}")
        return None

    # החזרת הטקסט המפוענח
    return decrypted_text.decode('utf-8')

# פונקציה לפענוח נתונים מוצפנים


def send_public_key(socket, public_key):
    # המרת המפתח הציבורי ל-bytes
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # שליחת אורך הנתונים
    socket.sendall(len(public_key_bytes).to_bytes(4, 'big'))
    # שליחת המפתח הציבורי
    socket.sendall(public_key_bytes)
