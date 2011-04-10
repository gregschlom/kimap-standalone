kimap-standalone
================

kimap-standalone is a set of python scripts that make it easy to compile the following modules from
KDE:
    - kdecore
    - kmime
    - kimap
    - ksmtp (not officially part of KDE libraries yet :)

How it works?
=============

The idea is to have a set of patches that we apply on top of a regular checkout of kdelibs and 
kdepimlibs. Those patches disable everything that is not needed, so that we can compile kdecore,
kmime and kimap with minimal dependencies (zlib, cyrus-sasl, and a boost subset)

Basic usage
===========

1. Clone kimap-standalone

    $ git://github.com/gregschlom/kimap-standalone.git
    
This will also clone the following sub-repositories from git.kde.org:
- automoc
- kdewin
- kdelibs
- kdepimlibs
- scratch/schlomoff/ksmtp

2. Apply the patches

    $ ./import-patches.py

This will create a kimap-standalone branch on kdelibs and kdepimlibs, and apply the patches in the
patches directory.

3. Configure

    $ ./configure.py --qmake=[path/to/qmake]

By default, it will build the libraries in Debug mode, for static linking    
If you don't specify --qmake, it will try to detect qmake in path.

The configure script will create a build directory with a subdirectory for each target, and a 
run-cmake.py script for each.

4. Build!

    $ ./build-all.py

This will go in each subdirectory of build, launch the run-cmake.py script, wait for CMake to finish,
and do the equivalent of a make && make install, according to your platform.

If everything goes well, you should have now a include and a lib folder with everything you need to
use kdecore, kmime, and kimap in your Qt application.

Requirements
============

- CMake
- Qt