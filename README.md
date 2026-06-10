# 🚗 AutoRent - Sistema de Aluguel de Veículos

## Sobre o Projeto

O AutoRent é um sistema de gerenciamento de locação de veículos desenvolvido com Django e PostgreSQL. O projeto foi concebido para automatizar os principais processos de uma locadora, incluindo gestão de clientes, controle de frota, reservas, pagamentos e avaliações.

Nesta fase foi desenvolvida a camada de backend, responsável pela modelagem dos dados, validações, regras de negócio e administração do sistema através do Django Admin, preparando a aplicação para futura integração com uma API REST e um front-end React.

---

## Funcionalidades Implementadas

### 🚙 Gestão de Veículos

* Cadastro de veículos
* Controle de status do veículo
* Identificação por placa
* Controle de valor da diária
* Validação de placa
* Controle de disponibilidade por status

Campos principais:

* Marca
* Modelo
* Ano
* Placa
* Valor da diária
* Status

---

### 👤 Gestão de Clientes

* Cadastro completo de clientes
* Controle de CPF único
* Controle de CNH única
* Armazenamento de endereço
* Validação de CPF
* Validação de CEP

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

### 📅 Gestão de Reservas

* Criação de reservas vinculadas a clientes e veículos
* Controle de períodos de locação
* Cálculo automático do valor da reserva
* Controle de conflitos de agenda
* Atualização automática do status do veículo
* Controle de status da reserva

Status disponíveis:

* Pendente
* Confirmada
* Finalizada
* Cancelada

---

### 💳 Gestão de Pagamentos

* Associação de pagamento a uma reserva
* Controle de valor pago
* Controle de método de pagamento
* Controle de status do pagamento
* Registro da data de pagamento

Métodos disponíveis:

* PIX
* Cartão de Crédito
* Cartão de Débito
* Dinheiro

---

### ⭐ Avaliações

* Avaliação de veículos por clientes
* Sistema de notas de 1 a 5
* Comentários sobre a experiência de locação

---

## Regras de Negócio Implementadas

### Controle de Conflito de Reservas

O sistema impede que um veículo possua duas reservas simultâneas para períodos sobrepostos.

### Validação de Datas

A data final da reserva deve ser posterior à data inicial.

### Cálculo Automático da Locação

O valor total da reserva é calculado automaticamente com base na quantidade de dias e no valor da diária do veículo.

### Preço Dinâmico

Reservas iniciadas na sexta-feira, sábado ou domingo recebem acréscimo de 15% sobre o valor total.

### Atualização Automática de Status

Ao confirmar uma reserva, o veículo passa automaticamente para o status "Alugado". Quando a reserva é finalizada ou cancelada, o veículo retorna para "Disponível".

### Soft Delete

Os registros não são removidos fisicamente do banco de dados. A exclusão é lógica, preservando o histórico para auditoria e rastreabilidade.

---

## Validações Implementadas

* CPF
* CEP
* Placa veicular
* Ano do veículo
* Valor mínimo da diária
* Nota da avaliação
* Data de nascimento
* Conflitos de reserva

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
└── manage.py
```

---

## Tecnologias Utilizadas

* Python 3
* Django
* Django REST Framework
* PostgreSQL
* Python Decouple
* Django Admin

---

## Banco de Dados

O projeto utiliza PostgreSQL como banco de dados principal.

A configuração é realizada através de variáveis de ambiente armazenadas em arquivo `.env`.

---

## Próximas Etapas

* Desenvolvimento da API REST
* Serializers
* ViewSets
* Routers
* Versionamento da API
* Autenticação JWT
* Documentação Swagger/OpenAPI
* Paginação
* Filtros e busca
* Cache
* Testes automatizados
* Integração com Front-end React

---

## Status do Projeto

🚧 Em desenvolvimento

Atualmente o domínio da aplicação, as entidades principais, as validações e as regras de negócio já estão implementados. O próximo passo será a construção da API REST responsável pela comunicação com aplicações externas e pelo futuro front-end React.
