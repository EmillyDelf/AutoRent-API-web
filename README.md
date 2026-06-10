# 🚗 AutoRent - Sistema de Locação de Veículos

## 📖 Sobre o Projeto

O **AutoRent** é um sistema de gerenciamento de locação de veículos desenvolvido utilizando **Python, Django, Django REST Framework e PostgreSQL**.

O objetivo do projeto é automatizar os principais processos de uma locadora de veículos, permitindo o gerenciamento de clientes, frota, reservas, pagamentos e avaliações por meio de uma API REST segura e documentada.

O sistema foi desenvolvido seguindo boas práticas de arquitetura, separação de responsabilidades e implementação de regras de negócio, sendo preparado para futura integração com uma aplicação Front-end desenvolvida em React.

---

## 🎯 Objetivos

* Gerenciar veículos disponíveis para locação.
* Gerenciar clientes e seus documentos.
* Controlar reservas e disponibilidade da frota.
* Processar pagamentos.
* Permitir avaliações dos veículos.
* Disponibilizar uma API REST versionada.
* Implementar autenticação segura com JWT.
* Fornecer documentação automática da API.
* Preparar integração futura com Front-end React.

---

## 🏗️ Arquitetura do Projeto

```text
autorent/
│
├── autorent_app/
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── serializers.py
│   │       ├── viewsets.py
│   │       ├── routers.py
│   │       └── urls.py
│   │
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── setup_autorent/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env
├── manage.py
└── requirements.txt
```

---

## 🛠 Tecnologias Utilizadas

### Backend

* Python 3
* Django
* Django REST Framework
* PostgreSQL

### Segurança

* JWT Authentication
* Django Permissions

### Documentação

* Swagger / OpenAPI
* DRF Spectacular

### Utilitários

* Django Filters
* Cache Framework
* Python Decouple

---

## 📦 Modelos Implementados

### 🚙 Veículo

Responsável pelo gerenciamento da frota.

Campos principais:

* Marca
* Modelo
* Ano
* Placa
* Preço da diária
* Status

Status disponíveis:

* Disponível
* Alugado
* Manutenção

---

### 👤 Cliente

Responsável pelo cadastro dos locatários.

Campos principais:

* Nome
* E-mail
* CPF
* CNH
* Telefone
* Data de nascimento
* Endereço
* CEP

---

### 📅 Reserva

Responsável pelo processo de locação.

Campos principais:

* Cliente
* Veículo
* Data de início
* Data de fim
* Valor total
* Status

Status disponíveis:

* Pendente
* Confirmada
* Finalizada
* Cancelada

---

### 💳 Pagamento

Responsável pelo controle financeiro das reservas.

Campos principais:

* Reserva
* Valor
* Método
* Status
* Data de pagamento

Métodos disponíveis:

* PIX
* Cartão de Crédito
* Cartão de Débito
* Dinheiro

Status disponíveis:

* Pendente
* Pago
* Cancelado

---

### ⭐ Avaliação

Responsável pelo feedback dos clientes.

Campos principais:

* Cliente
* Veículo
* Nota
* Comentário

---

## ⚙️ Regras de Negócio Implementadas

### Controle de Reservas

O sistema impede que um mesmo veículo possua duas reservas simultâneas para períodos conflitantes.

### Validação de Datas

A data final deve ser obrigatoriamente posterior à data inicial da reserva.

### Cálculo Automático da Locação

O valor total da reserva é calculado automaticamente utilizando:

```text
Valor da diária × Quantidade de dias
```

### Preço Dinâmico

Reservas iniciadas em:

* Sexta-feira
* Sábado
* Domingo

recebem acréscimo automático de 15%.

### Atualização Automática de Status

Quando uma reserva é confirmada:

```text
Veículo → ALUGADO
```

Quando uma reserva é finalizada ou cancelada:

```text
Veículo → DISPONÍVEL
```

### Soft Delete

Os registros não são removidos fisicamente do banco de dados.

Ao excluir um registro, o sistema apenas marca a data de exclusão, preservando histórico e auditoria.

---

## 🔒 Validações Implementadas

* CPF
* CEP
* Placa veicular
* Ano do veículo
* Valor mínimo da diária
* Nota da avaliação
* Data de nascimento
* Conflito de reservas

---

## 🧩 Recursos Implementados

### Backend

* BaseModel reutilizável
* Soft Delete
* Relacionamentos entre entidades
* Validators personalizados
* Django Admin configurado
* PostgreSQL integrado
* Variáveis de ambiente (.env)

### API REST

* Versionamento `/api/v1`
* Serializers
* ViewSets
* Routers
* CRUD completo dos modelos

### Segurança

* JWT Authentication
* Controle de acesso por token

### Performance

* Paginação
* Cache em listagens
* Search
* Ordering
* Query Parameters
* Filtros dinâmicos

### Documentação

* Swagger UI
* OpenAPI Schema

---

## 🔗 Principais Endpoints

```text
/api/v1/veiculos/
/api/v1/clientes/
/api/v1/reservas/
/api/v1/pagamentos/
/api/v1/avaliacoes/
```

### Autenticação

```text
/api/token/
/api/token/refresh/
```

### Documentação

```text
/api/docs/
/api/schema/
```

---

## 🧪 Testes da API

A API pode ser testada utilizando:

* Swagger UI
* Postman
* Insomnia

---


## 📌 Status do Projeto

🚧 Em desenvolvimento

Atualmente o backend e a API REST encontram-se implementados, contemplando os requisitos acadêmicos do projeto. O próximo passo será a construção do Front-end em React e a evolução dos recursos avançados da aplicação.
