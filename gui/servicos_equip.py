"""
Ordem de Serviço - Gestão de serviços de equipamentos
"""
import flet as ft
from datetime import datetime


class ServicoView:
    """View de ordem de serviço para equipamentos"""

    def __init__(self, orc, page, db, config):
        self.orc = orc
        self.page = page
        self.db = db
        self.config = config
        self._init_campos_servico()

    def _get_tipos_servico(self):
        """Retorna lista de tipos de serviço (padrão + customizados)"""
        tipos_padrao = [
            "Manutenção Preventiva",
            "Manutenção Corretiva",
            "Reparo",
            "Instalação",
            "Configuração",
            "Limpeza",
            "Atualização",
            "Diagnóstico",
        ]
        tipos_custom = self.config.get('tipos_servico_custom', [])
        return tipos_padrao + [t for t in tipos_custom if t not in tipos_padrao]

    def _salvar_tipo_servico_custom(self, novo_tipo: str) -> bool:
        """Persiste um novo tipo de serviço no config.json"""
        tipos = self.config.get('tipos_servico_custom', [])
        if novo_tipo in tipos:
            return False
        tipos.append(novo_tipo)
        self.config['tipos_servico_custom'] = tipos
        return self.orc.salvar_config()

    def _remover_tipo_servico_custom(self, tipo: str):
        """Remove um tipo customizado do config.json"""
        tipos = self.config.get('tipos_servico_custom', [])
        if tipo in tipos:
            tipos.remove(tipo)
            self.config['tipos_servico_custom'] = tipos
            self.orc.salvar_config()

    def _rebuild_tipo_servico_dropdown(self):
        """Reconstrói as opções do dropdown de tipo de serviço"""
        tipos = self._get_tipos_servico()
        self.tipo_servico_dropdown.options = (
            [ft.dropdown.Option(t) for t in tipos]
            + [ft.dropdown.Option("__novo__", "➕ Novo tipo de serviço...")]
        )

    def _on_tipo_servico_change(self, e):
        """Mostra/oculta o campo de novo tipo conforme seleção"""
        valor = getattr(e, 'data', None) or self.tipo_servico_dropdown.value
        if valor == "__novo__":
            self.novo_tipo_row.visible = True
            self.tipo_servico_dropdown.value = None
        else:
            self.novo_tipo_row.visible = False
        self.page.update()

    def _salvar_novo_tipo(self, e):
        """Salva o novo tipo e atualiza o dropdown"""
        novo = self.novo_tipo_field.value.strip()
        if not novo:
            return
        tipos_existentes = self._get_tipos_servico()
        if novo in tipos_existentes:
            self.tipo_servico_dropdown.value = novo
            self.novo_tipo_row.visible = False
            self.novo_tipo_field.value = ""
            self.page.update()
            return
        self._salvar_tipo_servico_custom(novo)
        self._rebuild_tipo_servico_dropdown()
        self.tipo_servico_dropdown.value = novo
        self.novo_tipo_row.visible = False
        self.novo_tipo_field.value = ""
        self.page.update()

    def _init_campos_servico(self):
        """Inicializa todos os campos do formulário de serviço"""
        self.data_servico_field = ft.TextField(
            label="Data do Serviço *",
            hint_text="AAAA-MM-DD ou DD/MM/AAAA",
            value=datetime.now().strftime("%Y-%m-%d"),
            expand=True,
        )

        tipos_iniciais = self._get_tipos_servico()
        self.tipo_servico_dropdown = ft.Dropdown(
            label="Tipo de Serviço *",
            expand=True,
            options=(
                [ft.dropdown.Option(t) for t in tipos_iniciais]
                + [ft.dropdown.Option("__novo__", "➕ Novo tipo de serviço...")]
            ),
            on_select=self._on_tipo_servico_change,
        )

        self.novo_tipo_field = ft.TextField(
            label="Nome do novo tipo *",
            hint_text="Ex: Troca de Tela",
            expand=True,
        )
        self.novo_tipo_row = ft.Row(
            [
                self.novo_tipo_field,
                self.orc.botao_primario(
                    "💾 Salvar tipo",
                    on_click=self._salvar_novo_tipo,
                    radius=8,
                ),
            ],
            spacing=8,
            visible=False,
        )

        self.cliente_servico_dropdown = ft.Dropdown(
            label="Cliente (opcional)",
            expand=True,
            options=[ft.dropdown.Option("0", "Sem cliente")],
            value="0",
        )
        self.descricao_problema_field = ft.TextField(
            label="Descrição do Problema",
            hint_text="Descreva o problema relatado",
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=3,
        )
        self.servico_realizado_field = ft.TextField(
            label="Serviço Realizado *",
            hint_text="Descreva o que foi feito",
            expand=True,
            multiline=True,
            min_lines=3,
            max_lines=5,
        )
        self.situacao_final_dropdown = ft.Dropdown(
            label="Situação Final *",
            expand=True,
            options=[
                ft.dropdown.Option("Resolvido"),
                ft.dropdown.Option("Parcialmente Resolvido"),
                ft.dropdown.Option("Não Resolvido"),
                ft.dropdown.Option("Aguardando Peças"),
                ft.dropdown.Option("Sem Conserto"),
            ],
        )
        self.tecnico_field = ft.TextField(
            label="Técnico Responsável *",
            value=self.config.get('usuario_padrao', 'Técnico'),
            expand=True,
        )
        self.valor_servico_field = ft.TextField(
            label="Valor do Serviço (R$)",
            hint_text="0.00",
            expand=True,
        )
        self.obs_servico_field = ft.TextField(
            label="Observações",
            hint_text="Informações adicionais",
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=3,
        )
        self.servico_status = ft.Text("", size=14)

    def mostrar_servicos(self):
        """Mostra a view de registro de serviços"""
        self.orc.view_atual = "servicos"

        if not self.orc.equipamento_selecionado:
            self.orc.content_container.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("⚠️ Nenhum equipamento selecionado", size=18, color=ft.Colors.ORANGE),
                        ft.Text("Busque um equipamento primeiro para registrar serviços", size=14),
                        self.orc.botao_primario(
                            "🔍 Buscar Equipamento",
                            on_click=lambda e: self.orc.mostrar_busca(),
                            radius=8,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=40,
            )
            self.page.update()
            return

        clientes = self.db.buscar_clientes()
        self.cliente_servico_dropdown.options = [ft.dropdown.Option("0", "Sem cliente")]
        for c in clientes:
            self.cliente_servico_dropdown.options.append(
                ft.dropdown.Option(str(c['id']), f"{c['nome']} - {c['telefone']}")
            )
        self.cliente_servico_dropdown.value = "0"

        self._rebuild_tipo_servico_dropdown()
        self.novo_tipo_row.visible = False
        self.novo_tipo_field.value = ""

        equip = self.orc.equipamento_selecionado
        info_equip = ft.Container(
            content=ft.Text(
                f"📦 {equip['tipo']} - {equip['numero_serie']} ({equip['marca']} {equip['modelo']})",
                size=16,
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=self.orc.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=15,
            border_radius=10,
        )

        self.orc.content_container.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("🔧 Registrar Serviço", size=20, weight=ft.FontWeight.BOLD),
                    info_equip,
                    ft.Divider(),
                    self.data_servico_field,
                    self.tipo_servico_dropdown,
                    self.novo_tipo_row,
                    self.cliente_servico_dropdown,
                    self.descricao_problema_field,
                    self.servico_realizado_field,
                    self.situacao_final_dropdown,
                    ft.Row([self.tecnico_field, self.valor_servico_field], spacing=10),
                    self.obs_servico_field,
                    self.servico_status,
                    ft.Row(
                        [
                            self.orc.botao_primario(
                                "💾 Salvar Serviço",
                                on_click=self.salvar_servico,
                                expand=True,
                                radius=8,
                            ),
                            self.orc.botao_primario(
                                "🔄 Limpar",
                                on_click=self.limpar_form_servico,
                                expand=True,
                                radius=8,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
        )
        self.page.update()

    def salvar_servico(self, e):
        """Salva um novo serviço"""
        data_servico = self.data_servico_field.value
        tipo_servico = self.tipo_servico_dropdown.value
        servico_realizado = self.servico_realizado_field.value
        situacao_final = self.situacao_final_dropdown.value
        tecnico = self.tecnico_field.value

        if not all([data_servico, tipo_servico, servico_realizado, situacao_final, tecnico]) or tipo_servico == "__novo__":
            self.servico_status.value = "❌ Preencha todos os campos obrigatórios (selecione ou crie um tipo de serviço)"
            self.servico_status.color = ft.Colors.RED
            self.page.update()
            return

        try:
            if '/' in data_servico:
                partes = data_servico.split('/')
                data_servico = f"{partes[2]}-{partes[1]}-{partes[0]}"
            datetime.strptime(data_servico, "%Y-%m-%d")
        except Exception:
            self.servico_status.value = "❌ Data inválida. Use AAAA-MM-DD ou DD/MM/AAAA"
            self.servico_status.color = ft.Colors.RED
            self.page.update()
            return

        cliente_id = None
        if self.cliente_servico_dropdown.value != "0":
            cliente_id = int(self.cliente_servico_dropdown.value)

        valor_servico = None
        if self.valor_servico_field.value:
            try:
                valor_servico = float(self.valor_servico_field.value.replace(',', '.'))
            except Exception:
                pass

        try:
            self.db.inserir_servico(
                self.orc.equipamento_selecionado['id'],
                data_servico,
                tipo_servico,
                servico_realizado,
                situacao_final,
                tecnico,
                cliente_id,
                self.descricao_problema_field.value or None,
                valor_servico,
                self.obs_servico_field.value or None,
            )
            self.servico_status.value = "✅ Serviço registrado com sucesso!"
            self.servico_status.color = ft.Colors.GREEN
            self.limpar_form_servico()
            self.page.update()
        except Exception as ex:
            self.servico_status.value = f"❌ Erro: {str(ex)}"
            self.servico_status.color = ft.Colors.RED
            self.page.update()

    def limpar_form_servico(self, e=None):
        """Limpa o formulário de serviço"""
        self.data_servico_field.value = datetime.now().strftime("%Y-%m-%d")
        self.tipo_servico_dropdown.value = None
        self.cliente_servico_dropdown.value = "0"
        self.descricao_problema_field.value = ""
        self.servico_realizado_field.value = ""
        self.situacao_final_dropdown.value = None
        self.tecnico_field.value = self.config.get('usuario_padrao', 'Técnico')
        self.valor_servico_field.value = ""
        self.obs_servico_field.value = ""
        self.servico_status.value = ""
        self.page.update()
