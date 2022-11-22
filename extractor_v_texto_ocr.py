# Import libraries
import platform
from tempfile import TemporaryDirectory
from pathlib import Path
 
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
 
if platform.system() == "Windows":
    
    # We may need to do some additional downloading and setup...
    # Windows needs a PyTesseract Download
    # https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine
 
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract"
    )
 
    # Windows also needs poppler_exe
    path_to_poppler_exe = Path(r"C:\Program Files\poppler-0.68.0\bin")
     
    # Put our output files in a sane place...
    out_directory = Path(r"~\Desktop").expanduser()
else:
    out_directory = Path("~").expanduser()    
 
# Path of the Input pdf
PDF_file = Path(r"pdf_pruebas/prueba1.pdf")
 
# Store all the pages of the PDF in a variable
image_file_list = []
 
text_file = out_directory / Path("out_text.txt")
 
def main():
    ''' Main execution point of the program'''
    with TemporaryDirectory() as tempdir:
        # Create a temporary directory to hold our temporary images.
 
        """
        Part #1 : convirtiendo PDF a img
        """
 
        if platform.system() == "Windows":
            pdf_pages = convert_from_path(
                PDF_file, 500, poppler_path=path_to_poppler_exe
            )
        else:
            # Read in the PDF file at 500 DPI
            pdf_pages = convert_from_path(PDF_file, 500)
 
        # Iterate through all the pages stored above
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            # enumerate() "counts" the pages for us.
 
            # Create a file name to store the image
            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
 
            # Declaring filename for each page of PDF as JPG
            # For each page, filename will be:
            # PDF page 1 -> page_001.jpg
            # PDF page 2 -> page_002.jpg
            # PDF page 3 -> page_003.jpg
            # ....
            # PDF page n -> page_00n.jpg
 
            # Save the image of the page in system
            page.save(filename, "JPEG")
            image_file_list.append(filename)
 
        """
        Part #2 - organizando text 
        """
 
        # with open(text_file, "a") as output_file:
        #     # Open the file in append mode so that
        #     # All contents of all images are added to the same file
 
        #     # Iterate from 1 to total number of pages
        #     for image_file in image_file_list:
 
        #         # Set filename to recognize text from
        #         # Again, these files will be:
        #         # page_1.jpg
        #         # page_2.jpg
        #         # ....
        #         # page_n.jpg
 
        #         # Recognize the text as string in image using pytesserct
        #         text = str(((pytesseract.image_to_string(Image.open(image_file)))))
 
            
        #         text = text.replace("-\n", "")
 
        #         # Finally, write the processed text to the file.
        #         output_file.write(text)
     
if __name__ == "__main__":
      # We only want to run this if it's directly executed!
    main()