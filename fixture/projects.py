from model.project import Project


class ProjectsHelper:

    def __init__(self, app):
        self.app = app

    projects_cache = None

    def open_home_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("my_view_page.php"):
            wd.find_element_by_link_text("My View").click()

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_page.php"):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_xpath("//a[contains(text(),'Manage Projects')]").click()

    def create(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_xpath("//input[@value = 'Create New Project']").click()
        self.filing_in_the_fields(project)
        wd.find_element_by_xpath("//input[@value = 'Add Project']").click()
        self.open_manage_projects_page()
        self.projects_cache = None

    def filing_in_the_fields(self, project):
        self.change_field_value("name", project.name)
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def get_project_list(self):
        if self.projects_cache is None:
            wd = self.app.wd
            self.open_manage_projects_page()
            self.projects_cache = []
            for row in wd.find_elements_by_xpath(
                    "//table//a[contains(@href, 'proj_edit_page')]/ancestor::tr"):
                cells = row.find_elements_by_tag_name("td")
                name = cells[0].find_element_by_tag_name("a").text
                id = cells[0].find_element_by_tag_name("a").get_attribute("href").replace(
                    "http://localhost/mantisbt-1.2.20/manage_proj_edit_page.php?project_id=", "")
                self.projects_cache.append(Project(name=name, id=id))
        return list(self.projects_cache)

    def delete_by_index(self, index):
        wd = self.app.wd
        self.open_manage_projects_page()
        self.select_project_by_index(index)
        wd.find_element_by_xpath("//input[@value = 'Delete Project']").click()
        wd.find_element_by_xpath("//input[@value = 'Delete Project']").click()
        self.projects_cache = None

    def select_project_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_xpath("//table//a[contains(@href, 'proj_edit_page')]/ancestor::tr//a")[index].click()
