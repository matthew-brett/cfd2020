""" ucb-page role
"""

from docutils.parsers.rst.roles import set_classes
from docutils import nodes, utils

from sphinx.util.nodes import split_explicit_title, set_role_source_info
from sphinx.errors import ExtensionError


UCB_URL = 'https://inferentialthinking.com'
UCB_NC_NB_URL = 'https://github.com/data-8/textbook/blob/64b20f0/notebooks'


class FilledRole(object):
    """ Class to support custom Sphinx roles
    """

    def __init__(self):
        """ Fill default structure
        """
        self.name = None
        self.rawtext = None
        self.text = None
        self.lineno = None
        self.inliner = None
        self.options = None
        self.content = None
        self.env = None

    def __call__(self, name, rawtext, text, lineno, inliner, options=None,
                 content=None):
        """ Boilerplate for Sphinx role callable

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
        options : None or dict, optional
            Directive options for customization.  Default of None corresponds
            to empty dict.
        content : None content, optional
            The directive content for customization.  Default of None
            corresponds to empty list.

        Returns
        -------
        nodes : list
            list of nodes to insert into the document. Can be empty.
        messages : list
            list of system messages. Can be empty.
        """
        options = {} if options is None else options
        content = [] if content is None else content
        self.name = name
        self.rawtext = rawtext
        self.text = text
        self.lineno = lineno
        self.inliner = inliner
        self.options = options
        self.content = content
        self.env = inliner.document.settings.env
        self.preprocess()
        return self.run()

    def preprocess(self):
        """ Do default pre-processing of inputs
        """
        # process class options.
        # http://docutils.sourceforge.net/docs/howto/rst-roles.html
        # Remaining options will be added as attributes of the node (see
        # below).
        set_classes(self.options)
        # Process escaped char
        self.text = utils.unescape(self.text)

    def run(self):
        has_fname, text, fname = split_explicit_title(self.text)
        if has_fname:
            raise ExtensionError('Page role cannot have explicit title')
        nb_url = f'{UCB_NC_NB_URL}/{text}.ipynb'
        license_url = f'{self.env.config.html_baseurl}/license'
        node = nodes.note(
            text,
            nodes.paragraph(
                text, '',
                nodes.Text('This page has content from the '),
                nodes.reference(nb_url, text, refuri=nb_url),
                nodes.Text(' notebook of an older version of the '),
                nodes.reference(UCB_URL, 'UC Berkeley data science course',
                                refuri=UCB_URL),
                nodes.Text('. See the Berkeley course section of the '),
                nodes.reference(
                    license_url,
                    'license file',
                    refuri= license_url),
                nodes.Text('.')
            ))
        set_role_source_info(self.inliner, self.lineno, node)
        return [node], []


def setup(app):
    """ Initialize Sphinx extension
    """
    app.add_role('ucb-page', FilledRole())
