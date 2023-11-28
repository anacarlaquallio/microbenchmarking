import os
import matplotlib.pyplot as plt
import timeit
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import psutil  # Para medir o uso de memória

def generate_keys(keys):
    rsa_keys = {}
    for key_size in keys:
        key = RSA.generate(key_size)
        rsa_keys[key_size] = key
    return rsa_keys

def benchmark_encrypt(num_executions, keys, rsa_keys):
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

def plot_graphs(times, memory_usage, iterations, keys):
# Plotar gráfico para os tempos de execução
    plt.figure(figsize=(8, 6))
    for i, key in enumerate(keys):
        plt.plot(iterations, [times[i] for times in times], marker='o', label=f'Criptografia {key}-bits')
    plt.xscale('log')
    plt.xlabel('Número de Iterações')
    plt.ylabel('Tempo Médio (segundos)')
    plt.title('Tempos Médios de Criptografia RSA')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Gerar gráfico para o uso de memória
    plt.figure(figsize=(8, 6))
    for i, key in enumerate(keys):
        plt.plot(iterations, [memory[i] for memory in memory_usage], marker='o', label=f'Uso de Memória {key}-bits')
    plt.xscale('log')
    plt.xlabel('Número de Iterações')
    plt.ylabel('Uso de Memória (bytes)')
    plt.title('Uso de Memória durante Criptografia RSA')
    plt.legend()
    plt.grid(True)
    plt.show()
    
if __name__ == "__main__":
    # Valores de num_executions para as diferentes iterações
    iterations = [10, 100, 1000, 10000]
    keys = [2048, 4096]

    # Gerar chaves RSA fora do loop principal
    rsa_keys = generate_keys(keys)

    encrypt_times = []
    encrypt_memory_usage = []

    for num in iterations:
        times, memory = benchmark_encrypt(num, keys, rsa_keys)
        encrypt_times.append(times)
        encrypt_memory_usage.append(memory)

    plot_graphs(encrypt_times, encrypt_memory_usage, iterations, keys)
