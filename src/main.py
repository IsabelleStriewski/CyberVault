import json             # Werkzeug zum Speichern von JSON-Dateien

import string           # für Passwort generieren lassen
import secrets          # später für die Verschlüsselung

import time             # damit die Generierung des Passworts auch kurz dauert, übersichtlicher und schöner
import datetime         # meine "Überwachung", wann wurde die Aktion ausgeführt?
import getpass          # um das Master Passwort bei der Eingabe unsichtbar zu machen
import os               # für die verschiedenen Betriebssysteme
import hashlib          # um Passwörter zu hashen

from cryptography.fernet import Fernet

# --- Werkzeuge und Daten implementieren ---

def daten_laden(safe):                                   # zweiter Code
    dateipfad = "data/vault.json"
    try:                                                 # liest Daten aus der Datei, öffnet sie
        with open (dateipfad, "rb") as datei:            # r = read, rb neu für binary
            verschluesselte_daten = datei.read()
        entschluesselte_bytes = safe.decrypt (verschluesselte_daten)    # Daten wieder entschlüsseln
        json_string = entschluesselte_bytes.decode()    # Bytes wieder in Text/String umwandeln
        return json.loads (json_string)                 # String wieder als Dictionary    
    
    except FileNotFoundError:                           # falls die Datei nicht existiert
        print (f"\nHinweis: Tresor-Datei nicht gefunden. Ein neuer Tresor wird angelegt.")
        return {}                                       # Ergebnis / leeres Dictionary wird zurückgegeben    
    except Exception as e:                              # wenn beim Entschlüsseln Fehler passiert, dann als e gespeichert
        print (f"\nFehler beim Entschlüsseln: {e}")       # die o.g. Ausgabe
        return {}                                       # gibt dann ein leeres Dictionary zurück


def check_ueberschreiben (dienst, safe):                       # Prüfung, ob Eintrag schon vorhanden oder nicht
    daten = daten_laden(safe)
    if dienst in daten:
        print (f"\nAchtung! Ein Passwort für {dienst} besteht bereits!")
        bestaetigung = input ("Möchten Sie das Passwort wirklich überschreiben? (j/n) ")
        if bestaetigung.lower() != "j":                  # lower() für Klein und Großschreibung
            print ("\nVorgang abgebrochen!") 
            log_schreiben ("Passwort überschreiben wurde abgebrochen.") 
            return False
    return True

def eintrag_hinzufuegen (dienst, passwort, safe):             # fügt neuen Dienst hinzu, ohne die alten Daten zu löschen
       
    daten = daten_laden(safe)                               # bestehende Daten aus der Datei laden
  
    daten [dienst] = passwort                           # den neuen Eintrag im Dictionary hinzufügen, wenn der Dienst schon
                                                        # in der Liste existiert, wird das Passwort aktualisiert  
    daten_speichern (daten, safe)
   
    print (f"\nDaten für {dienst} wurden erfolgreich in CyberVault gesichert.")    

def passwort_generieren(laenge):                              # erstellt ein neues Passwort
    pool = str (string.ascii_letters + string.digits + string.punctuation)      # Groß-und Kleinbuchstaben
    gen_pw = ""                                                                           # sowie Zahlen und Sonderzeichen
    for _ in range (laenge):                                    # hier wird keine Zählvariable benötigt, sondern nur die
        gen_pw = gen_pw + secrets.choice (pool)                 # Wiederholung, _ = Platzhalter, weil Nutzer die Länge bestimmmt
    return gen_pw

def log_schreiben(aktion):                              # erstellt einen Log Eintrag 
    jetzt = datetime.datetime.now()
    zeit_string = jetzt.strftime ("%Y-%m-%d %H:%M:%S")  # für das richtige Format
    log_daten = f"{zeit_string} - Aktion: {aktion}\n"
    dateipfad = "access.log"                       
    with open (dateipfad, "a") as datei:                  
        datei.write(log_daten) 

def log_protokoll_anzeigen ():                          # Aufrufen der Access Log Einträge
    dateipfad = "access.log"
    try:
        with open (dateipfad, "r") as datei:
            print ("\n"+"="*30)
            print ("\nCyberVault System-Log\n")
            print ("="*30+"\n")

            inhalt = datei.read()
            if inhalt:
                print (inhalt)
            else:
                print ("Das Protokoll ist noch leer.")

            print ("="*30)
            log_schreiben ("Das Log-Protokoll wurde eingesehen.")

    except FileNotFoundError:
        print ("\nFehler! Es wurde noch kein Log-Protokoll erstellt.")

def eintrag_loeschen (dienst, safe):
    daten = daten_laden(safe)
    if dienst in daten:
        bestaetigung = input (f"Soll der Eintrag für {dienst} wirklich gelöscht werden? (j/n): ")
        if bestaetigung.lower () == "j":
            del daten [dienst]                      # Daten löschen mit del
            daten_speichern (daten, safe)
            print (f"\nDer Eintrag für {dienst} wurde gelöscht.") 
            log_schreiben (f"Eintrag gelöscht für {dienst}") 
        else:
            print (f"\nLöschvorgang abgebrochen.")    
    else:
        print (f"\nFehler: Kein Eintrag für {dienst} gefunden.")
        log_schreiben (f"Löschung fehlgeschlagen. Dienst nicht gefunden: {dienst}")       

def daten_speichern (daten, safe):
    dateipfad = "data/vault.json"

    json_string = json.dumps (daten, indent = 4)        # Dictionary in einen json-String umwandeln
                                                        # und json.dumps (Text-String) zum späteren Verschlüsseln
    daten_als_bytes = json_string.encode()              # String in Bytes wandeln (.encode())    
    verschluesselt = safe.encrypt (daten_als_bytes)     # Bytes verschlüssseln                                                
    with open (dateipfad, "wb") as datei:
        datei.write (verschluesselt)
    log_schreiben ("Daten wurden verschlüsselt gespeichert.")      

def master_passwort_verwalten():                        # Master Passwort soll nicht direkt im Code stehen
    dateipfad = ".secret"                               # Name der versteckten Datei mit Master Passwort                 

    if not os.path.exists (dateipfad):                  # Datei mit dem Passwort existiert noch nicht
        print ("\n---Ersteinrichtung CyberVault---\n")
        time.sleep(1)
        neu = getpass.getpass ("Bitte legen Sie ein neues Master Passwort fest: ")
        
        hash_objekt = hashlib.sha256 (neu.encode())
        passwort_hash = hash_objekt.hexdigest()
        
        with open(dateipfad, "w") as geheime_datei:
            geheime_datei.write (passwort_hash)                               # Passwort eintragen in die neue Datei
        log_schreiben ("Ein neues Master Passwort wurde erstellt und gehashed gespeichert.")
        return passwort_hash
    else:
        with open (dateipfad, "r") as geheime_datei:
            return geheime_datei.read().strip()       #strip entfernt unsichtbare Leerzeichen

def schluessel_laden_oder_erstellen():
    schluessel_aus_system = os.environ.get ("CYBERVAULT_KEY")       # aus dem System (Umgebungsvariable) laden

    if schluessel_aus_system:
        log_schreiben ("Schlüssel erfolgreich aus System geladen.")
        return schluessel_aus_system.strip().encode()       # Fernet braucht den Schlüssel als Bytes
                                                            # strip() schneidet Leerzeichen u Zeilenumbrüche am Anfang u Ende eines Textes weg
    dateipfad = "vault.key"                         # quasi der alte Weg
    if os.path.exists (dateipfad):
        with open (dateipfad, "rb") as geheime_datei:
            log_schreiben ("SChlüssel aus Datei geladen. System-Variable fehlte.")
            return geheime_datei.read().strip()

    schluessel = Fernet.generate_key()              # wenn beides nicht da ist, neu erstellen
    with open (dateipfad, "wb") as geheime_datei:
        geheime_datei.write (schluessel)

    print ("\nNeuer Key generiert und gespeichert.")
    log_schreiben ("Neuer Key generiert und in vault.key gespeichert.")
    print ("\nWichtig! Übertrage den Key in deine Umgebungsvariablen.")
    return schluessel        


# --- CyberVault Hauptprogramm --- 

def main():                                             

    print ("\n\n=== CyberVault ===\n")
    master_pw = master_passwort_verwalten()             # die Klammern rufen die Funktion auf, ohne die klappt es nicht

    for versuch in range(3):                            # Schleife, um drei Versuche zur Passwort Eingabe zu haben
        if versuch == 0:                                # für den ersten Versuch, range zählt ab 0
            frage = "Bitte geben Sie das Master Passwort ein: "
        else:
            rest = 2 - versuch                          # um zu wissen, wieviele Versuche der Nutzer noch hat
            frage = f"\nFalsch. Sie haben noch {rest +1} Versuche. Bitte geben Sie das Passwort erneut ein: "
        kontrolle = getpass.getpass (frage)       # mit getpass wird das Passwort bei der Eingabe nicht angezeigt   
        eingabe_hash = hashlib.sha256(kontrolle.encode()).hexdigest()
        if eingabe_hash == master_pw:
            log_schreiben ("Login mit Master Passwort durchgeführt.")
            time.sleep(1)
            print ("\n\nWillkommen!\n")
            time.sleep(2)
            break 
        else:
            log_schreiben (f"Master Passwort wurde {versuch +1}/3 falsch eingegeben")
            if versuch == 2:
                log_schreiben ("Das Passwort wurde dreimal falsch eingegeben. Zugriff verweigert.")
                time.sleep(1)
                print ("\nZugriff verweigert. Das System wurde gesperrt.\n")
                return  
            
    schluessel = schluessel_laden_oder_erstellen()
    safe = Fernet (schluessel)            

    while True:                                         
        print ("")
        time.sleep(1)
        print ("\n=== CyberVault Menü ===\n")
        print ("1. Alle Passwörter anzeigen")
        print ("2. Neues Passwort hinzufügen")
        print ("3. Passwort generieren")
        print ("4. Eintrag löschen")
        print ("5. Log-Protokoll")
        print ("6. Programm beenden")

        wahl = input ("\nWas möchtest du tun? (1,2,3,4,5,6): ")   # Auswahl durch Nutzer

        if wahl == "1":
            log_schreiben ("Anzeige aller Passwörter angefordert.")
            inhalt = daten_laden(safe)
            if inhalt:
                maskieren = input ("Passwörter maskieren? (j/n): ").lower()
                if maskieren.lower () == "j":
                    log_schreiben ("Passwörter wurden maskiert angezeigt.")
                else: 
                    log_schreiben ("Passwörter wurden im Klartext angezeigt.") 
                print ("\n---Gefundene Einträge---")
                for dienst, pw in inhalt.items ():
                    if maskieren.lower() == "j":
                        anzeige_pw = "*" * len(pw)
                    else:
                        anzeige_pw = pw           
                    print (f"\nDienst: {dienst:<15} | Passwort: {anzeige_pw}")
            else:
                print ("\nDer Tresor ist noch leer.")
        elif wahl == "2":
            dienst = input ("\nName des Dienstes: ")
            if check_ueberschreiben (dienst, safe) == False:
                continue
            pw = input (f"Passwort für {dienst}: ")
            eintrag_hinzufuegen (dienst, pw, safe)
            log_schreiben (f"Manueller Eintrag für {dienst} erstellt.")
        elif wahl == "3":
            dienst = input ("\nFür welchen Dienst soll ein Passwort generiert werden? ")
            if check_ueberschreiben (dienst, safe) == False:
                continue
            laenge = int (input ("\nWie lang soll das Passwort sein? \n"))       
            time.sleep(1)              
            print ("\nDas Passwort wird generiert...\n")
            time.sleep(2)
            neues_pw = passwort_generieren (laenge)
            print (f"Das generierte Passwort lautet: {neues_pw}")
            eintrag_hinzufuegen (dienst, neues_pw, safe)
            time.sleep(1)
            print ("\nZurück zum Menü\n")
            time.sleep(1)
            log_schreiben (f"Passwort wurde für {dienst} generiert.")
        elif wahl == "4":
            dienst = input ("Welcher Dienst soll gelöscht werden?")
            eintrag_loeschen (dienst, safe)
        elif wahl == "5":
            log_protokoll_anzeigen()
        elif wahl == "6":
            time.sleep(1)
            print ("\nCyberVault wird beendet...\n")
            log_schreiben ("CyberVault wurde beendet.")
            break     
        else:
            print ("\nUngültige Angabe,bitte wähle 1, 2, 3, 4 oder 5!\n")

if __name__ == "__main__":                              # Code wird nur ausgeführt, wenn 
    main()                                              # die Datei direkt gestartet wird

