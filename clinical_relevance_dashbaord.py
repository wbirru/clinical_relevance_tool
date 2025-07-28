import streamlit as st
import pandas as pd
import datetime
import urllib.parse

st.set_page_config(page_title="Clinical Relevance Tools Dashboard", layout="wide")
st.title("💊 Clinical Relevance Tools Dashboard")

# Current date and memory/context note
current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
st.markdown(f"**📅 Date:** {current_date}")
st.info("""
This platform integrates genomic and therapeutic data, focusing on drug-gene interactions and dynamic data visualizations.
It uses tools such as DGIdb, DisGeNET, Open Targets Platform, and PharmGKB,
emphasizing user-friendly interfaces and transparent data sources.
Developed for advanced genomic analysis and related applications.
""")

# --- Sidebar ---
st.sidebar.header("Enter Gene Symbols")
default_genes = "FSHR, LHCGR, CYP19A1, ESR1, INHBA, GNRHR"
genes_input = st.sidebar.text_area("Gene list (comma-separated):", value=default_genes)
genes = [g.strip() for g in genes_input.split(",") if g.strip()]
run_button = st.sidebar.button("🚀 Run Clinical Search")

# === Clinical Tools Output ===
if run_button and genes:
    # DGIdb
    st.subheader("1️⃣ DGIdb (Drug–Gene Interaction Database)")
    st.markdown("""
    **Summary:**  
    Find known and putative drug–gene interactions for therapy mapping, clinical repurposing, and evidence synthesis.  
    **API/Automation:** ❌ (API not available for programmatic queries; web interface only)
    """)
    st.markdown("**Explore interactions for each gene individually:**")
    for g in genes:
        dg_url = f"https://dgidb.org/results?searchType=gene&searchTerms={urllib.parse.quote(g)}"
        st.markdown(f"- [{g} on DGIdb]({dg_url})")
    st.info("Use the DGIdb web search to see drug–gene records, evidence, sources, and interaction types.")

    # Open Targets Platform
    st.subheader("3️⃣ Open Targets Platform (Multi-Evidence Gene–Disease–Drug)")
    st.markdown("""
    **Summary:**  
    Integrates genetic, chemical, and clinical evidence for target-disease-drug associations, including burden/safety scores, tractability, and variant data.  
    **API/Automation:** ✅ (powerful GraphQL/REST API, batch result export)
    """)
    for g in genes:
        ot_url = f"https://platform.opentargets.org/search?q={urllib.parse.quote(g)}&page=1"
        st.markdown(f"- [{g} search on Open Targets]({ot_url})")
    st.info("Browse each gene for interactive overview of associated drugs, diseases, evidence, and variant landscapes.")

    # PharmGKB
    st.subheader("4️⃣ PharmGKB (Pharmacogenomics Knowledge Base)")
    st.markdown("""
    **Summary:**  
    Standardized clinical pharmacogenomics annotations, variant-drug relationships, and dosing guidelines.  
    **API/Automation:** ❌ Web and FTP downloads; search interface only for most users.
    """)
    for g in genes:
        pkb_url = "https://www.pharmgkb.org/search?query=" + urllib.parse.quote(g)
        st.markdown(f"- [{g} in PharmGKB]({pkb_url})")
    st.info("View gene-level PGx summaries, clinical significance of variants, and guideline interpretations.")

# --- Evaluation Table ---
st.markdown("---")
st.subheader("📊 Clinical Tools Evaluation Matrix")

criteria = {
    "🧬 Biological Context": "Pathway, disease/process relevance covering FSH, endocrine, or broad clinical genomics",
    "🔄 Network Connectivity": "Drug/variant/phenotype network depth and evidence links",
    "💊 Clinical Utility": "Direct evidence for therapy, diagnosis, pharmacogenomics",
    "🤖 AI-readiness": "Structured output, data mining/ML compatibility",
    "🛠 Interoperability": "API, web, and export features",
    "🧑‍⚕️ Clinical Explainability": "Ease of clinician use and interpretation",
    "🎯 Visual Insight": "Interactive, clear, and printable views"
}
default_scores = {
    "DGIdb": [1, 1, 5, 5, 5, 5, 2],
    "DisGeNET": [2, 2, 5, 5, 5, 4, 2],
    "Open Targets": [3, 2, 5, 5, 5, 5, 4],
    "PharmGKB": [3, 2, 5, 4, 4, 5, 3]
}
df_eval = pd.DataFrame(default_scores, index=criteria.keys()).T

for tool in df_eval.index:
    with st.expander(f"🔧 Adjust {tool} scores"):
        for crit in criteria:
            df_eval.loc[tool, crit] = st.slider(
                f"{crit}",
                min_value=1, max_value=5,
                value=int(df_eval.loc[tool, crit]),
                help=criteria[crit],
                key=f"{tool}-{crit}"
            )
df_eval["Total Score"] = df_eval[list(criteria.keys())].sum(axis=1)
st.dataframe(df_eval.astype(int))
st.download_button("⬇️ Download Evaluation Matrix", df_eval.to_csv(), "clinical_relevance_evaluation.csv")
