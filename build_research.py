#!/usr/bin/env python3
"""
Regenerates research.html from research.json.
Run from the repo root: python3 build_research.py
"""

import json
import html as html_module

with open("research.json", encoding="utf-8") as f:
    data = json.load(f)


def esc(text):
    return html_module.escape(str(text))


def coauthor_html(coauthors):
    if not coauthors:
        return ""
    parts = []
    for i, a in enumerate(coauthors):
        name = esc(a["name"])
        if a.get("url"):
            parts.append(f'<a href="{esc(a["url"])}" target="_blank">{name}</a>')
        else:
            parts.append(name)
    if len(parts) == 1:
        joined = parts[0]
    elif len(parts) == 2:
        joined = f"{parts[0]} and {parts[1]}"
    else:
        joined = ", ".join(parts[:-1]) + f", and {parts[-1]}"
    return f'<small>with {joined}</small>'


def extra_links_html(extra_links):
    if not extra_links:
        return ""
    parts = []
    for link in extra_links:
        parts.append(f'<a href="{esc(link["url"])}" target="_blank"><small>[{esc(link["label"])}]</small></a>')
    return " ".join(parts)


def paper_html(paper, show_abstract=True):
    lines = []
    title = esc(paper["title"])
    if paper.get("url"):
        lines.append(f'\t\t<a href="{esc(paper["url"])}" target="_blank"><strong>{title}</strong></a><br>')
    else:
        lines.append(f'\t\t<strong>{title}</strong><br>')

    coauth = coauthor_html(paper.get("coauthors", []))
    extra = extra_links_html(paper.get("extra_links", []))
    venue = f'<small>{esc(paper["venue"])}</small>' if paper.get("venue") else ""
    note = f'<small>{esc(paper["note"])}</small>' if paper.get("note") else ""

    meta_parts = [p for p in [coauth, venue, extra, note] if p]
    if meta_parts:
        lines.append("\t\t" + " ".join(meta_parts) + "<br>")

    if show_abstract and paper.get("abstract"):
        label = esc(paper.get("accordion_label", "Abstract"))
        lines.append(f'\t\t<button class="accordion">{label}</button>')
        lines.append('\t\t<div class="panel">')
        lines.append(f'\t\t\t<p class="abstract">{esc(paper["abstract"])}</p>')
        lines.append('\t\t</div>')

    return "\n".join(lines)


def works_in_progress_html(items):
    lines = ['\t<div class="paper">',
             '\t<strong> Works in Progress</strong>',
             '\t<ul>']
    for item in items:
        title = esc(item["title"])
        coauth = coauthor_html(item.get("coauthors", []))
        if coauth:
            lines.append(f'\t\t<li>{title}<br> {coauth}</li>')
        else:
            lines.append(f'\t\t<li>{title}</li>')
    lines += ['\t</ul>', '\t</div>']
    return "\n".join(lines)


def section_html(heading, papers):
    lines = ['\t<div class="paper">',
             f'\t<strong> {esc(heading)} </strong>']
    for p in papers:
        lines.append('\t<div class="paper">')
        lines.append(paper_html(p))
        lines.append('\t</div>')
    lines.append('\t</div>')
    return "\n".join(lines)


HEADER = """\
<!DOCTYPE html>
<html>

<head>
\t<meta charset="UTF-8">

\t<title>Research — Jacob Howard</title>
\t<meta name="description" content="Economics research by Jacob Howard: working papers and publications on international trade, supply chains, export controls, and production networks.">
\t<meta name = "keywords"  content = "economics, international trade, international economics, trade, boulder, labor, supply chains, trade war, jacobhowardecon, jacob howard economics, production networks, jacob howard, jacob, howard, colorado, boulder, cu, mitre, washington, washington dc, dc, virginia, washington d.c.">
\t<meta http-equiv = "author" content = "Jacob Howard"/>
\t<meta http-equiv = "pragma" content = "no-cache"/>
\t<meta name="viewport" content="width=device-width, initial-scale=1.0">
\t<meta name="google-site-verification" content="Q_jVWH0uFlSfWMEw8Qh0WWSQ347NZSNOxAUKobfq2U0" />

\t<!-- Open Graph / Social Media -->
\t<meta property="og:type" content="website">
\t<meta property="og:url" content="https://jacobhowardecon.github.io/research">
\t<meta property="og:title" content="Research — Jacob Howard">
\t<meta property="og:description" content="Working papers and publications on international trade, supply chains, export controls, and production networks.">
\t<meta property="og:image" content="https://jacobhowardecon.github.io/photos/Mesa_Arch.jpg">
\t<meta name="twitter:card" content="summary_large_image">
\t<meta name="twitter:title" content="Research — Jacob Howard">
\t<meta name="twitter:description" content="Working papers and publications on international trade, supply chains, export controls, and production networks.">
\t<meta name="twitter:image" content="https://jacobhowardecon.github.io/photos/Mesa_Arch.jpg">

\t<link rel="icon" type="image/png" href="photos/favicon-256.png">
\t<link href="research.css" type="text/css" rel="stylesheet">
\t<link href="footer.css" type="text/css" rel="stylesheet">
\t<link href="navbar_alt.css" type="text/css" rel="stylesheet">
\t<link href="fonts.css" type="text/css" rel="stylesheet">
\t<link rel="stylesheet" href="css/all.min.css">
\t<link href="theme.css" type="text/css" rel="stylesheet">
</head>

<body>
\t<div class="landing-wrapper">
\t<div class="fixed_topnav">
\t <div class="topnav">
\t\t <div class="topnav-left">
\t\t\t<a href="/index" class="logo">Jacob Howard</a>
\t\t </div>
\t\t<div class="topnav-right" id="myTopnav">
\t\t <a href="/index">Home</a>
\t\t <a href="/research">Research</a>
\t\t <a href="/docs/CV.pdf" target="_blank">CV</a>
\t\t <!-- <a href="/teaching">Teaching</a> -->
\t\t <a href="/advice">Resources</a>
\t\t <a href="javascript:void(0);" class="icon" onclick="openNav()">
\t\t\t <i class="fa-solid fa-bars"></i></a>
\t\t</div>
\t </div>
\t<div style="background-color: rgb(50,50,50); height:50px;"></div>
\t</div>
\t</div>

\t<div id="mySidenav" class="sidenav">
\t\t<a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
\t\t<a href="/index">Home</a>
\t\t<a href="/research">Research</a>
\t\t<a href="/docs/CV.pdf" target="_blank">CV</a>
\t\t<!-- <a href="/teaching">Teaching</a> -->
\t\t<a href="/advice">Resources</a>
\t</div>

\t<script>
\tfunction openNav() { document.getElementById("mySidenav").style.width = "250px"; }
\tfunction closeNav() { document.getElementById("mySidenav").style.width = "0"; }
\t</script>

<div class="article">

<div class="header">
<div class="boxed">
<h2>Economics Research</h2>
</div>
</div>
"""

FOOTER = """
<div class="footer">
<div class="column3of3">

<div class="cols">
\t<div> Affiliation </div>
\t<div class="br">
\t\t<a href="https://www.mitre.org" target="_blank">
\t\t\t<img class="social" loading="lazy" src="photos/mitre.svg"></a>
\t</div>
</div>
<div class="cols">
\t<div> Social </div>
\t<div class="br">
\t\t<a href="https://www.linkedin.com/in/jacob-howard-4301a738/" target="_blank">
\t\t\t<img class="social" loading="lazy" src="photos/linkedin.png"></a>
\t\t<a href="https://github.com/jacobhowardecon" target="_blank">
\t\t\t<img class="social" loading="lazy" src="photos/github-logo.png"></a>
\t</div>
</div>
<div class="cols">
\t<div> Contact </div>
\t<button onclick="copyStringToClipboard('jacob.b.howard@colorado.edu')">
\t\t<img class="social" loading="lazy" src="photos/email-filled-closed-envelope.png">
\t</button>
</div>
</div>
<p class="footer-disclaimer">The views expressed on this website are my own and do not necessarily reflect those of my employer.</p>
</div>

<script>
function copyStringToClipboard(str) {
\tvar el = document.createElement('textarea');
\tel.value = str;
\tel.setAttribute('readonly', '');
\tel.style = {position: 'absolute', left: '-9999px'};
\tdocument.body.appendChild(el);
\tel.select();
\tdocument.execCommand('copy');
\tdocument.body.removeChild(el);
\talert("Jacob's Email is Copied to your Clipboard");
}
</script>

<script>
var acc = document.getElementsByClassName("accordion");
for (var i = 0; i < acc.length; i++) {
\tacc[i].addEventListener("click", function() {
\t\tthis.classList.toggle("active");
\t\tvar panel = this.nextElementSibling;
\t\tpanel.style.display = (panel.style.display === "none") ? "block" : "none";
\t});
}
</script>

</body>
</html>
"""

body_parts = [HEADER]

# Economics research sections
body_parts.append('<div class="section">')
body_parts.append(works_in_progress_html(data["works_in_progress"]))
body_parts.append('</div>\n')

body_parts.append('<div class="section">')
body_parts.append(section_html("Working Papers", data["working_papers"]))
body_parts.append('</div>\n')

body_parts.append('<div class="section">')
body_parts.append(section_html("Publications", data["publications"]))
body_parts.append('</div>\n')

body_parts.append('</div>\n')  # close .article

# Projects section
body_parts.append("""<div class="header2">
<div class="boxed">
\t<h2>Projects, Grants, and Non-Economics Research</h2>
</div>
</div>

<div class="section">
<div class="paper">""")

for p in data["projects"]:
    body_parts.append(paper_html(p))

body_parts.append('</div>\n</div>\n')

body_parts.append(FOOTER)

output = "\n".join(body_parts)

with open("research.html", "w", encoding="utf-8") as f:
    f.write(output)

print("research.html rebuilt from research.json")
