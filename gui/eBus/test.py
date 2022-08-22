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
from threading import *


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

        self.mDevice = PvDevice.CreateAndConnect(lDeviceInfo)
        self.mStream = PvStream.CreateAndOpen(lDeviceInfo)
        print("mDevice is Connected: ", self.mDevice.IsConnected)
        print("mStream is Open: ", self.mStream.IsOpen)

        self.browser.GenParameterArray = self.mStream.Parameters

        self.mPipeline = PvPipeline(self.mStream)

        self.mPipeline.BufferSize = self.mDevice.PayloadSize
        self.mPipeline.BufferCount = cBufferCount

        # t = Thread(target=self.ThreadProc)
        # t.daemon = True
        # t.start()

        self.mDevice.StreamEnable()
        self.mDevice.Parameters.ExecuteCommand("AcquisitionStart")
        print("strea")

    def run(self):
        WinForms.Application.Run(self)

    def ThreadProc(self):
        print(self.mDevice.IsConnected)
        print(self.mStream.IsOpen)

        lBuffer = PvBuffer(None)

        while (True):
            lResult = self.mPipeline.RetrieveNextBuffer(lBuffer)
            print("lResult", type(lResult[0]), lResult[0].IsOK)
            print("lBuffer", type(lBuffer), lBuffer.OperationResult.IsOK)

            self.displayControl.Display(lBuffer)
            # if(lResult.IsOK):
            #     if lBuffer.OperationResult.IsOK:
            #
            # if lBuffer.OperationResult.IsOK:
            #     print(lResult.IsOK)


def main():
    form = HelloApp()
    app = WinForms.Application
    app.Run(form)


if __name__ == '__main__':
    main()
