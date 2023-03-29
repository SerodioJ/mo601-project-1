# Simulador Super Básico de Circuitos Lógicos - MO601 1s/2023

## João Alberto Moreira Seródio - 218548

## Instruções para build e execução

Execute na raiz do repostório o comando abaixo para construir a imagem Docker

```
docker build -t mo601-p1-218548 .
```

Para executar as simulações para todos os testes na pasta `test` utilize

```
docker run --rm -v ./test:/simulator/test mo601-p1-218548:latest python3 cli.py -p "/simulator/test/*"
```
