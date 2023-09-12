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

    def view_indexes_in_table(self, column_name, table_name):
        self.cursor.execute(f"""SELECT {column_name} FROM {table_name}""")
        information = self.cursor.fetchall()
        return [i[0] for i in information]

    def view_information_about_tables(self, table_name):
        self.cursor.execute(f"""SELECT * FROM {table_name}""")
        information = self.cursor.fetchall()
        return information

    def view_contract_in_project(self, project_id):
        self.cursor.execute("""SELECT projects.project_name as name, contracts.contract_name as contract_name FROM 
        projects join contracts on contracts.contract_id = projects.contract_id WHERE projects.project_id=?""",
                            (project_id,))
        rows = self.cursor.fetchall()
        return rows

    def view_table_value_with_search_term(self, column_name, table_name, search_term, search_value):
        self.cursor.execute(f"""SELECT {column_name} FROM {table_name} WHERE {search_term}=?""", (search_value,))
        return self.cursor.fetchall()

    def insert_information_into_project_table(self, contract_link, project_name, date_of_creation_project):
        self.cursor.execute("""INSERT INTO projects (contract_id, project_name, date_of_creation_project) VALUES(?, 
        ?, ?)""",
                            (contract_link, project_name, date_of_creation_project))
        self.connection.commit()

    def insert_information_into_contract_table(self, contract_name, date_of_creation, date_of_signing, project):
        self.cursor.execute("""INSERT INTO contracts (contract_name, date_of_creation_contract, date_of_signing, 
        status, project) VALUES(?, ?, ?, "Draft", ?)""",
                            (contract_name, date_of_creation, date_of_signing, project))
        self.connection.commit()

    def update_table_value(self, table, column_name, column_value, search_term, search_value):
        self.cursor.execute(f"""UPDATE {table} SET {column_name}=? WHERE {search_term}=?""",
                            (column_value, search_value))
        self.connection.commit()

    def view_contracts_with_selected_status(self, status):
        self.cursor.execute("""SELECT * FROM contracts WHERE status=?""", (status,))
        rows = self.cursor.fetchall()
        return rows

    def repeating_lines(self, contract_name, date_of_creation_contract, date_of_signing, status):
        self.cursor.execute("""SELECT COUNT(*) FROM contracts WHERE contract_name=? AND date_of_creation_contract=? 
        AND date_of_signing=? AND status=?""",
                            (contract_name, date_of_creation_contract, date_of_signing, status))
        return self.cursor.fetchall()[0][0]

    def repeating_name(self, table_name, column_name, column_value):
        self.cursor.execute(f"""SELECT COUNT(*) FROM {table_name} WHERE {column_name}=?""",
                            (column_value,))
        return self.cursor.fetchall()[0][0]
