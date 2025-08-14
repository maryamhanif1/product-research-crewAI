
import os
import streamlit as st
from crewai import Agent, Task, Crew
from duckduckgo_search import DDGS
from fpdf import FPDF

# Use OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")

st.title("Product Research with CrewAI")

# Ask user for product name
product_name = st.text_input("Enter a product name to research:")

if product_name:
    st.write(f"🔍 Searching for product: {product_name}")
    
    # 1️⃣ Run DuckDuckGo search
    with DDGS() as ddgs:
        results = ddgs.text(product_name, max_results=5)
    
    st.write("### Search Results")
    for i, r in enumerate(results, 1):
        st.write(f"{i}. {r['title']} - {r['href']}")
    
    # 2️⃣ Create a simple summary using CrewAI agent
    agent = Agent(name="research_agent")
    task = Task(
        description=f"Summarize these results for the product '{product_name}': {results}",
        agent=agent,
        expected_output="Provide a concise summary of findings."
    )
    output = Crew.run(task)
    
    st.write("### Summary")
    st.write(output)

    # 3️⃣ Save summary as PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, str(output))
    pdf_file = f"{product_name}_summary.pdf"
    pdf.output(pdf_file)
    
    st.success(f"✅ Summary saved as PDF: {pdf_file}")
