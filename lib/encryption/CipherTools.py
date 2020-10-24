from chatutils import utils

from lib.encryption import XChaCha20Poly1305
from lib.encryption.fernet import FernetCipher
from lib.encryption.salt import NaclCipher
from lib.encryption.aes256 import AES256Cipher

from nacl.encoding import Base64Encoder, HexEncoder, RawEncoder
from nacl.signing import SigningKey, VerifyKey

import config.filepaths as paths


def gen_nacl_key(path=paths.nacl_keys, *args, **kwargs) -> tuple:
    """Generates public and private keys with nacl algorithm."""
    prvk, pubk = NaclCipher.generate_keys(path)
    sgnk, vfyk = NaclCipher().generate_signing_keys()
    prvk_b64 = prvk.encode(encoder=Base64Encoder)
    pubk_b64 = pubk.encode(encoder=Base64Encoder)
    sgnk_b64 = sgnk.encode(encoder=Base64Encoder)
    vfyk_b64 = vfyk.encode(encoder=Base64Encoder)
    return prvk_b64, pubk_b64, sgnk_b64, vfyk_b64

def make_nacl_pub_box(pub_key, path=paths.nacl_keys, *args, **kwargs):
    """Makes Nacl Public Box with mutual authentication."""
    prv_key = NaclCipher().load_prv_key()
    public_box = NaclCipher().make_public_box(prv_key, pub_key)
    # Put symmetric key in box.
    public_box.encrypt("message")

