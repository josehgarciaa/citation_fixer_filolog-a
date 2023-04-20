import glob
import fitz  # PyMuPDF

filename_list = glob.glob("pdf_documents/rbonillacerezo1*pdf")

for filename in filename_list:

    print("Processing file:", filename)
    # Prepare a variable to store the extracted text
    output_text = ""
    current_ref =1

 #   # Open the PDF file
    doc = fitz.open(filename)

        
    # Loop through each page in the document
    for page_num in range(doc.page_count):
        # Get the current page
        page = doc[page_num]
        page_text = ""
        # read page text as a dictionary, suppressing extra spaces in CJK fonts
        blocks = page.get_text("dict", flags=11)["blocks"]
        for block in blocks:  # iterate through the text blocks
            block_text = ""
            for line in block["lines"]:  # iterate through the text lines
                first_token = line["spans"][0]
                txt_line = ""
                if first_token["size"]> 9.7 and first_token["size"]<= 10.0:                    
                    for token in line["spans"]:
                        txt_line+=token["text"]
                    int_num = None
                    try:
                        int_num = int(first_token["text"].split(" ")[0])
                    except:
                        pass                
                    if int_num == current_ref:
                        current_ref +=1
                        txt_line="\n"+txt_line
                        
                if len(txt_line) !=0:
                    block_text+=txt_line                
                
            if len(block_text)!=0:
                page_text+=block_text

        if len(page_text)!=0:
            output_text += page_text

    with open(filename.replace("pdf","txt"), "w", encoding="utf-8") as output_file:
        output_file.write(output_text)

