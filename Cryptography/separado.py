import os
import matplotlib.pyplot as plt
import timeit
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import psutil

def generate_keys(keys):
    rsa_keys = {}
    for key_size in keys:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        rsa_keys[key_size] = (private_key, public_key)
    return rsa_keys

def benchmark_encrypt(num_executions, key_size, rsa_keys):
    execution_time = 0
    memory_usage = 0  # Variável para armazenar o uso de memória

    private_key, public_key = rsa_keys[key_size]
    message = os.urandom(190)

    for _ in range(num_executions):
        mem_before = psutil.Process(os.getpid()).memory_info().rss  # Memória antes da execução

        start_time = timeit.default_timer()
        ciphertext = public_key.encrypt(message, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
        end_time = timeit.default_timer()

        execution_time += (end_time - start_time)

        mem_after = psutil.Process(os.getpid()).memory_info().rss  # Memória após a execução
        memory_usage += mem_after - mem_before  # Adiciona a diferença ao uso total de memória

    return execution_time / num_executions, memory_usage / num_executions  # Retorna tempo médio e uso médio de memória

def benchmark_decrypt(num_executions, key_size, rsa_keys):
    execution_time = 0
    memory_usage = 0  # Variável para armazenar o uso de memória

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

    for _ in range(num_executions):
        mem_before = psutil.Process(os.getpid()).memory_info().rss  # Memória antes da execução

        start_time = timeit.default_timer()
        plaintext = private_key.decrypt(ciphertext, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
        end_time = timeit.default_timer()

        execution_time += (end_time - start_time)

        mem_after = psutil.Process(os.getpid()).memory_info().rss  # Memória após a execução
        memory_usage += mem_after - mem_before  # Adiciona a diferença ao uso total de memória

    return execution_time / num_executions, memory_usage / num_executions  # Retorna tempo médio e uso médio de memória

# Parâmetros para as iterações e tamanho da chave
num_iterations = 1000
key_size = 4096

# Gerar chaves RSA fora do loop de execução
rsa_keys = generate_keys([key_size])

# Executar o benchmarking e capturar o tempo médio e uso médio de memória
encrypt_time, encrypt_memory = benchmark_encrypt(num_iterations, key_size, rsa_keys)
decrypt_time, decrypt_memory = benchmark_decrypt(num_iterations, key_size, rsa_keys)

# Exibir os resultados
print(f"Tempo médio Encrypt para {num_iterations} iterações com chave de {key_size} bits: {encrypt_time} segundos")
print(f"Uso médio de memória Encrypt: {encrypt_memory} bytes")
print(f"Tempo médio Decrypt para {num_iterations} iterações com chave de {key_size} bits: {decrypt_time} segundos")
print(f"Uso médio de memória Decrypt: {decrypt_memory} bytes")