import os
import matplotlib.pyplot as plt
import timeit
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def benchmark_encrypt(num_executions, keys):
    execution_times = []
    for key_size in keys:
        execution_time = 0
        for _ in range(num_executions):
            key = RSA.generate(key_size)
            public_key = key.publickey()
            message = os.urandom(190)

            cipher_rsa = PKCS1_OAEP.new(public_key)
            start_time = timeit.default_timer()
            ciphertext = cipher_rsa.encrypt(message)
            end_time = timeit.default_timer()

            execution_time += (end_time - start_time)
        execution_times.append(execution_time / num_executions)
    return execution_times

def benchmark_decrypt(num_executions, keys):
    execution_times = []
    for key_size in keys:
        execution_time = 0
        for _ in range(num_executions):
            key = RSA.generate(key_size)
            private_key = key.export_key().decode("utf-8")
            public_key = key.publickey().export_key().decode("utf-8")
            message = os.urandom(190)
            cipher_rsa = PKCS1_OAEP.new(key)
            ciphertext = cipher_rsa.encrypt(message)

            start_time = timeit.default_timer()
            plaintext = cipher_rsa.decrypt(ciphertext)
            end_time = timeit.default_timer()

            execution_time += (end_time - start_time)
        execution_times.append(execution_time / num_executions)
    return execution_times

# Valores de num_executions para as diferentes iterações
iterations = [10, 100, 1000, 10000]
keys = [2048, 4096]

# Listas para armazenar os tempos médios de criptografia e descriptografia
encrypt_times = []
decrypt_times = []

# Executar o benchmarking para cada valor de num_executions
for num in iterations:
    encrypt_times.append(benchmark_encrypt(num, keys))
    decrypt_times.append(benchmark_decrypt(num, keys))

# Plotar o gráfico
plt.figure(figsize=(8, 6))
for i, key in enumerate(keys):
    plt.plot(iterations, [times[i] for times in encrypt_times], marker='o', label=f'Criptografia {key}-bits')
    plt.plot(iterations, [times[i] for times in decrypt_times], marker='o', label=f'Descriptografia {key}-bits')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Número de Iterações')
plt.ylabel('Tempo Médio (segundos)')
plt.title('Tempos Médios de Criptografia e Descriptografia RSA')
plt.legend()
plt.grid(True)
plt.show()