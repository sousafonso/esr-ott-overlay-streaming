# ESR OTT Overlay Streaming

Projeto desenvolvido para o curso Engenharia de Serviços em Rede (Universidade do Minho). Este trabalho prático implementa um serviço Over-the-Top (OTT) para entrega de multimédia via redes overlay aplicacionais, usando Python e o emulador CORE.

## Descrição

O sistema cria uma rede lógica (overlay) sobre a infraestrutura IP física (underlay), permitindo streaming eficiente e escalável de vídeo. O serviço suporta replicação seletiva, roteamento baseado em métricas e diferentes cenários de teste.

## Funcionalidades

- Conexões TCP/UDP entre nós overlay com manutenção dinâmica de vizinhos
- Flooding controlado e tabelas de roteamento para fluxo multicast
- Transmissão de vídeo em formato MJPEG com buffering para qualidade
- Testes em topologias variadas simuladas no CORE Network Emulator
- Logs detalhados para diagnóstico e avaliação de métricas de rede

## Estrutura do Projeto

- `/src`: Código fonte dividido em módulos (overlay, routing, streaming, protocolo)
- `/tests`: Scripts de teste unitários e integração
- `/topologies`: Definição de cenários de rede no CORE
- `/docs`: Relatório e documentação técnica em formato LNCS

## Tecnologias

- Python 3.9+
- CORE Network Emulator (Ubuntu)
- Protocolos TCP e UDP
- JSON para mensagens estruturadas

## Como Usar

1. Instalar o emulador CORE no Ubuntu/Debian
2. Configurar topologia de rede com os scripts fornecidos
3. Executar nós overlay com `python src/overlay/node.py`
4. Monitorar logs e métricas para avaliação

## Team

- Afonso Sousa
- Gabriel Ribeiro
- Sofia Baixo


## Licença

[Indicar licença, ex: MIT License]
