import timeit
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import psutil  # Para medir o uso de memória
from memory_profiler import profile

@profile
def benchmark_encrypt(num_executions, keys):
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

        # Medir o uso de memória após a execução
        mem_after = psutil.Process(os.getpid()).memory_info().rss
        memory_usage = mem_after - mem_before

        print(f"Para {key_size}-bits:")
        print(f"Tempo Médio de Execução: {total_time / num_executions} segundos")
        print(f"Uso de Memória: {memory_usage} bytes\n")

if __name__ == "__main__":
    iterations = [10, 100, 1000, 10000]
    keys = [2048, 4096]

    for num in iterations:
        benchmark_encrypt(num, keys)
