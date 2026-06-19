# PROJECT_PROGRESS - FastTech Control

> **ATENÇÃO para IAs**: Este arquivo documenta o estado atual do projeto para evitar que alterações quebrem funcionalidades existentes. Leia antes de modificar qualquer arquivo.

---

## Estado Atual do Projeto

**Status**: Funcional e em uso  
**Versão**: 1.0.0  
**Última atualização**: 19/06/2026  
**Stack**: Python 3.8+ | Flet 0.82.2 | SQLite

---

## Arquitetura

### Layout da Interface

```
┌──────────────┬─────────────────────────────────┐
│              │  Header (azul, logo + título)    │
│   Sidebar    ├─────────────────────────────────┤
│  (lateral)   │                                 │
│              │  content_container              │
│  ⚙️ FastTech │  (conteúdo da aba ativa)        │
│  🏠 Dashboard│                                 │
│  👥 Clientes │                                 │
│  📦 Equip.   │                                 │
│  🔄 Mov.     │                                 │
│  🔍 Cons.    │                                 │
│  ⚙️ Config   │                                 │
│      ◀       │                                 │
└──────────────┴─────────────────────────────────┘
```

### Navegação

- **Sidebar customizada** em `app.py` (NÃO usa NavigationRail do Flet)
- Largura expandida: 220px | Colapsada: 72px
- Botão toggle (◀/▶) no rodapé
- Aba ativa: fundo `BLUE_700` + ícone preenchido branco
- Padding lateral: 8px esquerda, 6px direita

### Arquivos Principais

| Arquivo | Responsabilidade | Cuidados |
|---------|------------------|----------|
| `app.py` | Orquestração, sidebar, navegação | NÃO usar `ft.animation.Animation` (usar `ft.Animation`) |
| `database.py` | CRUD SQLite, 4 tabelas | Whitelist de campos em updates |
| `models.py` | Dataclasses e constantes | StatusEquipamento, TipoEquipamento, AcaoHistorico |
| `gui/base.py` | Classe BaseTab, design tokens | Todas as abas herdam daqui |
| `gui/dashboard.py` | Dashboard com cards | 3 níveis de hierarquia visual |
| `gui/clientes.py` | Gestão de clientes | 2 tipos: Cliente Final / Terceirizado |
| `gui/equipamentos.py` | Equipamentos + serviços | 3 views: Buscar, Cadastrar, Serviço |
| `gui/movimentacoes.py` | Entregas/devoluções | Atualiza status do equipamento |
| `gui/consultas.py` | Buscas + CSV | 3 sub-abas internas |
| `gui/configuracoes.py` | Config + backups | 3 sub-abas internas |
| `utils/validators.py` | CPF, CNPJ, telefone, email | Retorna Tuple[bool, str] |
| `utils/backup.py` | BackupManager | Cria backup antes de restaurar |

---

## Banco de Dados

### Tabelas (4)

1. **clientes** - Cadastro de clientes (Cliente Final / Terceirizado)
2. **equipamentos** - Equipamentos com número de série único
3. **historico_posse** - Histórico de movimentações
4. **servicos_equipamentos** - Serviços realizados nos equipamentos

### Relacionamentos

- `equipamentos` → `historico_posse`: CASCADE DELETE
- `equipamentos` → `servicos_equipamentos`: CASCADE DELETE
- `clientes` → `historico_posse`: SET NULL
- `clientes` → `servicos_equipamentos`: SET NULL

### Migração

- `database.py` executa `ALTER TABLE` silencioso para novas colunas
- Retrocompatível com bancos anteriores

---

## Regras Importantes para IAs

### SEMPRE FAZER

1. **Compilar após alterações**: `python -m py_compile app.py`
2. **Testar imports**: `python -c "import app"`
3. **Verificar versão do Flet**: `ft.Animation()` (PascalCase), NUNCA `ft.animation.Animation()`
4. **Manter sidebar**: A navegação é customizada em `app.py`, não usar NavigationRail
5. **Preservar `content_container`**: Mecanismo de troca de abas
6. **Usar design tokens**: Cores e tamanhos definidos em `BaseTab`

### NUNCA FAZER

1. **NÃO** usar `ft.animation.Animation()` - causa erro `module 'flet' has no attribute 'animation'`
2. **NÃO** alterar a estrutura da sidebar sem testar colapso/expansão
3. **NÃO** remover a lista `self.menu_items` ou `self.conteudos_abas`
4. **NÃO** alterar ordem dos itens no `menu_items` sem atualizar `conteudos_abas`
5. **NÃO** usar `visible=True` em Text dentro de Row - usar `expand=True`
6. **NÃO** alterar `self.sidebar_width` ou `self.sidebar_collapsed_width` sem ajustar botões

### AO ADICIONAR NOVA ABA

1. Criar `gui/nova_aba.py` herando de `BaseTab`
2. Importar em `app.py`
3. Criar método `criar_nova_aba()` que retorna `tab.build()`
4. Adicionar conteúdo em `self.conteudos_abas` (mesma posição do menu)
5. Adicionar item em `self.menu_items`:
   ```python
   ("ícone_emoji", ft.Icons.ICON_OUTLINED, ft.Icons.ICON, "Nome")
   ```

### AO MODIFICAR SIDEBAR

- Larguras: `sidebar_width=220`, `sidebar_collapsed_width=72`
- Padding container: `left=8, right=6`
- Padding botões: `left=14, right=10`
- Botão toggle: `width=56` (colapsado) ou `sidebar_width - 32` (expandido)

---

## Funcionalidades Implementadas

- [x] Dashboard com estatísticas em tempo real
- [x] CRUD completo de clientes (2 tipos)
- [x] CRUD completo de equipamentos
- [x] Sistema de movimentações
- [x] Histórico completo
- [x] Consultas avançadas
- [x] Exportação CSV
- [x] Backup automático/manual
- [x] Restauração de backups
- [x] Temas claro/escuro
- [x] Validações robustas (CPF, CNPJ, telefone, email)
- [x] Interface moderna com Flet
- [x] Sidebar lateral colapsável
- [x] Registro de serviços com datas retroativas

---

## Roadmap (Melhorias Futuras)

- [ ] Testes unitários automatizados
- [ ] Logs de auditoria
- [ ] Relatórios em PDF
- [ ] Gráficos e dashboards avançados
- [ ] Exportação para Excel
- [ ] Importação em lote
- [ ] API REST (opcional)
- [ ] Multi-usuário com autenticação

---

## Comandos Úteis

```bash
# Executar aplicação
python app.py

# Verificar compilação
python -m py_compile app.py

# Verificar imports
python -c "import app"

# Verificar versão do Flet
python -c "import flet as ft; print(ft.__version__)"

# Listar classes de animação disponíveis
python -c "import flet as ft; [print(x) for x in dir(ft) if 'nima' in x.lower()]"
```

---

## Histórico de Mudanças Importantes

| Data | Mudança | Arquivo | Cuidado |
|------|---------|---------|---------|
| 19/06/2026 | Sidebar lateral colapsável | `app.py` | Não usar NavigationRail |
| 19/06/2026 | Consolidação de documentação | `docs/` | Removidos 4 changelogs |
| 19/06/2026 | Correção `ft.Animation` | `app.py` | PascalCase, não lowercase |
