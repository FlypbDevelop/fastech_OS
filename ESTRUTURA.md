# 📁 Estrutura do Projeto

## 🗂️ Árvore de Arquivos

```
fastech_control/
│
├── 📄 README.md              # Documentação oficial completa
├── 📊 STATUS.md              # Status visual do projeto
├── 📋 ESTRUTURA.md           # Este arquivo
│
├── 🚀 app.py                 # Ponto de entrada da aplicação
├── 🗄️ database.py            # Gerenciamento do banco de dados
├── 📦 models.py              # Classes e constantes do sistema
├── 📋 requirements.txt       # Dependências Python
├── 🔒 .gitignore             # Arquivos ignorados pelo Git
│
├── 💾 fastech.db             # Banco de dados SQLite (gerado)
├── ⚙️ config.json            # Configurações do usuário (gerado)
│
├── 📁 gui/                   # Interface Gráfica
│   ├── main_window.py        # Janela principal com abas
│   ├── cliente_form.py       # Formulário de clientes
│   ├── equipamento_form.py   # Formulário de equipamentos
│   ├── movimentacao_form.py  # Sistema de movimentações
│   ├── consulta_form.py      # Consultas e relatórios
│   ├── config_form.py        # Configurações do sistema
│   ├── styles.py             # Sistema de estilos (tema claro)
│   ├── styles_dark.py        # Tema escuro
│   ├── widgets.py            # Widgets customizados
│   └── __init__.py           # Inicializador do módulo
│
├── 📁 utils/                 # Utilitários
│   ├── validators.py         # Validações (CPF, CNPJ, etc)
│   ├── backup.py             # Sistema de backup
│   └── __init__.py           # Inicializador do módulo
│
└── 📁 backups/               # Backups automáticos (gerado)
    └── fastech_backup_*.db   # Arquivos de backup
```

## 📊 Estatísticas

### Arquivos por Tipo
```
Python:         15 arquivos
Documentação:    3 arquivos
Configuração:    2 arquivos
Total:          20 arquivos
```

### Linhas de Código
```
GUI:           ~2000 linhas
Database:       ~500 linhas
Utils:          ~300 linhas
Models:         ~100 linhas
App:            ~50 linhas
Total:         ~3000 linhas
```

## 🎯 Arquivos Principais

### 🚀 Execução
- **app.py**: Inicia a aplicação GUI

### 📚 Documentação
- **README.md**: Documentação completa do projeto
- **STATUS.md**: Status visual das etapas
- **ESTRUTURA.md**: Este arquivo

### 💻 Código Core
- **database.py**: Toda lógica do banco de dados
- **models.py**: Constantes e classes do sistema

### 🎨 Interface
- **gui/main_window.py**: Janela principal
- **gui/*_form.py**: Formulários específicos
- **gui/styles.py**: Sistema de estilos

### 🔧 Utilitários
- **utils/validators.py**: Validações de dados
- **utils/backup.py**: Sistema de backup

## 📦 Módulos

### gui (Interface Gráfica)
```python
from gui.main_window import MainWindow
from gui.cliente_form import ClienteForm
from gui.equipamento_form import EquipamentoForm
from gui.movimentacao_form import MovimentacaoForm
from gui.consulta_form import ConsultaForm
from gui.config_form import ConfigForm
from gui.styles import COLORS, FONTS, PADDING
from gui.widgets import CustomButton, StatusLabel, LabeledEntry
```

### utils (Utilitários)
```python
from utils.validators import validar_cpf, validar_cnpj, validar_telefone
from utils.backup import BackupManager
```

### Core
```python
from database import Database
from models import TIPOS_EQUIPAMENTO, STATUS_EQUIPAMENTO
```

## 🗄️ Banco de Dados

### Tabelas
```sql
clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    tipo_documento TEXT,
    documento TEXT UNIQUE,
    telefone TEXT,
    email TEXT,
    endereco TEXT,
    data_cadastro TIMESTAMP
)

equipamentos (
    id INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL,
    marca TEXT,
    modelo TEXT,
    numero_serie TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL,
    cliente_id INTEGER,
    observacoes TEXT,
    data_cadastro TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)

historico_posse (
    id INTEGER PRIMARY KEY,
    equipamento_id INTEGER NOT NULL,
    cliente_id INTEGER,
    tipo_movimentacao TEXT NOT NULL,
    data_movimentacao TIMESTAMP NOT NULL,
    responsavel TEXT,
    observacoes TEXT,
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
```

## 🎨 Componentes GUI

### Janela Principal
- Header com logo e estatísticas
- Notebook com 5 abas
- Menu superior
- Barra de status
- Atalhos de teclado

### Abas
1. **👥 Clientes**: CRUD de clientes
2. **📦 Equipamentos**: CRUD de equipamentos
3. **🔄 Movimentações**: Registro de movimentações
4. **🔍 Consultas**: Buscas e relatórios
5. **⚙️ Configurações**: Configurações do sistema

### Widgets Customizados
- **CustomButton**: Botões estilizados
- **StatusLabel**: Labels de status com cores
- **LabeledEntry**: Campos de entrada com label
- **SearchBar**: Barra de busca
- **DataTable**: Tabela de dados

## 🔧 Dependências

```txt
# requirements.txt
# Nenhuma dependência externa!
# Usa apenas bibliotecas padrão do Python:
# - tkinter (GUI)
# - sqlite3 (Banco de dados)
# - json (Configurações)
# - datetime (Datas)
# - shutil (Backup)
# - os (Sistema de arquivos)
```

## 🚀 Como Executar

```bash
# 1. Clonar/baixar o projeto
cd fastech_control

# 2. Executar (sem instalação necessária!)
python app.py
```

## 📝 Arquivos Gerados

### Primeira Execução
- `fastech.db` - Banco de dados SQLite
- `config.json` - Configurações padrão

### Durante Uso
- `backups/fastech_backup_*.db` - Backups automáticos
- `*.csv` - Exportações de relatórios

## 🎯 Estrutura Limpa

### ✅ Mantido
- Código fonte essencial
- Documentação oficial
- Arquivos de configuração

### ❌ Removido
- Scripts de teste
- Documentações redundantes
- Arquivos de desenvolvimento
- Checklists de etapas
- Logs de correções

## 📊 Organização

```
Documentação:  3 arquivos (README, STATUS, ESTRUTURA)
Código Core:   3 arquivos (app, database, models)
GUI:           9 arquivos (interface completa)
Utils:         2 arquivos (validações, backup)
Config:        2 arquivos (requirements, gitignore)
```

---

**Total**: 19 arquivos essenciais  
**Linhas**: ~3000 linhas de código  
**Dependências**: 0 (apenas Python padrão)  
**Status**: ✅ Pronto para uso
