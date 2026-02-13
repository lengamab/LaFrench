
import os

FILEPATH = "/Users/bricelengama/Documents/Marketing Opti/LaFrench/it/parties-today.html"

TRANSLATIONS = {
    "Soirées Ce Soir à Barcelone": "Serate Stasera a Barcellona",
    "Où Sortir Aujourd'hui": "Dove Uscire Oggi",
    "Où sortir ce soir à Barcelone ?": "Dove uscire stasera a Barcellona?",
    "Découvre les clubs ouverts ce soir avec entrée gratuite via La French Barcelona.": "Scopri i club aperti stasera con ingresso gratuito via La French Barcelona.",
    "Découvre les clubs ouverts ce soir à Barcelone.": "Scopri i club aperti stasera a Barcellona.",
    "Guest list gratuite disponible maintenant.": "Guest list gratuita disponibile ora.",
    "Soirée Ce Soir": "Serata Stasera",
    "Before + Guest List gratuite + Club.": "Pre-serata + Guest List gratuita + Discoteca.",
    "L'expérience nightlife complète à Barcelone, chaque soir du jeudi au samedi.": "L'esperienza notturna completa a Barcellona, ogni sera dal giovedì al sabato.",
    "Soirées Ce Soir": "Serate Stasera",
    "Où sortir aujourd'hui ?": "Dove uscire oggi?",
    "Iscriviti pour Ce Soir": "Iscriviti per Stasera",
    "Le Programme de Ce Soir": "Il Programma di Stasera",
    "Ogni sera du jeudi au samedi — le même plan parfait": "Ogni sera dal giovedì al sabato — lo stesso piano perfetto",
    "On se retrouve au bar. 2 shots offerts, réductions toute la soirée, DJ live.": "Ci troviamo al bar. 2 chupitos offerti, sconti tutta la notte, DJ live.",
    "C'est le moment de se chauffer et de rencontrer du monde.": "È il momento di scaldarsi e conoscere gente.",
    "Départ vers le Club": "Partenza per il Club",
    "On part tous ensemble vers le club du soir.": "Partiamo tutti insieme verso il club della serata.",
    "Pas besoin de taxi, on y va à pied en groupe.": "Niente taxi, andiamo a piedi in gruppo.",
    "Entrée en Club — Gratis": "Ingresso nel Club — Gratis",
    "La soirée peut vraiment commencer !": "La serata può davvero iniziare!",
    "Fin de soirée": "Fine serata",
    "Lever de soleil sur la Barceloneta.": "Alba sulla Barceloneta.",
    "Tu rentreras avec des souvenirs mémorables.": "Tornerai a casa con ricordi indimenticabili.",
    "Les Clubs Ce Soir": "I Club di Stasera",
    "Le club de la soirée dépend du jour — voici les habituels": "Il club della serata dipende dal giorno — ecco i soliti",
    "On sort ce soir ?": "Usciamo stasera?",
    "Iscriviti maintenant et rejoins la soirée La French.": "Iscriviti ora e unisciti alla serata La French.",
    "C'est gratuit, c'est maintenant.": "È gratis, è ora.",
    "Ven / Sam": "Ven / Sab",
    "Jeu / Ven / Sam": "Gio / Ven / Sab",
    "Prochaine soirée : Giovedì": "Prossima serata: Giovedì",
    " Soir — Guest List Ouverte": " Sera — Guest List Aperta",
    "Centro Città": "Centro Città" # Already correct but good to keep
}

def translate_parties_today():
    with open(FILEPATH, 'r') as f:
        content = f.read()
    
    original_content = content
    
    for fr, it in TRANSLATIONS.items():
        content = content.replace(fr, it)
        
    if content != original_content:
        with open(FILEPATH, 'w') as f:
            f.write(content)
        print(f"Translated {FILEPATH}")
    else:
        print(f"No changes for {FILEPATH}")

if __name__ == "__main__":
    translate_parties_today()
