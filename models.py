"""
Classes de modelo para representar as entidades do sistema
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Cliente:
    """Representa um cliente/pessoa no sistema"""
    id: Optional[int] = None
    nome: str = ""
    telefone: str = ""
    email: Optional[str] = None
    endereco: Optional[str] = None
    documento: Optional[str] = None
    setor: Optional[str] = None
    data_cadastro: Optional[str] = None
    
    def __str__(self):
        return f"{self.nome} - {self.telefone}"
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'documento': self.documento,
            'setor': self.setor
        }


@dataclass
class Equipamento:
    """Representa um equipamento/ativo no sistema"""
    id: Optional[int] = None
    numero_serie: str = ""
    tipo: str = ""
    marca: Optional[str] = None
    modelo: Optional[str] = None
    data_registro: Optional[str] = None
    status_atual: str = "Em Estoque"
    data_garantia: Optional[str] = None
    valor_estimado: Optional[float] = None
    observacoes: Optional[str] = None
    
    def __str__(self):
        return f"{self.tipo} - {self.numero_serie}"
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'numero_serie': self.numero_serie,
            'tipo': self.tipo,
            'marca': self.marca,
            'modelo': self.modelo,
            'status_atual': self.status_atual,
            'data_garantia': self.data_garantia,
            'valor_estimado': self.valor_estimado,
            'observacoes': self.observacoes
        }


@dataclass
class HistoricoPosse:
    """Representa um registro de histórico de posse"""
    id: Optional[int] = None
    equipamento_id: int = 0
    cliente_id: Optional[int] = None
    data_inicio: str = ""
    data_fim: Optional[str] = None
    acao: str = ""
    usuario_responsavel: str = ""
    observacoes: Optional[str] = None
    
    # Campos extras para joins
    cliente_nome: Optional[str] = None
    cliente_telefone: Optional[str] = None
    numero_serie: Optional[str] = None
    tipo: Optional[str] = None
    
    def __str__(self):
        return f"{self.acao} - {self.data_inicio}"
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'equipamento_id': self.equipamento_id,
            'cliente_id': self.cliente_id,
            'data_inicio': self.data_inicio,
            'data_fim': self.data_fim,
            'acao': self.acao,
            'usuario_responsavel': self.usuario_responsavel,
            'observacoes': self.observacoes
        }
    
    @property
    def esta_ativo(self) -> bool:
        """Verifica se o registro está ativo (sem data_fim)"""
        return self.data_fim is None


# Constantes do sistema
class StatusEquipamento:
    """Status possíveis para equipamentos"""
    EM_ESTOQUE = "Em Estoque"
    COM_CLIENTE = "Com o Cliente"
    EM_REPARO = "Em Reparo"
    DEVOLVIDO = "Devolvido"
    BAIXADO = "Baixado"
    EM_MANUTENCAO = "Em Manutenção"
    
    @classmethod
    def todos(cls):
        return [
            cls.EM_ESTOQUE,
            cls.COM_CLIENTE,
            cls.EM_REPARO,
            cls.DEVOLVIDO,
            cls.BAIXADO,
            cls.EM_MANUTENCAO
        ]


class TipoEquipamento:
    """Tipos comuns de equipamentos"""
    NOTEBOOK = "Notebook"
    DESKTOP = "Desktop"
    SMARTPHONE = "Smartphone"
    TABLET = "Tablet"
    IMPRESSORA = "Impressora"
    MONITOR = "Monitor"
    ROTEADOR = "Roteador"
    SWITCH = "Switch"
    SERVIDOR = "Servidor"
    OUTRO = "Outro"
    
    @classmethod
    def todos(cls):
        return [
            cls.NOTEBOOK,
            cls.DESKTOP,
            cls.SMARTPHONE,
            cls.TABLET,
            cls.IMPRESSORA,
            cls.MONITOR,
            cls.ROTEADOR,
            cls.SWITCH,
            cls.SERVIDOR,
            cls.OUTRO
        ]


class AcaoHistorico:
    """Ações possíveis no histórico"""
    CADASTRO = "Cadastro"
    ENTREGA = "Entrega"
    DEVOLUCAO = "Devolução"
    MANUTENCAO = "Manutenção"
    REPARO = "Reparo"
    TRANSFERENCIA = "Transferência"
    BAIXA = "Baixa"
    
    @classmethod
    def todos(cls):
        return [
            cls.CADASTRO,
            cls.ENTREGA,
            cls.DEVOLUCAO,
            cls.MANUTENCAO,
            cls.REPARO,
            cls.TRANSFERENCIA,
            cls.BAIXA
        ]
