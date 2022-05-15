"""
header.py

Generate template Header for the application.
"""

def head(doc, tag, text):
    """ General CSS format for the web application """
    with tag("head"):
        with tag("title"):
            text("Merchable")
        with tag("style"):
            doc.asis(".head1 {font-size: 40px; color: #59bfff; font-weight: bold; margin-top: \
            20px; font-family: Helvetica;}")
            doc.asis("margin {0 auto; background-position: center; background-size: contain;}")
            doc.asis(".menu {position: sticky; top: 0; background-color: #59bfff; padding:10px \
            0px 10px 0px; color: white; margin-top: 20px; overflow: hidden;}")
            doc.asis(".menu a {float: left; color: white; text-align: center; padding: 14px 16px; \
                     text-decoration: none; font-size: 20px; font-family: Helvetica;}")
            doc.asis(".body_sec {margin-left: 20px; font-family: Helvetica; color: white;}")
            doc.asis(".menu-log {right: auto; float: right;}")
            doc.asis("a:link {color: #59bfff;}")
            doc.asis("a:visited {color: #e1affd;}")
            doc.asis(".management_buttons {outline: none; background-color: transparent; cursor: \
            pointer; color: #59bfff; background-repeat: no-repeat; border: none; text-decoration:\
            underline; display:inline-block; font-size: 16; font-family:Helvetica;}")
            doc.asis("img {width: 250px; height: 250px; max-width: 250px; max-height: 250px; \
            object-fit: cover;}")
            doc.asis("hr {display: inline-block; width: 100%;}")
            doc.asis("body {background-color: #252526;}")
            doc.asis("div#StandImage {overflow: hidden;}")
            doc.asis("div#StandImage1 {overflow: hidden;}")
            doc.asis("div#StandImage2 {overflow: hidden;}")
            doc.asis("div#StandImage3 {overflow: hidden;}")

def header_and_menu(tag, text):
    """ Header and Menu that will appear on every page """
    with tag("header"):
        with tag("div", klass = "head1"):
            text("Merchable")
    # navigation bar
    with tag("div", klass = "menu"):
        with tag("a", href = "{{ url_for('management_main', post_index=0, stand_first_index=0, \
        stand_second_index=3) }}", style = "color: white;"):
            text("Manage")
        with tag("a", href = "/create_stand", style = "color: white;"):
            text("Create Stand")
        with tag("a", href = "{{ url_for('view_all_stands', stand_first_index=0, \
        stand_second_index=3) }}", style = "color: white;"):
            text("View All Stands")
        with tag("a", href = "/search", style = "color: white;"):
            text("Search Posts")
        with tag("div", klass = "menu-log"):
            with tag("button", id = "sign-out", style = "outline: none; background-color: \
            transparent; cursor: pointer; color: white; background-repeat: no-repeat; border: \
            none; display:inline-block; font-size: 24; font-family:Helvetica; padding: 12px 10px;"):
                text("LOGOUT")
