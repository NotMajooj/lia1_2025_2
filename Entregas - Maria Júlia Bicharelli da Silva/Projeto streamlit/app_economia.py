import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
from passlib.context import CryptContext

# --- Configurações Iniciais ---
DATASET_DIR = "datasets"

# Categorias para Pessoa Física
CATEGORIAS_GANHO_PESSOA = ["Salário", "Freelance", "Investimentos", "Presente", "Outro"]
CATEGORIAS_GASTO_PESSOA = ["Moradia", "Alimentação", "Transporte", "Lazer", "Saúde", "Educação", "Assinaturas", "Compras", "Outro"]

# Categorias para Empresa (Pessoa Jurídica)
CATEGORIAS_GANHO_EMPRESA = ["Venda de Produtos", "Prestação de Serviço", "Juros/Rendimentos", "Outro"]
CATEGORIAS_GASTO_EMPRESA = ["Salários/RH", "Fornecedores", "Marketing/Vendas", "Infraestrutura", "Impostos", "Despesas Operacionais", "Outro"]

# Configuração de segurança para senhas
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- Funções de Backend ---

def inicializar_sistema():
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)

def path_user_csv(username: str) -> str:
    return os.path.join(DATASET_DIR, f"{username}.csv")

def path_user_pass(username: str) -> str:
    return os.path.join(DATASET_DIR, f"{username}_senha.txt")

def usuario_existe(username: str) -> bool:
    return os.path.exists(path_user_csv(username)) and os.path.exists(path_user_pass(username))

def criar_usuario_backend(username: str, password: str):
    hashed_password = pwd_context.hash(password)
    with open(path_user_pass(username), "w", encoding="utf-8") as f:
        f.write(hashed_password)
    
    if not os.path.exists(path_user_csv(username)):
        df = pd.DataFrame(columns=["data", "tipo", "categoria", "descricao", "valor"])
        df.to_csv(path_user_csv(username), index=False)

def verificar_senha(username: str, password: str) -> bool:
    try:
        with open(path_user_pass(username), "r", encoding="utf-8") as f:
            stored_hash = f.read().strip()
            if not stored_hash: return False
            return pwd_context.verify(password, stored_hash)
    except FileNotFoundError:
        return False

def carregar_dataframe_usuario(username: str) -> pd.DataFrame:
    p = path_user_csv(username)
    if not os.path.exists(p):
        return pd.DataFrame(columns=["data", "tipo", "categoria", "descricao", "valor"])
    
    df = pd.read_csv(p)
    
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors='coerce')
        df.dropna(subset=['data'], inplace=True)
    return df

def salvar_dataframe_usuario(username: str, df: pd.DataFrame):
    df_copy = df.copy()
    if "data" in df_copy.columns:
        df_copy["data"] = pd.to_datetime(df_copy["data"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_copy.to_csv(path_user_csv(username), index=False)

# --- Funções de Lógica Financeira ---

def adicionar_transacao(username: str, tipo: str, categoria: str, descricao: str, valor: float, data=None):
    df = carregar_dataframe_usuario(username)
    if data is None: data = datetime.now()
    nova_linha = pd.DataFrame([[data, tipo, categoria, descricao, valor]], columns=df.columns)
    df = pd.concat([df, nova_linha], ignore_index=True)
    salvar_dataframe_usuario(username, df)

def resumo_usuario(df: pd.DataFrame):
    if df.empty: return {"ganhos": 0.0, "gastos": 0.0, "saldo": 0.0}
    ganhos = df[df["tipo"] == "ganho"]["valor"].sum()
    gastos = df[df["tipo"] == "gasto"]["valor"].sum()
    return {"ganhos": float(ganhos), "gastos": float(gastos), "saldo": float(ganhos - gastos)}

def plot_transacoes(df: pd.DataFrame, username: str):
    if df.empty: st.info("Nenhuma transação no período para gerar o gráfico."); return
    df_plot = df.copy()
    df_plot["date_day"] = pd.to_datetime(df_plot["data"]).dt.date
    ganhos_agg = df_plot[df_plot["tipo"] == "ganho"].groupby("date_day")["valor"].sum()
    gastos_agg = df_plot[df_plot["tipo"] == "gasto"].groupby("date_day")["valor"].sum()
    dates = sorted(list(set(ganhos_agg.index) | set(gastos_agg.index)))
    if not dates: st.info("Nenhuma transação no período."); return
    ganhos_vals = [ganhos_agg.get(d, 0) for d in dates]
    gastos_vals = [gastos_agg.get(d, 0) for d in dates]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(dates, ganhos_vals, color="blue", label="Ganhos")
    ax.bar(dates, [-v for v in gastos_vals], color="red", label="Gastos")
    ax.axhline(0, color="black", linewidth=0.8); ax.set_title(f"Fluxo de Caixa — {username}"); ax.set_ylabel("Valor (R$)"); ax.legend(); plt.xticks(rotation=45); plt.tight_layout(); st.pyplot(fig)

def plot_gastos_por_categoria(df: pd.DataFrame):
    df_gastos = df[df["tipo"] == "gasto"]
    if df_gastos.empty: st.info("Nenhum gasto registrado no período para exibir o gráfico."); return
    gastos_por_categoria = df_gastos.groupby("categoria")["valor"].sum()
    fig, ax = plt.subplots(figsize=(8, 5)); ax.pie(gastos_por_categoria, labels=gastos_por_categoria.index, autopct='%1.1f%%', startangle=90); ax.axis('equal'); ax.set_title("Distribuição de Gastos por Categoria"); st.pyplot(fig)

def sugerir_cortes(username: str, meta_valor: float, meta_prazo_meses: int):
    df = carregar_dataframe_usuario(username)
    df_gastos = df[df["tipo"] == "gasto"].copy()
    if df_gastos.empty: return {"ok": False, "mensagem": "Nenhum gasto registrado para analisar."}
    economia_mensal = meta_valor / max(1, meta_prazo_meses)
    agrup = df_gastos.groupby("categoria").agg(total=("valor","sum"), freq=("valor","count")).sort_values("total",ascending=False)
    soma_gastos = agrup["total"].sum()
    if soma_gastos <= 0: return {"ok": False, "mensagem": "Gastos totais inválidos."}
    suggestions=[]
    for cat,row in agrup.head(5).iterrows():
        share=row["total"]/soma_gastos
        valor_corte_ideal = economia_mensal*share
        percentual = min(0.5, valor_corte_ideal/row["total"]) if row["total"]>0 else 0
        suggestions.append({"categoria": cat, "total_gasto": float(row["total"]), "sugestao_percentual": round(percentual*100,1), "economia_mensal_estimada": round(percentual*row["total"],2)})
    soma_estimativa=sum(s["economia_mensal_estimada"] for s in suggestions)
    return {"ok": True, "economia_mensal_necessaria": round(economia_mensal,2), "soma_estimativa": round(soma_estimativa,2), "suggestions": suggestions}

# --- Interface Streamlit ---
st.set_page_config(page_title="SmartSaver+", layout="wide")
inicializar_sistema()

if "username" not in st.session_state:
    st.session_state.username = None

# --- Tela de Login / Acesso ---
if not st.session_state.username:
    st.title("SmartSaver+ — Assistente Financeiro")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header("Acesso")
        mode = st.radio("Entrar ou Criar", ("Entrar", "Criar novo usuário"), key="login_mode")
        
        if mode == "Criar novo usuário":
            with st.form("form_create_user"):
                new_user = st.text_input("Nome de usuário").strip()
                new_pass = st.text_input("Senha", type="password")
                if st.form_submit_button("Criar conta"):
                    if not new_user or not new_pass: st.error("Preencha nome e senha.")
                    elif usuario_existe(new_user): st.error("Usuário já existe.")
                    else: criar_usuario_backend(new_user, new_pass); st.success(f"Usuário '{new_user}' criado! Faça login.")
        else: # modo == "Entrar"
            with st.form("form_login"):
                user = st.text_input("Usuário").strip()
                pwd = st.text_input("Senha", type="password")
                if st.form_submit_button("Entrar"):
                    if not usuario_existe(user): st.error("Usuário não encontrado.")
                    elif verificar_senha(user, pwd): st.session_state.username = user; st.rerun()
                    else: st.error("Senha incorreta.")

        st.markdown("---")
        st.header("Carregar Dados de Teste")
        st.write("Use para criar ou resetar usuários de teste.")

        if st.button("Carregar dados de 'pessoa'"):
            path_pessoa_ex = os.path.join(DATASET_DIR, "pessoa_exemplo.csv")
            if os.path.exists(path_pessoa_ex):
                criar_usuario_backend("pessoa", "pessoa123")
                df_ex = pd.read_csv(path_pessoa_ex)
                salvar_dataframe_usuario("pessoa", df_ex)
                st.success("Usuário 'pessoa' (senha: pessoa123) carregado/resetado com sucesso!")
            else: st.error("Arquivo 'pessoa_exemplo.csv' não encontrado. Rode o script 'gerar_datasets.py'.")

        if st.button("Carregar dados de 'empresa'"):
            path_empresa_ex = os.path.join(DATASET_DIR, "empresa_exemplo.csv")
            if os.path.exists(path_empresa_ex):
                criar_usuario_backend("empresa", "empresa123")
                df_ex = pd.read_csv(path_empresa_ex)
                salvar_dataframe_usuario("empresa", df_ex)
                st.success("Usuário 'empresa' (senha: empresa123) carregado/resetado com sucesso!")
            else: st.error(f"Arquivo 'empresa_exemplo.csv' não encontrado. Rode o script 'gerar_datasets.py'.")
                
    with col2:
        st.write("## Bem-vindo ao seu assistente financeiro pessoal!"); st.write("Controle ganhos e gastos, defina metas e receba sugestões para economizar.")

# --- Área Principal (após login) ---
else:
    username = st.session_state.username
    st.sidebar.header(f"Olá, {username}!")
    option = st.sidebar.radio("Menu", ("Resumo Financeiro", "Registrar Transação", "Metas e Sugestões"))
    if st.sidebar.button("Sair"): st.session_state.username = None; st.rerun()

    # --- LÓGICA PARA ESCOLHER AS CATEGORIAS CERTAS ---
    if username == 'empresa':
        categorias_gasto_atuais = CATEGORIAS_GASTO_EMPRESA
        categorias_ganho_atuais = CATEGORIAS_GANHO_EMPRESA
    else: # Padrão para 'pessoa' e qualquer outro usuário
        categorias_gasto_atuais = CATEGORIAS_GASTO_PESSOA
        categorias_ganho_atuais = CATEGORIAS_GANHO_PESSOA

    if option == "Resumo Financeiro":
        st.header("Resumo Financeiro"); df_full = carregar_dataframe_usuario(username)
        col1, col2 = st.columns(2); today = datetime.now().date(); default_start_date = today.replace(year=today.year - 1)
        start_date = col1.date_input("Data de Início", default_start_date); end_date = col2.date_input("Data Final", today)
        if not df_full.empty: df_filtered = df_full[(df_full["data"].dt.date >= start_date) & (df_full["data"].dt.date <= end_date)].copy()
        else: df_filtered = df_full
        resumo = resumo_usuario(df_filtered); m1, m2, m3 = st.columns(3); m1.metric("Ganhos", f"R$ {resumo['ganhos']:.2f}"); m2.metric("Gastos", f"R$ {resumo['gastos']:.2f}"); m3.metric("Saldo", f"R$ {resumo['saldo']:.2f}", delta=f"{resumo['saldo']:.2f}")
        st.subheader("Fluxo de Caixa"); plot_transacoes(df_filtered, username)
        st.subheader("Gastos por Categoria"); plot_gastos_por_categoria(df_filtered)
        st.subheader("Transações no Período"); st.dataframe(df_filtered.sort_values("data", ascending=False).reset_index(drop=True))

    elif option == "Registrar Transação":
        st.header("Registrar Nova Transação")
        with st.form("form_transacao", clear_on_submit=True):
            tipo_op = st.selectbox("Tipo", ("gasto", "ganho"))
            categoria = st.selectbox("Categoria", categorias_gasto_atuais if tipo_op == "gasto" else categorias_ganho_atuais)
            descricao = st.text_input("Descrição (opcional)").strip()
            valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
            if st.form_submit_button("Registrar"):
                adicionar_transacao(username, tipo_op, categoria, descricao, float(valor))
                st.success("Transação registrada!")

    elif option == "Metas e Sugestões":
        st.header("Defina uma Meta de Economia")
        with st.form("form_metas"):
            meta_valor = st.number_input("Valor (R$)", min_value=1.0, format="%.2f")
            meta_prazo = st.number_input("Prazo em meses", min_value=1, step=1)
            if st.form_submit_button("Calcular Sugestões"):
                resultado = sugerir_cortes(username, meta_valor, int(meta_prazo))
                if not resultado["ok"]: st.warning(resultado.get("mensagem", "Erro"))
                else:
                    st.success(f"Economia mensal necessária: R$ {resultado['economia_mensal_necessaria']:.2f}")
                    st.info(f"Soma estimada de economia: R$ {resultado['soma_estimativa']:.2f}")
                    st.subheader("Sugestões"); st.dataframe(pd.DataFrame(resultado["suggestions"]))
