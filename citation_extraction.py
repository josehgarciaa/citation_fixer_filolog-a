import glob
import fitz  # PyMuPDF



def flags_decomposer(flags):
    """Make font flags human readable."""
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)




filename_list = glob.glob("pdf_documents/rbonillacerezo1*pdf")

current_ref =1 
for filename in filename_list:
    print("Processing file:", filename)

 #   # Open the PDF file
    doc = fitz.open(filename)

    # Prepare a variable to store the extracted text
    output_text = ""
        
    # Loop through each page in the document
    for page_num in range(doc.page_count):
        # Get the current page
        page = doc[page_num]
            
        # read page text as a dictionary, suppressing extra spaces in CJK fonts
        blocks = page.get_text("dict", flags=11)["blocks"]
        for block in blocks:  # iterate through the text blocks
            reference_in_block = ""
            for line in block["lines"]:  # iterate through the text lines
                reference_in_line = ""
                start_reference = False

                line_text = ""
                for s in line["spans"]:  # iterate through the text spans
                    font_properties = "Font: '%s' (%s), size %g, color #%06x" % (
                        s["font"],  # font name
                        flags_decomposer(s["flags"]),  # readable font flags
                       s["size"],  # font size
                        s["color"],  # font color
                    )
                    fontsize = s["size"] 
                    span_text = s["text"]
                    if (fontsize ==10 ):
                        line_text+=span_text
                try:
                    potential_ref_num = int(line_text.split(" ")[0])
                    if potential_ref_num ==current_ref:
                        current_ref+=1
                        line_text="\n\n"+line_text
                except:
                    pass
                reference_in_line+=line_text

                reference_in_block+=reference_in_line
                     
        if len(reference_in_block)!=0:
            output_text += f"Page {page_num + 1}:\n"+reference_in_block+"\n"
    with open(filename.replace(".pdf",".txt"), "w", encoding="utf-8") as output_file:
        output_file.write(output_text)

