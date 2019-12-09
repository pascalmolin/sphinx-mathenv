#!/usr/bin/python
# -*- coding: utf-8 -*-

from docutils import nodes
class MathNode(nodes.Admonition, nodes.Element):
  pass

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
    self.body.append('\n\\begin{%s}~'%node.__class__.__name__[2:])
def depart_math_node_latex(self, node):
    self.body.append('\n\\end{%s}'%node.__class__.__name__[2:])

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
        admonition_node['classes'] += ['mathenv-' + self.node_class.__name__[2:]]
    self.state.nested_parse(self.content, self.content_offset,
                            admonition_node)
    admonition_node['label'] = self.options.get('label', 0)
    return [admonition_node]

class mndefinition(MathNode): pass
class Definition(MathEnvDirective):
  node_class = mndefinition
  shortname = 'def'
  label = u'Définition'
class mntheorem(MathNode): pass
class Theorem(MathEnvDirective):
  node_class = mntheorem
  shortname = 'th'
  label = u'Théorème'
class mnproposition(MathNode): pass
class Proposition(MathEnvDirective):
  node_class = mnproposition
  shortname = 'prop'
  label = u'Proposition'
class mncorollary(MathNode): pass
class Corollary(MathEnvDirective):
  node_class = mncorollary
  shortname = 'cor'
  label = u'Corollaire'
class mnlemma(MathNode): pass
class Lemma(MathEnvDirective):
  node_class = mnlemma
  shortname = 'lem'
  label = u'Lemme'
class mnproof(MathNode): pass
class Proof(MathEnvDirective):
  node_class = mnproof
  shortname = 'dem'
  label = u'Démonstration'
class mnremark(MathNode): pass
class Remark(MathEnvDirective):
  node_class = mnremark
  shortname = 'rem'
  label = u'Remarque'
class mnexample(MathNode): pass
class Example(MathEnvDirective):
  node_class = mnexample
  shortname = 'ex'
  label = u'Exemple'

def register_mathenv_labels(app, doctree):
  labels = app.env.domaindata['std']['labels']
  docname = app.env.docname
  for node in doctree.traverse(MathNode):
    labelid = "abc"
    sectname = node[0]
    name = node['label']
    print((name, docname, labelid, sectname))
    labels[name] = docname, labelid, sectname

def setup(app):
  all_env = [Definition,Theorem,Proposition, Corollary,
          Lemma,Remark,Proof,Example]
  for directive in all_env:
    # TODO: use add_enumerable_node(node, 'mathenv', title_getter=None,
    app.add_node(directive.node_class,
          html=(visit_math_node, depart_math_node),
          latex=(visit_math_node_latex, depart_math_node_latex),
          text=(visit_math_node, depart_math_node))
    app.add_directive(directive.shortname, directive)

  app.add_stylesheet('mathenv.css')
  """
  add types in html_context
  remove mn from name
  """
  app.config.html_context['mathenv'] = [ (e.node_class.__name__, e.label)
          for e in all_env]
  #app.connect('doctree-read', register_mathenv_labels)
