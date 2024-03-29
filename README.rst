Sphinx-mathenv
======================================================================

Usual theorem-like math environments in Sphinx.

Usage
----------------------------------------------------------------------

In ``conf.py``

::

  extensions = [
    # maybe 'sphinxcontrib.katex',
    'sphinxcontrib.mathenv',
    ]

In any file::

  .. th:: Dirichlet

     If $a$ is coprime to $m$, there exist infinitely many primes $p$
     congruent to $a$ mod $m$.

  .. cor::

     There are infinitely many primes whose last digits are $2019$.

  .. proof::

     Take $m=10000$ and $a=2019$.

Alternatives
----------------------------------------------------------------------

There exist an extension `sphinxcontrib-proof <https://framagit.org/spalax/sphinxcontrib-proof>`_
which seems much better designed. I suggest you give it a try.
