# Documentação Técnica - FastTech Control

## Visão Geral

Sistema de gestão de equipamentos e clientes para controle interno de ativos de TI. Interface gráfica moderna desenvolvida com Flet, banco de dados SQLite, arquitetura modular com herança.

**Versão**: 1.0.0  
**Stack**: Python 3.8+ | Flet >= 0.21.0 | SQLite

---

## Arquitetura Modular

### Padrão de Design

O sistema utiliza herança para padronizar comportamento entre abas:

```
BaseTab (gui/base.py)
├── DashboardTab
├── ClientesTab
├── EquipamentosTab
├── MovimentacoesTab
├── ConsultasTab
└── ConfiguracoesTab
```

### Classe Base (BaseTab)

Todas as abas herdam de `BaseTab`, que fornece:

- **Design tokens**: `BORDER_RADIUS`, `SPACING`, `PADDING`, tamanhos de fonte, cores
- **Cores adaptativas**: `get_adaptive_color()`, `get_bg_color()`, `get_text_color()`
- **Helpers de UI**: `botao_primario()`, `criar_container_secao()`, `criar_dialogo_confirmacao()`, `criar_linha_tabela_acoes()`
- **Persistência**: `salvar_config()` para gravar config.json

```python
class BaseTab:
    BORDER_RADIUS = 10
    SPACING = 10
    PADDING = 20
    PRIMARY_COLOR = ft.Colors.BLUE_700

    def __init__(self, page: ft.Page, db, config):
        self.page = page
        self.db = db
        self.config = config

    def build(self):
        raise NotImplementedError()
```

### Padrão de Módulo GUI

Cada módulo em `gui/` segue o padrão:

```python
from gui.base import BaseTab

class NomeTab(BaseTab):
    def __init__(self, page, db, config):
        super().__init__(page, db, config)

    def build(self):
        return ft.Container(...)
```

### Orquestração (app.py)

`FastTechApp` em `app.py` gerencia:
- Inicialização do banco de dados e configurações
- Navegação entre abas (swapping de conteúdo no `content_container`)
- Backup automático na inicialização
- Limpeza de backups antigos
- Header e barra de navegação

---

## Banco de Dados

### Tabelas

#### clientes
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_cliente TEXT DEFAULT 'Cliente Final',
    nome TEXT NOT NULL,
    telefone TEXT UNIQUE NOT NULL,
    email TEXT,
    endereco TEXT,
    documento TEXT UNIQUE,
    setor TEXT,
    regiao TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### equipamentos
```sql
CREATE TABLE equipamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_serie TEXT UNIQUE NOT NULL,
    tipo TEXT NOT NULL,
    marca TEXT,
    modelo TEXT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_atual TEXT DEFAULT 'Em Estoque',
    data_garantia DATE,
    valor_estimado REAL,
    observacoes TEXT
)
```

#### historico_posse
```sql
CREATE TABLE historico_posse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipamento_id INTEGER NOT NULL,
    cliente_id INTEGER,
    data_inicio TIMESTAMP NOT NULL,
    data_fim TIMESTAMP,
    acao TEXT NOT NULL,
    usuario_responsavel TEXT NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL
)
```

#### servicos_equipamentos
```sql
CREATE TABLE servicos_equipamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipamento_id INTEGER NOT NULL,
    cliente_id INTEGER,
    data_servico TIMESTAMP NOT NULL,
    tipo_servico TEXT NOT NULL,
    descricao_problema TEXT,
    servico_realizado TEXT NOT NULL,
    situacao_final TEXT NOT NULL,
    tecnico_responsavel TEXT NOT NULL,
    valor_servico REAL,
    observacoes TEXT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL
)
```

### Relacionamentos

- **clientes → equipamentos**: Via `historico_posse` (N:N lógico)
- **equipamentos → historico_posse**: 1:N (cascade delete)
- **equipamentos → servicos_equipamentos**: 1:N (cascade delete)
- **clientes → servicos_equipamentos**: 1:N (set null on delete)

### Migração Automática

O `database.py` executa `ALTER TABLE` silencioso para adicionar colunas novas (`tipo_cliente`, `regiao`), garantindo retrocompatibilidade.

---

## Camada de Dados (database.py)

### Métodos Principais

| Método | Descrição |
|--------|-----------|
| `inserir_cliente()` | Cadastra cliente com validação de integridade |
| `buscar_clientes(termo)` | Busca por nome, telefone ou documento |
| `atualizar_cliente(id, **kwargs)` | Atualiza campos específicos (whitelist contra SQL injection) |
| `deletar_cliente(id)` | Remove apenas se não tiver equipamentos ativos |
| `inserir_equipamento()` | Cadastra com número de série único |
| `buscar_equipamento_por_serie(serie)` | Busca case-insensitive por serial |
| `inserir_historico()` | Registra movimentação com data_inicio |
| `finalizar_historico(id)` | Preenche data_fim (encerra posse) |
| `inserir_servico()` | Registra serviço realizado no equipamento |
| `buscar_servicos_equipamento(id)` | Lista histórico de serviços |
| `get_estatisticas()` | Retorna totais e contagens por status/tipo |

### Segurança

- Campos permitidos em `atualizar_*()` são definidos em whitelist (`campos_permitidos`)
- Foreign keys mantêm integridade referencial
- `ON DELETE CASCADE` em equipamentos/serviços
- `ON DELETE SET NULL` em cliente_id opcional

---

## Módulos GUI

### Dashboard (`gui/dashboard.py`)
- Cards com 3 níveis de hierarquia visual (180px, 150px, 120px)
- Sistema de 3 cores: PRIMARY (azul escuro), SECONDARY (azul claro), ACCENT (amarelo)
- Hover com elevação e scale
- Calendário integrado
- Estatísticas em tempo real

### Clientes (`gui/clientes.py`)
- Dois tipos: **Cliente Final** (CPF/CNPJ, setor) e **Terceirizado** (WhatsApp, empresa, região)
- Formulário dinâmico que muda conforme tipo selecionado
- Confirmações para editar, salvar e excluir
- Validação por tipo (telefone vs WhatsApp)

### Equipamentos (`gui/equipamentos.py`)
- Navegação por 3 views: Buscar por Serial, Cadastrar, Registrar Serviço
- Busca com foco automático
- Cadastro independente (sem cliente vinculado)
- Registro de serviços com datas retroativas
- Tabela de histórico por equipamento

### Movimentações (`gui/movimentacoes.py`)
- Registro de entregas, devoluções e manutenções
- Atualização automática de status do equipamento
- Histórico completo com responsável e observações

### Consultas (`gui/consultas.py`)
- Busca de equipamentos por múltiplos critérios
- Busca de clientes
- Exportação para CSV
- Sub-abas para consulta de cliente, equipamento e relatórios

### Configurações (`gui/configuracoes.py`)
- Backup automático e limpeza de backups antigos
- Tema (claro/escuro)
- Usuário padrão para movimentações
- Lista de backups com opção de restaurar/deletar

---

## Sistema de Temas

### Implementação

```python
if self.config['tema'] == 'claro':
    self.page.theme_mode = ft.ThemeMode.LIGHT
else:
    self.page.theme_mode = ft.ThemeMode.DARK
```

### Paleta de Cores Adaptativa

| Elemento | Tema Escuro | Tema Claro |
|----------|-------------|------------|
| Fundo | `BLUE_GREY_900` | `GREY_100` |
| Texto | `WHITE` | `BLACK` |
| Texto secundário | `GREY_400` | `GREY_700` |

### Design Tokens (BaseTab)

```python
BORDER_RADIUS = 10
SPACING = 10
PADDING = 20
BODY_SIZE = 14
TITLE_SIZE = 18
SMALL_SIZE = 12
CAPTION_SIZE = 10
H1_SIZE = 32
H2_SIZE = 24
PRIMARY_COLOR = ft.Colors.BLUE_700
SECONDARY_COLOR = ft.Colors.BLUE_400
ACCENT_COLOR = ft.Colors.AMBER_600
```

---

## Sistema de Backup

### Gerenciador (utils/backup.py)

```python
class BackupManager:
    def __init__(self, db_path="fastech.db", backup_dir="backups")
    def criar_backup(nome_customizado=None) -> str
    def listar_backups() -> List[dict]
    def restaurar_backup(backup_path) -> bool
    def deletar_backup(backup_path) -> bool
    def limpar_backups_antigos(dias=30) -> int
```

### Comportamento

1. **Backup automático**: Executado ao iniciar se `backup_automatico: true` no config.json
2. **Limpeza automática**: Remove backups mais antigos que `backup_dias` dias
3. **Restauração segura**: Cria backup do banco atual antes de restaurar
4. **Formato do arquivo**: `fastech_backup_YYYYMMDD_HHMMSS.db`

---

## Validações (utils/validators.py)

| Função | Validação | Obrigatório |
|--------|-----------|-------------|
| `validar_cpf(cpf)` | 11 dígitos, dígitos verificadores, rejeita sequências iguais | Não |
| `validar_cnpj(cnpj)` | 14 dígitos, dígitos verificadores, rejeita sequências iguais | Não |
| `validar_documento(doc)` | Auto-detecta CPF (11) ou CNPJ (14) | Não |
| `validar_telefone(tel)` | 10-11 dígitos, DDD válido (11-99) | Sim |
| `validar_email(email)` | Formato padrão com @ e domínio | Não |
| `validar_numero_serie(serie)` | Mínimo 3 caracteres | Sim |

### Funções de Formatação

- `formatar_cpf()` → XXX.XXX.XXX-XX
- `formatar_cnpj()` → XX.XXX.XXX/XXXX-XX
- `formatar_telefone()` → (XX) XXXXX-XXXX

---

## Convenções de Código

### Nomenclatura

- **Arquivos**: `snake_case` (ex: `clientes.py`)
- **Classes**: `PascalCase` (ex: `ClientesTab`)
- **Métodos**: `snake_case` (ex: `criar_interface()`)
- **Constantes**: `UPPER_CASE` (ex: `TIPOS_EQUIPAMENTO`)

### Estrutura de Métodos

```python
def metodo_exemplo(self):
    """Docstring explicativa"""
    # Validações
    # Lógica principal
    # Atualização de interface
    self.page.update()
```

### Constantes (models.py)

```python
class StatusEquipamento:
    EM_ESTOQUE = "Em Estoque"
    COM_CLIENTE = "Com o Cliente"
    EM_REPARO = "Em Reparo"
    EM_MANUTENCAO = "Em Manutenção"

class TipoEquipamento:
    NOTEBOOK = "Notebook"
    DESKTOP = "Desktop"
    IMPRESSORA = "Impressora"
    MONITOR = "Monitor"
    # ... 10 tipos no total

class AcaoHistorico:
    ENTREGA = "Entrega"
    DEVOLUCAO = "Devolução"
    MANUTENCAO = "Manutenção"
    # ... 7 ações no total
```

---

## Como Estender o Sistema

### Adicionar Nova Aba

1. Criar `gui/nova_aba.py`:
```python
from gui.base import BaseTab

class NovaAbaTab(BaseTab):
    def build(self):
        return ft.Container(...)
```

2. Importar em `app.py` e adicionar método de criação
3. Adicionar botão de navegação na barra lateral

### Adicionar Nova Validação

1. Adicionar função em `utils/validators.py`:
```python
def validar_novo_campo(valor: str) -> Tuple[bool, str]:
    # Lógica de validação
    return True, ""
```

2. Importar e usar no módulo GUI correspondente

### Adicionar Nova Tabela

1. Adicionar `CREATE TABLE` em `database.py` → `create_tables()`
2. Implementar métodos CRUD (inserir, buscar, atualizar, deletar)
3. Usar whitelist de campos permitidos em updates

---

## Fluxo de Dados

### Cadastro de Cliente
```
Interface (clientes.py)
    ↓
Validação (validators.py)
    ↓
Database.inserir_cliente()
    ↓
SQLite (fastech.db)
```

### Movimentação de Equipamento
```
Interface (movimentacoes.py)
    ↓
Database.inserir_historico()
    ↓
Database.atualizar_status_equipamento()
    ↓
SQLite (historico_posse + equipamentos)
```

### Registro de Serviço
```
Interface (equipamentos.py)
    ↓
Validação de campos obrigatórios
    ↓
Database.inserir_servico()
    ↓
SQLite (servicos_equipamentos)
```

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `No module named 'flet'` | `pip install flet>=0.21.0` |
| `Database is locked` | Fechar outras instâncias da aplicação |
| Tema não aplica | Verificar se salvou em Configurações |
| Backup falha | Verificar permissões da pasta `backups/` |
| Python < 3.8 | Atualizar Python para 3.8+ |

### Debug

Para debug detalhado, remover a supressão de warnings em `app.py`:
```python
# Remover esta linha:
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

---

## Dependências

### requirements.txt
```
flet>=0.21.0
pyinstaller>=5.0  # apenas para gerar executável
```

### Bibliotecas Padrão Python
- `sqlite3` — banco de dados
- `json` — configurações
- `datetime` — datas e timestamps
- `shutil` — cópia de arquivos (backup)
- `os` — manipulação de arquivos
- `re` — expressões regulares (validações)
- `calendar` — calendário integrado
- `csv` — exportação de relatórios
- `dataclasses` — modelos de dados

---

## Roadmap Futuro

### Melhorias Planejadas
- [ ] Testes unitários automatizados
- [ ] Logs de auditoria
- [ ] Relatórios em PDF
- [ ] Gráficos e dashboards avançados
- [ ] Exportação para Excel
- [ ] Importação em lote
- [ ] API REST (opcional)
- [ ] Multi-usuário com autenticação

### Otimizações
- [ ] Cache de consultas frequentes
- [ ] Paginação de resultados grandes
- [ ] Índices adicionais no banco
- [ ] Compressão de backups

---

## Métricas de Performance

- **Tempo de inicialização**: < 2 segundos
- **Módulos GUI**: 7+ arquivos independentes
- **Linhas de código GUI**: ~2.300
- **Design tokens**: 12 constantes centralizadas em BaseTab

---

**Versão do Documento**: 1.0.0  
**Última Atualização**: 19/06/2026
