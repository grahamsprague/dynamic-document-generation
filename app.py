'''
Test
'''


from flask import Flask, render_template, request
import functions

app = Flask(__name__)


@app.route("/generate_previews")
def generate_previews():

    my_templates = functions.f_generate_previews()
    return render_template('index.html', pdf_templates=my_templates)


@app.route("/")
def hello():

    my_templates = functions.f_index()
    return render_template('index.html', pdf_templates=my_templates)


@app.route('/template/<template_name>')
def template_select(template_name):
    # scan template and load dup the form
    my_template = functions.f_template(template_name)
    return render_template('template.html', pdf_template=my_template)

@app.route('/template_form_processor', methods = ['POST'])
def template_form_process():
    # handle form submission

    data = request.form
    download_link = functions.f_template_use(request.form)
    print('download_link:')
    print(download_link)

    return render_template('response.html', my_data=data, link=download_link)

@app.route('/static')
def static_file(path):
    '''
    route for all static files like html, css, js, img, pdf, etc
    '''
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()
