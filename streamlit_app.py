# 1️⃣ Install dependencies
!pip install crewai duckduckgo-search openai fpdf

# 2️⃣ Imports
from crewai import Agent, Task, Crew
from duckduckgo_search import DDGS
from fpdf import FPDF
from getpass import getpass
import os

# 3️⃣ Ask YOU for OpenAI API key (hidden)
api_key = getpass("Enter your OpenAI API key: ")
os.environ["OPENAI_API_KEY"] = api_key

# 4️⃣ Ask USER for product details
product_name = input("Enter the product name: ")
product_category = input("Enter product category (e.g., electronics, clothing): ")

# 5️⃣ DuckDuckGo search function
def search_product(product: str, category: str) -> str:
    results = []
    with DDGS() as ddgs:
        query = f"{product} {category}"
        for r in ddgs.text(query, max_results=5):
            results.append(f"{r['title']} - {r['body']} ({r['href']})")
    return "\n".join(results)

search_results = search_product(product_name, product_category)

# 6️⃣ Create CrewAI agent
research_agent = Agent(
    role="Product Researcher",
    goal=f"Summarize research about '{product_name}' in category '{product_category}'",
    backstory="Expert at researching products online and creating concise, relevant summaries",
    memory=True,
    llm="gpt-4",
    verbose=True
)

# 7️⃣ Create Task
task = Task(
    description=f"Summarize these results:\n{search_results}",
    agent=research_agent,
    expected_output="A concise summary of the product research focused on the correct category."
)

# 8️⃣ Run Crew
crew = Crew(agents=[research_agent], tasks=[task])
print("\nRunning research...\n")
result = crew.kickoff()

# 9️⃣ Extract summary text
result_text = str(result)
print("\n🔍 Research Summary:\n")
print(result_text)

# 🔟 Save summary as PDF
pdf_file = f"{product_name.replace(' ','_')}_summary.pdf"
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, result_text)
pdf.output(pdf_file)
print(f"\n✅ Summary saved as PDF: {pdf_file}")
