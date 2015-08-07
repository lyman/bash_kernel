A simple IPython kernel for odpscmd
===================================

This is a IPython kernel for `odpscmd <http://odps.aliyun.com>`__,
modified from
`bash\_kernel <https://github.com/takluyver/bash_kernel>`__.

Requirement
-----------

-  IPython 3
-  Command odpscmd in PATH
-  File odps\_config.ini should be found in current folder and is
   properly configured

Download
--------

-  git clone git@github.com:lyman/odpscmd\_kernel.git

Run
---

Install with ``pip install .``, and then run one of:

-  ``ipython notebook``, In the notebook interface, select Bash from the
   'New' menu
-  ``ipython console --kernel odpscmd``

Debug
-----

Just run ``./debug.sh``

License
-------

Licensed under the `BSD
License <http://www.linfo.org/bsdlicense.html>`__
