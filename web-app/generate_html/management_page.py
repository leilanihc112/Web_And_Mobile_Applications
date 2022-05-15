"""
management_page.py

Generate management page template.
"""
import sys
from yattag import Doc, indent
from header import head, header_and_menu

sys.path.insert(0, "../templates")
doc, tag, text = Doc().tagtext()

with tag("html", id = "manage_content"):
    head(doc, tag, text)
    with tag("body"):
        header_and_menu(tag, text)
        with tag("div", klass = "body_sec"):
            with tag("section", id = "Content"):
                with tag("h3"):
                    text("Manage your content")
                # horizontal divider
                doc.stag("hr")
                with tag("h3"):
                    text("Your posts")
                # post
                with tag("div", id = "your_posts", style = "width: 96%;margin:auto;"):
                    text(" {% if prev_post_link %} ")
                    # prev button - only show if necessary
                    with tag("div", style = "width: 24%; float: left; \
                    padding:100px 0;text-align: right;"):
                        with tag("a", id = "prev_post", klass = "prev_post", href =
                        "{{ url_for('management_main', stand_first_index=first_stand_index, \
                        post_index=post_index-1, stand_second_index=last_stand_index) }}"):
                            text("Prev post")
                    text("{% else %}")
                    text("{% if post_link %}")
                    with tag("div", style = "width: 24%; float: left; padding:100px 0; \
                    text-align: right;"):
                        text("")
                    text("{% else %}")
                    with tag("div", style = "width: 24%; float: left;"):
                        text("")
                    text(" {% endif %} ")
                    text(" {% endif %} ")
                    # posts
                    with tag("div", style = "width: 24%; float: left;"):
                        text(" {% if post_link %} ")
                        doc.stag("img", id = "StandImage", src = "{{ stand_image }}", 
                        alt = "Stand", style = "float: right;display:\
                        block;padding-right: 20px;padding-bottom: 20px;")
                        text(" {% endif %} ")
                    with tag("div", style = "width: 24%; float: left;"):
                        text(" {% if post_link %} ")
                        with tag("p", id = "StandName", style = "font-size: 18;"):
                            with tag("b"):
                                text("{{ stand_name }}")
                        with tag("p", id = "PostName"):
                            with tag("b"):
                                text("{{ post[\"title\"] }}")
                        with tag("p", id = "PostDate", style = "font-size: 12;"):
                            text("{{ post_timestamp }}")
                        with tag("p", id = "PostText"):
                            text("{{ post[\"text\"] }}")
                        text(" {% endif %} ")
                    # next button - only show if necessary
                    text(" {% if next_post_link %} ")
                    with tag("div", style = "width: 24%; float: right;padding:100px 0; \
                    text-align: left;"):
                        with tag("a", id = "next_post", klass = "next_post", href =
                        "{{ url_for('management_main', stand_first_index=first_stand_index, \
                        post_index=post_index+1, stand_second_index=last_stand_index) }}"):
                            text("Next post")
                    text(" {% else %} ")
                    text("{% if post_link %}")
                    with tag("div", style = "width: 24%; float: right; \
                    padding:100px 0;text-align: left;"):
                        text("")
                    text("{% else %}")
                    with tag("div", style = "width: 24%; float: right;"):
                        text("")
                    text(" {% endif %} ")
                    text(" {% endif %} ")
                # horizontal divider
                doc.stag("hr")
                with tag("h3"):
                    text("Subscribed stands")
                # stands
                with tag("div", id = "subscribed_stands", style="width: 100%;"):
                    # prev link - only show if necessary
                    with tag("div", style = "width: 20%; float: left;padding:150px 0; \
                    text-align: center;"):
                        text(" {% if prev_stands_link %} ")
                        with tag("a", id = "prev_stand", klass = "prev_stand", href =
                        "{{ url_for('management_main', stand_first_index=first_stand_index-3, \
                        post_index=post_index, stand_second_index=last_stand_index-3) }}"):
                            text("Prev")
                        text(" {% endif %} ")
                    # put 3 stands next to each other
                    text("{% for num in range(num_stands) %}")
                    with tag("div", style="width: (60/{{ num }})%;float: left;"):
                        with tag("div"):
                            with tag("a", href = "/view/stand/{{ stands_id[num] }}/0/{{max_posts_per_page}}/",
                            style = "padding:20px;"):
                                text("{{ stands_name[num] }}")
                        with tag("div"):
                            doc.stag("img", src ="{{ stands_photo[num] }}",
                            alt = "Stand", style = "width:auto;padding:20px;")
                        with tag("div"):
                            with tag("button", klass = "management_buttons", onclick =
                            "unsubscribeStand('{{ stands_id[num] }}', \
                            {{ post_index }}, {{ first_stand_index }}, \
                            {{ last_stand_index }})", style = "padding: 20px;"):
                                text("unsubscribe")
                    text("{% endfor %}")
                    # next link - only show if necessary
                    with tag("div", style = "width: 20%; float: right;padding:150px 0; \
                    text-align: left;"):
                        text(" {% if next_stands_link %} ")
                        with tag("a", id = "next_stand", klass = "next_stand", href =
                        "{{ url_for('management_main', stand_first_index=first_stand_index+3, \
                        post_index=post_index, stand_second_index=last_stand_index+3) }}"):
                            text("Next")
                        text(" {% endif %} ")

    with tag("script", src = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.js"):
        text("")
    doc.stag("link", type = "text/css", rel = "stylesheet", href =
    "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.css")
    with tag("script", type = "module", src = "{{ url_for('static', filename='login.js') }}"):
        text("")
    with tag("script", src = "https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"):
        text("")
    with tag("script", src = "{{ url_for('static', filename='management.js') }}"):
        text("")

with open("templates/management.html", "w", encoding="utf8") as file:
    file.write(indent(doc.getvalue(), indent_text = True))
    file.close()
