[![Download](https://api.bintray.com/packages/helmesjo/public-conan/aeron%3Ahelmesjo/images/download.svg) ](https://bintray.com/helmesjo/public-conan/aeron%3Ahelmesjo/_latestVersion)
[![Build Status](https://travis-ci.org/helmesjo/conan-aeron.svg?branch=stable%2F1.27.0)](https://travis-ci.org/helmesjo/conan-aeron)
[![Build status](https://ci.appveyor.com/api/projects/status/github/helmesjo/conan-aeron?branch=stable%2F1.27.0&svg=true)](https://ci.appveyor.com/project/helmesjo/conan-aeron)

[Conan.io](https://conan.io) package recipe for [*aeron*](https://github.com/real-logic/aeron/wiki).

Efficient reliable UDP unicast,                     UDP multicast, and IPC message transport

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/helmesjo/public-conan/aeron%3Ahelmesjo).

## For Users: Use this package

### Basic setup

    $ conan install aeron/1.27.0@helmesjo/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    aeron/1.27.0@helmesjo/stable

    [generators]
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to helmesjo conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create helmesjo/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| shared      | False |  [True, False] |
| fPIC      | True |  [True, False] |
| build_aeron_driver      | False |  [True, False] |

## Add Remote

    $ conan remote add helmesjo "https://api.bintray.com/conan/helmesjo/public-conan"

## Upload

    $ conan upload aeron/1.27.0@helmesjo/stable --all -r helmesjo


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package aeron.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/helmesjo/conan-aeron/blob/stable/1.27.0/LICENSE.md)
