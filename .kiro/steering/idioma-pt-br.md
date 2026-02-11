---
inclusion: auto
---

# Diretriz de Idioma - Português Brasileiro

## Regra Principal

**SEMPRE mantenha a conversa em português brasileiro (pt-br)** em todas as interações, especialmente:

- Ao iniciar uma nova sessão
- Ao terminar uma tarefa
- Durante todo o desenvolvimento
- Em mensagens de status e feedback
- Em documentação e comentários de código

## Aplicação

Esta regra se aplica a:

- ✅ Todas as respostas e mensagens ao usuário
- ✅ Documentação gerada (README, STATUS, etc.)
- ✅ Comentários em código Python
- ✅ Mensagens de commit (se aplicável)
- ✅ Nomes de variáveis e funções em português quando apropriado
- ✅ Strings de interface do usuário (labels, botões, mensagens)

## Exceções

Manter em inglês apenas:

- ❌ Palavras-chave de linguagens de programação (def, class, import, etc.)
- ❌ Nomes de bibliotecas e frameworks (flet, sqlite, etc.)
- ❌ Termos técnicos consolidados sem tradução adequada

## Exemplo de Aplicação

```python
# ✅ CORRETO - Comentários em pt-br
def criar_cliente(nome, telefone):
    """Cria um novo cliente no banco de dados"""
    # Validar dados obrigatórios
    if not nome or not telefone:
        return "❌ Nome e telefone são obrigatórios"
    
    # Inserir no banco
    return db.inserir_cliente(nome, telefone)

# ❌ INCORRETO - Comentários em inglês
def criar_cliente(nome, telefone):
    """Creates a new client in the database"""
    # Validate required data
    if not nome or not telefone:
        return "❌ Name and phone are required"
```

---

**Última atualização**: 11/02/2026
