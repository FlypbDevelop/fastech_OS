# ⚙️ FastTech Control

Sistema de Gestão de Equipamentos e Clientes desenvolvido em Python com interface gráfica.

## 📋 Sobre o Projeto

Sistema completo para controle interno de equipamentos, permitindo:
- Cadastro de clientes (CPF/CNPJ validados)
- Gestão de equipamentos (notebooks, impressoras, monitores, etc.)
- Rastreamento de movimentações (entregas, devoluções, manutenções)
- Consultas avançadas e relatórios
- Sistema de backup automático
- Temas claro e escuro

## 🚀 Como Usar

### Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
```

### Primeira Execução

1. A aplicação criará automaticamente o banco de dados `fastech.db`
2. Configure o sistema em **⚙️ Configurações**:
   - Ative backup automático (recomendado)
   - Escolha o tema (claro/escuro)
   - Defina o usuário padrão

## 📚 Funcionalidades

### 👥 Gestão de Clientes
- Cadastro com validação de CPF/CNPJ
- Busca por nome, documento ou telefone
- Edição e exclusão com confirmação
- Validação de unicidade de documentos

### 📦 Gestão de Equipamentos
- Cadastro vinculado a clientes
- Tipos: Notebook, Desktop, Monitor, Impressora, Smartphone, Tablet, Servidor, Roteador
- Status: Com o Cliente, Em Estoque, Em Manutenção, Descartado
- Número de série único
- Histórico completo de movimentações

### 🔄 Movimentações
- Registro de entregas, devoluções e manutenções
- Histórico completo por equipamento
- Rastreamento de responsável atual
- Data e observações de cada movimentação

### 🔍 Consultas e Relatórios
- Busca de equipamentos por múltiplos critérios
- Busca de clientes
- Exportação para CSV
- Estatísticas do sistema

### ⚙️ Configurações
- **Backup Automático**: Cria backup ao iniciar
- **Limpeza de Backups**: Remove backups antigos automaticamente
- **Temas**: Claro (padrão) ou Escuro
- **Usuário Padrão**: Nome usado nas movimentações
- **Restauração**: Restaurar backups anteriores

## 🎨 Interface

### Abas Principais
- **👥 Clientes**: Cadastro e gestão de clientes
- **📦 Equipamentos**: Cadastro e gestão de equipamentos
- **🔄 Movimentações**: Registro de entregas/devoluções
- **🔍 Consultas**: Buscas e relatórios
- **⚙️ Configurações**: Configurações do sistema

### Temas
- **☀️ Tema Claro**: Ideal para ambientes iluminados
- **🌙 Tema Escuro**: Reduz fadiga ocular, ideal para uso prolongado

Para alterar: Configurações → Geral → Tema → Salvar → Reiniciar

## ⌨️ Atalhos de Teclado

### Navegação
- `Ctrl+1` - Aba Clientes
- `Ctrl+2` - Aba Equipamentos
- `Ctrl+3` - Aba Movimentações
- `Ctrl+4` - Aba Consultas
- `Ctrl+5` - Aba Configurações

### Funções
- `Ctrl+B` - Criar Backup
- `Ctrl+S` - Salvar Configurações
- `F5` - Atualizar Estatísticas
- `F1` - Mostrar Atalhos
- `Enter` - Executar busca (em campos de busca)

## 💾 Sistema de Backup

### Backup Automático
1. Vá em **Configurações → Backup**
2. Marque ☑️ "Criar backup automático ao iniciar"
3. Configure dias de retenção (padrão: 7 dias)
4. Clique em **💾 Salvar Configurações**

### Backup Manual
- **Configurações → Backup → 💾 Criar Backup Agora**
- Ou pressione `Ctrl+B` em qualquer aba

### Restaurar Backup
1. **Configurações → Backup → ♻️ Restaurar Backup**
2. Selecione o backup desejado
3. Confirme a restauração
4. Reinicie a aplicação

**Importante**: Um backup do banco atual é criado automaticamente antes da restauração.

## 🗄️ Estrutura do Banco de Dados

### Tabelas
- **clientes**: Dados dos clientes (nome, documento, contatos)
- **equipamentos**: Dados dos equipamentos (tipo, marca, modelo, série)
- **historico_posse**: Histórico de movimentações

### Relacionamentos
- Cliente → Equipamentos (1:N)
- Equipamento → Histórico (1:N)

## 📁 Estrutura do Projeto

```
fastech_control/
├── app.py                 # Ponto de entrada da aplicação
├── database.py            # Gerenciamento do banco de dados
├── models.py              # Classes e constantes
├── requirements.txt       # Dependências Python
├── fastech.db            # Banco de dados SQLite
├── config.json           # Configurações do usuário
│
├── gui/                  # Interface gráfica
│   ├── main_window.py    # Janela principal
│   ├── cliente_form.py   # Formulário de clientes
│   ├── equipamento_form.py
│   ├── movimentacao_form.py
│   ├── consulta_form.py
│   ├── config_form.py
│   ├── styles.py         # Sistema de estilos
│   ├── styles_dark.py    # Tema escuro
│   └── widgets.py        # Widgets customizados
│
├── utils/                # Utilitários
│   ├── validators.py     # Validações (CPF, CNPJ, etc)
│   └── backup.py         # Sistema de backup
│
└── backups/              # Backups automáticos
```

## 🔧 Tecnologias

- **Python 3.8+**
- **SQLite**: Banco de dados
- **tkinter**: Interface gráfica
- **Bibliotecas**: json, datetime, shutil, os

## 📊 Validações Implementadas

### CPF
- Formato: XXX.XXX.XXX-XX
- Validação de dígitos verificadores
- Rejeita CPFs conhecidos como inválidos

### CNPJ
- Formato: XX.XXX.XXX/XXXX-XX
- Validação de dígitos verificadores
- Rejeita CNPJs conhecidos como inválidos

### Telefone
- Formato: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
- Validação de DDD e número

### E-mail
- Validação de formato padrão
- Verifica presença de @ e domínio

### Número de Série
- Único no sistema
- Obrigatório para equipamentos

## 🎯 Status do Projeto

### ✅ Etapas Concluídas (7/8)

1. ✅ **Etapa 1**: Base de dados SQLite com validações
2. ✅ **Etapa 2**: Interface GUI para clientes
3. ✅ **Etapa 3**: Interface GUI para equipamentos
4. ✅ **Etapa 4**: Sistema de movimentações
5. ✅ **Etapa 5**: Consultas e relatórios
6. ✅ **Etapa 6**: Interface principal e navegação
7. ✅ **Etapa 7**: Melhorias e recursos extras
   - Sistema de backup completo
   - Temas claro/escuro
   - Configurações persistentes
   - Botões de ação visíveis
8. ⏳ **Etapa 8**: Distribuição (pendente)

### 🎨 Recursos Implementados

- ✅ CRUD completo de clientes
- ✅ CRUD completo de equipamentos
- ✅ Sistema de movimentações
- ✅ Histórico completo
- ✅ Consultas avançadas
- ✅ Exportação CSV
- ✅ Backup automático/manual
- ✅ Restauração de backups
- ✅ Temas claro/escuro
- ✅ Validações robustas
- ✅ Interface intuitiva
- ✅ Atalhos de teclado
- ✅ Estatísticas do sistema

## 🐛 Solução de Problemas

### Aplicação não inicia
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar Python
python --version  # Deve ser 3.8+
```

### Erro no banco de dados
```bash
# Verificar integridade
python verificar_banco.py

# Restaurar backup (se disponível)
# Use: Configurações → Backup → Restaurar
```

### Tema não aplica
- Certifique-se de salvar as configurações
- Feche e reabra a aplicação completamente

## 📝 Configuração (config.json)

```json
{
    "backup_automatico": false,
    "backup_dias": 7,
    "backup_pasta": "backups",
    "tema": "claro",
    "usuario_padrao": "Técnico"
}
```

## 🔐 Segurança

- ✅ Validação de dados de entrada
- ✅ Confirmação para exclusões
- ✅ Backup antes de restauração
- ✅ Integridade referencial no banco
- ✅ Unicidade de documentos e séries

## 📈 Estatísticas

- Total de clientes cadastrados
- Total de equipamentos
- Equipamentos por status
- Equipamentos por tipo
- Tamanho do banco de dados

## 🤝 Contribuindo

Este é um projeto interno. Para sugestões ou melhorias:
1. Documente o problema/sugestão
2. Teste em ambiente de desenvolvimento
3. Crie backup antes de modificações

## 📄 Licença

Projeto interno - Todos os direitos reservados

---

**Versão**: 0.7.0  
**Data**: 02/12/2024  
**Status**: ✅ Funcional e Testado  
**Desenvolvido com**: Python 3.8+ | SQLite | tkinter
