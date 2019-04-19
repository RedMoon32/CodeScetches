from django.contrib.admin import AdminSite

SITE_NAME = 'Innopoints'


class InnopointsAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = SITE_NAME

    # Text to put in each page's <h1> (and above loginapp form).
    site_header = SITE_NAME

    # Text to put at the top of the admin index page.
    index_title = SITE_NAME


admin_site = InnopointsAdminSite()
