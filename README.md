# Novastar MCTRL300 basic controller

Simple, basic control of brightness and test patterns/mode for the [Novastar MCTRL300](https://www.novastar.tech/products/controller/mctrl300/).

## Why?

I repair several types of LED panels, among which are Desay 6mm and UPAD 2.6mm.

The Novastar software is written for Windows and overkill for simple control of patterns and brightness (which is all I need during testing and repair). This PyQt based solution works faster and runs on my Linux machines as well instead of having to set up a virtual machine (or Wine).

## Novastar hardware: the MCTRL300 LED controller

The [Novastar MCTRL300](https://www.novastar.tech/products/controller/mctrl300/) controller that can be used to drive these panels has a Windows software that allows you configure your whole led screen as well as display test patterns (full r/g/b, moving lines, white, ...). During repair and testing this last function is something I use all the time. Thus, the software and overkill and rather cumbersome. I decided to write my own (simple) interface to call up test patteren quickly.

The controller has a [Silicon Labs CP2102](https://www.silabs.com/interface/usb-bridges/classic/device.cp2102) USB to UART bridge. Opening the housing reveals a rather pretty board that seems to be made so that it can be used as a PCI extention card in a computer instead of a standalone controller as well. Soldering a couple of wires to the QFN28 package and connecting a logic analyzer allows to log the commands that are sent to the controller. After getting these commands, only a bit of Python remains to be written.

## Example

![Screenshot of beta version](/assets/images/screenshot.png)

## Thanks / Acknowledgements

I found a couple of useful documents about the protocol Novastar uses for a couple of other of their controllers on the __Bitfocus Companion module novastar controller [repository](https://github.com/bitfocus/companion-module-novastar-controller)__, mostly while reading through the issues.

## Links

See this [link](www.vansteenwegen.org) for information on some of my other projects.

Version numbers according to [Semantic Versioning 2.0.0](https://semver.org/).

![GitHub last commit (branch)](https://img.shields.io/github/last-commit/dietervansteenwegen/Novastar_MCTRL300_basic_controller/develop?style=plastic)

![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/dietervansteenwegen/Novastar_MCTRL300_basic_controller/develop?style=plastic)

![GitHub](https://img.shields.io/github/license/dietervansteenwegen/Novastar_MCTRL300_basic_controller?style=plastic)
