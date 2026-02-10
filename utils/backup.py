"""
Funções para backup e restauração do banco de dados
"""

import os
import shutil
from datetime import datetime
from typing import List, Optional


class BackupManager:
    """Gerenciador de backups do banco de dados"""
    
    def __init__(self, db_path: str = "fastech.db", backup_dir: str = "backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir
        
        # Cria diretório de backups se não existir
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def criar_backup(self, nome_customizado: str = None) -> str:
        """
        Cria um backup do banco de dados
        Retorna o caminho do arquivo de backup criado
        """
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Banco de dados não encontrado: {self.db_path}")
        
        # Define nome do backup
        if nome_customizado:
            backup_filename = f"{nome_customizado}.db"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"fastech_backup_{timestamp}.db"
        
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        # Copia o arquivo
        shutil.copy2(self.db_path, backup_path)
        
        return backup_path
    
    def listar_backups(self) -> List[dict]:
        """
        Lista todos os backups disponíveis
        Retorna lista de dicionários com informações dos backups
        """
        backups = []
        
        if not os.path.exists(self.backup_dir):
            return backups
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                
                backups.append({
                    'nome': filename,
                    'caminho': filepath,
                    'tamanho': stat.st_size,
                    'data_criacao': datetime.fromtimestamp(stat.st_ctime),
                    'data_modificacao': datetime.fromtimestamp(stat.st_mtime)
                })
        
        # Ordena por data de criação (mais recente primeiro)
        backups.sort(key=lambda x: x['data_criacao'], reverse=True)
        
        return backups
    
    def restaurar_backup(self, backup_path: str) -> bool:
        """
        Restaura um backup do banco de dados
        ATENÇÃO: Sobrescreve o banco atual!
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup não encontrado: {backup_path}")
        
        # Cria backup do banco atual antes de restaurar
        if os.path.exists(self.db_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_atual = f"fastech_antes_restauracao_{timestamp}.db"
            shutil.copy2(self.db_path, os.path.join(self.backup_dir, backup_atual))
        
        # Restaura o backup
        shutil.copy2(backup_path, self.db_path)
        
        return True
    
    def deletar_backup(self, backup_path: str) -> bool:
        """Deleta um arquivo de backup"""
        if os.path.exists(backup_path):
            os.remove(backup_path)
            return True
        return False
    
    def limpar_backups_antigos(self, dias: int = 30) -> int:
        """
        Remove backups mais antigos que X dias
        Retorna quantidade de backups removidos
        """
        removidos = 0
        limite = datetime.now().timestamp() - (dias * 24 * 60 * 60)
        
        for backup in self.listar_backups():
            if backup['data_criacao'].timestamp() < limite:
                self.deletar_backup(backup['caminho'])
                removidos += 1
        
        return removidos
    
    def formatar_tamanho(self, tamanho_bytes: int) -> str:
        """Formata tamanho em bytes para formato legível"""
        for unidade in ['B', 'KB', 'MB', 'GB']:
            if tamanho_bytes < 1024.0:
                return f"{tamanho_bytes:.2f} {unidade}"
            tamanho_bytes /= 1024.0
        return f"{tamanho_bytes:.2f} TB"


# Testes
if __name__ == "__main__":
    manager = BackupManager()
    
    print("=== Teste de Backup ===\n")
    
    # Cria um backup de teste
    try:
        backup_path = manager.criar_backup("teste_manual")
        print(f"Backup criado: {backup_path}")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    
    # Lista backups
    print("\n=== Backups Disponíveis ===\n")
    backups = manager.listar_backups()
    for backup in backups:
        tamanho = manager.formatar_tamanho(backup['tamanho'])
        data = backup['data_criacao'].strftime("%d/%m/%Y %H:%M:%S")
        print(f"{backup['nome']} - {tamanho} - {data}")
