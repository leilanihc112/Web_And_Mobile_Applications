"""
search_page.py

Generate Search page template.
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
                    # search bar
                    doc.stag("label", "Search")
                    doc.stag("input", type="search", id="tag-search", name="search_post",
                    value="{{ current_value }}")
                    doc.stag("input", type="button", value="Submit",
                    onclick="search_click({{ max_per_page }})")
                    doc.stag("hr")
                # posts - list the total count and the current posts shown in that count
                doc.stag("br")
                with tag("h3"):
                    text("Posts")
                    text("{% if post_count  %}")
                    text(" -  {{post_count}}")
                    doc.stag("br")
                    text("Displaying results {{search_first_index_plus}} to {{search_second_index}}")
                    text("{% endif %}")
                doc.stag("hr")
                doc.stag("br")
                doc.stag("br")

                # posts
                text("{% if post_count  %}")
                text("{% for idx in range(search_first_index, search_second_index) %}")
                with tag("div", style="width: 96%;margin:auto;"):
                    # display all of the posts
                    with tag("div", style="width: 96%;float: left;"):
                        with tag("a", href="/view/stand/{{ stand_ids[idx] }}/0/5",
                            style="font-family:Helvetica;"):
                            text("{{ post_stands_names[idx] }}")
                        with tag("p", id="Post"):
                            with tag("b"):
                                text("{{ posts[idx][\"title\"] }}")
                        with tag("p", id="PostUser", style="font-size: 14"):
                            text("{{ post_users[idx] }}")
                        with tag("p", id="PostDate", style="font-size: 14"):
                            text("{{ post_hours[idx] }}")
                        with tag("p", id="PostText"):
                            text("{{ posts[idx][\"text\"] }}")
                        with tag("p", id="PostTags"):
                            with tag("ul", style="padding-left: 0pt; font-size: 14;"):
                                text("{% for tag in posts[idx][\"tags\"]%}")
                                with tag("li", style="display:inline; padding-right:5px"):
                                    with tag("a", href="/search/{{ tag }}"):
                                        text("#{{ tag }}")
                                text("{% endfor %}")
                        # if there are images
                        text("{% if post_image_names[idx] %}")
                        doc.stag("br")
                        with tag("div", klass="scrollmenu", id="PostImages",
                                style="overflow: auto; white-space: nowrap;"):
                            text("{% for images in range(post_image_count[idx])%}")
                            doc.stag("img", src="{{ post_image_names[idx][images] }}",
                                    alt="Post", style="padding-bottom: 20px; padding-right: 5px;")
                            text("{% endfor %}")
                        text("{% endif %}")
                doc.stag("hr")
                doc.stag("br")
                text("{% endfor %}")

                # prev post link - only show if necessary
                with tag("div", style="width: 20%; float: left;text-align: center;"):
                    text(" {% if prev_button_link %} ")
                    with tag("button", klass="search_buttons",
                        onclick="prevPosts( {{ search_first_index }}, " + \
                        "{{ post_count }}, {{max_per_page}} )"):
                        text("Prev")
                    text(" {% endif %}")
                # next post link - only show if necessary
                with tag("div", style="width: 20%; float: center;text-align: center; "+\
                "margin-left: auto;"):
                        text(" {% if next_button_link %} ")
                        with tag("button", klass="search_buttons",
                            onclick="nextPosts( {{ search_second_index }}," + \
                            "{{ post_count }}, {{max_per_page}} )"):
                            text("Next")
                        text(" {% endif %}")                  
                text("{% endif %}")
    with tag("script", src = "{{ url_for('static', filename='search.js') }}"):
        text("")
    with tag("script", src = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.js"):
        text("")
    doc.stag("link", type = "text/css", rel = "stylesheet",
        href = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.css")
    with tag("script", type = "module", src = "{{ url_for('static', filename='login.js') }}"):
        text("")

with open("templates/search.html", "w", encoding="utf8") as file:
    file.write(indent(doc.getvalue(),indent_text=True))
    file.close()
