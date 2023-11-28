import os
import matplotlib.pyplot as plt
import timeit
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import psutil 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_keys_cryptography(keys):
    rsa_keys = {}
    for key_size in keys:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        rsa_keys[key_size] = (private_key, public_key)
    return rsa_keys

def generate_keys_pycrypto(keys):
    rsa_keys = {}
    for key_size in keys:
        rsa_keys[key_size] = RSA.generate(key_size)
    return rsa_keys

def benchmark_encrypt_pycrypto(num_executions, keys, rsa_keys):
    memory_usage = []
    execution_times = []

    for key_size in keys:
        key = rsa_keys[key_size]
        public_key = key.publickey()
        cipher_rsa = PKCS1_OAEP.new(public_key)
        message = os.urandom(190)

        # Medir o uso de memória antes da execução
        mem_before = psutil.Process(os.getpid()).memory_info().rss

        total_time = sum(timeit.timeit(lambda: cipher_rsa.encrypt(message), number=1) for _ in range(num_executions))

        execution_times.append(total_time / num_executions)

        # Medir o uso de memória após a execução
        mem_after = psutil.Process(os.getpid()).memory_info().rss
        memory_usage.append(mem_after - mem_before)

        # Exibir o uso de memória após cada execução
        print(f"Uso de memória após a execução para {key_size}-bits: {mem_after - mem_before} bytes")

    return execution_times, memory_usage

def benchmark_encrypt_cryptography(num_executions, keys, rsa_keys):
    memory_usage = []
    execution_times = []
    for key_size in keys:
        private_key, public_key = rsa_keys[key_size]
        message = os.urandom(190)

        # Medir o uso de memória antes da execução
        mem_before = psutil.Process(os.getpid()).memory_info().rss

        total_time = sum(timeit.timeit(lambda: public_key.encrypt(message, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )), number=1) for _ in range(num_executions))

        execution_times.append(total_time / num_executions)

        # Medir o uso de memória após a execução
        mem_after = psutil.Process(os.getpid()).memory_info().rss
        memory_usage.append(mem_after - mem_before)

    return execution_times, memory_usage

# Valores de num_executions para as diferentes iterações
iterations = [10, 100, 1000, 10000]
keys = [2048, 4096]

# Gerar chaves RSA para as duas implementações
rsa_keys_cryptography = generate_keys_cryptography(keys)
rsa_keys_pycrypto = generate_keys_pycrypto(keys)

# Listas para armazenar os tempos médios de criptografia e o uso de memória
encrypt_times_cryptography = []
encrypt_times_pycrypto = []
memory_usage_cryptography = []
memory_usage_pycrypto = []

# Executar o benchmarking para cada valor de num_executions
for num in iterations:
    times_cryptography, memory_cryptography = benchmark_encrypt_cryptography(num, keys, rsa_keys_cryptography)
    times_pycrypto, memory_pycrypto = benchmark_encrypt_pycrypto(num, keys, rsa_keys_pycrypto)
    
    encrypt_times_cryptography.append(times_cryptography)
    encrypt_times_pycrypto.append(times_pycrypto)
    memory_usage_cryptography.append(memory_cryptography)
    memory_usage_pycrypto.append(memory_pycrypto)

# Plotar os gráficos comparativos de tempo de execução
plt.figure(figsize=(8, 6))
for i, key in enumerate(keys):
    plt.plot(iterations, [times[i] for times in encrypt_times_cryptography], marker='o', label=f'Cryptography {key}-bits')
    plt.plot(iterations, [times[i] for times in encrypt_times_pycrypto], marker='o', label=f'Pycrypto {key}-bits')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Número de Iterações')
plt.ylabel('Tempo Médio (segundos)')
plt.title('Comparação de Tempos Médios de Criptografia RSA (Cryptography vs Pycrypto)')
plt.legend()
plt.grid(True)
plt.show()

# Plotar os gráficos comparativos de uso de memória
plt.figure(figsize=(8, 6))
for i, key in enumerate(keys):
    plt.plot(iterations, [mem[i] for mem in memory_usage_cryptography], marker='o', label=f'Cryptography {key}-bits')
    plt.plot(iterations, [mem[i] for mem in memory_usage_pycrypto], marker='o', label=f'Pycrypto {key}-bits')
plt.xscale('log')
plt.xlabel('Número de Iterações')
plt.ylabel('Uso de Memória (MiB)')
plt.title('Comparação de Uso de Memória durante Criptografia RSA (Cryptography vs Pycrypto)')
plt.legend()
plt.grid(True)
plt.show()

