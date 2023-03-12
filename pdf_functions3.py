'''
This file uses the PDF api from https://app.pdf.co
the info to get the api key is just my email address graham.sprague@gmail.com
the accounbt is free, full time access is like 9.99 a month.
'''
import os
import json as json_module
import requests  # pip install requests
from dotenv import load_dotenv

load_dotenv()

# The authentication key (API Key).
# Get your own by registering at https://app.pdf.co
API_KEY = os.getenv('PDFCO_API_KEY')

# Base URL for PDF.co Web API requests
BASE_URL = "https://api.pdf.co/v1"

# Source PDF file
SourceFile = ".\\sample.pdf"
# PDF document password. Leave empty for unprotected documents.
Password = ""
# Destination PDF file name
DestinationFile = ".\\result.pdf"


def main(args=None):
    uploadedFileUrl = uploadFile(SourceFile)
    if (uploadedFileUrl != None):
        replaceStringFromPdf(uploadedFileUrl, DestinationFile)


def replaceStringFromPdf(uploadedFileUrl, destinationFile, searchStrings, replacementStrings):
    """Replace Text FROM UPLOADED PDF FILE using PDF.co Web API"""



    # Prepare requests params as JSON
    # See documentation: https://apidocs.pdf.co
    parameters = {
        "name": os.path.basename(destinationFile),
        "password": Password,
        "url": uploadedFileUrl,
        "searchStrings": searchStrings,
        "replaceStrings": replacementStrings
    }

    parameters_json = json_module.dumps(parameters)

    print(parameters_json)



    # Prepare URL for 'Replace Text from PDF' API request
    url = "{}/pdf/edit/replace-text".format(BASE_URL)

    # Execute request and get response as JSON
    response = requests.post(url, data=parameters_json, headers={"x-api-key": API_KEY})
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            #  Get URL of result file
            resultFileUrl = json["url"]
            # Download result file
            r = requests.get(resultFileUrl, stream=True)
            if (r.status_code == 200):
                with open(destinationFile, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destinationFile}\" file.")
                return destinationFile
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            # Show service reported error
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")


def uploadFile(fileName):
    """Uploads file to the cloud"""

    print('key')
    print(API_KEY)

    # 1. RETRIEVE PRESIGNED URL TO UPLOAD FILE.

    # Prepare URL for 'Get Presigned URL' API request
    url = "{}/file/upload/get-presigned-url?contenttype=application/octet-stream&name={}".format(
        BASE_URL, os.path.basename(fileName))

    # Execute request and get response as JSON
    response = requests.get(url, headers={"x-api-key": API_KEY})
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            # URL to use for file upload
            uploadUrl = json["presignedUrl"]
            # URL for future reference
            uploadedFileUrl = json["url"]

            # 2. UPLOAD FILE TO CLOUD.
            with open(fileName, 'rb') as file:
                requests.put(uploadUrl, data=file,
                             headers={"x-api-key": API_KEY, "content-type": "application/octet-stream"})

            return uploadedFileUrl
        else:
            # Show service reported error
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None


if __name__ == '__main__':
    main()

