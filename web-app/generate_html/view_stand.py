"""
view_stand.py

Generate View Stand page template.
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
                # Start stand header
                with tag("h3"):
                    text("{{ stand_name }}")
                    with tag("div", id="StandImage"):
                        doc.stag("img", src="{{ image_name }}",
                                 alt="Stand", style="width:auto;padding:20px;")
                    with tag("p", style="font-size: 14; padding-left: 10px"):
                        text("Created by: {{ creator }}")
                    text(" {% if user_is_subscribed %} ")
                    with tag("button", klass="unsubscribe_button", style="padding: 3px 5px;",
                             onclick="unsubscribe('{{ stand_id }}', '0', '{{ max_per_page }}' )"):
                        text("Unsubscribe")
                    text(" {% else %} ")
                    with tag("button", klass="subscribe_button", style="padding: 3px 5px;",
                             onclick="subscribe('{{ stand_id }}', '0', '{{ max_per_page }}')"):
                        text("Subscribe")
                    text(" {% endif %} ")

                    with tag("button", klass="create_post_button", style="padding: 3px 5px;",
                             onclick="create_post('{{ stand_id }}')"):
                        text("Create Post")
                    with tag("p", style="font-size: 14"):
                        text("Hours: {{ time }}")
                    with tag("p", style="font-size: 14"):
                        text("Location: {{ location[0] }}, {{ location[1] }}")
                    with tag("p", style="font-size: 14"):
                        text("Inventory list: ")
                    with tag("ul", style="background-color: #ffffff; width: 100px; \
                             height: 150px; overflow-y: auto; font-size:14"):
                        text("{% for inventory_item in inventory_list %}")
                        with tag("li", style="display:inline; padding-left:0px;\
                                 padding-right:1px;color:#252526;"):
                            text("{{ inventory_item }}")
                            doc.stag("br")
                        text("{% endfor %}")
                doc.stag("br")
                # End stand header

                # Posts, displays 5 max
                with tag("h3"):
                    text("Posts")
                doc.stag("hr")
                doc.stag("br")
                doc.stag("br")
                text("{% for idx in range(posts_display_count) %}")
                with tag("div", style="width: 96%;margin:auto;"):
                    # Posts with images
                    with tag("div", style="width: 96%;float: left;"):
                        # User, date, text, and tags
                        with tag("p", id="Post"):
                            with tag("b"):
                                text("{{ posts_to_display[idx][\"title\"] }}")
                        with tag("p", id="PostUser", style="font-size: 14"):
                            text("{{ post_users[idx] }}")
                        with tag("p", id="PostDate", style="font-size: 14"):
                            text("{{ post_hours[idx] }}")
                        with tag("p", id="PostText"):
                            text("{{ posts_to_display[idx][\"text\"] }}")
                        with tag("p", id="PostTags"):
                            with tag("ul", style="padding-left: 0pt; font-size: 14;"):
                                text("{% for tag in posts_to_display[idx][\"tags\"]%}")
                                with tag("li", style="display:inline; padding-right:5px"):
                                    with tag("a", href="/search/{{ tag }}/0/10"):
                                        text("#{{ tag }}")
                                text("{% endfor %}")
                        doc.stag("br")
                        text("{% if post_image_names[idx] %}")
                        # Photo carousel for multiple images on a post
                        with tag("div", klass="scrollmenu", id="PostImages",
                                 style="overflow: auto; white-space: nowrap;"):
                            text("{% for images in range(post_image_count[idx])%}")
                            doc.stag("img", src="{{ post_image_names[idx][images] }}", 
                            alt="Post", style="padding-bottom: 20px; padding-right: 5px;")
                            text("{% endfor %}")
                        text("{% endif %}")
                doc.stag("hr")
                doc.stag("br")
                doc.stag("br")
                text("{% endfor %}")
                # If a stand has no posts, display a message instead
                text("{% if post_count == 0 %}")
                with tag("div", style="width: 96%;margin:auto;"):
                    with tag("p", id="Post"):
                        with tag("b"):
                            text("No posts for this stand yet.")
                doc.stag("br")
                doc.stag("br")
                doc.stag("hr")
                text("{% endif %}")
                with tag("h3"):
                    # Prev posts (up to last 5)
                    with tag("div", style="width: 20%; float: left;text-align: center;"):
                        text(" {% if prev_post_link %} ")
                        with tag("button", klass="posts_buttons",
                                 onclick="prevPosts( '{{ stand_id }}', {{ last_post_index }}, {{ post_count }}, {{ max_per_page }} )"):
                            text("Prev")
                        text(" {% endif %}")
                    with tag("div", style="width: 20%; float: center;text-align: center; \
                                                    margin-left: auto;"):
                    # Next posts (up to next 5)
                        text(" {% if next_post_link %} ")
                        with tag("button", klass="posts_buttons",
                                 onclick="nextPosts( '{{ stand_id }}', {{ last_post_index }}, {{ post_count }}, {{ max_per_page }} )"):
                            text("Next")
                        text(" {% endif %}")
        with tag("script"):
            text("function create_post(stand_id) \
                 {window.location.href = '/create_post/' + stand_id;}")
    with tag("script"):
        text("function create_post(stand_id) {window.location.href = '/create_post/' + stand_id;}")
    with tag("script", src = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.js"):
        text("")
    doc.stag("link", type = "text/css", rel = "stylesheet",
             href = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.css")
    with tag("script", type = "module", src = "{{ url_for('static', filename='login.js') }}"):
        text("")
    with tag("script", src = "{{ url_for('static', filename='stands.js') }}"):
        text("")

with open('templates/view-stand.html', 'w', encoding="utf8") as file:
    file.write(indent(doc.getvalue(), indent_text=True))
    file.close()
