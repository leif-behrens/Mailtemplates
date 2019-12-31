import sqlite3

# sqlite3 Datenbank erstellen mit den unterschiedlichen Templates

class Templates:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS templates " \
                         "(subject text PRIMARY KEY, message text, attributes text)")
        

    def new_template(self, subject, attributes, message):
        """
        :subject: String -> Überschrift/Titel der Nachricht (Primary Key => Darf nur einmal vorkommen)
        :message: String -> Die Nachricht zu der Überschrift
        :attributes: String -> Attribute, ob bspw. Anrede (Attribut 'a'), Preis (Attribut 'p'), Datum (Attribut 'd') etc. benötigt werden
        :return: Bool
        """
        try:
            self.cur.execute("INSERT INTO templates VALUES (?, ?, ?)", (subject, message, attributes))
            self.conn.commit()
            return True
        except:
            print("Überschrift existiert bereits")
            return False
        
    def get_templates_subjects(self):
        """
        :return: List -> Alle Überschriften
        """
        
        all_subjects = []
        self.cur.execute("SELECT subject FROM templates")
        
        for template in self.cur.fetchall():
            all_subjects.append(template[0])
                    
        return all_subjects
    
    def get_attributes_from_subject(self, subject):
        """
        :subject: String -> Template Überschrift
        :return: List -> Alle Attribute vom Subject
        """
        self.cur.execute("SELECT attributes FROM templates WHERE subject IS (?)", (subject,))

        try:
            return self.cur.fetchone()[0]
        except TypeError:
            return "Überschrift existiert nicht"

    def get_templates_message(self, subject):
        """
        :subject: String -> Überschrift
        :return: String -> Nachricht zur Überschrift
        """
                
        self.cur.execute("SELECT message FROM templates WHERE subject IS (?)", (subject,))
        
        try:
            return self.cur.fetchone()[0]
        except TypeError:
            return "Überschrift existiert nicht"
    
    def change_templates_message(self, subject, new_message):
        """
        :subject: String -> Überschrift des zu bearbeitenden Templates
        :new_message: Strin -> Neue Nachricht
        :return: None
        """
        
        try:
            self.cur.execute("UPDATE templates SET message = (?) WHERE (subject IS (?))", (new_message, subject))
            self.conn.commit()
        except:
            print("Überschrift existiert nicht.")
        
    def change_templates_subject(self, subject, new_subject):
        """
        :subject: String -> Aktuelle Überschrift
        :new_subject: String -> Neue Überschrift
        :return: None
        """
        
        try:
            self.cur.execute("UPDATE templates SET subject = (?) WHERE (subject IS (?))", (new_subject, subject))
            self.conn.commit()
        except:
            # Hier kann man sonst auch noch mehr Filtern bzw. eine genauere Fehlermeldung generieren.
            print("Überschrift existiert nicht oder neue Überschrift bereits vorhanden")
    
    def change_templates_attributes(self, attribute, subject):
        """
        :subject: String -> Aktuelle Überschrift
        :attribute: String -> Neue Attribute
        :return: None
        """
        
        try:
            self.cur.execute("UPDATE templates SET attributes = (?) WHERE (subject IS (?))", (attribute, subject))
            self.conn.commit()
        except Exception as e:
            # Hier kann man sonst auch noch mehr Filtern bzw. eine genauere Fehlermeldung generieren.
            print(e)
    
    def delete_template(self, subject):
        """
        :subject: String -> Überschrift (Primarykey) zum löschen
        :return: None
        """

        try:
            self.cur.execute("DELETE FROM templates WHERE (subject IS (?))", (subject,))
            self.conn.commit()
        except Exception as e:
            print(e)
            

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    db = Templates("Mail.db")
    db.new_template("template1", "Dies ist die Nachricht für das Template 1", "dp")
    db.new_template("template2", "Dies ist die Nachricht für das Template 2", "dpa")

    print(db.get_attributes_from_subject("template1"))
