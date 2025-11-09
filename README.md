# Projeto Integrado: CallSystem + TaskManager

Este repositório reúne dois sistemas desenvolvidos como prática da disciplina de Computação Distribuída: **CallSystem** e **TaskManager**. Ambos foram projetados para funcionar de forma independente, mas integrados por meio de um mecanismo de comunicação assíncrona utilizando Redis Pub/Sub.

---

# CallSystem

O CallSystem é um sistema simples para gerenciamento de chamadas (ou tarefas relacionadas a um call center). Ele permite o registro, acompanhamento e encerramento de chamadas. Cada ação realizada no sistema gera um evento que é publicado em um canal específico do Redis, permitindo que outros sistemas ou serviços possam reagir a essas mudanças em tempo real.

---

# TaskManager

O TaskManager é um sistema de gerenciamento de tarefas que suporta a criação de subtarefas. Ele permite organizar atividades em estruturas hierárquicas, facilitando o controle de processos mais complexos. Assim como o CallSystem, o TaskManager publica eventos no Redis sempre que uma tarefa é criada, concluída ou removida.

---

# Integração via Redis Pub/Sub

A integração entre os dois sistemas é feita por meio do padrão Publish/Subscribe do Redis. Cada sistema publica eventos em canais distintos, e um **consumer unificado** é responsável por escutar esses canais simultaneamente. Esse consumer centraliza o processamento dos eventos, registrando logs e permitindo a expansão para funcionalidades como dashboards, notificações ou análises em tempo real.

---

# Estrutura do Projeto

O repositório está organizado em dois diretórios principais, um para cada sistema, além de um script de consumo centralizado. Cada sistema possui sua própria aplicação Django, com modelos, views e templates independentes, mas conectados logicamente por meio do Redis.

---

# Objetivos do Projeto

- Demonstrar a comunicação assíncrona entre sistemas distribuídos.
- Aplicar o padrão Pub/Sub em um cenário prático.
- Integrar dois sistemas distintos com um consumidor centralizado.
- Explorar conceitos de escalabilidade, desacoplamento e interoperabilidade.

---

# Considerações Finais

Este projeto serve como base para estudos sobre integração de sistemas distribuídos e pode ser expandido com novas funcionalidades, como autenticação, dashboards em tempo real, relatórios analíticos e integração com outros serviços. A arquitetura adotada favorece a manutenção e a escalabilidade, tornando o sistema adaptável a diferentes contextos e demandas.