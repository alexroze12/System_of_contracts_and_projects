import datetime
from Database import Database


class Contract:
    def __init__(self):
        self.contract_name = None
        self.date_of_creation_contract = datetime.date.today()
        self.date_of_signing = None
        self.status = "Draft"
        self.project = None
        self.database = Database()

    def view_all_contracts(self):
        return self.database.view_information_about_tables("Contracts")

    def view_contract_indexes(self):
        return self.database.view_indexes_in_table("contract_id", "contracts")

    def view_contracts(self, status):
        return self.database.view_contracts_with_selected_status(f"{status}")

    def view_project_name(self, contract_id):
        return self.database.view_table_value_with_search_term("project", "contracts", "contract_id", contract_id)[0][0]

    def view_id_with_project_name(self, project_name):
        return self.database.view_table_value_with_search_term("contract_id", "contracts", "project", project_name)

    def add_contract(self, name_of_contract):
        self.contract_name = name_of_contract
        self.database.insert_information_into_contract_table(self.contract_name,
                                                             self.date_of_creation_contract,
                                                             self.date_of_signing,
                                                             self.project)

    def confirmation_of_the_contract(self, contract_id):
        self.database.update_table_value("contracts", "status", "Active", "contract_id", contract_id)
        self.database.update_table_value("contracts", "date_of_signing", datetime.date.today(), "contract_id",
                                         contract_id)

    def completion_of_the_contract(self, project_name, contract_id):
        self.database.update_table_value("contracts", "status", "Completed", "contract_id", contract_id)
        self.database.update_table_value("contracts", "project", project_name, "contract_id", contract_id)

    def add_contract_to_project(self, project_name, contract_id):
        self.database.update_table_value("contracts", "project", project_name, "contract_id", contract_id)

    def status_check(self, contract_id):
        return self.database.view_table_value_with_search_term("status", "contracts", "contract_id", contract_id)[0][0]

    def check_repeating_contract_name(self, name):
        return self.database.repeating_name("contracts", "contract_name", name)
