
import os
from flask import Blueprint, Flask, render_template, send_file, request, url_for, redirect, Response, make_response
from werkzeug import secure_filename
import pandas as pd
import logging
from tool1 import tool1
from tool2 import tool2


_log = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('upload.html', genes_in_HPO=3777)


@app.route('/help')
def help():
   return render_template('help.html', genes_in_HPO=3777)


@app.route('/reference')
def reference():
   return render_template('reference.html')

@app.route('/contact')
def contact():
   return render_template('contact.html')



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        
        try:
            clientinput_unic = request.form['list_genes']
            print clientinput_unic
            clientinput_genelist = clientinput_unic.replace('\r','').split('\n')
            print type(clientinput_unic)
            clientinput_genelist = [x.encode('UTF8') for x in clientinput_genelist] # removing the Unicode from the list
            print type(clientinput_genelist)
            print clientinput_genelist


            phen_df, genescores_df, numbers, outfile_phen, outfile_genes, outfile_phenpergenes, accepted_df, dropped_df, Q, missing, dupli = tool2(clientinput_genelist)
            print "Numbers:", numbers
            print "missing:", missing
            print len(missing)
            print len(dupli)
            print len(dropped_df)
            print len(accepted_df)

            number_dropped = len(dropped_df)
            number_accepted = len(accepted_df)
            try:
                accepted = accepted_df.to_html()
            except:
                accepted = accepted_df
                
            try:
                dropped = dropped_df.to_html()
            except:
                dropped = dropped_df

            return render_template('result.html', genes_in_HPO=3777,output_phen=outfile_phen[7:],output_genes=outfile_genes[7:], output_phenpergenes=outfile_phenpergenes[7:], accepted=accepted, dropped=dropped, Q=Q, missing=missing, dupli=dupli, number_accepted=number_accepted, number_dropped=number_dropped)

        except:
            return redirect(url_for(".index"), code=302)



@app.route('/download/<filename>')
def download(filename):
    file = os.path.join(os.getcwd(), 'output', filename)
    return send_file(file, as_attachment=True)



if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug = True)

