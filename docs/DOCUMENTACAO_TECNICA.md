# 📘 Documentação Técnica - FastTech Control

## 📊 Informações do Projeto

**Nome**: FastTech Control  
**Versão**: 1.0.0  
**Data**: 11/02/2026  
**Linguagem**: Python 3.8+  
**Framework GUI**: Flet 0.80.5  
**Banco de Dados**: SQLite  

---

## 🏗️ Arquitetura do Sistema

### Estrutura de Arquivos

```
FastTech Control/
├── app.py (360 linhas)           # Orquestração principal
├── database.py                    # Camada de dados
├── models.py                      # Modelos e constantes
├── config.json                    # Configurações do usuário
├── fastech.db                     # Banco de dados SQLite
├── requirements.txt               # Dependências
│
├── gui/                          # Módulos de interface
│   ├── __init__.py
│   ├── base.py                   # Classe base (35 linhas)
│   ├── dashboard.py              # Dashboard (180 linhas)
│   ├── clientes.py               # Gestão de clientes (300 linhas)
│   ├── equipamentos.py           # Gestão de equipamentos (468 linhas)
│   ├── movimentacoes.py          # Movimentações (367 linhas)
│   ├── consultas.py              # Consultas e relatórios (627 linhas)
│   └── configuracoes.py          # Configurações (332 linhas)
│
├── utils/                        # Utilitários
│   ├── __init__.py
│   ├── validators.py             # Validações (CPF, CNPJ, etc)
│   └── backup.py                 # Sistema de backup
│
└── backups/                      # Backups automáticos
    └── fastech_backup_*.db
```

---

## 🔧 Arquitetura Modular

### Padrão de Design

O sistema utiliza uma arquitetura modular baseada em:
- **Separação de responsabilidades**: Cada módulo tem uma função específica
- **Herança**: Todos os módulos GUI herdam de `BaseTab`
- **Orquestração centralizada**: `app.py` gerencia navegação e estado global

### Classe Base (BaseTab)

```python
class BaseTab:
    """Classe base para todas as abas"""
    
    def __init__(self, page: ft.Page, db, config):
        self.page = page
        self.db = db
        self.config = config
    
    def get_adaptive_color(self, dark_color, light_color):
        """Retorna cor adaptativa baseada no tema"""
        
    def build(self):
        """Método abstrato - implementado pelas subclasses"""
        raise NotImplementedError()
```

### Módulos GUI

Cada módulo segue o padrão:

```python
from gui.base import BaseTab

class NomeTab(BaseTab):
    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        # Inicialização específica
    
    def build(self):
        """Constrói a interface"""
        # Retorna ft.Container com a interface
```

---

## 🗄️ Camada de Dados

### Database.py

Gerencia todas as operações com SQLite:

**Principais Métodos**:
- `criar_tabelas()`: Cria estrutura do banco
- `adicionar_cliente()`: Insere novo cliente
- `buscar_clientes()`: Busca com filtros
- `adicionar_equipamento()`: Insere equipamento
- `registrar_movimentacao()`: Registra histórico
- `get_estatisticas()`: Retorna estatísticas do sistema

### Estrutura do Banco

```sql
-- Tabela de Clientes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT,
    documento TEXT UNIQUE,
    setor TEXT,
    endereco TEXT,
    data_cadastro TEXT
)

-- Tabela de Equipamentos
CREATE TABLE equipamentos (
    id INTEGER PRIMARY KEY,
    numero_serie TEXT UNIQUE NOT NULL,
    tipo TEXT NOT NULL,
    marca TEXT,
    modelo TEXT,
    status_atual TEXT,
    data_registro TEXT,
    valor_estimado REAL,
    data_garantia TEXT
)

-- Tabela de Histórico
CREATE TABLE historico_posse (
    id INTEGER PRIMARY KEY,
    equipamento_id INTEGER,
    cliente_id INTEGER,
    acao TEXT,
    data_inicio TEXT,
    data_fim TEXT,
    usuario_responsavel TEXT,
    observacoes TEXT,
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
```

---

## 🎨 Sistema de Temas

### Implementação

O sistema suporta temas claro e escuro com aplicação em tempo real:

```python
# Configuração do tema
if self.config['tema'] == 'claro':
    self.page.theme_mode = ft.ThemeMode.LIGHT
else:
    self.page.theme_mode = ft.ThemeMode.DARK

# Cores adaptativas
def get_adaptive_color(self, dark_color, light_color):
    if self.page.theme_mode == ft.ThemeMode.LIGHT:
        return light_color
    return dark_color
```

### Paleta de Cores

**Tema Escuro**:
- Background: `BLUE_GREY_900`
- Texto: `WHITE`
- Texto secundário: `GREY_400`

**Tema Claro**:
- Background: `GREY_100`
- Texto: `BLACK`
- Texto secundário: `GREY_700`

---

## 🔄 Sistema de Backup

### Funcionalidades

1. **Backup Automático**: Executado ao iniciar a aplicação
2. **Backup Manual**: Botão na aba Configurações
3. **Limpeza Automática**: Remove backups antigos (configurável)
4. **Restauração**: Restaura backup anterior com segurança

### Implementação

```python
# Backup automático
if self.config['backup_automatico']:
    criar_backup('fastech.db', 'backups')
    limpar_backups_antigos('backups', dias=self.config['backup_dias'])

# Formato do arquivo
fastech_backup_YYYYMMDD_HHMMSS.db
```

---

## ✅ Sistema de Validações

### Validadores Implementados

**CPF**:
```python
def validar_cpf(cpf: str) -> bool:
    # Remove formatação
    # Valida dígitos verificadores
    # Rejeita CPFs conhecidos como inválidos
```

**CNPJ**:
```python
def validar_cnpj(cnpj: str) -> bool:
    # Remove formatação
    # Valida dígitos verificadores
    # Rejeita CNPJs conhecidos como inválidos
```

**Telefone**:
```python
def validar_telefone(telefone: str) -> bool:
    # Formato: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    # Valida DDD e número
```

**E-mail**:
```python
def validar_email(email: str) -> bool:
    # Validação de formato padrão
    # Verifica @ e domínio
```

---

## 🔐 Segurança e Integridade

### Validações de Entrada
- ✅ CPF/CNPJ validados antes de salvar
- ✅ Número de série único por equipamento
- ✅ Documento único por cliente
- ✅ Campos obrigatórios verificados

### Integridade Referencial
- ✅ Foreign keys no banco de dados
- ✅ Cascata de exclusões configurada
- ✅ Validação de relacionamentos

### Confirmações
- ✅ Diálogos de confirmação para exclusões
- ✅ Backup automático antes de restauração
- ✅ Validação de dados antes de operações críticas

---

## 📊 Fluxo de Dados

### Cadastro de Cliente
```
Interface (clientes.py)
    ↓
Validação (validators.py)
    ↓
Database (database.py)
    ↓
SQLite (fastech.db)
```

### Movimentação de Equipamento
```
Interface (movimentacoes.py)
    ↓
Validação de status
    ↓
Database.registrar_movimentacao()
    ↓
Atualiza histórico_posse
    ↓
Atualiza status_atual do equipamento
```

### Consulta e Relatório
```
Interface (consultas.py)
    ↓
Database.buscar_*()
    ↓
Processamento de dados
    ↓
Exibição ou Exportação CSV
```

---

## 🚀 Performance e Otimizações

### Otimizações Implementadas

1. **Lazy Loading**: Módulos carregados sob demanda
2. **Índices no Banco**: Campos de busca indexados
3. **Cache de Configurações**: Config carregado uma vez
4. **Queries Otimizadas**: JOINs eficientes
5. **Supressão de Warnings**: Avisos de depreciação removidos

### Métricas

- **Tempo de inicialização**: < 2 segundos
- **Tamanho do app.py**: 360 linhas (redução de 85.5%)
- **Módulos independentes**: 7 arquivos
- **Linhas totais de código GUI**: ~2.300 linhas

---

## 🧪 Testes e Validação

### Testes Manuais Realizados

- ✅ CRUD completo de clientes
- ✅ CRUD completo de equipamentos
- ✅ Registro de movimentações
- ✅ Consultas e filtros
- ✅ Exportação CSV
- ✅ Backup e restauração
- ✅ Troca de tema em tempo real
- ✅ Validações de CPF/CNPJ
- ✅ Integridade referencial

### Casos de Teste

1. **Cadastro duplicado**: Sistema rejeita documentos duplicados
2. **Exclusão com relacionamento**: Cascata funciona corretamente
3. **Backup corrompido**: Sistema valida antes de restaurar
4. **Campos vazios**: Validação impede salvamento
5. **Número de série duplicado**: Sistema rejeita

---

## 📈 Histórico de Refatoração

### Versão Inicial (2492 linhas)
- Código monolítico em `app.py`
- Difícil manutenção
- Código duplicado

### Refatoração Modular (360 linhas)
- ✅ Separação em módulos
- ✅ Remoção de código duplicado (445 linhas)
- ✅ Padrão de herança com `BaseTab`
- ✅ Imports organizados
- ✅ Nomenclatura limpa (sem sufixo `_tab`)

### Redução Total
- **Antes**: 2492 linhas no app.py
- **Depois**: 360 linhas no app.py
- **Redução**: 85.5%

---

## 🔧 Manutenção e Extensão

### Adicionar Nova Aba

1. Criar arquivo `gui/nova_aba.py`:
```python
from gui.base import BaseTab

class NovaAbaTab(BaseTab):
    def build(self):
        return ft.Container(...)
```

2. Importar em `app.py`:
```python
from gui.nova_aba import NovaAbaTab
```

3. Adicionar método de criação:
```python
def criar_nova_aba(self):
    tab = NovaAbaTab(self.page, self.db, self.config)
    return tab.build()
```

4. Adicionar botão de navegação

### Adicionar Nova Validação

1. Adicionar função em `utils/validators.py`:
```python
def validar_novo_campo(valor: str) -> bool:
    # Lógica de validação
    return True/False
```

2. Importar onde necessário:
```python
from utils.validators import validar_novo_campo
```

### Adicionar Nova Tabela

1. Atualizar `database.py`:
```python
def criar_tabelas(self):
    self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS nova_tabela (
            id INTEGER PRIMARY KEY,
            campo TEXT
        )
    """)
```

2. Adicionar métodos CRUD correspondentes

---

## 📝 Convenções de Código

### Nomenclatura

- **Arquivos**: snake_case (ex: `clientes.py`)
- **Classes**: PascalCase (ex: `ClientesTab`)
- **Métodos**: snake_case (ex: `criar_interface()`)
- **Constantes**: UPPER_CASE (ex: `TIPOS_EQUIPAMENTO`)

### Estrutura de Métodos

```python
def metodo_exemplo(self):
    """Docstring explicativa"""
    # Validações
    # Lógica principal
    # Atualização de interface
    self.page.update()
```

### Comentários

- Docstrings em todos os métodos públicos
- Comentários inline para lógica complexa
- Seções separadas por comentários descritivos

---

## 🐛 Troubleshooting

### Problemas Comuns

**Erro: "No module named 'flet'"**
```bash
pip install flet==0.80.5
```

**Erro: "Database is locked"**
- Fechar outras instâncias da aplicação
- Verificar permissões do arquivo

**Tema não aplica**
- Verificar se salvou as configurações
- Tema aplica imediatamente (sem reiniciar)

**Backup falha**
- Verificar permissões da pasta `backups/`
- Verificar espaço em disco

---

## 📚 Dependências

```txt
flet==0.80.5
```

**Bibliotecas Padrão Python**:
- sqlite3
- json
- datetime
- shutil
- os
- warnings
- calendar
- csv

---

## 🎯 Roadmap Futuro

### Melhorias Planejadas

- [ ] Testes unitários automatizados
- [ ] Logs de auditoria
- [ ] Relatórios em PDF
- [ ] Gráficos e dashboards avançados
- [ ] Exportação para Excel
- [ ] Importação em lote
- [ ] API REST (opcional)
- [ ] Multi-usuário com autenticação

### Otimizações Futuras

- [ ] Cache de consultas frequentes
- [ ] Paginação de resultados grandes
- [ ] Índices adicionais no banco
- [ ] Compressão de backups

---

## 📞 Suporte Técnico

### Informações de Debug

Para reportar problemas, incluir:
- Versão do Python (`python --version`)
- Versão do Flet (`pip show flet`)
- Sistema operacional
- Mensagem de erro completa
- Passos para reproduzir

### Logs

Logs são exibidos no console durante execução.
Para debug detalhado, remover:
```python
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

---

**Última Atualização**: 11/02/2026  
**Versão do Documento**: 1.0.0  
**Mantido por**: Equipe de Desenvolvimento
