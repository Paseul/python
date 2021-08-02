import clr
import sys
SWF = clr.AddReference("System.Windows.Forms")
print
SWF.Location

assembly_path = r"C:\github\python\gui\eBus\dll"
sys.path.append(assembly_path)
clr.AddReference("PvGUIDotNet")
clr.AddReference("PvDotNet")
import System.Windows.Forms as WinForms
from System.Drawing import Size, Point
from PvDotNet import *
from PvGUIDotNet import *
import PvDotNet
import PvGUIDotNet
import numpy as np
import ctypes


class HelloApp(WinForms.Form):
        #simple hello world app that demonstrates the essentials of  winforms programming and event-based programming in Python."""

    def __init__(self):
        self.Text = "Hello World From Python"
        self.AutoScaleBaseSize = Size(5, 13)
        self.ClientSize = Size(1024, 720);
        h = WinForms.SystemInformation.CaptionHeight
        self.MinimumSize = Size(392, (117 + h))

        # Create the button
        self.button = WinForms.Button()
        self.button.Location = Point(160, 64)
        self.button.Size = Size(220, 20)
        self.button.TabIndex = 2
        self.button.Text = "Click Me!"

        # Register the event handler
        self.button.Click += self.button_Click

        # Create the text box
        self.textbox = WinForms.TextBox()
        self.textbox.Text = "Hello World"
        self.textbox.TabIndex = 1
        self.textbox.Size = Size(220, 40)
        self.textbox.Location = Point(160, 24)

        # Browser
        self.browser = PvGUIDotNet.PvGenBrowserControl()
        self.browser.GenParameterArray = None
        self.browser.Location = Point(620, 100)
        self.browser.Name = "browser"
        self.browser.Size = Size(299, 408)
        self.browser.TabIndex = 18

        # Display Control
        self.displayControl = PvGUIDotNet.PvDisplayControl()
        self.displayControl.Location = Point(139, 100)
        self.displayControl.Name = "displayControl"
        self.displayControl.Size = Size(461, 411)
        self.displayControl.TabIndex = 7

        # Add the controls to the form
        self.AcceptButton = self.button
        self.Controls.Add(self.button)
        self.Controls.Add(self.textbox)
        self.Controls.Add(self.browser)
        self.Controls.Add(self.displayControl)

    def button_Click(self, sender, args):
        cBufferCount = 16
        lBuffers = []

        lForm = PvDeviceFinderForm()

        lForm.ShowDialog()
        lDeviceInfo = lForm.Selected

        mDevice = PvDevice.CreateAndConnect(lDeviceInfo)
        mStream = PvStream.CreateAndOpen(lDeviceInfo)

        self.browser.GenParameterArray = mStream.Parameters

        lPayloadSize = mDevice.PayloadSize



        # if mStream.QueuedBufferMaximum < cBufferCount:
        #     lBufferCount = mStream.QueuedBufferMaximum
        # else:
        #     lBufferCount = cBufferCount
        #
        # for i in range(lBufferCount):
        #     lBuffers.append(PvBuffer())
        #     mStream.QueueBuffer(lBuffers[i])
        #
        # mDevice.StreamEnable()
        # mDevice.Parameters.ExecuteCommand("AcquisitionStart")
        #
        # print(mDevice)
        #
        # while (True):
        #     lBuffer = None
        #     lOperationResult = PvResult(PvResultCode.OK)
        # #     # print(lOperationResult)
        # #
        #     lResult = mStream.RetrieveBuffer(lBuffer, lOperationResult, np.int32(100))
        #     if(lResult[0].IsOK):
        #         self.displayControl.Display(lBuffer)
        #     for i in range(len(lResult)):
        #         print(lResult[i])

    def run(self):
        WinForms.Application.Run(self)


def main():
    form = HelloApp()
    print("form created")
    app = WinForms.Application
    print("app referenced")
    app.Run(form)


if __name__ == '__main__':
    main()
