"""
Módulo de gerenciamento do banco de dados SQLite
Responsável por criar tabelas, conexões e operações CRUD
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import os


class Database:
    def __init__(self, db_name: str = "fastech.db"):
        """Inicializa a conexão com o banco de dados"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Cria as tabelas do sistema se não existirem"""
        
        # Tabela de clientes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT UNIQUE NOT NULL,
                email TEXT,
                endereco TEXT,
                documento TEXT UNIQUE,
                setor TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de equipamentos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipamentos (
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
        """)
        
        # Tabela de histórico de posse
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_posse (
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
        """)
        
        self.conn.commit()
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
    
    # ==================== OPERAÇÕES DE CLIENTES ====================
    
    def inserir_cliente(self, nome: str, telefone: str, email: str = None, 
                       endereco: str = None, documento: str = None, setor: str = None) -> int:
        """Insere um novo cliente no banco de dados"""
        try:
            self.cursor.execute("""
                INSERT INTO clientes (nome, telefone, email, endereco, documento, setor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, telefone, email, endereco, documento, setor))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erro ao inserir cliente: {str(e)}")
    
    def buscar_cliente_por_id(self, cliente_id: int) -> Optional[Dict]:
        """Busca um cliente pelo ID"""
        self.cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def buscar_clientes(self, termo: str = "") -> List[Dict]:
        """Busca clientes por nome ou telefone"""
        termo = f"%{termo}%"
        self.cursor.execute("""
            SELECT * FROM clientes 
            WHERE nome LIKE ? OR telefone LIKE ? OR documento LIKE ?
            ORDER BY nome
        """, (termo, termo, termo))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def atualizar_cliente(self, cliente_id: int, **kwargs) -> bool:
        """Atualiza dados de um cliente"""
        campos = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        valores = list(kwargs.values()) + [cliente_id]
        
        try:
            self.cursor.execute(f"""
                UPDATE clientes SET {campos} WHERE id = ?
            """, valores)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def deletar_cliente(self, cliente_id: int) -> bool:
        """Deleta um cliente (apenas se não tiver equipamentos vinculados)"""
        # Verifica se há equipamentos vinculados
        self.cursor.execute("""
            SELECT COUNT(*) FROM historico_posse 
            WHERE cliente_id = ? AND data_fim IS NULL
        """, (cliente_id,))
        
        if self.cursor.fetchone()[0] > 0:
            return False  # Não pode deletar, tem equipamentos ativos
        
        self.cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        self.conn.commit()
        return True
    
    # ==================== OPERAÇÕES DE EQUIPAMENTOS ====================
    
    def inserir_equipamento(self, numero_serie: str, tipo: str, marca: str = None,
                           modelo: str = None, status_atual: str = "Em Estoque",
                           data_garantia: str = None, valor_estimado: float = None,
                           observacoes: str = None) -> int:
        """Insere um novo equipamento no banco de dados"""
        try:
            self.cursor.execute("""
                INSERT INTO equipamentos 
                (numero_serie, tipo, marca, modelo, status_atual, data_garantia, valor_estimado, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (numero_serie, tipo, marca, modelo, status_atual, data_garantia, valor_estimado, observacoes))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Número de série já cadastrado: {numero_serie}")
    
    def buscar_equipamento_por_id(self, equipamento_id: int) -> Optional[Dict]:
        """Busca um equipamento pelo ID"""
        self.cursor.execute("SELECT * FROM equipamentos WHERE id = ?", (equipamento_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def buscar_equipamento_por_serie(self, numero_serie: str) -> Optional[Dict]:
        """Busca um equipamento pelo número de série"""
        self.cursor.execute("SELECT * FROM equipamentos WHERE numero_serie = ?", (numero_serie,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def buscar_equipamentos(self, termo: str = "", status: str = None) -> List[Dict]:
        """Busca equipamentos por número de série, tipo, marca ou modelo"""
        termo = f"%{termo}%"
        query = """
            SELECT * FROM equipamentos 
            WHERE (numero_serie LIKE ? OR tipo LIKE ? OR marca LIKE ? OR modelo LIKE ?)
        """
        params = [termo, termo, termo, termo]
        
        if status:
            query += " AND status_atual = ?"
            params.append(status)
        
        query += " ORDER BY data_registro DESC"
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def atualizar_equipamento(self, equipamento_id: int, **kwargs) -> bool:
        """Atualiza dados de um equipamento"""
        campos = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        valores = list(kwargs.values()) + [equipamento_id]
        
        try:
            self.cursor.execute(f"""
                UPDATE equipamentos SET {campos} WHERE id = ?
            """, valores)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def atualizar_status_equipamento(self, equipamento_id: int, novo_status: str) -> bool:
        """Atualiza o status atual de um equipamento"""
        return self.atualizar_equipamento(equipamento_id, status_atual=novo_status)
    
    # ==================== OPERAÇÕES DE HISTÓRICO ====================
    
    def inserir_historico(self, equipamento_id: int, acao: str, usuario_responsavel: str,
                         cliente_id: int = None, data_inicio: str = None, 
                         observacoes: str = None) -> int:
        """Insere um novo registro no histórico de posse"""
        if data_inicio is None:
            data_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute("""
            INSERT INTO historico_posse 
            (equipamento_id, cliente_id, data_inicio, acao, usuario_responsavel, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (equipamento_id, cliente_id, data_inicio, acao, usuario_responsavel, observacoes))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def finalizar_historico(self, historico_id: int, data_fim: str = None) -> bool:
        """Finaliza um registro de histórico (preenche data_fim)"""
        if data_fim is None:
            data_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute("""
            UPDATE historico_posse SET data_fim = ? WHERE id = ?
        """, (data_fim, historico_id))
        self.conn.commit()
        return True
    
    def buscar_historico_equipamento(self, equipamento_id: int) -> List[Dict]:
        """Busca todo o histórico de um equipamento"""
        self.cursor.execute("""
            SELECT h.*, c.nome as cliente_nome, c.telefone as cliente_telefone
            FROM historico_posse h
            LEFT JOIN clientes c ON h.cliente_id = c.id
            WHERE h.equipamento_id = ?
            ORDER BY h.data_inicio DESC
        """, (equipamento_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def buscar_historico_cliente(self, cliente_id: int) -> List[Dict]:
        """Busca todo o histórico de equipamentos de um cliente"""
        self.cursor.execute("""
            SELECT h.*, e.numero_serie, e.tipo, e.marca, e.modelo, e.status_atual
            FROM historico_posse h
            JOIN equipamentos e ON h.equipamento_id = e.id
            WHERE h.cliente_id = ?
            ORDER BY h.data_inicio DESC
        """, (cliente_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def buscar_historico_ativo_equipamento(self, equipamento_id: int) -> Optional[Dict]:
        """Busca o registro ativo (sem data_fim) de um equipamento"""
        self.cursor.execute("""
            SELECT h.*, c.nome as cliente_nome, c.telefone as cliente_telefone
            FROM historico_posse h
            LEFT JOIN clientes c ON h.cliente_id = c.id
            WHERE h.equipamento_id = ? AND h.data_fim IS NULL
            ORDER BY h.data_inicio DESC
            LIMIT 1
        """, (equipamento_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def buscar_equipamentos_cliente_ativo(self, cliente_id: int) -> List[Dict]:
        """Busca todos os equipamentos atualmente com um cliente"""
        self.cursor.execute("""
            SELECT DISTINCT e.*, h.data_inicio, h.acao, h.observacoes
            FROM equipamentos e
            JOIN historico_posse h ON e.id = h.equipamento_id
            WHERE h.cliente_id = ? AND h.data_fim IS NULL
            ORDER BY h.data_inicio DESC
        """, (cliente_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ==================== OPERAÇÕES AUXILIARES ====================
    
    def backup_database(self, backup_path: str = None) -> str:
        """Cria um backup do banco de dados"""
        import shutil
        import os
        
        if backup_path is None:
            # Cria pasta de backups se não existir
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"fastech_backup_{timestamp}.db")
        
        shutil.copy2(self.db_name, backup_path)
        return backup_path
    
    def get_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais do sistema"""
        stats = {}
        
        # Total de clientes
        self.cursor.execute("SELECT COUNT(*) FROM clientes")
        stats['total_clientes'] = self.cursor.fetchone()[0]
        
        # Total de equipamentos
        self.cursor.execute("SELECT COUNT(*) FROM equipamentos")
        stats['total_equipamentos'] = self.cursor.fetchone()[0]
        
        # Equipamentos por status
        self.cursor.execute("""
            SELECT status_atual, COUNT(*) as total 
            FROM equipamentos 
            GROUP BY status_atual
        """)
        stats['por_status'] = {row['status_atual']: row['total'] for row in self.cursor.fetchall()}
        
        # Equipamentos por tipo
        self.cursor.execute("""
            SELECT tipo, COUNT(*) as total 
            FROM equipamentos 
            GROUP BY tipo
        """)
        stats['por_tipo'] = {row['tipo']: row['total'] for row in self.cursor.fetchall()}
        
        return stats


# Função auxiliar para testes
if __name__ == "__main__":
    db = Database()
    print("Banco de dados inicializado com sucesso!")
    print("\nEstatísticas:")
    stats = db.get_estatisticas()
    print(f"Total de clientes: {stats['total_clientes']}")
    print(f"Total de equipamentos: {stats['total_equipamentos']}")
    db.close()
