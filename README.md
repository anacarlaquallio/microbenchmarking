# Microbenchmarking RSA Python

## Informações gerais:

O experimento consiste em uma investigação detalhada da implementação do algoritmo RSA por meio da comparação entre duas bibliotecas da linguagem de programação Python. Essa análise é conduzida por meio de microbenchmarking, avaliando métricas como tempo de execução e o consumo de memória.
No escopo do RSA, foram examinados o desempenho tanto na cifragem quanto na decifragem, utilizando chaves de 2048 e 4096 bits. A implementação foi realizada por meio das bibliotecas de criptografia Cryptography e PyCrypto.
Para avaliar o desempenho por meio de microbenchmarking, foram empregadas as bibliotecas timeit, psutil e memory_profiler. A primeira foi utilizada para a análise do tempo de execução, enquanto as duas últimas foram empregadas para avaliar o consumo de memória durante a execução.
A biblioteca memory_profile permite o monitoramento de memória linha por linha do código, permitindo a visualização da alocação de memória. Já o psutil é uma biblioteca multiplataforma que oferece funcionalidades para consultar informações do Sistema Operacional, como o uso de CPU, memória, discos, rede e outros recursos do sistema.
É executada uma lista de iterações (10, 100, 1000 e 10000) a fim de obter uma medida mais precisa e estável do tempo médio de execução para cada operação (criptografia e descriptografia) em diferentes cenários de tamanho de chave.
