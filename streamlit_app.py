
import streamlit as st
import os
from crewai import Agent, Task, Crew
from duckduckgo_search import DDGS
from fpdf import FPDF

st.title("🛠 Product Research AI")
st.write("Enter a product name and category to get a research summary.")

api_key = st.secrets["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = api_key

product_name = st.text_input("Product Name")
product_category = st.text_input("Product Category (e.g., electronics, clothing)")

if st.button("Run Research"):
    if not product_name.strip() or not product_category.strip():
        st.warning("Please enter both product name and category.")
    else:
        results = []
        with DDGS() as ddgs:
            query = f"{product_name} {product_category}"
            for r in ddgs.text(query, max_results=5):
                results.append(f"{r['title']} - {r['body']} ({r['href']})")
        search_results = "\n".join(results)

        research_agent = Agent(
            role="Product Researcher",
            goal=f"Summarize research about '{product_name}' in category '{product_category}'",
            backstory="Expert at researching products online and creating concise, relevant summaries",
            memory=True,
            llm="gpt-4",
            verbose=True
        )

        task = Task(
            description=f"Summarize these results:\n{search_results}",
            agent=research_agent,
            expected_output="A concise summary of the product research focused on the correct category."
        )

        crew = Crew(agents=[research_agent], tasks=[task])
        with st.spinner("Running research..."):
            result = crew.kickoff()

        result_text = str(result)
        st.subheader("🔍 Research Summary")
        st.text_area("Summary", result_text, height=300)

        pdf_file = f"{product_name.replace(' ','_')}_summary.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, result_text)
        pdf.output(pdf_file)

        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=pdf_file)
