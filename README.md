# ⚙️ FastTech Control

Sistema de Gestão de Equipamentos e Clientes desenvolvido em Python com interface gráfica moderna Flet.

## 📋 Sobre o Projeto

Sistema completo para controle interno de equipamentos, permitindo:
- Cadastro de clientes (CPF/CNPJ validados)
- Gestão de equipamentos (notebooks, impressoras, monitores, etc.)
- Rastreamento de movimentações (entregas, devoluções, manutenções)
- Consultas avançadas e relatórios
- Sistema de backup automático
- Temas claro e escuro
- Interface moderna e intuitiva com Flet

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

### Dashboard
- Visão geral do sistema com cards informativos
- Estatísticas em tempo real
- Calendário e relógio integrados
- Indicadores de status do sistema

### Abas Principais
- **🏠 Dashboard**: Visão geral e estatísticas
- **👥 Clientes**: Cadastro e gestão de clientes
- **📦 Equipamentos**: Cadastro e gestão de equipamentos
- **🔄 Movimentações**: Registro de entregas/devoluções
- **🔍 Consultas**: Buscas e relatórios
- **⚙️ Configurações**: Configurações do sistema

### Temas
- **☀️ Tema Claro**: Ideal para ambientes iluminados
- **🌙 Tema Escuro**: Reduz fadiga ocular, ideal para uso prolongado

Para alterar: Configurações → Geral → Tema → Salvar (aplicação imediata)

## ⌨️ Atalhos de Teclado

### Navegação
- Clique nos botões de navegação para alternar entre abas
- Interface intuitiva com botões destacados

### Funções
- `Enter` - Executar busca (em campos de busca)
- Botões de ação claramente identificados em cada aba

## 💾 Sistema de Backup

### Backup Automático
1. Vá em **Configurações → Backup**
2. Marque ☑️ "Criar backup automático ao iniciar"
3. Configure dias de retenção (padrão: 7 dias)
4. Clique em **💾 Salvar Configurações**

### Backup Manual
- **Configurações → Backup → 💾 Criar Backup Agora**

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
├── app.py                 # Aplicação principal Flet
├── database.py            # Gerenciamento do banco de dados
├── models.py              # Classes e constantes
├── requirements.txt       # Dependências Python
├── fastech.db            # Banco de dados SQLite
├── config.json           # Configurações do usuário
│
├── gui/                  # Interface gráfica (legado)
│   └── __init__.py
│
├── utils/                # Utilitários
│   ├── validators.py     # Validações (CPF, CNPJ, etc)
│   ├── backup.py         # Sistema de backup
│   └── __init__.py
│
├── backups/              # Backups automáticos
│
└── .kiro/                # Configurações Kiro
    ├── steering/         # Diretrizes do projeto
    └── skills/           # Habilidades customizadas
```

## 🔧 Tecnologias

- **Python 3.8+**
- **Flet 0.80.5**: Framework de interface moderna e multiplataforma
- **SQLite**: Banco de dados leve e eficiente
- **Bibliotecas**: json, datetime, shutil, os, warnings

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

### ✅ Etapas Concluídas (8/8)

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
8. ✅ **Etapa 8**: Migração para Flet
   - Interface moderna e responsiva
   - Melhor experiência do usuário
   - Temas adaptativos com alto contraste
   - Aplicação de tema em tempo real

### 🎨 Recursos Implementados

- ✅ Dashboard com estatísticas em tempo real
- ✅ CRUD completo de clientes
- ✅ CRUD completo de equipamentos
- ✅ Sistema de movimentações
- ✅ Histórico completo
- ✅ Consultas avançadas
- ✅ Exportação CSV
- ✅ Backup automático/manual
- ✅ Restauração de backups
- ✅ Temas claro/escuro adaptativos
- ✅ Validações robustas
- ✅ Interface moderna com Flet
- ✅ Aplicação de tema em tempo real
- ✅ Estatísticas do sistema
- ✅ Calendário integrado
- ✅ Cards informativos com alto contraste

## 🐛 Solução de Problemas

### Aplicação não inicia
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar Python
python --version  # Deve ser 3.8+

# Verificar Flet
pip show flet  # Deve ser 0.80.5 ou superior
```

### Erro no banco de dados
```bash
# Verificar integridade do banco
# Use: Configurações → Backup → Restaurar (se disponível)
```

### Tema não aplica
- O tema é aplicado imediatamente ao salvar
- Não é necessário reiniciar a aplicação
- Verifique se salvou as configurações

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
- Equipamentos por status (Em Estoque, Com Cliente, Em Manutenção)
- Movimentações do mês
- Status do sistema
- Tamanho do banco de dados
- Dashboard com cards informativos e visuais

## 🤝 Contribuindo

Este é um projeto interno. Para sugestões ou melhorias:
1. Documente o problema/sugestão
2. Teste em ambiente de desenvolvimento
3. Crie backup antes de modificações

## 📄 Licença

Projeto interno - Todos os direitos reservados

---

**Versão**: 1.0.0  
**Data**: 11/02/2026  
**Status**: ✅ Funcional e Testado  
**Desenvolvido com**: Python 3.8+ | Flet 0.80.5 | SQLite

## 🎉 Novidades da Versão 1.0.0

### Interface Moderna com Flet
- Migração completa de Tkinter para Flet
- Interface mais moderna e profissional
- Melhor experiência do usuário

### Melhorias Visuais
- Dashboard com cards informativos
- Temas adaptativos com alto contraste
- Cores otimizadas para melhor legibilidade
- Botões com relevo e efeitos visuais

### Funcionalidades Aprimoradas
- Aplicação de tema em tempo real (sem reiniciar)
- Calendário integrado no dashboard
- Estatísticas visuais e intuitivas
- Navegação simplificada com botões destacados

### Otimizações
- Remoção de avisos de depreciação
- Código mais limpo e manutenível
- Melhor performance geral
- Interface responsiva
