import matplotlib.pyplot as plt
import timeit
import os
import psutil
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def benchmark_encrypt(num_executions, keys):
    memory_usage = []
    execution_times = []

    for key_size in keys:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
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

def plot_execution_times(times, iterations, keys):
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

def plot_memory_usage(memory_usage, iterations, keys):
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
    iterations = [10, 100, 1000, 10000]
    keys = [2048, 4096]

    # Listas para armazenar os tempos médios de criptografia e uso de memória
    encrypt_times = []
    encrypt_memory_usage = []

    # Executar o benchmarking para cada valor de num_executions
    for num in iterations:
        times, memory = benchmark_encrypt(num, keys)
        encrypt_times.append(times)
        encrypt_memory_usage.append(memory)

    # Plotar os gráficos separadamente para tempos de execução e uso de memória
    plot_execution_times(encrypt_times, iterations, keys)
    plot_memory_usage(encrypt_memory_usage, iterations, keys)
