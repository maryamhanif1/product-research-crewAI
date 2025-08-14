
import streamlit as st
from fpdf import FPDF

st.title("🛠 Product Research AI")

product_name = st.text_input("Enter product name")
if st.button("Run Research"):
    result = """Through the research conducted, several insights into the iPhone 16, iPhone 16 Pro, and iPhone 16 Pro Max were highlighted. The differences between the iPhone 16 Pro and iPhone 16 Pro Max are minimal, and it is suggested to disregard the distinctions in battery life, as the iPhone 16 Pro's battery life is already sufficient for daily use. 

Information on the setup process for iPhone 16's Lingdong Island feature within settings was also provided, but the complete setup steps were not provided in the snippets. 

In terms of user experience, it has been two months since the launch of the iPhone 16 series, and with large-scale price drops during promotional sale periods, it is considered a good time to purchase. However, further details on the user experience, whether it's worth buying, and which model is more worth buying were not found in the snippets.

For the iPhone 16 Pro Max, it is noted that performance improvement wasn't just due to chipset changes, but the series also introduced a graphite layer aluminum substructure to aid heat dissipation, and the iPhone 16 Pro series has increased its sustained performance output by 20% compared to its predecessor.

As for the differences between the iPhone 16 and 16 Pro, the suggestion is to outline the core differences and choose the model that better meets individual needs and expectations. However, specific points of differentiation were not given in the snippets provided."""
    st.subheader("🔍 Research Summary")
    st.text_area("Summary", result, height=300)
    pdf_file = f"iphone_16_summary.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, result)
    pdf.output(pdf_file)
    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download PDF", f, file_name=pdf_file)
