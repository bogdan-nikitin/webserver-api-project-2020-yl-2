import os
import markdown

opening_lines = ['{%extends "docs.jinja2" %}\n',
                 '{% block docs %}\n',
                 '<div class="container">\n']
completion_lines = ['\n',
                    '</div>\n',
                    '{% endblock %}']


def markdown_to_html(root, file_to_convert, path):
    md_file = open(os.path.join(root, file_to_convert), 'r')
    all_file = ''
    for line in md_file.readlines():
        all_file += line + '\n'
    md_file.close()
    html = markdown.markdown(all_file)
    html_file = open(os.path.join(root, path), 'w')
    html_file.writelines(opening_lines)
    html_file.write(html)
    html_file.writelines(completion_lines)
    html_file.close()
