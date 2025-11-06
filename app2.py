import streamlit as st
import pandas as pd


def format_currency(value):
    """Formata valor como moeda brasileira"""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Calculadora de Markup + Break-even", page_icon="💹", layout="wide")

st.title("💹 Calculadora de Markup e Ponto de Equilíbrio")
st.write("Simule seus custos, margens e descubra o volume mínimo de vendas necessário para cobrir seus custos fixos.")

# ======================================================
# SEÇÃO 1 — CÁLCULO DE MARKUP
# ======================================================
st.header("🧾 Parte 1 — Cálculo do Markup e Preço de Venda")

col1, col2, col3 = st.columns(3)
with col1:
    materia_prima = st.number_input("Matéria-prima (R$)", min_value=0.0, step=0.01)
    embalagem = st.number_input("Embalagem (R$)", min_value=0.0, step=0.01)
with col2:
    frete_compra = st.number_input("Frete de Compra (R$)", min_value=0.0, step=0.01)
    outros_custos = st.number_input("Outros Custos Diretos (R$)", min_value=0.0, step=0.01)
with col3:
    quantidade_unidades = st.number_input("Quantidade Produzida", min_value=1, step=1, value=1)

st.subheader("📈 Índices de Despesas e Lucro (em %)")

col4, col5, col6, col7 = st.columns(4)
with col4:
    desp_fixas = st.number_input("Despesas Fixas (%)", min_value=0.0, step=0.1)
with col5:
    desp_comerciais = st.number_input("Despesas Comerciais (%)", min_value=0.0, step=0.1)
with col6:
    impostos = st.number_input("Impostos (%)", min_value=0.0, step=0.1)
with col7:
    lucro_desejado = st.number_input("Lucro Desejado (%)", min_value=0.0, step=0.1)


st.header("📊 Parte 2 — Cálculo do Ponto de Equilíbrio (Break-even Point)")
st.write("Informe seus custos fixos totais para calcular o ponto de equilíbrio em unidades e em valor de venda.")

custo_fixo_total = st.number_input("Custos Fixos Totais (R$)", min_value=0.0, step=100.0)

# ======================================================
# BOTÃO DE CÁLCULO DO MARKUP
# ======================================================
if st.button("Calcular Markup e Preço de Venda"):
    cmv_unitario = materia_prima + embalagem + frete_compra + outros_custos
    cmv_total = cmv_unitario * quantidade_unidades

    soma_indices = desp_fixas + desp_comerciais + impostos + lucro_desejado

    if soma_indices >= 100:
        st.error("❌ A soma dos índices não pode ser igual ou superior a 100%.")
    else:
        fator_markup = 1 / (1 - (soma_indices / 100))
        preco_venda_unit = cmv_unitario * fator_markup
        preco_venda_total = preco_venda_unit * quantidade_unidades

        st.success("✅ Cálculo de Markup concluído!")

        colA, colB, colC = st.columns(3)
        with colA:
            st.metric("CMV Unitário (R$)", f"{format_currency(cmv_unitario)}")
        with colB:
            st.metric("Fator de Markup", f"{fator_markup:,.3f}")
        with colC:
            st.metric("Preço de Venda Unitário (R$)", f"{format_currency(preco_venda_unit)}")

        st.dataframe(
            pd.DataFrame({
                "Item": ["Despesas Fixas", "Despesas Comerciais", "Impostos", "Lucro Desejado"],
                "Percentual (%)": [desp_fixas, desp_comerciais, impostos, lucro_desejado]
            }),
            hide_index=True, use_container_width=True
        )

        st.write(f"**Preço Total de Venda (R$):** {format_currency(preco_venda_total)}")

    # ======================================================
    # SEÇÃO 2 — CÁLCULO DO BREAK-EVEN POINT
    # ======================================================
    if custo_fixo_total > 0:
        margem_contribuicao_unit = round(preco_venda_unit,2) - cmv_unitario
        if margem_contribuicao_unit <= 0:
            st.error("❌ Margem de contribuição negativa ou zero. Verifique os dados de custo e preço.")
        else:
            margem_contribuicao_perc = (margem_contribuicao_unit / preco_venda_unit) * 100
            ponto_equilibrio_unid = custo_fixo_total / margem_contribuicao_unit
            ponto_equilibrio_valor = int(ponto_equilibrio_unid) * round(preco_venda_unit,2)

            st.success("✅ Cálculo do ponto de equilíbrio realizado com sucesso!")

            colD, colE, colF = st.columns(3)
            with colD:
                st.metric("Margem de Contribuição Unitária (R$)", f"{format_currency(margem_contribuicao_unit)}")
            with colE:
                st.metric("Margem de Contribuição (%)", f"{round(margem_contribuicao_perc,2)}%")
            with colF:
                st.metric("Ponto de Equilíbrio (Unidades)", f"{int(ponto_equilibrio_unid)}")

            st.write(f"**Ponto de Equilíbrio (R$):** R$ {format_currency(ponto_equilibrio_valor)}")
    else:
        st.info("👉 Informe o valor dos custos fixos totais para calcular o ponto de equilíbrio.")
