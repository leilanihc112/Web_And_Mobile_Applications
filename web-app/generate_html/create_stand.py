"""
create_stand.py

Generate Create Stand template.
"""
import sys
from yattag import Doc, indent
from header import head, header_and_menu

sys.path.insert(0, "../templates")
doc, tag, text = Doc().tagtext()

with tag("html"):
    head(doc, tag, text)
    with tag("body"):
        header_and_menu(tag, text)
        with tag("div", klass="body_sec"):
            with tag("section", id="Content"):
                with tag("h3"):
                    text("Create Stand")
                # horizontal divider
                doc.stag("hr")
                with tag("div", klass="content", style = "max-width: 750px; margin: auto; \
                    background: #4f4f4f; padding: 20px; justify-content: center; \
                    align-items: center; position:relative; top:50px; border-radius: 25px;"):
                    # Form to add new stqands
                    with tag("form", enctype="multipart/form-data", method="post"):
                        with tag("div"):
                            with tag("p",  id = "Information", style = "font-size: 14;"):
                                text("Fields marked with an * are required")
                            with tag("label", style = "color:red; display: \
                            {{ hidden_value7 }}"):
                                text("Stand with this information already exists. Please enter \
                                different information.")
                            # Stand name
                            with tag("p",  id = "StandNameLabel", style = "font-size: 18;"):
                                text("*Stand Name")
                            with tag("div"):
                                text("{% if show_val %}")
                                doc.stag("input", name = "StandName", type = "text",
                                placeholder="Insert a stand name", style = "width:100%; \
                                height:30px;", value="{{ request.form['StandName'] }}")
                                text("{% else %}")
                                doc.stag("input", name = "StandName", type = "text",
                                placeholder="Insert a stand name", style = "width:100%; \
                                height:30px;")
                                text("{% endif %}")
                                with tag("label", style = "color:red; display: \
                                {{ hidden_value5 }}"):
                                    text("Input a name for the stand")
                        # Location text fields (Latitutde and Longitude)
                        with tag("div"):
                            with tag("p", id = "Location", style = "font-size: 18;"):
                                text("*Location")
                            with tag("div"):
                                text("{% if show_val %}")
                                doc.stag("input", name = "Latitude", type = "text",
                                placeholder="Latitude", style = "width:50%; height:30px;",
                                value="{{ request.form['Latitude'] }}")
                                text("{% else %}")
                                doc.stag("input", name = "Latitude",
                                type = "text", placeholder="Latitude", style =
                                "width:50%; height:30px;")
                                text("{% endif %}")
                                with tag("label", style = "color:red; display: \
                                {{ hidden_value1 }}"):
                                    text("Value must be between -90 and 90")
                                text("{% if show_val %}")
                                doc.stag("input", name = "Longitude",
                                type = "text", placeholder="Longitude", style =
                                "width:50%; height:30px;", value="{{ request.form['Longitude'] }}")
                                text("{% else %}")
                                doc.stag("input", name = "Longitude",
                                type = "text", placeholder="Longitude", style =
                                "width:50%; height:30px;")
                                text("{% endif %}")
                                with tag("label", style = "color:red; display: \
                                {{ hidden_value2 }}"):
                                    text("Value must be between -180 and 180")
                        # Inventory List
                        with tag("div"):
                            with tag("p", id = "InventoryLabel", style =
                            "font-size: 18;"):
                                text("Inventory (separate items by comma)")
                            text("{% if show_val %}")
                            doc.stag("input", name = "Inventory", type = "text",
                            placeholder="Insert item", style = "width:100%; \
                            height:30px;", value="{{ request.form['Inventory'] }}")
                            text("{% else %}")
                            doc.stag("input", name = "Inventory", type = "text",
                            placeholder="Insert item", style = "width:100%; \
                            height:30px;")
                            text("{% endif %}")
                        # Date input field for opening
                        with tag("div"):
                            with tag("p", id = "Opens", style = "font-size: 18;"):
                                text("*Opens")
                            text("{% if show_val %}")
                            doc.stag("input", name = "OpenDate", type = "datetime-local",
                            style = "width:50%; height:30px;", value="{{ \
                            request.form['OpenDate'] }}")
                            text("{% else %}")
                            doc.stag("input", name = "OpenDate", type = "datetime-local",
                            style = "width:50%; height:30px;")
                            text("{% endif %}")
                            with tag("label", style = "color:red; display: \
                            {{ hidden_value3 }}"):
                                text("Input Date")
                        # Date input field for closing
                        with tag("div"):
                            with tag("p", id = "Closes", style = "font-size: 18;"):
                                text("*Closes")
                            text("{% if show_val %}")
                            doc.stag("input", name = "CloseDate", type = "datetime-local",
                            style = "width:50%; height:30px;", value="{{ \
                            request.form['CloseDate'] }}")
                            text("{% else %}")
                            doc.stag("input", name = "CloseDate", type = "datetime-local",
                            style = "width:50%; height:30px;")
                            text("{% endif %}")
                            with tag("label", style = "color:red; display: \
                            {{ hidden_value4 }}"):
                                text("Input Date")
                            with tag("label", style = "color:red; display: \
                            {{ hidden_value6 }}"):
                                text("Open must be before close")
                        # Post image
                        with tag("div"):
                            with tag("p", id = "Image", style = "font-size: 18;"):
                                text("Image")
                            doc.stag("input", type="file", id="files", name="img",
                            accept="image/*", multiple="false")
                            # Submit button
                            doc.stag("input", type="submit", value="Done",
                            style="float: right;text-align: right;")

    with tag("script", src = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.js"):
        text("")
    doc.stag("link", type = "text/css", rel = "stylesheet", href =
    "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.css")
    with tag("script", type = "module", src = "{{ url_for('static', filename='login.js') }}"):
        text("")
    with tag("script"):
        text("if ('{{ alert }}' == 'True') { \
                window.alert('Stand added successfully'); \
                window.location.href('/create_stand/'); \
                }")

with open("templates/createStand.html", "w", encoding="utf8") as file:
    file.write(indent(doc.getvalue(), indent_text=True))
    file.close()
