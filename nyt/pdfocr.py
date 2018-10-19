from PIL import Image as PI
import sys
import io
import pyocr
import pyocr.builders
import PyPDF2 
import re

filePath = './test5.pdf'

"""
pdfFileObj = open(filePath, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
print(pdfReader.numPages)
pageObj = pdfReader.getPage(0)
print(pageObj.extractText())

"""
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.


from wand.image import Image as Img
image_pdf = Img(filename=filePath, resolution=300)
image_jpeg = image_pdf.convert('jpeg')


req_image = []
final_text = []


for img in image_jpeg.sequence:
    img_page = Img(image=img)
    req_image.append(img_page.make_blob('jpeg'))

for img in req_image: 
    txt = tool.image_to_string(
        PI.open(io.BytesIO(img)),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    final_text.append(txt)
	
print(final_text)

output_file = open("test.txt", "wb")
for page in final_text:
	output_file.write(page.encode("utf-8"))
output_file.close()

# fetching the date article was published
#match = re.search(r'Published: (\w+)(\s+)(\d+)(\s+),(\s+)(\d+)',final_text[0])
match = re.search(r'Published:(\s*)(\w*)(\s*)(\d*),(\s*)(\d*)',final_text[0])

print(match[0])
print(match[1])
print(match[2])
print(match[4])
print(match[6])
