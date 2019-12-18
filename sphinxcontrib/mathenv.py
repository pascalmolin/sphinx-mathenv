#!/usr/bin/python
# -*- coding: utf-8 -*-

from docutils import nodes
class MathNode(nodes.Admonition, nodes.Element):
    pass

def title_getter(node):
    """Return the title of a node (or `None`)."""
    return node.get('title','')

#admonitionlabels                = {}
# overwritten
def visit_math_node(self, node):
  if isinstance(node.parent, nodes.section):
    node.insert(0, node['title'])
  self.visit_admonition(node)
def depart_math_node(self, node):
  self.depart_admonition(node)

def visit_math_node_latex(self, node):
    """ space after so that a list begins on next line """
    self.body.append('\n\\begin{%s}~'%node.latexname)
def depart_math_node_latex(self, node):
    self.body.append('\n\\end{%s}'%node.latexname)

from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst.roles import set_classes
class MathEnvDirective(BaseAdmonition):
  has_content = True
  required_arguments = 0
  optional_arguments = 1
  option_spec = {
          'name': directives.unchanged,
          }
  """
  node_class = MathNode
  """
  def run(self):
    set_classes(self.options)
    self.assert_has_content()
    text = '\n'.join(self.content)
    admonition_node = self.node_class(text, **self.options)
    self.add_name(admonition_node)
    
    if self.arguments:
      title_text = self.arguments[0]
    else:
      title_text = self.label
    textnodes, messages = self.state.inline_text(title_text,
                                                 self.lineno)
    title = nodes.title(title_text, '', *textnodes)
    title.source, title.line = (
            self.state_machine.get_source_and_line(self.lineno))
    admonition_node['title'] = title
    admonition_node += messages
    if not 'classes' in self.options:
        # remove prefix mn from node name
        admonition_node['classes'] += ['mathenv-' + self.node_class.latexname]
    self.state.nested_parse(self.content, self.content_offset,
                            admonition_node)
    admonition_node['label'] = self.options.get('label', 0)
    return [admonition_node]

mathenv_environments = [
        # (rst directive, output, latex env)
        ('def'  , 'Définition'    , 'definition')  , 
        ('th'   , 'Théorème'      , 'theorem')     , 
        ('prop' , 'Proposition'   , 'proposition') , 
        ('cor'  , 'Corollaire'    , 'corollary')   , 
        ('lem'  , 'Lemme'         , 'lemma')       , 
        ('dem'  , 'Démonstration' , 'proof')       , 
        ('rem'  , 'Remarque'      , 'remark')      , 
        ('ex'   , 'Exemple'       , 'example')     , 
        ('exo'  , 'Exercice'      , 'exercise')    , 
        ('sol'  , 'Solution'      , 'solution')    , 
]
mathenv_nonumber = [ 'dem', 'sol' ]

def create_mathenv(mathenv_environments):
    import __main__

    mathdir = []
    for name, label, latexname in mathenv_environments:

        nodename = 'mn%s'%latexname
        node = type(nodename,(MathNode,), dict(name=nodename, latexname=latexname) )
        directive = type(name, (MathEnvDirective,), dict(node_class=node, shortname=name, label=label))

        # hack to prevent pickling failure: register node to main domain
        # see https://stackoverflow.com/questions/16377215/how-to-pickle-a-namedtuple-instance-correctly
        setattr(__main__, node.__name__, node)
        node.__module__ = "__main__"

        mathdir.append(directive)

    return mathdir

def register_mathenv(app, config):

    mathdir = create_mathenv(config.mathenv_environments)

    for directive in mathdir:

        name = directive.shortname

        app.add_directive(name, directive)

        node = directive.node_class

        if name in config.mathenv_nonumber:
            app.add_node(node,
                html=(visit_math_node, depart_math_node),
                latex=(visit_math_node_latex, depart_math_node_latex),
                text=(visit_math_node, depart_math_node)
                )
        else:
            app.add_enumerable_node(
                node,
                'mathenv',
                title_getter,
                html=(visit_math_node, depart_math_node),
                latex=(visit_math_node_latex, depart_math_node_latex),
                text=(visit_math_node, depart_math_node)
                )

    """
    add types in html_context
    remove mn from name
    """
    #app.config.html_context['mathenv'] = env_names
    app.config.html_context['mathenv'] = [ (e.node_class.__name__, e.label)
          for e in mathdir]    

filename_css = 'mathenv.css'
def setup_static_path(app):
    app._mathenv_static_path = mkdtemp()
    if app._mathenv_static_path not in app.config.html_static_path:
        app.config.html_static_path.append(app._mathenv_static_path)

def copy_contrib_file(app, file_name):
    pwd = os.path.abspath(os.path.dirname(__file__))
    source = os.path.join(pwd, file_name)
    dest = os.path.join(app._mathenv_static_path, file_name)
    copyfile(source, dest)

def builder_inited(app):

    # Sphinx 1.8 renamed `add_stylesheet` to `add_css_file`
    add_css = getattr(app, 'add_css_file', getattr(app, 'add_stylesheet'))
    add_js = getattr(app, 'add_js_file', getattr(app, 'add_javascript'))

    # Ensure the static path is setup
    setup_static_path(app)

    # custom js and CSS
    copy_contrib_file(app, filename_css)
    add_css(filename_css)


def setup(app):

  app.connect("builder-inited", builder_inited)

  app.add_config_value("mathenv_environments", mathenv_environments, "env")
  app.add_config_value("mathenv_nonumber", mathenv_nonumber, "env")
  app.connect("config-inited", register_mathenv)

  app.add_stylesheet('mathenv.css')
  #app.connect('doctree-read', register_mathenv_labels)

"""
def register_mathenv_labels(app, doctree):
  labels = app.env.domaindata['std']['labels']
  docname = app.env.docname
  for node in doctree.traverse(MathNode):
    labelid = "abc"
    sectname = node[0]
    name = node['label']
    print((name, docname, labelid, sectname))
    labels[name] = docname, labelid, sectname
"""
