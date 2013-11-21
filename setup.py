#-*- coding: ISO-8859-1 -*-
# setup.py: the distutils script
#
# Copyright (C) 2004-2007 Gerhard Häring <gh@ghaering.de>
# Copyright (C) 20010 Lokkju Brennr <lokkju@lokkju.com>
#
# This file was part of pysqlite
# This file is part of pyspatialite.
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import glob, os, re, sys
import urllib
import zipfile
import string

from setuptools import setup, find_packages, Extension, Command
from setuptools.command.build_ext import build_ext

import cross_bdist_wininst

# If you need to change anything, it should be enough to change setup.cfg.

sqlite = "spatialite"

long_description = \
"""Python interface to SQLite 3 + Spatialite

pyspatialite is an interface to the SQLite 3.x embedded relational database engine with spatialite extensions.
It is almost fully compliant with the Python database API version 2.0 also
exposes the unique features of SQLite and spatialite."""

class DocBuilder(Command):
    description = "Builds the documentation"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os, shutil
        try:
            shutil.rmtree("build/doc")
        except OSError:
            pass
        os.makedirs("build/doc")
        rc = os.system("sphinx-build doc/sphinx build/doc")
        if rc != 0:
            print "Is sphinx installed? If not, try 'sudo easy_install sphinx'."

AMALGAMATION_ROOT = "amalgamation/libspatialite-amalgamation-3.0.1"

#if not self.compiler.has_function("iconv"):
#          ext.libraries.append("iconv")



#    def __setattr__(self, k, v):
#        # Make sure we don't link against the SQLite library, no matter what setup.cfg says
#        if self.amalgamation and k == "libraries":
#            v = None
#        self.__dict__[k] = v

class OverrideSystemIncludeOrderBuildCommand(build_ext):
    @staticmethod
    def strip_includes(opts):
        includes = []
        for i in reversed(range(len(opts))):
            if opts[i].startswith("-I"):
                includes.append(opts[i].replace('^-I', ''))
                del opts[i]
        return includes

    @staticmethod
    def uniq(seq, idfun=None):
        return list(OverrideSystemIncludeOrderBuildCommand._uniq(seq, idfun))

    @staticmethod
    def _uniq(seq, idfun=None):
        seen = set()
        if idfun is None:
            for x in seq:
                if x in seen:
                    continue
                seen.add(x)
                yield x
        else:
            for x in seq:
                x = idfun(x)
                if x in seen:
                    continue
                seen.add(x)
                yield x

    def build_extension(self,ext):
        # Load includes from module directories first!
        include_dirs = []
        include_dirs.extend(self.strip_includes(self.compiler.compiler))
        include_dirs.extend(self.strip_includes(self.compiler.compiler_so))
        include_dirs.extend(self.strip_includes(self.compiler.compiler_cxx))
        include_dirs.extend(self.strip_includes(self.compiler.linker_so))
        include_dirs.extend(self.strip_includes(self.compiler.linker_exe))
        include_dirs.extend(self.strip_includes(self.compiler.preprocessor))
        self.compiler.include_dirs.extend(self.uniq(include_dirs))

        if sys.platform.startswith("darwin") or not self.compiler.has_function("iconv"):
            ext.libraries.append("iconv")

        build_ext.build_extension(self,ext)


def get_setup_args():

    PYSPATIALITE_VERSION = None

    version_re = re.compile('#define PYSPATIALITE_VERSION "(.*)"')
    f = open(os.path.join("src", "module.h"))
    for line in f:
        match = version_re.match(line)
        if match:
            PYSPATIALITE_VERSION = match.groups()[0]
            PYSPATIALITE_MINOR_VERSION = ".".join(PYSPATIALITE_VERSION.split('.')[:2])
            break
    f.close()

    if not PYSPATIALITE_VERSION:
        print "Fatal error: PYSPATIALITE_VERSION could not be detected!"
        sys.exit(1)

    data_files = [("pyspatialite-doc",
                        glob.glob("doc/*.html") \
                      + glob.glob("doc/*.txt") \
                      + glob.glob("doc/*.css")),
                   ("pyspatialite-doc/code",
                        glob.glob("doc/code/*.py"))]

    py_modules = ["spatialite"]
    setup_args = dict(
            name = "pyspatialite",
            version = PYSPATIALITE_VERSION,
            description = "DB-API 2.0 interface for SQLite 3.x with Spatialite " + PYSPATIALITE_VERSION,
            long_description=long_description,
            author = "Lokkju Brennr",
            author_email = "lokkju@lokkju.com",
            license = "zlib/libpng license",
            platforms = "ALL",
            url = "http://pyspatialite.googlecode.com/",
            # no download_url, since pypi hosts it!
            #download_url = "http://code.google.com/p/pyspatialite/downloads/list",

            # Description of the modules and packages in the distribution
            package_dir = {"": "lib"},
            packages = find_packages('lib', exclude = ['ez_setup', '*.tests', '*.tests.*', 'tests.*', 'tests']),
            scripts=[],
            data_files = data_files,
            ext_modules = [
                Extension(
                    name="pyspatialite._spatialite",
                    sources = [
                        "src/module.c",
                        "src/connection.c",
                        "src/cursor.c",
                        "src/cache.c",
                        "src/microprotocols.c",
                        "src/prepare_protocol.c",
                        "src/statement.c",
                        "src/util.c",
                        "src/row.c",
                        os.path.join(AMALGAMATION_ROOT, "sqlite3.c"),
                        os.path.join(AMALGAMATION_ROOT, "spatialite.c")
                    ],
                    include_dirs = [
                        os.path.join(AMALGAMATION_ROOT,"headers"),
                        "/Library/Frameworks/GEOS.framework/unix/include/",
                        "/Library/Frameworks/PROJ.framework/unix/include/",

                    ],
                    library_dirs = [
                        "/Library/Frameworks/GEOS.framework/unix/lib",
                        "/Library/Frameworks/PROJ.framework/unix/lib"
                    ],
                    libraries = ['geos','geos_c','proj'],
                    runtime_library_dirs = [],
                    extra_objects = [],
                    define_macros = [
                        ("VERSION",'"%s"' % PYSPATIALITE_VERSION),
                        ("SQLITE_ENABLE_FTS3", "1"),   # build with fulltext search enabled
                        ("SQLITE_ENABLE_RTREE", "1"),   # build with fulltext search enabled
                        ("SQLITE_ENABLE_COLUMN_METADATA", "1"),   # build with fulltext search enabled
                        ("OMIT_FREEXL","1"),
                        ('MODULE_NAME', '\\"spatialite.dbapi2\\"') if sys.platform == "win32" else ('MODULE_NAME', '"spatialite.dbapi2"')
                    ],
                )
            ],
            classifiers = [
                "Development Status :: 3 - Alpha",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: zlib/libpng License",
                "Operating System :: MacOS :: MacOS X",
                "Operating System :: Microsoft :: Windows",
                "Operating System :: POSIX",
                "Programming Language :: C",
                "Programming Language :: Python",
                "Topic :: Database :: Database Engines/Servers",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
            cmdclass = {"build_docs": DocBuilder},
            test_suite = "pyspatialite.tests.suite"
    )

    setup_args["cmdclass"].update(
        {
            "build_docs": DocBuilder,
            "cross_bdist_wininst": cross_bdist_wininst.bdist_wininst,
            "build_ext": OverrideSystemIncludeOrderBuildCommand
        }
    )
    return setup_args

def main():
    setup(**get_setup_args())

if __name__ == "__main__":
    main()
