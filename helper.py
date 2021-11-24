from passlib.hash import sha256_crypt


def get_hashed_password(plain_text_password):
    hashed_psw = sha256_crypt.encrypt(plain_text_password)
    return hashed_psw

def check_password(input_password, hashed_password):
    check = sha256_crypt.verify(input_password, hashed_password)
    return check