from cryptography.fernet import Fernet, InvalidToken

# 메시지 복호화
def decrypt_message(encrypted_message, key):
    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message
    except InvalidToken as e:
        print("에러 발생: 복호화 실패 - 잘못된 키 또는 데이터입니다.")
        return None

# 암호화된 데이터를 파일로부터 읽어옴
with open("encrypted_data.bin", "rb") as f:
    encrypted_data = f.read()

# 랜덤 키를 파일로부터 읽어옴
with open("encryption_key.key", "rb") as key_file:
    key = key_file.read()

# 메시지 복호화 시도
decrypted_message = decrypt_message(encrypted_data, key)

if decrypted_message is not None:
    print("복호화된 메시지:", decrypted_message)
else:
    print("복호화 실패. 에러가 발생했습니다.")
