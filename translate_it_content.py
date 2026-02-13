import os
import re

BASE_DIR = "/Users/bricelengama/Documents/Marketing Opti/LaFrench/it"

# Translation Dictionary (FR -> IT)
# Ordered by length (longest first) to avoid partial matches
TRANSLATIONS = {
    # Index & Common
    "Ta Soirée à Barcelone": "La Tua Serata a Barcellona",
    "Commence Ici": "Inizia Qui",
    "Before + Guest List + Clubs — L'expérience complète, gratuite": "Pre-serata + Guest List + Discoteche — L'esperienza completa, gratis",
    "Rejoins la Liste Gratuite": "Entra in Lista",
    "Découvrir l'Expérience": "Scopri l'Esperienza",
    "Entrée 100% Gratuite sur Liste": "Ingresso 100% Gratuito in Lista",
    "Entrée 100% gratuite sur liste": "Ingresso 100% gratuito in lista",
    "Iscriviti et entre gratuitement dans les meilleurs clubs de Barcelone": "Iscriviti ed entra gratis nelle migliori discoteche di Barcellona",
    "Pas de frais cachés": "Nessun costo nascosto",
    "Le plan parfait pour ta soirée": "Il piano perfetto per la tua serata",
    "L'Expérience Complète": "L'Esperienza Completa",
    "On ne fait pas que des listes — on organise ta soirée de A à Z": "Non facciamo solo liste — organizziamo la tua serata dalla A alla Z",
    "Le Before — Si Pub Musical": "Il Pre-serata — Si Pub Musical",
    "On commence la soirée au": "Iniziamo la serata al",
    "bar mythique du centre-ville de Barcelone": "storico bar nel centro di Barcellona",
    "L'endroit parfait pour se chauffer comme il faut avant le club": "Il posto perfetto per scaldarsi prima della discoteca",
    "2 shots gratuits": "2 chupitos gratis",
    "Réductions toute la soirée": "Sconti tutta la notte",
    "Rencontres Erasmus & touristes": "Incontri Erasmus & turisti",
    "Ensuite, on t'emmène directement en club": "Poi, ti portiamo direttamente in discoteca",
    "Il Club — Entrée Gratuite": "La Discoteca — Ingresso Gratuito",
    "Guest list confirmée, on y va ensemble": "Guest list confermata, andiamo insieme",
    "Tu passes devant tout le monde, entrée gratuite dans un": "Salti la fila, ingresso gratuito in un",
    "club partenaire ultra réputé": "club partner esclusivo",
    "Zéro galère": "Zero stress",
    "Entrée sur liste — 100% gratuit": "Ingresso in lista — 100% gratis",
    "Entrée groupée — on arrive ensemble": "Ingresso di gruppo — arriviamo insieme",
    "Zéro attente — coupe-file garanti": "Zero attesa — saltafila garantito",
    "Tables VIP & Bottle Service": "Tavoli VIP & Bottle Service",
    "Envie de plus ? Réserve une table VIP avec bouteilles et service privé": "Vuoi di più? Prenota un tavolo VIP con bottiglie e servizio privato",
    "L'expérience ultime pour un anniversaire, un EVG/EVJF ou juste une nuit mémorable": "L'esperienza definitiva per un compleanno, addio al celibato/nubilato o solo una notte memorabile",
    "Service bouteille premium": "Servizio bottiglia premium",
    "Espace privé dédié": "Spazio privato dedicato",
    "Conciergerie personnalisée": "Concierge personalizzato",
    "Je veux l'expérience complète — C'est gratuit": "Voglio l'esperienza completa — È gratis",
    "Top 10 Clubs de Barcelone": "Top 10 Discoteche di Barcellona",
    "Entrée gratuite sur guest list — Étudiants • Touristes • Erasmus": "Ingresso gratuito in lista — Studenti • Turisti • Erasmus",
    "Tables VIP Exclusives": "Tavoli VIP Esclusivi",
    "Vivre la nuit barcelonaise de l'intérieur": "Vivi la notte di Barcellona dall'interno",
    "Tables privées avec bouteilles premium et service dédié": "Tavoli privati con bottiglie premium e servizio dedicato",
    "Accès exclusif aux salons privés": "Accesso esclusivo alle sale private",
    "L'expérience nightlife ultime à Barcelone": "L'esperienza notturna definitiva a Barcellona",
    "Réserver une Table VIP": "Prenota un Tavolo VIP",
    "Jeudi / Vendredi / Samedi": "Giovedì / Venerdì / Sabato",
    "L'événement incontournable pour la communauté française et internationale à Barcelone": "L'evento imperdibile per la comunità internazionale a Barcellona",
    "Experiences complètes : before + clubs + guest list gratuite": "Esperienza completa: pre-serata + discoteca + guest list gratuita",
    "Chaque soir": "Ogni sera",
    "Réserve Ta Place — Gratis": "Prenota il Tuo Posto — Gratis",
    "Blog — Guide Nightlife Barcelone": "Blog — Guida Nightlife Barcellona",
    "Tout ce qu'il faut savoir pour sortir à Barcelone": "Tutto quello che devi sapere per uscire a Barcellona",
    "Contacte-Nous": "Contattaci",
    "Iscriviti sur la guest list ou réserve ta table VIP": "Iscriviti in guest list o prenota il tuo tavolo VIP",
    
    # Guest Lists Page
    "Guest List Gratuita Barcelone": "Guest List Gratuita Barcellona",
    "Entrée gratuite dans les meilleurs clubs — Zéro frais, zéro attente": "Ingresso gratuito nelle migliori discoteche — Zero costi, zero attesa",
    "Come funziona?": "Come funziona?",
    "3 étapes simples pour entrer gratuitement en club": "3 semplici passi per entrare gratis in discoteca",
    "Envoie ton nom et le nombre de personnes via WhatsApp ou Instagram": "Invia il tuo nome e il numero di persone via WhatsApp o Instagram",
    "C'est tout — pas de formulaire compliqué": "Tutto qui — nessun modulo complicato",
    "Rejoins-nous au Si Pub Musical à 22h": "Unisciti a noi al Si Pub Musical alle 22:00",
    "2 shots offerts, ambiance de folie, et on te met sur la liste": "2 chupitos offerti, atmosfera pazzesca, e ti mettiamo in lista",
    "On part ensemble au club": "Andiamo insieme in discoteca",
    "Tu passes devant tout le monde, entrée gratuite": "Salti la fila, ingresso gratuito",
    "Entrée gratuite disponible dans tous ces clubs": "Ingresso gratuito disponibile in tutti questi club",
    "Club emblématique de la plage": "Club iconico sulla spiaggia",
    "Terrasse face à la mer": "Terrazza fronte mare",
    "L'héritage Ibiza au Port Olímpic": "L'eredità di Ibiza al Port Olímpic",
    "Décoration orientale luxueuse": "Decorazione orientale lussuosa",
    "Style industriel unique sur plusieurs étages": "Stile industriale unico su più piani",
    "Ancien théâtre reconverti": "Antico teatro riconvertito",
    "Ambiance techno & électro underground": "Atmosfera techno & elettro underground",
    "Oui, 100%. Nos guest lists sont entièrement gratuites": "Sì, 100%. Le nostre liste sono completamente gratuite",
    "Pas de frais cachés, pas de consommation obligatoire": "Nessun costo nascosto, nessuna consumazione obbligatoria",
    "Tu payes uniquement tes boissons au club si tu le souhaites": "Paghi solo le tue bevande al club se lo desideri",
    "Il faut arriver à quelle heure ?": "A che ora bisogna arrivare?",
    "On recommande d'arriver au before (Si Pub Musical) vers 22h": "Consigliamo di arrivare al pre-serata (Si Pub Musical) verso le 22:00",
    "On part ensemble au club vers 00h30": "Partiamo insieme per il club verso le 00:30",
    "L'arrivée au club avant 01h30 garantit ton entrée sur liste": "L'arrivo al club prima dell'01:30 garantisce il tuo ingresso in lista",
    "Quel est le dress code ?": "Qual è il dress code?",
    "Abbigliamento elegante pour la plupart des clubs": "Abbigliamento elegante per la maggior parte dei club",
    "(chemise, chaussures de ville)": "(camicia, scarpe eleganti)",
    "Certains clubs comme Otto Zutz ou City Hall sont plus décontractés": "Alcuni club come Otto Zutz o City Hall sono più casual",
    "Consulte la page de chaque club pour plus de détails": "Consulta la pagina di ogni club per maggiori dettagli",
    "Je peux venir seul(e) ?": "Posso venire da solo/a?",
    "Absolument ! C'est même l'occasion parfaite pour rencontrer du monde": "Assolutamente! È l'occasione perfetta per conoscere gente",
    "Le before est fait pour ça — Erasmus, touristes, locaux, tout le monde est bienvenu": "Il pre-serata è fatto per questo — Erasmus, turisti, locali, tutti sono i benvenuti",
    "Iscriviti maintenant via WhatsApp et fais partie de la prochaine soirée La French": "Iscriviti ora via WhatsApp e partecipa alla prossima serata La French",
    
    # VIP Reservations
    "Réserver une Table VIP à Barcelone": "Prenotare un Tavolo VIP a Barcellona",
    "Les meilleurs emplacement, service premium, zéro attente": "Le migliori posizioni, servizio premium, zero attesa",
    "Pourquoi réserver une table VIP ?": "Perché prenotare un tavolo VIP?",
    "L'expérience nightlife ultime": "L'esperienza notturna definitiva",
    "Pas de file d'attente": "Nessuna fila",
    "Entrée prioritaire pour toi et tes amis": "Ingresso prioritario per te e i tuoi amici",
    "Espace Privatif": "Spazio Privato",
    "Ta propre table dans la zone VIP": "Il tuo tavolo nella zona VIP",
    "Service à Table": "Servizio al Tavolo",
    "Pas besoin d'aller au bar": "Non serve andare al bar",
    "Vue Imprenable": "Vista Mozzafiato",
    "Meilleure vue sur le DJ et la piste": "Migliore vista sul DJ e sulla pista",
    "Comment réserver ?": "Come prenotare?",
    "Choisis ton Club": "Scegli il tuo Club",
    "Sélectionne le club et la zone VIP": "Seleziona il club e la zona VIP",
    "Contacte-nous": "Contattaci",
    "Envoie-nous un message WhatsApp": "Inviaci un messaggio WhatsApp",
    "Confirmation": "Conferma",
    "On confirme ta réservation instantanément": "Confermiamo la tua prenotazione istantaneamente",
    "Prix approximatifs (par table / 5 pers)": "Prezzi indicativi (per tavolo / 5 pers)",
    "À partir de": "A partire da",
    "Réserver Maintenant": "Prenota Ora",
    "Conditions Générales VIP": "Condizioni Generali VIP",
    "Le prix inclut l'entrée pour 5 personnes max": "Il prezzo include l'ingresso per max 5 persone",
    "Le montant est un crédit de consommation (bouteilles)": "L'importo è un credito di consumazione (bottiglie)",
    "Tenue correcte exigée (pas de shorts/tongs/baskets sport)": "Abbigliamento adeguato richiesto (no shorts/infradito/scarpe sportive)",
    "Acompte parfois demandé pour les gros événements": "Acconto a volte richiesto per grandi eventi",
    
    # Club Pages Specifics
    "Le club iconique du front de mer": "Il club iconico fronte mare",
    "Club emblématique de la Barceloneta avec terrasse face à la mer": "Club iconico della Barceloneta con terrazza fronte mare",
    "intérieur ultra-design": "interni ultra-design",
    "spot incontournable pour une nuit mémorable": "luogo imperdibile per una notte memorabile",
    "Arrivée avant 01h30 recommandée": "Arrivo prima dell'01:30 raccomandato",
    "Inscription simple via WhatsApp": "Iscrizione semplice via WhatsApp",
    "Accès prioritaire sans file d'attente": "Accesso prioritario senza fila",
    "Espace VIP exclusif": "Spazio VIP esclusivo",
    "Abbigliamento elegante obligatoire": "Abbigliamento elegante obbligatorio",
    "Chemise recommandée pour les hommes": "Camicia consigliata per gli uomini",
    "Chaussures de ville exigées": "Scarpe eleganti richieste",
    "pas de baskets de sport, shorts ou tongs": "no scarpe sportive, pantaloncini o infradito",
    "Le club se réserve le droit de refuser l'entrée": "Il club si riserva il diritto di rifiutare l'ingresso",
    "Prêt pour Opium ?": "Pronto per l'Opium?",
    "Prêt pour ": "Pronto per ",
    "Iscriviti sur la guest list gratuite et entre sans payer": "Iscriviti in guest list gratuita ed entra senza pagare",
    "C'est simple, rapide et garanti": "È semplice, veloce e garantito",
    "Découvre aussi": "Scopri anche",
    "Entra in Guest List — Gratis": "Entra in Guest List — Gratis", # Already IT?
    "Entra in Guest List": "Entra in Guest List",
    
    # Misc
    "Lire l'article": "Leggi l'articolo",
    "Bon Plan": "Buon Piano", # Or "Consiglio"
    "Guide": "Guida",
    "Tourisme": "Turismo",
    
    # Events Page
    "Les Prochaines Soirées": "Le Prossime Serate",
    "Ton agenda nightlife complet": "La tua agenda nightlife completa",
    "Toute la semaine": "Tutta la settimana",
    "Lundi": "Lunedì", "Mardi": "Martedì", "Mercredi": "Mercoledì", "Jeudi": "Giovedì", "Vendredi": "Venerdì", "Samedi": "Sabato", "Dimanche": "Domenica",
    "La French Party": "La French Party",
    "Rejoins la meilleure soirée française": "Unisciti alla migliore serata",
    "Infos & Guest List": "Info & Guest List",
}

def translate_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    for fr, it in TRANSLATIONS.items():
        # Case insensitive might be dangerous, stick to explicit replaces.
        # Use simple replace for safety.
        content = content.replace(fr, it)
        
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Translated {filepath}")
    else:
        print(f"No changes for {filepath}")

# Walk IT Directory
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".html"):
            translate_file(os.path.join(root, file))
