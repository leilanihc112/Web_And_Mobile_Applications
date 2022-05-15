"""
view_all_stands.py

Generate View All Stands page template.
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
                    text("View All Stands")
                doc.stag("hr")
                # Stands
                with tag("h3"):
                    with tag("div", style="width: 100%;"):
                        text("{% for idx in range(stand_list_count) %}")
                        with tag("div", style="width: 33%;float: left;"):
                            # Stand name and link to stand page, image, and hours
                            with tag("div"):
                                with tag("a", href="/view/stand/{{ all_stand_ids[idx] }}/0/{{ max_posts_per_page }}/",
                                         style="padding: 20px;font-family:Helvetica;"):
                                    text("{{ all_stand_names[idx] }}")
                            with tag("div", id="StandImage"):
                                doc.stag("img",
                                         src="{{ all_stand_images[idx] }}",
                                         alt="Stand", style="width:auto;padding:20px;")
                            with tag("div", id="StandTime",
                                     style="padding: 20px;font-family:Helvetica; font-size: 14"):
                                text("Hours: {{ all_stand_times[idx] }}")
                                doc.stag("br")
                                text("Location: {{ all_stand_locations[idx] }}")
                        # stand end
                        text("{% endfor %}")
                doc.stag("hr")

                with tag("h3"):
                    # Prev stands (up to last 3)
                    with tag("div", style="width: 20%; float: left;text-align: center;"):
                        text(" {% if prev_stands_link %} ")
                        with tag("button", klass="stands_buttons",
                                 onclick="prevStands( {{ last_stand_index }}, \
                                        {{ all_stand_count }}, {{max_stands_per_page}} )"):
                            text("Prev")
                        text(" {% endif %}")
                    # Next stands (up to next 3)
                    with tag("div", style="width: 20%; float: center;text-align: center; \
                                margin-left: auto;"):
                        text(" {% if next_stands_link %} ")
                        with tag("button", klass="stands_buttons",
                                 onclick="nextStands( {{ last_stand_index }}, \
                                 {{ all_stand_count }}, {{max_stands_per_page}} )"):
                            text("Next")
                        text(" {% endif %}")
    with tag("script", src = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.js"):
        text("")
    doc.stag("link", type = "text/css", rel = "stylesheet",
             href = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.css")
    with tag("script", type = "module", src = "{{ url_for('static', filename='login.js') }}"):
        text("")
    with tag("script", src = "{{ url_for('static', filename='stands.js') }}"):
        text("")

with open("templates/view-all-stands.html", "w", encoding="utf8") as file:
    file.write(indent(doc.getvalue(), indent_text=True))
    file.close()
