import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from memory_profiler import profile

def generate_keys(keys):
    rsa_keys = {}
    for key_size in keys:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        rsa_keys[key_size] = (private_key, public_key)
    return rsa_keys

@profile
def do_decrypt(private_key, ciphertext, num_executions):
    for _ in range(num_executions):
        private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

@profile
def benchmark_decrypt(num_executions, keys, rsa_keys):
    for key_size in keys:
        private_key, public_key = rsa_keys[key_size]
        message = os.urandom(190)
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        print(f"Para {key_size}-bits:")
        do_decrypt(private_key, ciphertext, num_executions)

if __name__ == "__main__":
    iterations = [10, 100, 1000, 10000]
    keys = [2048, 4096]

    rsa_keys = generate_keys(keys)

    for num in iterations:
        benchmark_decrypt(num, keys, rsa_keys)
