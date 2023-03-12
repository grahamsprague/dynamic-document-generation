#!chapter_007/src/snippet_013.py
from borb.pdf import Document
from borb.pdf import PDF
from borb.toolkit import SimpleFindReplace

import typing


def borb_pdf_replace(in_file, replacements):

    # attempt to read a PDF
    doc: typing.Optional[Document] = None
    with open('./static/pdf_templates/' + in_file + '.pdf', "rb") as pdf_file_handle:
        doc = PDF.loads(pdf_file_handle)

    # check whether we actually read a PDF
    assert doc is not None

    # find/replace
    for my_key in replacements:
        doc = SimpleFindReplace.sub('[['+my_key+']]', replacements[my_key], doc)

    # store
    with open( './static/pdf_generated/' + in_file + '_out.pdf', "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

    return './static/pdf_generated/' + in_file + '_out.pdf'






def main():

    # attempt to read a PDF
    doc: typing.Optional[Document] = None
    with open("output.pdf", "rb") as pdf_file_handle:
        doc = PDF.loads(pdf_file_handle)

    # check whether we actually read a PDF
    assert doc is not None

    # find/replace
    doc = SimpleFindReplace.sub("Jots", "Joris", doc)

    # store
    with open("output2.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)


if __name__ == "__main__":
    main()
