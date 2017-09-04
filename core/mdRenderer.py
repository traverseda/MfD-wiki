import mistune
from mistune_contrib.toc import TocMixin
class TocRenderer(TocMixin, mistune.Renderer):
    pass
toc = TocRenderer()
markdown = mistune.Markdown(renderer=toc)
