# Microbenchmarking RSA Python - METEP

### Informações gerais:

O experimento consiste em uma investigação detalhada da implementação do algoritmo RSA por meio da comparação entre duas bibliotecas da linguagem de programação Python. Essa análise é conduzida por meio de microbenchmarking, avaliando métricas como tempo de execução e o consumo de memória.
No escopo do RSA, foram examinados o desempenho tanto na cifragem quanto na decifragem, utilizando chaves de 2048 e 4096 bits. A implementação foi realizada por meio das bibliotecas de criptografia Cryptography e PyCrypto.
Para avaliar o desempenho por meio de microbenchmarking, foram empregadas as bibliotecas timeit, psutil e memory_profiler. A primeira foi utilizada para a análise do tempo de execução, enquanto as duas últimas foram empregadas para avaliar o consumo de memória durante a execução.
A biblioteca memory_profile permite o monitoramento de memória linha por linha do código, permitindo a visualização da alocação de memória. Já o psutil é uma biblioteca multiplataforma que oferece funcionalidades para consultar informações do Sistema Operacional, como o uso de CPU, memória, discos, rede e outros recursos do sistema.
É executada uma lista de iterações (10, 100, 1000 e 10000) a fim de obter uma medida mais precisa e estável do tempo médio de execução para cada operação (criptografia e descriptografia) em diferentes cenários de tamanho de chave.

### Detalhes sobre a estrutura do repositório:

No repositório, há duas pastas: uma para biblioteca Cryptography e outra para a PyCrypto. As duas consistem de um arquivo que contém a implementação disponibilizada na documentação e mais 4 arquivos de código de microbenchmarking, que são:

* Microbenchmarking 1: gera um gráfico que exibe os tempos médios de criptografia e descriptografia em relação ao número de iterações, para chaves de 2048 e 4096 bits. As chaves são geradas dentro do loop a cada iteração, o que torna-se muito lento.
* Microbenchmarking 2: essa análise é semelhante à anterior, mas as chaves são geradas fora do loop e reutilizadas durante as iterações, o que faz o tempo de execução diminuir significativamente.
* Microbenchmarking 3: o código gera chaves RSA de diferentes tamanhos e executa operações de criptografia, medindo o tempo médio de execução e o uso de memória para cada iteração.
* Microbenchmarking 4: o código gera chaves RSA de diferentes tamanhos e executa operações de decifração, medindo o tempo médio de execução e o uso de memória para cada iteração,.

Note que cada um desses códigos oferece uma perspectiva diferente e, em conjunto, podem ajudar a compreender aspectos do desempenho do RSA em Python, como tempo de execução, consumo de memória e variações desses fatores com diferentes tamanhos de chave e iterações.
