#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os
import shutil
import re

def replace(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, "{} # <-- Line edited by conan package -->".format(subst), file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()

class LibnameConan(ConanFile):
    name = "aeron"
    version = "1.27.0"
    description =   "Efficient reliable UDP unicast, \
                    UDP multicast, and IPC message transport"
    url = "https://github.com/real-logic/aeron"
    homepage = "https://github.com/real-logic/aeron/wiki"
    author = "helmesjo <helmesjo@gmail.com>"
    # Indicates License type of the packaged library
    license = "Apache License 2.0"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False], 
        "fPIC": [True, False],
        "build_aeron_driver": [True, False],
        "build_tests": [True, False],
        "build_samples": [True, False],
    }
    default_options = {
        "shared": False, 
        "fPIC": True,
        "build_aeron_driver": True,
        "build_tests": False,
        "build_samples": False
    }

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    requires = ()

    def requirements(self):
        if self.settings.os == "Windows":
            self.requires.add("pthreads4w/3.0.0")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
            # C-Driver still experimental on Windows: https://github.com/real-logic/aeron#c-media-driver
            self.options.build_aeron_driver = False

        if self.settings.compiler == "Visual Studio" and self.settings.arch != "x86_64":
            # https://github.com/real-logic/aeron#c-build
            raise ConanException("{} currently only supports 64-bit builds on Windows".format(self.name))

    def source(self):
        source_url = "https://github.com/real-logic/aeron"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        
        cmake.definitions["AERON_INSTALL_TARGETS"] = True

        cmake.definitions["BUILD_AERON_DRIVER"] = self.options.build_aeron_driver
        cmake.definitions["AERON_TESTS"] = self.options.build_tests
        cmake.definitions["AERON_BUILD_SAMPLES"] = self.options.build_samples

        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

        if self.options.build_tests:
            self.output.info("Running {} tests".format(self.name))
            source_path = os.path.join(self.build_subfolder, self.source_subfolder)
            with tools.chdir(source_path):
                self.run("ctest")

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

        # Files install straight to './include', but we want './include/aeron'
        fileDir = self.package_folder
        old_include_folder = os.path.join(fileDir, "include/")
        new_include_folder = os.path.join(fileDir, "include/{}/".format(self.name))
        tools.rmdir(new_include_folder)
        tools.mkdir(new_include_folder)
        files = os.listdir(old_include_folder)
        with tools.chdir(fileDir):
            for f in files:
                shutil.move(old_include_folder + f, new_include_folder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs.append("include/{}".format(self.name))

        self.output.info("{} requires C++11. Enforcing for downstream targets...".format(self.name))
        self.cpp_info.cppflags.append("-std=c++11")
        
        # See: https://github.com/real-logic/aeron/blob/23f9ef8c6bd25955c3a64454f4e5d9c4a86c8d5a/CMakeLists.txt#L213
        self.cpp_info.defines.append("_ENABLE_EXTENDED_ALIGNED_STORAGE")