from suds.client import Client

from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def get_project_list(self):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        projects_list = []
        for row in client.service.mc_projects_get_user_accessible("administrator", "root"):
            projects_list.append(Project(name=row.name, id=row.id))
        return projects_list
