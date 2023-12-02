import os
import matplotlib.pyplot as plt
import timeit
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Geração das chaves fora do loop
def generate_keys(keys):
    rsa_keys = {}
    for key_size in keys:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        rsa_keys[key_size] = (private_key, public_key)
    return rsa_keys

def benchmark_encrypt(num_executions, keys, rsa_keys):
    execution_times = []
    for key_size in keys:
        private_key, public_key = rsa_keys[key_size]
        message = os.urandom(190)

        total_time = sum(timeit.timeit(lambda: public_key.encrypt(message, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )), number=1) for _ in range(num_executions))

        execution_times.append(total_time / num_executions)

    return execution_times

def benchmark_decrypt(num_executions, keys, rsa_keys):
    execution_times = []
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

        total_time = sum(timeit.timeit(lambda: private_key.decrypt(ciphertext, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )), number=1) for _ in range(num_executions))

        execution_times.append(total_time / num_executions)

    return execution_times

# Valores de num_executions para as diferentes iterações
iterations = [10, 100, 1000, 10000]
keys = [2048, 4096]

# Gerar chaves RSA fora do loop de execução
rsa_keys = generate_keys(keys)

# Listas para armazenar os tempos médios de criptografia e descriptografia
encrypt_times = []
decrypt_times = []

# Executar o benchmarking para cada valor de num_executions
for num in iterations:
    encrypt_times.append(benchmark_encrypt(num, keys, rsa_keys))
    decrypt_times.append(benchmark_decrypt(num, keys, rsa_keys))

# Plotar o gráfico
plt.figure(figsize=(8, 6))
for i, key in enumerate(keys):
    plt.plot(iterations, [times[i] for times in encrypt_times], marker='o', label=f'Cifração {key}-bits')
    plt.plot(iterations, [times[i] for times in decrypt_times], marker='o', label=f'Decifração {key}-bits')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Número de Iterações')
plt.ylabel('Tempo Médio (segundos)')
plt.title('Tempos Médios de Encrypt e Decrypt RSA')
plt.legend()
plt.grid(True)
plt.show()
