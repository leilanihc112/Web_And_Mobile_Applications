"""
create_new_post_page.py

Generate New Post template.
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
                    text("Create Post")
                # horizontal divider
                doc.stag("hr")
                with tag("div", klass="content", style = "max-width: 750px; margin: auto; \
                        background: #4f4f4f; padding: 20px; justify-content: center; \
                        align-items: center; position:relative; top:50px; border-radius: 25px;"):
                    # form to add a new post
                    with tag("form", method="POST",action="/add_post/",
                                enctype="multipart/form-data"):
                        with tag("div"):
                            with tag("div"):
                                # header information
                                with tag("p",  id = "PostInformation",
                                    style = "width:50%; font-size: 14;"):
                                    text("Fields marked with an * are required")
                                    # hidden uuid to prevent duplicate posts in a row
                                    doc.stag("input", name = "uuid_form",
                                            type = "hidden", value="{{ uuid_form }}",
                                    readonly= "readonly", style = "width:50%; height:30px;")
                                # stand name
                                with tag("p",  id = "StandNameLabel",
                                         style = "width:50%; font-size: 18;"):
                                    text("Stand Name")
                                    doc.stag("input", name = "StandName",
                                            type = "text", value="{{ stand_name }}",
                                    readonly= "readonly", style = "width:50%; height:30px;")
                                    doc.stag("input", name = "stand_id",
                                             type = "hidden", value="{{ stand_id }}")
                                # post tags
                                with tag("p",  id = "PostTagsLabel",
                                         style = "width:75%; font-size: 18;"):
                                    text("Post Tags")
                                    doc.stag("input", name = "PostTags",
                                            type = "text", placeholder="Add Post Tags",
                                    style = "width:60%; height:30px;")
                        # post title
                        with tag("div"):
                            with tag("p", id = "PostTitleLabel",
                                     style = "font-size: 18; width:50%;"):
                                text("*Post Title")
                                doc.stag("input", name = "PostTitle",
                                        type = "text", placeholder="Add Post Title",
                                        required="true",style = "width:125%; height:30px;")
                        # post description
                        with tag("div"):
                            with tag("p", id = "PostDescriptionLabel",
                                     style = "width:25%, font-size: 18, height:50px;"):
                                text("*Post Description")
                                with tag("textarea", name = "post_description",
                                    rows="6",cols="100",required="true",
                                    style="min-height: 80px;max-height: 130px;min-height: 80px;"
                                    "max-width:90%;min-width:25%;"):
                                    pass
                            # post images
                            with tag("p", id = "PostImagesLabel",
                                    style = "font-size: 18; width:50%;"):
                                text("Post Images")
                                doc.stag("input", type="file", id="files", name="post_images",
                                         accept="image/*", multiple="true")
                        # submit and cancel buttons
                        with tag("div"):
                            doc.stag("input", type="submit",
                                     style="float: right;text-align: right;")
                            doc.stag("input", type="button", value="Cancel",
                                onclick="cancel_click()",
                                style="float: right;text-align: right; margin-right: 10px;")

    with tag("script", src = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.js"):
        text("")
    doc.stag("link", type = "text/css", rel = "stylesheet",
         href = "https://www.gstatic.com/firebasejs/ui/4.4.0/firebase-ui-auth.css")
    with tag("script", type = "module", src = "{{ url_for('static', filename='login.js') }}"):
        text("")
    with tag("script"):
        text("function cancel_click() {window.location.href  = '/view/stand/{{ stand_id }}/0/5'}")

with open("templates/create_post.html", "w", encoding="utf8") as file:
    file.write(indent(doc.getvalue(),indent_text=True))
    file.close()
