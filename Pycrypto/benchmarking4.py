import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import timeit

def generate_keys(keys):
    rsa_keys = {}
    for key_size in keys:
        private_key = RSA.generate(key_size)
        public_key = private_key.publickey()
        rsa_keys[key_size] = (private_key, public_key)
    return rsa_keys

def do_decrypt(private_key, ciphertext, num_executions):
    for _ in range(num_executions):
        cipher_rsa = PKCS1_OAEP.new(private_key)
        cipher_rsa.decrypt(ciphertext)

def benchmark_decrypt(num_executions, keys, rsa_keys):
    for key_size in keys:
        private_key, public_key = rsa_keys[key_size]
        message = os.urandom(190)
        cipher_rsa = PKCS1_OAEP.new(public_key)
        ciphertext = cipher_rsa.encrypt(message)

        print(f"Para {key_size}-bits:")
        total_time = sum(timeit.timeit(lambda: do_decrypt(private_key, ciphertext, num_executions), number=1) 
                         for _ in range(num_executions))
        execution_time = total_time / num_executions
        print(f"Tempo Médio: {execution_time} segundos")

if __name__ == "__main__":
    iterations = [10, 100, 1000, 10000]
    keys = [2048, 4096]
  
    rsa_keys = generate_keys(keys)
  
    for num in iterations:
        benchmark_decrypt(num, keys, rsa_keys)