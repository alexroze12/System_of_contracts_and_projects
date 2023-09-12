import json
import pandas as pd
from Project import Project
from Contract import Contract


class ConsoleApp:
    def __init__(self):
        self.project = Project()
        self.contracts = Contract()

    @staticmethod
    def view_menus(key):
        with open("data_file.json", "r", encoding="utf-8") as read_file:
            list_of_numbering = []
            data = json.load(read_file)
            for i, k in enumerate(data[f"{key}"], 1):
                list_of_numbering.append(i)
                print(f"{i}. {k}")
            return list_of_numbering

    @staticmethod
    def check_the_correctness_of_the_number(data, numbering):
        return True if data.isdigit() and int(data) in numbering else False

    def check_input_project_indexes(self, project_id):
        numbering = self.project.view_project_indexes()
        if self.check_the_correctness_of_the_number(project_id, numbering):
            return True

    def check_input_contract_indexes(self, contract_id):
        numbering = self.contracts.view_contract_indexes()
        if self.check_the_correctness_of_the_number(contract_id, numbering):
            return True

    def main_menu(self):
        while True:
            print("Hello! Select operation to continue: ")
            main_numbering = self.view_menus("main_menu")
            temp = input("Your choice in the 'Main menu' menu: ")
            temp = int(temp) if self.check_the_correctness_of_the_number(temp, main_numbering) else print(
                "Please, enter a valid numeric value!")
            if temp == 1:
                project_numbering = self.view_menus("project_menu")
                self.project_menu(project_numbering)
            elif temp == 2:
                contract_numbering = self.view_menus("contract_menu")
                self.contract_menu(contract_numbering)
            elif temp == 3:
                print(pd.DataFrame((self.project.view_all_projects()),
                                   columns=['Id', 'Contact id', 'Name', 'Date of creation']))
            elif temp == 4:
                view_contract_numbering = self.view_menus("view_contract_menu")
                self.view_contract_menu(view_contract_numbering)
            elif temp == 5:
                break

    def project_menu(self, projects_numbering):
        while True:
            project_temp = input("Your choice in the 'Work with projects' menu:  ")
            project_temp = int(project_temp) if self.check_the_correctness_of_the_number(project_temp,
                                                                                         projects_numbering) else print(
                "Please, enter a valid numeric value!")
            if project_temp == 1:
                if len(self.contracts.view_contracts("Active")) == 0:
                    print("Projects cannot be created! No active contracts!")
                else:
                    name_of_project = input("Enter a name to create the project: ")
                    if self.project.check_repeating_project_name(name_of_project) == 0:
                        self.project.add_project(name_of_project)
                        print("The project was successfully created!")
                    else:
                        print("A project by that name already exists! Enter another name!")
            elif project_temp == 2:
                project_identifier = input("Enter the project number to which you want to add the contact: ")
                if not self.check_input_project_indexes(project_identifier):
                    print("There is no project with this id!")
                    continue
                elif len(self.project.view_all_projects()) == 0:
                    print("You cannot add a contract to a project because there are no projects available!")
                    continue
                elif len(self.project.view_contracts_in_project(project_identifier)) != 0:
                    print("This project already has an active contract! You can't add another contract!")
                    continue
                contract_identifier = input("Enter the contract number to add it to the project: ")
                if not self.check_input_contract_indexes(contract_identifier):
                    print("There is no contract with this id!")
                    continue
                if self.contracts.status_check(contract_identifier) != "Active":
                    print("The contract cannot be added, it is not active!")
                elif self.contracts.view_project_name(contract_identifier) is not None:
                    print("This contract is being used in another project!")
                else:
                    self.project.change_contract_links_in_project(contract_identifier, project_identifier)
                    project_name = self.project.view_project_name(project_identifier)
                    self.contracts.add_contract_to_project(project_name, contract_identifier)
                    print("The contract was successfully added to the project!")
            elif project_temp == 3:
                project_identifier = input("Enter the project number to finalize the contract belonging to this "
                                           "project: ")
                if not self.check_input_project_indexes(project_identifier):
                    print("There is no project with this id!")
                    continue
                project_name = self.project.view_project_name(project_identifier)
                if len(self.contracts.view_id_with_project_name(project_name)) == 0:
                    print("This project dose not have an active contract!")
                else:
                    contract_id = self.contracts.view_id_with_project_name(project_name)[0][0]
                    self.contracts.completion_of_the_contract(None, contract_id)
                    self.project.change_contract_links_in_project(None, project_identifier)
                    print("The contract has been successfully completed!")
            elif project_temp == 4:
                identifier = input(
                    "Enter the project number to view the current active contract for this project: ")
                if not self.check_input_project_indexes(identifier):
                    print("There is no project with this id!")
                    continue
                active_contract = self.project.view_contracts_in_project(identifier)
                if len(active_contract) == 0:
                    print("This project does not have an active contract!")
                else:
                    print(active_contract)
            elif project_temp == 5:
                print(pd.DataFrame((self.project.view_all_projects()),
                                   columns=['Id', 'Contact id', 'Name', 'Date of creation']))
            elif project_temp == 6:
                view_contract_numbering = self.view_menus("view_contract_menu")
                self.view_contract_menu(view_contract_numbering)
            elif project_temp == 7:
                break

    def contract_menu(self, contracts_numbering):
        while True:
            contract_temp = input("Your choice in the 'Work with contracts' menu:  ")
            contract_temp = int(contract_temp) if self.check_the_correctness_of_the_number(contract_temp,
                                                                                           contracts_numbering) else \
                print("Please, enter a valid numeric value!")
            if contract_temp == 1:
                contract_name = input("Enter the name of the contract to create it: ")
                if self.contracts.check_repeating_contract_name(contract_name) == 0:
                    self.contracts.add_contract(contract_name)
                    print("The contract has been successfully established!")
                else:
                    print("A contract by that name already exists! Enter another name!")
            elif contract_temp == 2:
                identifier = input("Enter the id of the contract you would like to confirm: ")
                if not self.check_input_contract_indexes(identifier):
                    print("There is no contract with this id!")
                    continue
                if self.contracts.status_check(identifier) == "Active":
                    print("This contract has already been confirmed!")
                else:
                    self.contracts.confirmation_of_the_contract(identifier)
                    print("Contract successfully confirmed!")
            elif contract_temp == 3:
                identifier = input("Enter the id of the contract you would like to finalize: ")
                if not self.check_input_contract_indexes(identifier):
                    print("There is no contract with this id!")
                    continue
                if self.contracts.status_check(identifier) == "Completed":
                    print("This contract has already been completed!")
                else:
                    self.contracts.completion_of_the_contract(None, identifier)
                    print("The contract has been successfully completed!")
            elif contract_temp == 4:
                print(pd.DataFrame((self.project.view_all_projects()),
                                   columns=['Id', 'Contact id', 'Name', 'Date of creation']))
            elif contract_temp == 5:
                view_contract_numbering = self.view_menus("view_contract_menu")
                self.view_contract_menu(view_contract_numbering)
            elif contract_temp == 6:
                break

    def view_contract_menu(self, view_menu_contracts_numbering):
        while True:
            view_contract_temp = input("Your choice in the 'View existing contracts' menu: ")
            view_contract_temp = int(view_contract_temp) if self.check_the_correctness_of_the_number(view_contract_temp,
                                                                                                     view_menu_contracts_numbering) else print(
                "Please, enter a valid numeric value!")
            if view_contract_temp == 1:
                print(pd.DataFrame((self.contracts.view_contracts("Draft")),
                                   columns=['Id', 'Name', 'Date of creation', 'Date of signing', 'Status',
                                            'Name of project']))
            elif view_contract_temp == 2:
                print(pd.DataFrame((self.contracts.view_contracts("Active")),
                                   columns=['Id', 'Name', 'Date of creation', 'Date of signing', 'Status',
                                            'Name of project']))
            elif view_contract_temp == 3:
                print(pd.DataFrame((self.contracts.view_contracts("Completed")),
                                   columns=['Id', 'Name', 'Date of creation', 'Date of signing', 'Status',
                                            'Name of project']))
            elif view_contract_temp == 4:
                print(pd.DataFrame((self.contracts.view_all_contracts()),
                                   columns=['Id', 'Name', 'Date of creation', 'Date of signing', 'Status',
                                            'Name of project']))
            elif view_contract_temp == 5:
                break


if __name__ == "__main__":
    consoleApp = ConsoleApp()
    consoleApp.main_menu()
