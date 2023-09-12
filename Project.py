import datetime
from Database import Database


class Project:
    def __init__(self):
        self.project_name = None
        self.date_of_creation_project = datetime.date.today()
        self.contracts_links = None
        self.database = Database()

    def view_all_projects(self):
        return self.database.view_information_about_tables("Projects")

    def add_project(self, name_of_project):
        self.project_name = name_of_project
        self.database.insert_information_into_project_table(self.contracts_links,
                                                            self.project_name,
                                                            self.date_of_creation_project)

    def change_contract_links_in_project(self, contract_id, project_id):
        self.database.update_table_value("projects", "contract_id", contract_id, "project_id", project_id)

    def view_contracts_in_project(self, project_id):
        return self.database.view_contract_in_project(project_id)

    def view_project_name(self, project_id):
        return self.database.view_table_value_with_search_term("project_name", "projects", "project_id",
                                                               project_id)[0][0]

    def view_project_indexes(self):
        return self.database.view_indexes_in_table("project_id", "projects")

    def check_repeating_project_name(self, name):
        return self.database.repeating_name("projects", "project_name", name)
