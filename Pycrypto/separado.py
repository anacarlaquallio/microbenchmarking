import os
import timeit
import psutil
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_key(key_size):
    key = RSA.generate(key_size)
    return key

def benchmark_encrypt(num_executions, key_size):
    execution_time = 0
    memory_usage = 0

    key = generate_key(key_size)
    public_key = key.publickey()
    message = os.urandom(190)

    for _ in range(num_executions):
        mem_before = psutil.Process(os.getpid()).memory_info().rss

        cipher_rsa = PKCS1_OAEP.new(public_key)
        start_time = timeit.default_timer()
        ciphertext = cipher_rsa.encrypt(message)
        end_time = timeit.default_timer()

        execution_time += (end_time - start_time)

        mem_after = psutil.Process(os.getpid()).memory_info().rss
        memory_usage += mem_after - mem_before

    return execution_time / num_executions, memory_usage / num_executions

def benchmark_decrypt(num_executions, key_size):
    execution_time = 0
    memory_usage = 0

    key = generate_key(key_size)
    private_key = key.export_key().decode("utf-8")
    public_key = key.publickey().export_key().decode("utf-8")
    message = os.urandom(190)
    cipher_rsa = PKCS1_OAEP.new(key)
    ciphertext = cipher_rsa.encrypt(message)

    for _ in range(num_executions):
        mem_before = psutil.Process(os.getpid()).memory_info().rss

        start_time = timeit.default_timer()
        plaintext = cipher_rsa.decrypt(ciphertext)
        end_time = timeit.default_timer()

        execution_time += (end_time - start_time)

        mem_after = psutil.Process(os.getpid()).memory_info().rss
        memory_usage += mem_after - mem_before

    return execution_time / num_executions, memory_usage / num_executions

# Parâmetros para as iterações e tamanho da chave
num_iterations = 10000
key_size = 4096

# Executar o benchmarking para criptografia e descriptografia
encrypt_time, encrypt_memory = benchmark_encrypt(num_iterations, key_size)
decrypt_time, decrypt_memory = benchmark_decrypt(num_iterations, key_size)

# Exibir os resultados
print(f"Tempo médio Encrypt para {num_iterations} iterações com chave de {key_size} bits: {encrypt_time} segundos")
print(f"Uso médio de memória Encrypt: {encrypt_memory} bytes")
print(f"Tempo médio Decrypt para {num_iterations} iterações com chave de {key_size} bits: {decrypt_time} segundos")
print(f"Uso médio de memória Decrypt: {decrypt_memory} bytes")
