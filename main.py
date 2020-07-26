from jinja2 import Environment, FileSystemLoader
import pdfkit

import os
try:
    os.mkdir("output")
except FileExistsError:
    pass

env = Environment(loader=FileSystemLoader('templates'))

# pdfkit options
options = {
    'dpi': 365,
    # 'page-size': 'A4',
    'page-width': 88,  # should be in mm
    'page-height': 58,
    'margin-top': '0',
    'margin-right': '0',
    'margin-bottom': '0',
    'margin-left': '0',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'quiet': '',
}


def getColor(num):
    # Cards have different colors, this function determines which card gets which color
    colors = ["#F5F749",  # yellow
              "#FF5E5B",  # red
              "#A833B9",  # purple
              "#44BBA4",  # green
              "#3F88C5"]  # blue
    return colors[num % len(colors)]


file = open("questions.txt")

number = 1
for question in file:

    # Don't generate all cards when debugging
    # if number > 10:
    #     break

    # Remove \n
    if question[-1] == '\n':
        question = question[:-1]

    print("Generating question {}: {}".format(number, question))

    # Html escaping (didn't find a function that could do it)
    question = question.replace("é", "&eacute;") \
                       .replace("ê", "&ecirc;")

    # Render the front
    template = env.get_template('template-front.html')
    output_from_parsed_template = template.render(question=question,
                                                  number=number,
                                                  color=getColor(number))

    # Write out the result
    html_file = "output/question-{}-a.html".format(number)
    with open(html_file, "w+") as f:
        f.write(output_from_parsed_template)

    pdf_file = "output/question-{}-a.pdf".format(number)
    pdfkit.from_url(html_file, pdf_file, options=options)

    # Render the back
    template = env.get_template('template-back.html')
    output_from_parsed_template = template.render(color=getColor(number))

    # Write out the result
    html_file = "output/question-{}-b.html".format(number)
    with open(html_file, "w+") as f:
        f.write(output_from_parsed_template)

    pdf_file = "output/question-{}-b.pdf".format(number)
    pdfkit.from_url(html_file, pdf_file, options=options)

    number += 1

# Merge the pdf's
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

print("Merging questions")

# Call the PdfFileMerger
mergedObjectFront = PdfFileMerger()
mergedObjectBack = PdfFileMerger()
mergedObjectCombined = PdfFileMerger()

# Merge pdf files into a single document
# Loop through all of them and append their pages
for fileNumber in range(1, number):
    mergedObjectFront.append(PdfFileReader('output/question-{}-a.pdf'.format(fileNumber), 'rb'))
    mergedObjectBack.append(PdfFileReader('output/question-{}-b.pdf'.format(fileNumber), 'rb'))

    mergedObjectCombined.append(PdfFileReader('output/question-{}-a.pdf'.format(fileNumber), 'rb'))
    mergedObjectCombined.append(PdfFileReader('output/question-{}-b.pdf'.format(fileNumber), 'rb'))

# Write all the files into a file which is named as shown below
mergedObjectFront.write("output/questions-front.pdf")
mergedObjectBack.write("output/questions-back.pdf")
mergedObjectCombined.write("output/questions-combined.pdf")

print("Rotating pdf")


# Rotate every page (since the site where I'll print the cards must have the portrait version) (printenbind.nl)
def rotate_pdf(input, output):
    pdf_in = open(input, 'rb')
    pdf_reader = PdfFileReader(pdf_in)
    pdf_writer = PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        page.rotateClockwise(90)
        pdf_writer.addPage(page)

    pdf_out = open(output, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()


rotate_pdf("output/questions-front.pdf", "output/questions-front-rotated.pdf")
rotate_pdf("output/questions-back.pdf", "output/questions-back-rotated.pdf")
rotate_pdf("output/questions-combined.pdf", "output/questions-combined-rotated.pdf")

# Cleanup the files
for i in range(1, number):
    os.remove('output/question-{}-a.pdf'.format(i))
    os.remove('output/question-{}-b.pdf'.format(i))