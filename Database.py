import datetime
import sqlite3


class Database:
    database_name = "System_of_contracts_and_projects.db"

    def __init__(self):
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS contracts (contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    contract_name TEXT,
                                                    date_of_creation_contract TEXT,
                                                    date_of_signing TEXT,
                                                    status TEXT,
                                                    project TEXT)""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    contract_id INT,
                                                    project_name TEXT,
                                                    date_of_creation_project TEXT,
                                                    FOREIGN KEY(contract_id) REFERENCES contracts(contract_id))""")
        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def view_information_about_tables(self, table_name):
        self.cursor.execute(f"""SELECT * FROM {table_name}""")
        information = self.cursor.fetchall()
        return information

    def insert_information_into_project_table(self, project_name, date_of_creation_project):
        self.cursor.execute("""INSERT INTO projects (project_name, date_of_creation_project) VALUES(?, ?)""",
                            (project_name, date_of_creation_project))
        self.connection.commit()

    def insert_information_into_contract_table(self, contract_name, date_of_creation_contract, date_of_signing, project):
        self.cursor.execute("""INSERT INTO contracts (contract_name, date_of_creation_contract, date_of_signing, status, project) VALUES(?, ?, ?, "Черновик", ?)""",
                            (contract_name, date_of_creation_contract, date_of_signing, project))
        self.connection.commit()

    def update_contract_status(self, status, contract_id):
        self.cursor.execute("""UPDATE contracts SET status=? WHERE contract_id=?""",
                            (status, contract_id))
        self.connection.commit()

    def delete_contract(self, contract_id):
        self.cursor.execute(f"""DELETE FROM contracts WHERE contract_id=?""", contract_id)
        self.connection.commit()

    def delete_project(self, project_id):
        self.cursor.execute(f"""DELETE FROM projects WHERE project_id=?""", project_id)
        self.connection.commit()

db = Database()
current_data = datetime.date.today()
db.insert_information_into_contract_table("Contract", current_data, None, None)
db.update_contract_status("Активный", 1)
