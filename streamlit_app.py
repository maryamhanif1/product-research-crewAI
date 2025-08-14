
import streamlit as st
from crewai import Agent, Task, Crew
from duckduckgo_search import ddg
from fpdf import FPDF
import os

# Get OpenAI API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = api_key

st.title("Product Research AI")

# Ask user for product name
product_name = st.text_input("Enter the product name:")

if product_name:
    st.write(f"Searching for: {product_name}")
    
    # Run DuckDuckGo search (top 5 results)
    search_results = ddg(product_name, max_results=5)
    
    # Initialize CrewAI in-memory (avoids ChromaDB)
    crew = Crew(in_memory=True)
    research_agent = Agent(name="ResearchAgent", crew=crew)

    # Create a task to summarize results
    task = Task(
        description=f"Summarize these results concisely:\n{search_results}",
        agent=research_agent,
        expected_output="A clear, concise summary of the product search results."
    )

    result = task.run()

    st.subheader("Summary:")
    st.write(result)

    # Save summary as PDF
    pdf_file = f"{product_name.replace(' ', '_')}_summary.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, result)
    pdf.output(pdf_file)
    
    st.success(f"✅ Summary saved as PDF: {pdf_file}")
    st.download_button("Download PDF", data=open(pdf_file, "rb"), file_name=pdf_file)
