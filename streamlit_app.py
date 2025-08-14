import streamlit as st
import os
from crewai import Agent, Task, Crew
from duckduckgo_search import ddg
from fpdf import FPDF

# Load API key from secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.title("Product Research AI 🛒")

product_name = "treadmill"

if product_name:
    st.info(f"Running research for '{product_name}'...")

    # Initialize CrewAI agent
    research_agent = Agent(name="Research Agent")
    crew = Crew([research_agent])

    # Search product online
    search_results = ddg(product_name, max_results=5)

    # Summarization task
    task = Task(
        description=f"Summarize these results for the product '{product_name}':\n{search_results}",
        agent=research_agent,
        expected_output="Provide a concise, clear summary with key points."
    )

    # Run agent
    result = crew.run(task)

    # Display summary
    st.subheader("Summary")
    st.write(result)

    # Save summary as PDF
    pdf_file = f"{product_name}_summary.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, str(result))
    pdf.output(pdf_file)
    st.success(f"✅ Summary saved as PDF: {pdf_file}")
