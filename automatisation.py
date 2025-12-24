from flask import Flask, render_template, request
from datetime import datetime



app = Flask(__name__)


@app.route("/")
def formulaire():
    return render_template('index.html')


@app.route("/generer", methods=['POST'])
def generer():
    nom = request.form['name']
    entreprise = request.form['entreprise']
    objet = request.form['objet']
    texte = request.form['texte']
    
    # Date automatique
    # date = datetime.now().strftime("%d/%m/%Y")
    
    return render_template('lettre_template.html', 
                         nom=nom,
                         email="zeinab@exemple.com",
                         entreprise=entreprise, 
                         objet=objet, 
                         texte=texte,
                         date="24/10/2025")




@app.route("/telecharger", methods=['POST'])
def telecharger():
    nom = request.form['name']
    entreprise = request.form['entreprise']
    objet = request.form['objet']
    texte = request.form['texte']
    
    date = datetime.now().strftime("%d/%m/%Y")
    
    # Génère le HTML
    html_content = render_template('lettre_template.html', 
                                  nom=nom,
                                  email="ton.email@exemple.com",
                                  entreprise=entreprise, 
                                  objet=objet, 
                                  texte=texte,
                                  date=date)
    # Convertit en PDF
    pdf = HTML(string=html_content).write_pdf()
    
    # Prépare la réponse
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=lettre_motivation_{entreprise}.pdf'
    
    return response


if __name__ == '__main__':
    app.run(debug=True)

