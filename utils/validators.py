"""
Funções de validação para dados do sistema
"""

import re
from typing import Tuple


def validar_cpf(cpf: str) -> Tuple[bool, str]:
    """
    Valida um CPF brasileiro
    Retorna (True, "") se válido ou (False, "mensagem de erro")
    """
    if not cpf:
        return True, ""  # CPF é opcional
    
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False, "CPF deve ter 11 dígitos"
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False, "CPF inválido"
    
    # Validação dos dígitos verificadores
    def calcular_digito(cpf_parcial, peso_inicial):
        soma = sum(int(cpf_parcial[i]) * (peso_inicial - i) for i in range(len(cpf_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    # Valida primeiro dígito
    if int(cpf[9]) != calcular_digito(cpf[:9], 10):
        return False, "CPF inválido"
    
    # Valida segundo dígito
    if int(cpf[10]) != calcular_digito(cpf[:10], 11):
        return False, "CPF inválido"
    
    return True, ""


def validar_cnpj(cnpj: str) -> Tuple[bool, str]:
    """
    Valida um CNPJ brasileiro
    Retorna (True, "") se válido ou (False, "mensagem de erro")
    """
    if not cnpj:
        return True, ""  # CNPJ é opcional
    
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False, "CNPJ deve ter 14 dígitos"
    
    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False, "CNPJ inválido"
    
    # Validação dos dígitos verificadores
    def calcular_digito(cnpj_parcial, pesos):
        soma = sum(int(cnpj_parcial[i]) * pesos[i] for i in range(len(cnpj_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    # Pesos para validação
    pesos_primeiro = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_segundo = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Valida primeiro dígito
    if int(cnpj[12]) != calcular_digito(cnpj[:12], pesos_primeiro):
        return False, "CNPJ inválido"
    
    # Valida segundo dígito
    if int(cnpj[13]) != calcular_digito(cnpj[:13], pesos_segundo):
        return False, "CNPJ inválido"
    
    return True, ""


def validar_documento(documento: str) -> Tuple[bool, str]:
    """
    Valida CPF ou CNPJ automaticamente baseado no tamanho
    """
    if not documento:
        return True, ""
    
    # Remove caracteres não numéricos
    doc_limpo = re.sub(r'\D', '', documento)
    
    if len(doc_limpo) == 11:
        return validar_cpf(documento)
    elif len(doc_limpo) == 14:
        return validar_cnpj(documento)
    else:
        return False, "Documento deve ser CPF (11 dígitos) ou CNPJ (14 dígitos)"


def validar_telefone(telefone: str) -> Tuple[bool, str]:
    """
    Valida formato de telefone brasileiro
    Aceita: (11) 98765-4321, 11987654321, etc.
    """
    if not telefone:
        return False, "Telefone é obrigatório"
    
    # Remove caracteres não numéricos
    tel_limpo = re.sub(r'\D', '', telefone)
    
    # Verifica se tem 10 ou 11 dígitos (com ou sem 9 no celular)
    if len(tel_limpo) not in [10, 11]:
        return False, "Telefone deve ter 10 ou 11 dígitos"
    
    # Verifica se começa com DDD válido (11-99)
    ddd = int(tel_limpo[:2])
    if ddd < 11 or ddd > 99:
        return False, "DDD inválido"
    
    return True, ""


def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida formato básico de email
    """
    if not email:
        return True, ""  # Email é opcional
    
    # Regex simples para validação de email
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(padrao, email):
        return False, "Email inválido"
    
    return True, ""


def formatar_cpf(cpf: str) -> str:
    """Formata CPF para o padrão XXX.XXX.XXX-XX"""
    cpf_limpo = re.sub(r'\D', '', cpf)
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf


def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ para o padrão XX.XXX.XXX/XXXX-XX"""
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    if len(cnpj_limpo) == 14:
        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    return cnpj


def formatar_telefone(telefone: str) -> str:
    """Formata telefone para o padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX"""
    tel_limpo = re.sub(r'\D', '', telefone)
    
    if len(tel_limpo) == 11:
        return f"({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}"
    elif len(tel_limpo) == 10:
        return f"({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}"
    
    return telefone


def validar_numero_serie(numero_serie: str) -> Tuple[bool, str]:
    """Valida número de série (não pode ser vazio)"""
    if not numero_serie or not numero_serie.strip():
        return False, "Número de série é obrigatório"
    
    if len(numero_serie.strip()) < 3:
        return False, "Número de série muito curto"
    
    return True, ""


# Testes
if __name__ == "__main__":
    # Testes de validação
    print("=== Testes de Validação ===\n")
    
    # CPF
    print("CPF válido:", validar_cpf("123.456.789-09"))
    print("CPF inválido:", validar_cpf("111.111.111-11"))
    
    # CNPJ
    print("CNPJ válido:", validar_cnpj("11.222.333/0001-81"))
    
    # Telefone
    print("Telefone válido:", validar_telefone("(11) 98765-4321"))
    print("Telefone inválido:", validar_telefone("123"))
    
    # Email
    print("Email válido:", validar_email("teste@exemplo.com"))
    print("Email inválido:", validar_email("teste@"))
    
    print("\n=== Testes de Formatação ===\n")
    print("CPF formatado:", formatar_cpf("12345678909"))
    print("Telefone formatado:", formatar_telefone("11987654321"))
