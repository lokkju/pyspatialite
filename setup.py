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

settings = {}

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

TRUTHY = ("yes", "true", "t", "1")

class HeaderNotFoundException(Exception):
    def __init__(self,msg):
        super(HeaderNotFoundException,self).__init__(msg)
class LibraryNotFoundException(Exception):
    def __init__(self,msg):
        super(LibraryNotFoundException,self).__init__(msg)

class OverrideSystemIncludeOrderBuildCommand(build_ext):

    # TODO: allow user to define these options
    user_options = build_ext.user_options + [
        ('with-proj=', None, "build with PROJ4 (default: True)"),
        ('with-geos=', None, "build with GEOS (default: True)"),
        ('with-geosadvanced=', None, "build with GEOS advanced features (default: True)"),
        ('with-iconv=', None, "build with iconv (default: depends on OS)"),
        ('with-freexl=', None, "build with FreeXL (default: False)")
    ]

    def initialize_options(self):
        self.with_proj4 = 1
        self.with_geos = 1
        self.with_geosadvanced = 0
        self.with_iconv = 1
        self.with_freexl = 0

        build_ext.initialize_options(self)

    def finalize_options(self):
        self.with_proj4 = self.truthify(self.with_proj4)
        self.with_geos = self.truthify(self.with_geos)
        self.with_geosadvanced = self.truthify(self.with_geosadvanced)
        self.with_iconv = self.truthify(self.with_iconv)
        self.with_freexl = self.truthify(self.with_freexl)

        build_ext.finalize_options(self)

    @staticmethod
    def truthify(val):
        if str(val).lower() in TRUTHY:
            return True
        return False

    @staticmethod
    def strip_includes(opts):
        includes = []
        for i in reversed(range(len(opts))):
            if opts[i].startswith("-I"):
                includes.append(opts[i].replace('-I', ''))
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

    def check_header(self, ext, header):
        for dir in self.compiler.include_dirs:
            if os.path.exists(os.path.join(dir,header)):
                ext.define_macros.append(("HAVE_"+header.upper().replace(".","_"),"1"))
                return True
        for dir in self.include_dirs:
            if os.path.exists(os.path.join(dir,header)):
                ext.define_macros.append("HAVE_"+header.upper().replace(".","_"))
                return True

        raise HeaderNotFoundException("cannot find %s, bailing out" % header)

    def check_lib(self, ext,func, lib, msg, libz):
        if self.compiler.has_function(func,libraries=libz + [lib],library_dirs=self.compiler.library_dirs + ext.library_dirs):
            ext.libraries.append(lib)
            ext.libraries.extend(libz)
            return True
        raise LibraryNotFoundException("cannot find function '%s' in '%s': %s" % (func,lib,msg))

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

        if self.with_proj4:
            self.check_header(ext,"proj_api.h")
            self.check_lib(ext,"pj_init_plus", "proj", "'libproj' is required but it doesn't seem to be installed on this system.",["m"])
        else:
            ext.extra_compile_args.append("-DOMIT_PROJ")


        if self.with_geos:
            self.check_header(ext,"geos_c.h")
            self.check_lib(ext,"GEOSTopologyPreserveSimplify","geos_c","'libgeos_c' is required but it doesn't seem to be installed on this system.",["m","geos"])
            if self.with_geosadvanced:
                ext.extra_compile_args.append("-DGEOS_ADVANCED")
                self.check_lib(ext,"GEOSCoveredBy","geos_c","obsolete 'libgeos_c' (< v.3.3.0). please retry specifying: --without-geosadvanced.",["m","geos"])
        else:
            ext.extra_compile_args.append("-DOMIT_GEOS")

        if self.with_iconv:
            if sys.platform.startswith("darwin") or not self.compiler.has_function("iconv"):
                ext.libraries.append("iconv")
        else:
            ext.extra_compile_args.append("-DOMIT_ICONV")

        if self.with_freexl:
            self.check_header(ext,"freexl.h")
            self.check_lib(ext,"freexl_open","freexl","'libfreexl' is required but it doesn't seem to be installed on this system.",["m"])
        else:
            ext.extra_compile_args.append("-DOMIT_FREEXL")

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
            version = PYSPATIALITE_VERSION + "-alpha-0",
            description = "DB-API 2.0 interface for SQLite 3.x with Spatialite " + PYSPATIALITE_VERSION,
            long_description=long_description,
            author = "Lokkju Brennr",
            author_email = "lokkju@lokkju.com",
            license = "zlib/libpng license",
            platforms = "ALL",
            url = "https://github.com/lokkju/pyspatialite/",
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
                        os.path.join(AMALGAMATION_ROOT,"headers")
                    ],
                    library_dirs = [],
                    runtime_library_dirs = [],
                    extra_objects = [],
                    define_macros = [
                        ("VERSION",'"%s"' % PYSPATIALITE_VERSION),
                        ("SQLITE_ENABLE_RTREE", "1"),   # build with fulltext search enabled
                        ("NDEBUG","1"),
                        ("SPL_AMALGAMATION","1"),
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
