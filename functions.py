import os
import fitz
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject
import pdf_functions3
import re
import json


def f_generate_previews():
    # read the directory and get the template files
    template_list = os.listdir('static/pdf_templates/')
    my_templates = [];

    print(template_list)

    # To get better resolution
    zoom_x = 2.0  # horizontal zoom
    zoom_y = 2.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

    for my_template in template_list:
        if not my_template == '.DS_Store':
            # get filename pieces
            my_template_parts = os.path.splitext(my_template)
            filename = 'static/pdf_templates/' + my_template  # name of pdf file you want to render
            doc = fitz.open(filename)
            counter = 0
            for page in doc:
                counter += 1
                pix = page.get_pixmap(matrix=mat)  # render page to an image
                my_template_preview = my_template_parts[0] + '[' + str(counter) + ']' + '.png'
                pix.save('static/pdf_previews/' + my_template_preview)  # store image as a PNG

            # capture just the first image for preview
            my_templates.append(
                {'name': my_template_parts[0], 'filename': my_template, 'preview': my_template_parts[0] + '[1]' + '.png'})

    return my_templates


def f_index():
    # read the directory and get the template files
    template_list = os.listdir('static/pdf_templates/')
    preview_list = os.listdir('static/pdf_previews/')
    my_templates = [];

    # To get better resolution
    zoom_x = 2.0  # horizontal zoom
    zoom_y = 2.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

    for my_template in template_list:
        # get filename pieces
        my_template_parts = os.path.splitext(my_template)

        # make a list of the previews
        my_previews = []
        for my_preview in preview_list:
            my_preview_parts = os.path.splitext(my_preview)
            if my_preview_parts[0] == my_template_parts[0]:
                my_previews.append(my_preview)
        # capture just the previews
        my_templates.append(
            {'name': my_template_parts[0], 'filename': my_template, 'preview': my_template_parts[0] + '[1]' + '.png',
             'previews': my_previews})

    return my_templates


def f_template(template_name):
    # get previews for this template
    my_previews = []
    preview_list = os.listdir('static/pdf_previews/')
    for my_preview in preview_list:
        my_preview_parts = my_preview.split('[')
        if my_preview_parts[0] == template_name:
            my_previews.append(my_preview)

    my_previews.sort()
    my_fields = f_scan_template(template_name + '.pdf')
    my_template = {
            'name': template_name,
            'filename': template_name + '.pdf',
            'previews': my_previews,
            'fields': my_fields
    }

    return my_template


def f_scan_template(template_name):

    in_file = './static/pdf_templates/' + template_name
    pdf = PdfReader(in_file)
    matches = []
    for page_number in range(0, len(pdf.pages) ):
        page = pdf.pages[page_number]
        contents = page.extract_text()
        lines = contents.splitlines()
        for line in lines:
            # print(line)
            pattern = '\[\[.+\]\]'
            found = re.findall(pattern, line)
            found = [sub.replace('[', '') for sub in found]
            found = [sub.replace(']', '') for sub in found]
            matches.extend(found)

    # de-dupe
    matches = list(dict.fromkeys(matches))
    # print(matches)

    return matches

def f_template_use(data):

    print(data)
    # print(data['name'])
    # print(data['email_address'])
    # print(data['template'])

    my_fields = f_scan_template(data['template'] + '.pdf')

    print(my_fields)

    search_strings = []
    replacement_strings = []

    for my_field in my_fields:
        if data[my_field]:
            search_strings.extend(['[['+my_field+']]'])
            replacement_strings.extend([data[my_field]])

    print(search_strings)
    print(replacement_strings)

    my_source_file = './static/pdf_templates/' + data['template'] + '.pdf'
    my_destination_file = './static/pdf_generated/' + data['template'] + '_out.pdf'

    uploaded_file = None
    generated_file = None

    uploaded_file = pdf_functions3.uploadFile(my_source_file)
    if uploaded_file is not None:

        generated_file = pdf_functions3.replaceStringFromPdf(uploaded_file, my_destination_file, search_strings, replacement_strings)
        if generated_file is not None:
            print(generated_file)
            return generated_file
        else:
            print('error requesting replacement')
    else:
        print('error uploading')
    return None