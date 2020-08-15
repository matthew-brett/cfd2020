""" data8page role
"""

from docutils.parsers.rst.roles import set_classes
from docutils import nodes, utils

from sphinx.util.nodes import split_explicit_title, set_role_source_info
from sphinx.errors import ExtensionError


def data8pagerole(name, rawtext, text, lineno, inliner, options={},
                  content=[]):
    """  Place reference to data 8 page.

    Parameters
    ----------
    name : str
        The role name used in the document.
    rawtext : str
        The entire markup snippet, including the role markup.
    text : str
        The text marked with the role.
    lineno : int
        The line number where `rawtext` appears in the input.
    inliner : object
        The inliner instance that called us.
    options : dict, optional
        Directive options for customization.
    content : content, optional
        The directive content for customization.

    Returns
    -------
    nodes : list
        list of nodes to insert into the document. Can be empty.
    messages : list
        list of system messages. Can be empty.
    """
    env = inliner.document.settings.env
    # process class options.
    # http://docutils.sourceforge.net/docs/howto/rst-roles.html
    # Remaining options will be added as attributes of the node (see
    # below).
    set_classes(options)
    # Get title and link
    text = utils.unescape(text)
    has_fname, title, fname = split_explicit_title(text)
    if has_fname:
        raise ExtensionError('Page role cannot have explicit title')
    refnode = nodes.paragraph(title, title, **options)
    # We may need the line number for warnings
    set_role_source_info(inliner, lineno, refnode)
    return [refnode], []


def setup(app):
    # Add runrole roles
    app.add_role('data8page', data8pagerole)
