"""
Générateur de Lettres de Motivation - Application Flask
========================================================

Application web pour générer des lettres de motivation professionnelles
en PDF avec 3 styles modernes et distincts.

Auteur: Votre Nom
Version: 1.0.0
"""

from flask import Flask, render_template, request, send_file, jsonify, abort
from datetime import datetime

# Configuration de l'application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete_a_changer'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite 16MB

# Configuration du logging


@app.route('/')
def index():
    """
    Page d'accueil avec le formulaire de génération
    """

    return render_template('index.html')



@app.route('/preview/<style>')
def preview_style(style):


    STYLES = ['corporate', 'startup', 'creatif']

    if style not in STYLES:
        style = 'corporate'
    
    # Données d'exemple
    data_exemple = {
        'prenom': 'Zéïnab Aly',
        'name': 'CAMARA',
        'adresse': 'Quartier de la gare, résidence central fac, Corte',
        'email': 'zeinabaly@email.com',
        'telephone': '06 12 34 56 78',
        'ville': 'Corte',
        'date': '31 janvier 2026',
        'entreprise': 'ACME Corporation',
        'recruteur': 'Madame la Directrice des Ressources Humaines',
        'objet': 'Candidature pour un stage en Data Science',
        'paragraphe1': 'Actuellement en dernière année de Master Data Science à l\'Université Paris-Saclay, je souhaite intégrer votre équipe Data pour un stage de 6 mois à partir d\'avril 2026. Votre entreprise, reconnue pour son innovation dans le domaine de l\'intelligence artificielle, représente pour moi l\'environnement idéal pour approfondir mes compétences en Machine Learning.',
        'paragraphe2': 'Mon parcours académique m\'a permis de développer une solide expertise en Python, en analyse de données et en modélisation prédictive. Lors de mon précédent stage chez DataTech, j\'ai contribué au développement d\'un modèle de prédiction des ventes qui a amélioré la précision des prévisions de 15%. Cette expérience m\'a également sensibilisée aux enjeux business de la data science.',
        'paragraphe3': 'Passionnée par les défis techniques et dotée d\'un excellent esprit d\'équipe, je suis convaincue que je pourrais apporter une réelle valeur ajoutée à vos projets. Je serais ravie de pouvoir échanger avec vous sur les opportunités de collaboration.',
        'formule_politesse': 'Je vous prie d\'agréer, Madame, Monsieur, l\'expression de mes salutations distinguées.',
        'nom': 'Zéïnab Aly CAMARA'
    }
    
    return render_template('lettre_template.html', **data_exemple, style=style, preview=True)



@app.route('/form/<style>')
def form(style):

    STYLES = ['corporate', 'startup', 'creatif']

    if style not in STYLES:
        style = 'corporate'
        

    return render_template('form.html', style=style)




@app.route('/generer', methods=['POST'])
def generer_lettre():
    """
    Génère la lettre de motivation en PDF
    
    Returns:
        Fichier PDF à télécharger
    """
    try:
        # Validation et récupération des données
        data = {
            'prenom': request.form.get('prenom', '').strip(),
            'name': request.form.get('nom', '').strip(),
            'adresse': request.form.get('adresse', '').strip(),
            'email': request.form.get('email', '').strip(),
            'telephone': request.form.get('telephone', '').strip(),
            'ville': request.form.get('ville', '').strip(),
            'date': request.form.get('date', datetime.now().strftime('%d %B %Y')),
            'entreprise': request.form.get('entreprise', '').strip(),
            'recruteur': request.form.get('recruteur', '').strip(),
            'objet': request.form.get('objet', '').strip(),
            'paragraphe1': request.form.get('paragraphe1', '').strip(),
            'paragraphe2': request.form.get('paragraphe2', '').strip(),
            'paragraphe3': request.form.get('paragraphe3', '').strip(),
            'formule_politesse': request.form.get('formule_politesse', '').strip(),
            'nom': request.form.get('nom', '').strip(),
        }
        
        # Validation des champs obligatoires
        champs_obligatoires = ['prenom', 'name', 'email', 'telephone', 
                               'entreprise', 'objet', 'paragraphe1', 
                               'paragraphe2', 'paragraphe3']
        
        champs_manquants = [champ for champ in champs_obligatoires if not data[champ]]
        
        if champs_manquants:
            return render_template(
                'form.html',
                error="Veuillez remplir tous les champs obligatoires",
                champs_manquants=champs_manquants
            )

        
        # Récupération du style choisi
        style_choisi = request.form.get('style')
        
        
        return render_template(
            'lettre_template.html',
            **data,
            style=style_choisi
        )

    except Exception as e:
        # logger.error(f"Erreur lors de la génération du PDF: {str(e)}", exc_info=True)
        return jsonify({'error': f'Erreur lors de la génération: {str(e)}'}), 500


if __name__ == '__main__':
    
    # Lancement de l'application
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )