# FastTech Control

Sistema de Gestão de Equipamentos e Clientes desenvolvido em Python com interface gráfica Flet.

## Instalação

```bash
pip install -r requirements.txt
python app.py
```

Na primeira execução, o banco de dados `fastech.db` é criado automaticamente.

## Funcionalidades

- **Clientes**: Cadastro com validação de CPF/CNPJ, dois tipos (Cliente Final e Terceirizado)
- **Equipamentos**: Cadastro por número de série, busca rápida, registro de serviços realizados
- **Movimentações**: Registro de entregas, devoluções e manutenções com histórico completo
- **Consultas**: Busca avançada e exportação para CSV
- **Dashboard**: Visão geral com estatísticas em tempo real
- **Backup**: Criptografia automática e restauração de backups
- **Temas**: Claro e escuro com aplicação em tempo real

## Estrutura do Projeto

```
fastech_OS/
├── app.py                 # Aplicação principal (orquestração)
├── database.py            # Camada de dados (SQLite)
├── models.py              # Modelos e constantes
├── config.json            # Configurações do usuário
├── requirements.txt       # Dependências
├── gui/                   # Interface gráfica
│   ├── base.py            # Classe BaseTab (design system)
│   ├── dashboard.py       # Dashboard principal
│   ├── clientes.py        # Gestão de clientes
│   ├── equipamentos.py    # Gestão de equipamentos e serviços
│   ├── movimentacoes.py   # Registro de movimentações
│   ├── consultas.py       # Consultas e relatórios
│   ├── configuracoes.py   # Configurações do sistema
│   └── ...                # Outros módulos de consulta
├── utils/
│   ├── validators.py      # Validações (CPF, CNPJ, telefone, email)
│   └── backup.py          # Sistema de backup
└── backups/               # Diretório de backups automáticos
```

## Tecnologias

- Python 3.8+
- Flet >= 0.21.0 (interface gráfica multiplataforma)
- SQLite (banco de dados leve)

## Configurações

O arquivo `config.json` controla:

```json
{
    "backup_automatico": false,
    "backup_dias": 7,
    "tema": "claro",
    "usuario_padrao": "Técnico"
}
```

## Documentação Técnica

Consulte [docs/DOCUMENTACAO_TECNICA.md](docs/DOCUMENTACAO_TECNICA.md) para detalhes sobre arquitetura, banco de dados, convenções de código e como estender o sistema.

## Licença

Projeto interno - Todos os direitos reservados.
