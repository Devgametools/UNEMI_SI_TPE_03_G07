import os, time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature, InvalidTag

msg = b"Transferencia: $1500 a la cuenta 001-UNEMI"
print("== 1. Cifrado simetrico AES-256-GCM ==")
k = AESGCM.generate_key(bit_length=256); nonce = os.urandom(12)
ct = AESGCM(k).encrypt(nonce, msg, None)
print("Texto claro :", msg.decode())
print("Texto cifrado (hex):", ct.hex()[:64] + "...")
print("Descifrado  :", AESGCM(k).decrypt(nonce, ct, None).decode())
mod = bytearray(ct); mod[0] ^= 1
try: AESGCM(k).decrypt(nonce, bytes(mod), None)
except InvalidTag: print("Alteracion de 1 bit detectada -> InvalidTag (integridad)")

print("\n== 2. Firma digital RSA-2048 + SHA-256 (PSS) ==")
priv = rsa.generate_private_key(public_exponent=65537, key_size=2048); pub = priv.public_key()
pss = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)
sig = priv.sign(msg, pss, hashes.SHA256())
print("Firma (", len(sig), "bytes):", sig.hex()[:48] + "...")
pub.verify(sig, msg, pss, hashes.SHA256()); print("Verificacion con mensaje original: VALIDA")
try: pub.verify(sig, msg.replace(b"1500", b"9500"), pss, hashes.SHA256())
except InvalidSignature: print("Verificacion con mensaje alterado: INVALIDA")

print("\n== 3. Cifrado hibrido (RSA-OAEP protege la clave AES) ==")
oaep = padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
ks = AESGCM.generate_key(bit_length=256)
kw = pub.encrypt(ks, oaep)
datos = os.urandom(10*1024*1024)
n2 = os.urandom(12); c2 = AESGCM(ks).encrypt(n2, datos, None)
ks2 = priv.decrypt(kw, oaep)
ok = AESGCM(ks2).decrypt(n2, c2, None) == datos
print("Clave de sesion envuelta con RSA:", len(kw), "bytes; 10 MiB cifrados con AES; recuperacion correcta:", ok)

print("\n== 4. Rendimiento comparativo (promedios en este equipo) ==")
N=200; blk=os.urandom(190)
t=time.perf_counter()
for _ in range(N): pub.encrypt(blk, oaep)
t_rsa_e=(time.perf_counter()-t)/N
t=time.perf_counter()
for _ in range(N): priv.decrypt(pub.encrypt(blk,oaep), oaep)
t_rsa_d=(time.perf_counter()-t)/N - t_rsa_e
mb = os.urandom(50*1024*1024)
t=time.perf_counter(); AESGCM(ks).encrypt(n2, mb, None); t_aes=time.perf_counter()-t
t=time.perf_counter(); ChaCha20Poly1305(ChaCha20Poly1305.generate_key()).encrypt(n2, mb, None); t_cha=time.perf_counter()-t
print(f"RSA-2048 OAEP cifrado de 190 bytes  : {t_rsa_e*1e3:.3f} ms/op")
print(f"RSA-2048 OAEP descifrado de 190 bytes: {t_rsa_d*1e3:.3f} ms/op")
print(f"AES-256-GCM sobre 50 MiB           : {50/t_aes:.0f} MiB/s")
print(f"ChaCha20-Poly1305 sobre 50 MiB     : {50/t_cha:.0f} MiB/s")
rsa_mbps = 190/(t_rsa_d)/1048576
print(f"Throughput equivalente RSA (descifrado): {rsa_mbps:.3f} MiB/s")

print("\n== 5. Firma ECDSA P-256 vs RSA-2048 ==")
ek = ec.generate_private_key(ec.SECP256R1())
es = ek.sign(msg, ec.ECDSA(hashes.SHA256()))
print("Tamano clave publica: RSA 2048 bits vs ECC 256 bits; firma ECDSA:", len(es), "bytes")
