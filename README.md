# Desay 6mm and UPAD 2.6mm test pattern control


I repair several types of LED panels, among which are Desay 6mm and UPAD 2.6mm.

The [Novastar MCTRL300](https://www.novastar.tech/products/controller/mctrl300/)controller that can be used to drive these panels has a user interface that allows you to display test patterns (full r/g/b, moving lines, white, ...). During repair and testing this is something you use all the time. However, the control software is Windows only, and rather cumbersome to use. I decided to write my own (simple) interface to call up test patteren quickly.

The controller has a [Silicon Labs CP2102](https://www.silabs.com/interface/usb-bridges/classic/device.cp2102) USB to UART bridge. Opening the housing reveals a rather pretty board that seems to be made so that it can be used as a PCI extention card in a computer instead of a standalone controller as well. Soldering a couple of wires to the QFN28 package and connecting a logic analyzer allows to log the commands that are sent to the controller. After getting these commands, only a bit of Python remains to be written.


See the [link](www.vansteenwegen.org) for information on the project and hardware.

Version numbers according to [Semantic Versioning 2.0.0](https://semver.org/).
