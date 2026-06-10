# 🚗 AutoRent - Sistema de Aluguel de Veículos

## Sobre o Projeto

O AutoRent é um sistema de gerenciamento de aluguel de veículos desenvolvido com Django. O objetivo do projeto é permitir o cadastro e gerenciamento de veículos, clientes, reservas e avaliações, aplicando regras de negócio relacionadas à disponibilidade dos veículos e cálculo automático de preços.

Nesta etapa inicial, foi desenvolvida a camada de backend responsável pela modelagem dos dados e implementação das regras de negócio principais do sistema.

---

## Funcionalidades Implementadas

### 🚙 Gestão de Veículos

* Cadastro de veículos
* Controle de disponibilidade
* Armazenamento de informações como marca, modelo, ano e valor da diária

### 👤 Gestão de Clientes

* Cadastro de clientes
* Armazenamento de informações de contato
* Controle de CNH única por cliente

### 📅 Gestão de Reservas

* Criação de reservas vinculadas a clientes e veículos
* Validação automática de datas
* Controle de conflito de reservas
* Cálculo automático do valor total da locação
* Aplicação de preço dinâmico para reservas iniciadas em finais de semana
* Controle de status da reserva

### ⭐ Avaliações

* Cadastro de avaliações dos usuários
* Associação entre cliente e veículo
* Sistema de notas e comentários

---

## Regras de Negócio Implementadas

### Controle de Disponibilidade

O sistema impede que um veículo seja reservado para períodos que já possuam reservas ativas, evitando conflitos de agenda.

### Validação de Datas

A data final da reserva deve ser obrigatoriamente posterior à data inicial.

### Cálculo Automático

O valor total da reserva é calculado automaticamente com base na quantidade de dias alugados e no valor da diária do veículo.

### Preço Dinâmico

Reservas iniciadas na sexta-feira, sábado ou domingo recebem um acréscimo de 15% sobre o valor total da locação.

### Soft Delete

Os registros não são removidos fisicamente do banco de dados. Quando excluídos, recebem uma marcação de exclusão lógica, preservando o histórico para auditoria.

---

## Estrutura Atual

```text
autorent/
│
├── autorent_app/
│   ├── api/
│   │   └── v1/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── setup_autorent/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── manage.py
```

---

## Tecnologias Utilizadas

* Python
* Django
* Django REST Framework (configurado para etapas futuras)
* SQLite (desenvolvimento)
* PostgreSQL (planejado)
* JWT (planejado)
* Swagger (planejado)

---

## Próximas Etapas

* Implementação da API REST
* Serializers
* ViewSets
* Routers
* Versionamento da API
* Autenticação JWT
* Documentação Swagger
* Paginação
* Cache de listagens
* Filtros e Query Params
* Integração futura com Front-end React

---

## Status do Projeto

🚧 Em desenvolvimento

Atualmente o backend e as regras de negócio principais estão implementados e sendo preparados para exposição através de uma API REST.
