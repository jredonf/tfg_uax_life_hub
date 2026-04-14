from html import escape
from html.parser import HTMLParser

from django.utils.safestring import mark_safe


ALLOWED_TAGS = {
    "b",
    "blockquote",
    "br",
    "div",
    "em",
    "font",
    "h2",
    "h3",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "s",
    "strong",
    "strike",
    "u",
    "ul",
    "a",
}
VOID_TAGS = {"br", "img"}
ALLOWED_ALIGNMENTS = {"left", "center", "right"}
ALLOWED_ATTRS = {
    "a": {"href", "target", "rel"},
    "img": {"src", "alt"},
    "font": {"face", "size"},
    "p": {"style"},
    "div": {"style"},
    "h2": {"style"},
    "h3": {"style"},
}


def clean_url(value):
    value = value.strip()
    if value.startswith(("http://", "https://", "/")):
        return value
    return ""


def clean_style(value):
    declarations = []
    for declaration in value.split(";"):
        if ":" not in declaration:
            continue
        key, raw_value = [part.strip().lower() for part in declaration.split(":", 1)]
        if key == "text-align" and raw_value in ALLOWED_ALIGNMENTS:
            declarations.append(f"text-align: {raw_value}")
    return "; ".join(declarations)


class RichTextSanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if tag in ALLOWED_TAGS:
            safe_attrs = []
            for attr_name, attr_value in attrs:
                if attr_name not in ALLOWED_ATTRS.get(tag, set()):
                    continue
                if attr_name in {"href", "src"}:
                    attr_value = clean_url(attr_value or "")
                    if not attr_value:
                        continue
                elif attr_name == "style":
                    attr_value = clean_style(attr_value or "")
                    if not attr_value:
                        continue
                elif attr_name == "target":
                    attr_value = "_blank"
                elif attr_name == "rel":
                    attr_value = "noopener noreferrer"
                else:
                    attr_value = escape(attr_value or "", quote=True)
                safe_attrs.append(f'{attr_name}="{attr_value}"')
            attr_text = f" {' '.join(safe_attrs)}" if safe_attrs else ""
            self.output.append(f"<{tag}{attr_text}>")

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if tag in ALLOWED_TAGS and tag not in VOID_TAGS:
            self.output.append(f"</{tag}>")

    def handle_data(self, data):
        if self.skip_depth:
            return
        self.output.append(escape(data).replace("\n", "<br>"))


def sanitize_rich_text(value):
    if not value:
        return ""
    parser = RichTextSanitizer()
    parser.feed(value)
    parser.close()
    return "".join(parser.output).strip()


def render_rich_text(value):
    return mark_safe(sanitize_rich_text(value))
