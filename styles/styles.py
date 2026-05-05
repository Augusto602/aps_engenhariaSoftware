import tkinter as tk

# ── Cores ────────────────────────────────────────────────────
CORES = {
    "fundo":         "#ECEFF4",   # fundo geral
    "superficie":    "#FFFFFF",   # cards / painéis
    "primaria":      "#37474F",   # cinza-ardósia (cabeçalhos, botões secundários)
    "destaque":      "#00897B",   # verde-água (ação principal, sucesso)
    "perigo":        "#E53935",   # vermelho (erros)
    "texto":         "#212121",   # texto principal
    "texto_suave":   "#757575",   # placeholder / texto secundário
    "borda":         "#CFD8DC",   # bordas sutis
    "sombra":        "#CFD8DC",   # sombra simulada
}

# ── Tipografia ───────────────────────────────────────────────
FONTES = {
    "titulo":    ("Segoe UI", 15, "bold"),
    "rotulo":    ("Segoe UI", 10),
    "entrada":   ("Segoe UI", 10),
    "botao":     ("Segoe UI", 10, "bold"),
    "pequena":   ("Segoe UI",  9),
    "resultado": ("Segoe UI", 10),
}


def construir_cabecalho(pai, titulo: str, ao_voltar=None) -> tk.Frame:
    """
    Barra de cabeçalho padrão.
    - titulo    : texto exibido à esquerda
    - ao_voltar : se fornecido, adiciona botão '← Voltar' à direita
    """
    barra = tk.Frame(pai, bg=CORES["primaria"], height=52)
    barra.pack(fill="x")
    barra.pack_propagate(False)

    tk.Label(
        barra, text=titulo,
        bg=CORES["primaria"], fg="#FFFFFF",
        font=FONTES["titulo"], padx=16,
    ).pack(side="left", fill="y")

    if ao_voltar:
        botao_voltar = tk.Label(
            barra, text="← Voltar",
            bg=CORES["primaria"], fg="#ECEFF4",
            font=FONTES["botao"], padx=16,
            cursor="hand2",
        )
        botao_voltar.pack(side="right", fill="y")
        botao_voltar.bind("<Enter>",    lambda e: botao_voltar.config(bg="#455A64"))
        botao_voltar.bind("<Leave>",    lambda e: botao_voltar.config(bg=CORES["primaria"]))
        botao_voltar.bind("<Button-1>", lambda e: ao_voltar())

    return barra


def construir_card(pai) -> tk.Frame:
    """
    Frame com borda e sombra simulada.
    Retorna o frame interno pronto para receber widgets.
    """
    sombra = tk.Frame(pai, bg=CORES["sombra"])
    sombra.pack(fill="x")

    card = tk.Frame(
        sombra, bg=CORES["superficie"],
        highlightbackground=CORES["borda"],
        highlightthickness=1,
    )
    card.pack(fill="x", padx=3, pady=3)

    interno = tk.Frame(card, bg=CORES["superficie"])
    interno.pack(fill="x", padx=20, pady=16)

    return interno


def construir_campo(pai, rotulo: str, placeholder: str = "", largura: int = 40) -> tk.Entry:
    """
    Rótulo + Entry estilizados com suporte a placeholder.
    Retorna o widget Entry.
    """
    container = tk.Frame(pai, bg=CORES["superficie"])
    container.pack(fill="x", pady=6)

    tk.Label(
        container, text=rotulo,
        bg=CORES["superficie"], fg=CORES["texto"],
        font=FONTES["rotulo"], anchor="w",
    ).pack(fill="x")

    campo = tk.Entry(
        container,
        font=FONTES["entrada"],
        width=largura,
        bg="#F8FAFB",
        fg=CORES["texto"],
        insertbackground=CORES["primaria"],
        relief="flat",
        highlightbackground=CORES["borda"],
        highlightcolor=CORES["destaque"],
        highlightthickness=1,
    )
    campo.pack(fill="x", ipady=7)

    if placeholder:
        campo.insert(0, placeholder)
        campo.config(fg=CORES["texto_suave"])

        def _foco_entrar(e):
            if campo.get() == placeholder:
                campo.delete(0, tk.END)
                campo.config(fg=CORES["texto"])

        def _foco_sair(e):
            if not campo.get():
                campo.insert(0, placeholder)
                campo.config(fg=CORES["texto_suave"])

        campo.bind("<FocusIn>",  _foco_entrar)
        campo.bind("<FocusOut>", _foco_sair)

    return campo


def construir_botao(pai, texto: str, ao_clicar, destaque: bool = False) -> tk.Frame:
    """
    Botão com sombra e hover.
    - destaque=True  → verde-água (ação principal)
    - destaque=False → cinza-ardósia (ação secundária)
    """
    fundo        = CORES["destaque"] if destaque else CORES["primaria"]
    fundo_hover  = "#00796B"         if destaque else "#455A64"
    fundo_sombra = "#00695C"         if destaque else "#263238"

    moldura = tk.Frame(pai, bg=fundo_sombra)
    moldura.pack_propagate(False)
    moldura.config(height=40, width=153)

    btn = tk.Frame(moldura, bg=fundo, cursor="hand2")
    btn.place(x=0, y=0, width=150, height=37)

    rotulo_btn = tk.Label(
        btn, text=texto,
        bg=fundo, fg="#FFFFFF",
        font=FONTES["botao"],
    )
    rotulo_btn.place(relx=0.5, rely=0.5, anchor="center")

    def _entrar(e):
        btn.config(bg=fundo_hover)
        rotulo_btn.config(bg=fundo_hover)

    def _sair(e):
        btn.config(bg=fundo)
        rotulo_btn.config(bg=fundo)

    for w in [btn, rotulo_btn]:
        w.bind("<Enter>",    _entrar)
        w.bind("<Leave>",    _sair)
        w.bind("<Button-1>", lambda e: ao_clicar())

    return moldura


def construir_resultado(pai) -> tk.Label:
    """
    Card de resultado padronizado.
    Atualize com: rotulo.config(text=..., fg=CORES['destaque'|'perigo'])
    """
    card = tk.Frame(
        pai, bg=CORES["superficie"],
        highlightbackground=CORES["borda"],
        highlightthickness=1,
    )
    card.pack(fill="x", pady=(8, 0))

    rotulo = tk.Label(
        card, text="Aguardando…",
        bg=CORES["superficie"], fg=CORES["texto_suave"],
        font=FONTES["resultado"],
        justify="left", anchor="w",
        padx=16, pady=12,
    )
    rotulo.pack(fill="x")

    return rotulo


def divisor(pai) -> tk.Frame:
    """Linha separadora horizontal."""
    linha = tk.Frame(pai, bg=CORES["borda"], height=1)
    linha.pack(fill="x", pady=(12, 0))
    return linha