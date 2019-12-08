import unittest
import tkinter as tk
from TaskerGui import Application
from TaskerMenuBar import TaskerMenuBar
from multicolumnlistbox import GUI
from satCatScraper import Scraper
import os
from spacecraft2 import spacecraft
from TaskerPoint import Point
import threading
from datetime import datetime
from matplotlib.backend_bases import MouseEvent, MouseButton
from PIL import Image
from math import sqrt

class TestTaskerGuiMethods(unittest.TestCase):
    """
    Unit test for TaskerGui
    """

    def test_TaskerGui(self):
        root=tk.Tk()
        app=Application(master=root)
        self.assertTrue(True) # Test passes if it doesn't crash before this line

class TestTaskerMenuBarMethods(unittest.TestCase):
    """
    Unit tests for TaskerMenuBar methods
    """

    def setUp(self):
        """
        Sets up GUI
        """

        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_MenuBar_addSatellite(self):
        """
        Tests addSatellite function
        """

        self.app.menubar.addSatellite()
        self.assertTrue(True) # Test passes if it doesn't crash before this line

    def test_MenuBar_addSatelliteToTree1(self):
        """
        Tests addSatelliteToTree function
        """

        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 0
        self.app.menubar.addSatelliteToTree()
        self.assertEqual(self.app.treeview.satList[-1].name, "CALSPHERE 1")

    def test_MenuBar_addSatelliteToTree2(self):
        """
        Tests addSatelliteToTree function
        """

        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 1
        self.app.menubar.addSatelliteToTree()
        self.assertEqual(self.app.treeview.satList[-1].name, "CALSPHERE 2")

    def test_MenuBar_addSatelliteToTree3(self):
        """
        Tests addSatelliteToTree function
        """

        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 2
        self.app.menubar.addSatelliteToTree()
        self.assertEqual(self.app.treeview.satList[-1].name, "LCS 1")

    def test_MenuBar_addPoint(self):
        """
        Tests addPoint function
        """

        self.app.menubar.addPoint()
        self.assertTrue(True) # Test passes if it doesn't crash before this line

    def test_MenuBar_addPointToTree1(self):
        """
        Tests addPointToTree function
        """

        self.app.menubar.addPoint()
        self.app.menubar.pointName.delete(0, tk.END)
        self.app.menubar.pointName.insert(0, "test1")
        self.app.menubar.pointLat.delete(0, tk.END)
        self.app.menubar.pointLat.insert(0, "42.2808")
        self.app.menubar.pointLon.delete(0, tk.END)
        self.app.menubar.pointLon.insert(0, "-83.7430")
        self.app.menubar.addPointToTree()
        self.assertEqual(self.app.treeview.pointList[-1].name, "test1")
        self.assertEqual(self.app.treeview.pointList[-1].lat, 42.2808)
        self.assertEqual(self.app.treeview.pointList[-1].lon, -83.7430)

    def test_MenuBar_addPointToTree2(self):
        """
        Tests addPointToTree function
        """

        self.app.menubar.addPoint()
        self.app.menubar.pointName.delete(0, tk.END)
        self.app.menubar.pointName.insert(0, "test2")
        self.app.menubar.pointLat.delete(0, tk.END)
        self.app.menubar.pointLat.insert(0, "-42.2808")
        self.app.menubar.pointLon.delete(0, tk.END)
        self.app.menubar.pointLon.insert(0, "83.7430")
        self.app.menubar.addPointToTree()
        self.assertEqual(self.app.treeview.pointList[-1].name, "test2")
        self.assertEqual(self.app.treeview.pointList[-1].lat, -42.2808)
        self.assertEqual(self.app.treeview.pointList[-1].lon, 83.7430)

    def test_MenuBar_addPointToTree3(self):
        """
        Tests addPointToTree function
        """

        self.app.menubar.addPoint()
        self.app.menubar.pointName.delete(0, tk.END)
        self.app.menubar.pointName.insert(0, "test3")
        self.app.menubar.pointLat.delete(0, tk.END)
        self.app.menubar.pointLat.insert(0, "0")
        self.app.menubar.pointLon.delete(0, tk.END)
        self.app.menubar.pointLon.insert(0, "0")
        self.app.menubar.addPointToTree()
        self.assertEqual(self.app.treeview.pointList[-1].name, "test3")
        self.assertEqual(self.app.treeview.pointList[-1].lat, 0)
        self.assertEqual(self.app.treeview.pointList[-1].lon, 0)

    def test_pointer1(self):
        """
        Tests Pointer pop-up
        """

        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 0
        self.app.menubar.addSatelliteToTree()

        self.app.menubar.addPoint()
        self.app.menubar.pointName.delete(0, tk.END)
        self.app.menubar.pointName.insert(0, "test1")
        self.app.menubar.pointLat.delete(0, tk.END)
        self.app.menubar.pointLat.insert(0, "42.2808")
        self.app.menubar.pointLon.delete(0, tk.END)
        self.app.menubar.pointLon.insert(0, "-83.7430")
        self.app.menubar.addPointToTree()

        self.app.menubar.pointer()
        self.app.menubar.ptrSatVar.set("CALSPHERE 1")
        self.app.menubar.ptrPointVar.set("test1")

        self.app.menubar.calcVector()
        self.assertTrue(self.app.menubar.results.get(0)[4:] != "0")
        self.assertTrue(self.app.menubar.results.get(1)[4:] != "0")
        self.assertTrue(self.app.menubar.results.get(2)[4:] != "0")

    def test_pointer2(self):
        """
        Tests Pointer pop-up
        """

        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 1
        self.app.menubar.addSatelliteToTree()

        self.app.menubar.addPoint()
        self.app.menubar.pointName.delete(0, tk.END)
        self.app.menubar.pointName.insert(0, "test2")
        self.app.menubar.pointLat.delete(0, tk.END)
        self.app.menubar.pointLat.insert(0, "-42.2808")
        self.app.menubar.pointLon.delete(0, tk.END)
        self.app.menubar.pointLon.insert(0, "83.7430")
        self.app.menubar.addPointToTree()

        self.app.menubar.pointer()
        self.app.menubar.ptrSatVar.set("CALSPHERE 2")
        self.app.menubar.ptrPointVar.set("test2")

        self.app.menubar.calcVector()
        self.assertTrue(self.app.menubar.results.get(0)[4:] != "0")
        self.assertTrue(self.app.menubar.results.get(1)[4:] != "0")
        self.assertTrue(self.app.menubar.results.get(2)[4:] != "0")

    def test_pointer3(self):
        """
        Tests Pointer pop-up
        """

        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 1
        self.app.menubar.addSatelliteToTree()

        self.app.menubar.addPoint()
        self.app.menubar.pointName.delete(0, tk.END)
        self.app.menubar.pointName.insert(0, "test2")
        self.app.menubar.pointLat.delete(0, tk.END)
        self.app.menubar.pointLat.insert(0, "-42.2808")
        self.app.menubar.pointLon.delete(0, tk.END)
        self.app.menubar.pointLon.insert(0, "83.7430")
        self.app.menubar.addPointToTree()

        self.app.menubar.pointer()
        self.app.menubar.ptrSatVar.set("CALSPHERE 2")
        self.app.menubar.ptrPointVar.set("test2")

        self.app.menubar.calcVector()
        self.assertTrue(self.app.menubar.results.get(0)[4:] != "0")
        self.assertTrue(self.app.menubar.results.get(1)[4:] != "0")
        self.assertTrue(self.app.menubar.results.get(2)[4:] != "0")

    def test_scheduler(self):
        """
        Tests Scheduler pop-up
        """

        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 2
        self.app.menubar.addSatelliteToTree()

        self.app.menubar.scheduler()
        self.app.menubar.satVar.set("LCS 1")
        self.app.menubar.search()

    def test_time2String1(self):
        """
        Tests time to string converter
        """

        time = datetime(2012, 12, 21, 12, 00, 00)
        timeString = self.app.menubar.time2String(time)
        self.assertEqual(timeString, "2012:12:21:12:00:00")

    def test_time2String2(self):
        """
        Tests time to string converter
        """

        time = datetime(2016, 6, 24, 9, 42, 31)
        timeString = self.app.menubar.time2String(time)
        self.assertEqual(timeString, "2016:06:24:09:42:31")

    def test_time2String3(self):
        """
        Tests time to string converter
        """

        time = datetime(2019, 3, 8, 16, 32, 59)
        timeString = self.app.menubar.time2String(time)
        self.assertEqual(timeString, "2019:03:08:16:32:59")

    def test_string2Time1(self):
        """
        Tests string to time converter
        """

        timeString = "2012:12:21:12:00:00"
        time = self.app.menubar.string2Time(timeString)
        self.assertEqual(time, datetime(2012, 12, 21, 12, 00, 00))

    def test_string2Time2(self):
        """
        Tests string to time converter
        """

        timeString = "2016:06:24:09:42:31"
        time = self.app.menubar.string2Time(timeString)
        self.assertEqual(time, datetime(2016, 6, 24, 9, 42, 31))

    def test_string2Time3(self):
        """
        Tests string to time converter
        """

        timeString = "2019:03:08:16:32:59"
        time = self.app.menubar.string2Time(timeString)
        self.assertEqual(time, datetime(2019, 3, 8, 16, 32, 59))

    def cleanUp(self):
        """
        Close out test suite
        """

        # Join the threads on close out
        self.thread.join()

class TestTaskerButtonBarMethods(unittest.TestCase):
    """
    Unit tests for button bar methods
    """

    def setUp(self):
        """
        Sets up GUI
        """

        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_zoomIn(self):
        """
        Tests zoom in button
        """

        self.app.buttonbar.zoomIn()
        self.assertTrue(self.app.buttonbar.zoomInEnabled)
        self.app.buttonbar.zoomIn()
        self.assertFalse(self.app.buttonbar.zoomInEnabled)

    def test_zoomOut(self):
        """
        Tests zoom out button
        """

        self.app.buttonbar.zoomOut()
        self.assertTrue(self.app.buttonbar.zoomOutEnabled)
        self.app.buttonbar.zoomOut()
        self.assertFalse(self.app.buttonbar.zoomOutEnabled)

    def test_setTime1(self):
        """
        Tests setTime and updateTime
        """

        self.app.buttonbar.setTime()
        self.app.buttonbar.year.delete(0, tk.END)
        self.app.buttonbar.year.insert(tk.END, "2019")
        self.app.buttonbar.month.delete(0, tk.END)
        self.app.buttonbar.month.insert(tk.END, "12")
        self.app.buttonbar.day.delete(0, tk.END)
        self.app.buttonbar.day.insert(tk.END, "21")
        self.app.buttonbar.hour.delete(0, tk.END)
        self.app.buttonbar.hour.insert(tk.END, "12")
        self.app.buttonbar.minute.delete(0, tk.END)
        self.app.buttonbar.minute.insert(tk.END, "00")
        self.app.buttonbar.second.delete(0, tk.END)
        self.app.buttonbar.second.insert(tk.END, "00")

        self.app.buttonbar.updateTime()
        self.assertEqual(self.app.statusbar.statusbar.get('1.0', tk.END).strip(), "Time Plotted: 2019-12-21 12:00:00")

    def test_setTime2(self):
        """
        Tests setTime and updateTime
        """

        self.app.buttonbar.setTime()
        self.app.buttonbar.year.delete(0, tk.END)
        self.app.buttonbar.year.insert(tk.END, "2016")
        self.app.buttonbar.month.delete(0, tk.END)
        self.app.buttonbar.month.insert(tk.END, "3")
        self.app.buttonbar.day.delete(0, tk.END)
        self.app.buttonbar.day.insert(tk.END, "8")
        self.app.buttonbar.hour.delete(0, tk.END)
        self.app.buttonbar.hour.insert(tk.END, "16")
        self.app.buttonbar.minute.delete(0, tk.END)
        self.app.buttonbar.minute.insert(tk.END, "32")
        self.app.buttonbar.second.delete(0, tk.END)
        self.app.buttonbar.second.insert(tk.END, "59")

        self.app.buttonbar.updateTime()
        self.assertEqual(self.app.statusbar.statusbar.get('1.0', tk.END).strip(), "Time Plotted: 2016-03-08 16:32:59")

    def test_setTime3(self):
        """
        Tests setTime and updateTime
        """

        self.app.buttonbar.setTime()
        self.app.buttonbar.year.delete(0, tk.END)
        self.app.buttonbar.year.insert(tk.END, "2012")
        self.app.buttonbar.month.delete(0, tk.END)
        self.app.buttonbar.month.insert(tk.END, "12")
        self.app.buttonbar.day.delete(0, tk.END)
        self.app.buttonbar.day.insert(tk.END, "21")
        self.app.buttonbar.hour.delete(0, tk.END)
        self.app.buttonbar.hour.insert(tk.END, "4")
        self.app.buttonbar.minute.delete(0, tk.END)
        self.app.buttonbar.minute.insert(tk.END, "5")
        self.app.buttonbar.second.delete(0, tk.END)
        self.app.buttonbar.second.insert(tk.END, "6")

        self.app.buttonbar.updateTime()
        self.assertEqual(self.app.statusbar.statusbar.get('1.0', tk.END).strip(), "Time Plotted: 2012-12-21 04:05:06")

    def cleanUp(self):
        """
        Closes out test suite
        """

        # Join the threads on close out
        self.thread.join()

class TestTaskerTreeViewMethods(unittest.TestCase):
    """
    Unit tests for tree view methods
    """

    def setUp(self):
        """
        Sets up GUI
        """
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_addSatellite1(self):
        """
        Tests addSatellite function
        """
        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   19341.76426397  .00000123  00000-0  10168-4 0  9998"
        line2 = "2 25544  51.6434 220.7574 0006991  10.3191 120.6360 15.50092039202187"
        sat = spacecraft(name, line1, line2)
        self.app.treeview.addSatellite(sat)
        self.assertEqual(self.app.treeview.satList[-1].name, name)
        self.assertEqual(self.app.treeview.masterList[-1].name, name)

    def test_addSatellite2(self):
        """
        Tests addSatellite function
        """
        name = "ORBCOMM FM27"
        line1 = "1 25481U 98053G   19340.54693811 -.00000035  00000-0  38449-4 0  9990"
        line2 = "2 25481  45.0083  64.2409 0001227 226.3801 133.6943 14.32857430107779"
        sat = spacecraft(name, line1, line2)
        self.app.treeview.addSatellite(sat)
        self.assertEqual(self.app.treeview.satList[-1].name, name)
        self.assertEqual(self.app.treeview.masterList[-1].name, name)

    def test_addSatellite3(self):
        """
        Tests addSatellite function
        """
        name = "ASTRA 1G"
        line1 = "1 25071U 97076A   19341.46766885  .00000034  00000-0  00000+0 0  9998"
        line2 = "2 25071   4.2014  74.2996 0004010 178.3727  54.8839  1.00271202 80634"
        sat = spacecraft(name, line1, line2)
        self.app.treeview.addSatellite(sat)
        self.assertEqual(self.app.treeview.satList[-1].name, name)
        self.assertEqual(self.app.treeview.masterList[-1].name, name)


    def test_addPoint1(self):
        """
        Tests addPoint function
        """
        point = Point("test", 42.2808, -83.7430)
        self.app.treeview.addPoint(point)
        self.assertEqual(self.app.treeview.pointList[-1].name, "test")
        self.assertEqual(self.app.treeview.pointList[-1].lat, 42.2808)
        self.assertEqual(self.app.treeview.pointList[-1].lon, -83.7430)
        self.assertEqual(self.app.treeview.masterList[-1].name, "test")

    def test_addPoint2(self):
        """
        Tests addPoint function
        """
        point = Point("test2", -42.2808, 83.7430)
        self.app.treeview.addPoint(point)
        self.assertEqual(self.app.treeview.pointList[-1].name, "test2")
        self.assertEqual(self.app.treeview.pointList[-1].lat, -42.2808)
        self.assertEqual(self.app.treeview.pointList[-1].lon, 83.7430)
        self.assertEqual(self.app.treeview.masterList[-1].name, "test2")

    def test_addPoint3(self):
        """
        Tests addPoint function
        """
        point = Point("test3", 45, -45)
        self.app.treeview.addPoint(point)
        self.assertEqual(self.app.treeview.pointList[-1].name, "test3")
        self.assertEqual(self.app.treeview.pointList[-1].lat, 45)
        self.assertEqual(self.app.treeview.pointList[-1].lon, -45)
        self.assertEqual(self.app.treeview.masterList[-1].name, "test3")

    def cleanUp(self):
        """
        Closes out test suite
        """
        # Join the threads on close out
        self.thread.join()


class TestTaskerCanvasMethods(unittest.TestCase):
    """
    Unit tests for canvas methods
    """

    def setUp(self):
        """
        Set up GUI
        """
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_enableDisableZoomIn(self):
        """
        Test zoom in enable/disable
        """
        self.app.canvas.enableZoomIn()
        self.assertEqual(self.app["cursor"], "cross")
        self.app.canvas.disableZoomIn()
        self.assertEqual(self.app["cursor"], "arrow")

    def test_enableDisableZoomOut(self):
        """
        Test zoom out enable/disable
        """
        self.app.canvas.enableZoomOut()
        self.assertEqual(self.app["cursor"], "cross")
        self.app.canvas.disableZoomOut()
        self.assertEqual(self.app["cursor"], "arrow")

    def test_onZoomIn1(self):
        """
        Test zoom in on top-left quadrant
        """
        currentZoom = self.app.canvas.plotter.zoom
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = -90
        event.ydata = 45
        event.button = MouseButton.LEFT
        self.app.canvas.onZoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)

    def test_onZoomIn2(self):
        """
        Test zoom in on top-right quadrant
        """
        currentZoom = self.app.canvas.plotter.zoom
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = 90
        event.ydata = 45
        event.button = MouseButton.LEFT
        self.app.canvas.onZoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)

    def test_onZoomIn3(self):
        """
        Test zoom in on bottom-left quadrant
        """
        currentZoom = self.app.canvas.plotter.zoom
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = -90
        event.ydata = -45
        event.button = MouseButton.LEFT
        self.app.canvas.onZoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)

    def test_onZoomIn1(self):
        """
        Test zoom in on bottom-right quadrant
        """
        currentZoom = self.app.canvas.plotter.zoom
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = 90
        event.ydata = -45
        event.button = MouseButton.LEFT
        self.app.canvas.onZoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)

    def test_onZoomOut(self):
        """
        Test zoom out
        """
        currentZoom = self.app.canvas.plotter.zoom
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = -90
        event.ydata = 45
        event.button = MouseButton.LEFT
        self.app.canvas.onZoomIn(event)

        event.xdata = 1
        event.ydata = 1
        self.app.canvas.onZoomOut(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom)

    def cleanUp(self):
        """
        Close out test suite
        """
        # Join the threads on close out
        self.thread.join()


class TestTaskerStatusBarMethods(unittest.TestCase):
    """
    Unit tests for status bar
    """

    def setUp(self):
        """
        Set up GUI
        """
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_update1(self):
        """
        Tests that time displayed in status bar can update
        """
        time = datetime(2019, 12, 21, 12, 00, 00)
        self.app.statusbar.update(time)
        self.assertEqual(self.app.time, time)

    def test_update2(self):
        """
        Tests that time displayed in status bar can update
        """
        time = datetime(2015, 3, 2, 15, 39, 3)
        self.app.statusbar.update(time)
        self.assertEqual(self.app.time, time)

    def test_update3(self):
        """
        Tests that time displayed in status bar can update
        """
        time = datetime(2012, 3, 4, 5, 6, 7)
        self.app.statusbar.update(time)
        self.assertEqual(self.app.time, time)

    def cleanUp(self):
        """
        Closes out test suite
        """
        # Join the threads on close out
        self.thread.join()


class TestTaskerOrbitPlotterMethods(unittest.TestCase):
    """
    Unit tests for Tasker Orbit Plotter methods
    """

    def setUp(self):
        """
        Set up GUI
        """
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_show(self):
        """
        Tests the show function
        """
        self.app.canvas.plotter.show()
        self.assertTrue(self.app.canvas.plotter.fig is not None)

    def test_plot1(self):
        """
        Tests the plot function for a satellite
        """
        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   19341.76426397  .00000123  00000-0  10168-4 0  9998"
        line2 = "2 25544  51.6434 220.7574 0006991  10.3191 120.6360 15.50092039202187"
        sat = spacecraft(name, line1, line2)
        self.app.canvas.plotter.plot(sat)

    def test_plot2(self):
        """
        Tests the plot function for a satellite
        """
        name = "ORBCOMM FM27"
        line1 = "1 25481U 98053G   19340.54693811 -.00000035  00000-0  38449-4 0  9990"
        line2 = "2 25481  45.0083  64.2409 0001227 226.3801 133.6943 14.32857430107779"
        sat = spacecraft(name, line1, line2)
        self.app.canvas.plotter.plot(sat)

    def test_plot3(self):
        """
        Tests the plot function for a satellite
        """
        name = "ASTRA 1G"
        line1 = "1 25071U 97076A   19341.46766885  .00000034  00000-0  00000+0 0  9998"
        line2 = "2 25071   4.2014  74.2996 0004010 178.3727  54.8839  1.00271202 80634"
        sat = spacecraft(name, line1, line2)
        self.app.canvas.plotter.plot(sat)

    def test_plotPoint1(self):
        """
        Tests the plotPoint function
        """
        point = Point("test1", 42.2808, -83.7430)
        self.app.canvas.plotter.plotPoint(point)

    def test_plotPoint2(self):
        """
        Tests the plotPoint function
        """
        point = Point("test2", -42.2808, 83.7430)
        self.app.canvas.plotter.plotPoint(point)

    def test_plotPoint3(self):
        """
        Tests the plotPoint function
        """
        point = Point("test2", 45, -90)
        self.app.canvas.plotter.plotPoint(point)

    def test_search1(self):
        """
        According to NASA, the ISS will be above Troy, MI on 12/8/19 at 6:38 PM EST (23:38 UTC).
        This test verifies that the search function can find this pass according to the TLE
        generated from celestrak on 12/7/19 around 9:00pm EST.
        """

        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   19341.76426397  .00000123  00000-0  10168-4 0  9998"
        line2 = "2 25544  51.6434 220.7574 0006991  10.3191 120.6360 15.50092039202187"
        sat = spacecraft(name, line1, line2)
        lat= 42.6064
        lon = -83.1498
        timeStart = datetime(2019, 12, 8, 23, 00, 00)
        timeEnd  = datetime(2019, 12, 8, 23, 59, 00)
        tolerance = 50
        timeResult = self.app.canvas.plotter.search(sat, lat, lon, timeStart, timeEnd, tolerance)
        self.assertTrue(timeResult is not None)

    def test_search2(self):
        """
        According to NASA, the ISS will be above Ann Arbor, MI on 12/11/19 at 5:49 PM EST (22:49 UTC).
        This test verifies that the search function can find this pass according to the TLE
        generated from celestrak on 12/7/19 around 9:00pm EST.
        """

        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   19341.76426397  .00000123  00000-0  10168-4 0  9998"
        line2 = "2 25544  51.6434 220.7574 0006991  10.3191 120.6360 15.50092039202187"
        sat = spacecraft(name, line1, line2)
        lat= 42.2808
        lon = -83.7430
        timeStart = datetime(2019, 12, 11, 22, 00, 00)
        timeEnd  = datetime(2019, 12, 11, 23, 00, 00)
        tolerance = 200
        timeResult = self.app.canvas.plotter.search(sat, lat, lon, timeStart, timeEnd, tolerance)
        self.assertTrue(timeResult is not None)

    def test_updateAll(self):
        """
        Tests the update function following a time change
        """
        time = datetime(2019, 12, 21, 12, 0, 0)
        self.app.time = time
        self.app.canvas.plotter.updateAll()

    def test_download_url1(self):
        """
        Tests the download_url function for downloading osm map tiles
        """
        self.app.canvas.plotter.download_url(5, 2, 3, "maps/test_osm1.png")
        self.assertTrue(os.path.exists("maps/test_osm1.png"))

    def test_download_url2(self):
        """
        Tests the download_url function for downloading osm map tiles
        """
        self.app.canvas.plotter.download_url(4, 2, 1, "maps/test_osm2.png")
        self.assertTrue(os.path.exists("maps/test_osm2.png"))

    def test_download_url3(self):
        """
        Tests the download_url function for downloading osm map tiles
        """
        self.app.canvas.plotter.download_url(7, 5, 6, "maps/test_osm3.png")
        self.assertTrue(os.path.exists("maps/test_osm3.png"))
        
    def test_get_concat_h(self):
        """
        Tests the get_concat_h function
        """
        self.app.canvas.plotter.download_url(2, 0, 0, "maps/test_concat_h_1.png")
        self.app.canvas.plotter.download_url(2, 1, 0, "maps/test_concat_h_2.png")
        im1 = Image.open("maps/test_concat_h_1.png")
        im2 = Image.open("maps/test_concat_h_2.png")
        im3 = self.app.canvas.plotter.get_concat_h(im1, im2)
        im3.save("maps/test_concat_h.png")
        self.assertTrue(os.path.exists("maps/test_concat_h.png"))

    def test_get_concat_v(self):
        """
        Tests the get_concat_v function
        """
        self.app.canvas.plotter.download_url(2, 0, 0, "maps/test_concat_v_1.png")
        self.app.canvas.plotter.download_url(2, 0, 1, "maps/test_concat_v_2.png")
        im1 = Image.open("maps/test_concat_v_1.png")
        im2 = Image.open("maps/test_concat_v_2.png")
        im3 = self.app.canvas.plotter.get_concat_v(im1, im2)
        im3.save("maps/test_concat_v.png")
        self.assertTrue(os.path.exists("maps/test_concat_v.png"))

    def test_drawMap(self):
        """
        Tests the drawMap function
        """
        self.app.canvas.plotter.drawMap()
        self.assertTrue(os.path.exists("map.png"))

    def test_zoomInTopLeftAndZoomOut(self):
        """
        Tests the zoomIn and zoomOut function for the top-left quadrant
        """
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = -90
        event.ydata = 45
        event.button = MouseButton.LEFT
        currentZoom = self.app.canvas.plotter.zoom
        currentCenterX = self.app.canvas.plotter.centerX
        currentCenterY = self.app.canvas.plotter.centerY
        width = self.app.canvas.plotter.width
        height = self.app.canvas.plotter.height

        self.app.canvas.plotter.zoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)
        self.assertEqual(self.app.canvas.plotter.centerX, currentCenterX - width/4)
        self.assertEqual(self.app.canvas.plotter.centerY, currentCenterY + height/4)

        self.app.canvas.plotter.zoomOut(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom)
        self.assertEqual(self.app.canvas.plotter.centerX, currentCenterX)
        self.assertEqual(self.app.canvas.plotter.centerY, currentCenterY)

    def test_zoomInTopRightAndZoomOut(self):
        """
        Tests the zoomIn and zoomOut function for the top-right quadrant
        """
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = 90
        event.ydata = 45
        event.button = MouseButton.LEFT
        currentZoom = self.app.canvas.plotter.zoom
        currentCenterX = self.app.canvas.plotter.centerX
        currentCenterY = self.app.canvas.plotter.centerY
        width = self.app.canvas.plotter.width
        height = self.app.canvas.plotter.height

        self.app.canvas.plotter.zoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)
        self.assertEqual(self.app.canvas.plotter.centerX, currentCenterX + width/4)
        self.assertEqual(self.app.canvas.plotter.centerY, currentCenterY + height/4)

        self.app.canvas.plotter.zoomOut(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom)
        self.assertEqual(self.app.canvas.plotter.centerX, currentCenterX)
        self.assertEqual(self.app.canvas.plotter.centerY, currentCenterY)

    def test_zoomInBottomLeftAndZoomOut(self):
        """
        Tests the zoomIn and zoomOut function for the bottom-left quadrant
        """
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = -90
        event.ydata = -45
        event.button = MouseButton.LEFT
        currentZoom = self.app.canvas.plotter.zoom
        currentCenterX = self.app.canvas.plotter.centerX
        currentCenterY = self.app.canvas.plotter.centerY
        width = self.app.canvas.plotter.width
        height = self.app.canvas.plotter.height

        self.app.canvas.plotter.zoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)
        self.assertEqual(self.app.canvas.plotter.centerX, currentCenterX - width/4)
        self.assertEqual(self.app.canvas.plotter.centerY, currentCenterY - height/4)

        self.app.canvas.plotter.zoomOut(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom)
        self.assertEqual(self.app.canvas.plotter.centerX, currentCenterX)
        self.assertEqual(self.app.canvas.plotter.centerY, currentCenterY)

    def test_zoomInBottomRightAndZoomOut(self):
        """
        Tests the zoomIn and zoomOut function for the bottom-right quadrant
        """
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = 90
        event.ydata = -45
        event.button = MouseButton.LEFT
        currentZoom = self.app.canvas.plotter.zoom
        currentCenterX = self.app.canvas.plotter.centerX
        currentCenterY = self.app.canvas.plotter.centerY
        width = self.app.canvas.plotter.width
        height = self.app.canvas.plotter.height

        self.app.canvas.plotter.zoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)
        self.assertEqual(self.app.canvas.plotter.centerX, currentCenterX + width/4)
        self.assertEqual(self.app.canvas.plotter.centerY, currentCenterY - height/4)

        self.app.canvas.plotter.zoomOut(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom)
        self.assertEqual(self.app.canvas.plotter.centerX, currentCenterX)
        self.assertEqual(self.app.canvas.plotter.centerY, currentCenterY)

    def test_calcOrientationVector1(self):
        """
        Tests the calcOrientationVector function for a satellite directly
        over (0, 0)
        """
        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   19341.76426397  .00000123  00000-0  10168-4 0  9998"
        line2 = "2 25544  51.6434 220.7574 0006991  10.3191 120.6360 15.50092039202187"
        sat = spacecraft(name, line1, line2)
        point = Point("test1", 0, 0)

        # Search for at time when ISS is over the point
        timeStart = datetime(2019, 12, 8, 0, 0, 0)
        timeEnd = datetime(2019, 12, 15, 0, 0, 0)
        tolerance = 200
        time = self.app.canvas.plotter.search(sat, 0, 0, timeStart, timeEnd, tolerance)
        self.app.time = time
        self.app.canvas.plotter.updateAll()

        # Get orientation vector
        vector = self.app.canvas.plotter.calcOrientationVector(sat, point)
        self.assertTrue(vector[0] < -400) # x-component should be greater than ISS altitude
        self.assertTrue(abs(vector[1]) < tolerance)
        self.assertTrue(abs(vector[2]) < tolerance)

    def test_calcOrientationVector2(self):
        """
        Tests the calcOrientationVector function for a satellite directly
        over (0, 90)
        """
        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   19341.76426397  .00000123  00000-0  10168-4 0  9998"
        line2 = "2 25544  51.6434 220.7574 0006991  10.3191 120.6360 15.50092039202187"
        sat = spacecraft(name, line1, line2)
        point = Point("test2", 0, 90)

        # Search for at time when ISS is over the point
        timeStart = datetime(2019, 12, 8, 0, 0, 0)
        timeEnd = datetime(2019, 12, 15, 0, 0, 0)
        tolerance = 200
        time = self.app.canvas.plotter.search(sat, 0, 90, timeStart, timeEnd, tolerance)
        self.app.time = time
        self.app.canvas.plotter.updateAll()

        # Get orientation vector
        vector = self.app.canvas.plotter.calcOrientationVector(sat, point)
        self.assertTrue(abs(vector[0]) < tolerance)
        self.assertTrue(vector[1] < -400) # y-component should be greater than ISS altitude
        self.assertTrue(abs(vector[2]) < tolerance)

    def test_calcOrientationVector3(self):
        """
        Tests the calcOrientationVector function for a satellite approximately
        over Michigan
        """
        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   19341.76426397  .00000123  00000-0  10168-4 0  9998"
        line2 = "2 25544  51.6434 220.7574 0006991  10.3191 120.6360 15.50092039202187"
        sat = spacecraft(name, line1, line2)
        point = Point("test2", 42, -83)

        # Search for at time when ISS is over the point
        timeStart = datetime(2019, 12, 8, 0, 0, 0)
        timeEnd = datetime(2019, 12, 15, 0, 0, 0)
        tolerance = 200
        time = self.app.canvas.plotter.search(sat, 42, -83, timeStart, timeEnd, tolerance)
        self.app.time = time
        self.app.canvas.plotter.updateAll()

        # Get orientation vector
        vector = self.app.canvas.plotter.calcOrientationVector(sat, point)
        self.assertTrue(sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2) > 400 and
                        sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2) < 500) 
                        # Magnitude of vector should be approximately ISS altitude


    def test_lla2ecef1(self):
        """
        Tests the LLA to ECEF conversion function
        """
        p = self.app.canvas.plotter.lla2ecef(45, 90, 2)
        self.assertTrue(abs(p[0] - 0) < 100)
        self.assertTrue(abs(p[1] - 4519) < 1)
        self.assertTrue(abs(p[2] - 4488.8) < 1)
        
    def test_lla2ecef2(self):
        """
        Tests the LLA to ECEF conversion function
        """
        p = self.app.canvas.plotter.lla2ecef(0, 45, 1)
        self.assertTrue(abs(p[0] - 4510.7) < 1)
        self.assertTrue(abs(p[1] - 4510.7) < 1)
        self.assertTrue(abs(p[2] - 0) < 100)
        

    def cleanUp(self):
        """
        Closes out the test suite
        """
        # Join the threads on close out
        self.thread.join()


class TestMultiColumnListBox(unittest.TestCase):
    """
    Unit Test for multi-column listbox
    """
    
    def test_multiColumnListBox(self):
        """
        Runs the example multi-column listbox to verify functionality
        """
        root = tk.Tk()
        win = GUI(root)
        win.pack(fill=tk.BOTH, expand=True)

class TestSatCatScraper(unittest.TestCase):
    """
    Unit tests for satellite catalog scraper
    """

    def setUp(self):
        """
        Set up scraper
        """
        Scraper()

    def checkFileExists(self):
        """
        Checks that the satellite catalog file was created
        """
        self.assertTrue(os.path.exists("satCat.txt"))

    def test_Scraper1(self):
        """
        Tests that the satellite catalog file read in is correct
        """
        file = open("satCat.txt", "r")
        lines = file.readlines()
        name = lines[0]
        line1 = lines[1]
        line2 = lines[2]

        self.assertEqual(name.strip(), "CALSPHERE 1")

    def test_Scraper2(self):
        """
        Tests that the satellite catalog file read in is correct
        """
        file = open("satCat.txt", "r")
        lines = file.readlines()
        name = lines[3]
        line1 = lines[4]
        line2 = lines[5]

        self.assertEqual(name.strip(), "CALSPHERE 2")

    def testScraper3(self):
        """
        Tests that the satellite catalog file read in is correct
        """
        file = open("satCat.txt", "r")
        lines = file.readlines()
        file.close()
        name = lines[6]
        line1 = lines[7]
        line2 = lines[8]

        self.assertEqual(name.strip(), "LCS 1")

class testSpacecraft(unittest.TestCase):
    """
    Unit tests for spacecraft class
    """

    def setUp(self):
        """
        Reads in the satellite catalog file
        """
        Scraper()
        file = open("satCat.txt", "r")
        self.lines = file.readlines()
        file.close()

    def testSpacecraft1(self):
        """
        Tests that spacecraft class can be constructed correctly
        """
        name = self.lines[0]
        line1 = self.lines[1]
        line2 = self.lines[2]

        sc = spacecraft(name, line1, line2)

        self.assertEqual(sc.name, "CALSPHERE 1")
        self.assertEqual(sc.catalogNumber.strip(), "00900U")
        self.assertEqual(sc.intlDesignator.strip(), "64063C")

    def testSpacecraft2(self):
        """
        Tests that spacecraft class can be constructed correctly
        """
        name = self.lines[3]
        line1 = self.lines[4]
        line2 = self.lines[5]

        sc = spacecraft(name, line1, line2)

        self.assertEqual(sc.name, "CALSPHERE 2")
        self.assertEqual(sc.catalogNumber.strip(), "00902U")
        self.assertEqual(sc.intlDesignator.strip(), "64063E")

    def testSpacecraft3(self):
        """
        Tests that spacecraft class can be constructed correctly
        """
        name = self.lines[6]
        line1 = self.lines[7]
        line2 = self.lines[8]

        sc = spacecraft(name, line1, line2)

        self.assertEqual(sc.name, "LCS 1")
        self.assertEqual(sc.catalogNumber.strip(), "01361U")
        self.assertEqual(sc.intlDesignator.strip(), "65034C")

class testPoint(unittest.TestCase):
    """
    Unit tests for Tasker points
    """

    def testPoint1(self):
        """
        Tests that points can be constructed correctly
        """
        point = Point("test1", 42.2808, -83.7430)
        self.assertEqual(point.name, "test1")
        self.assertEqual(point.lat, 42.2808)
        self.assertEqual(point.lon, -83.7430)

    def testPoint2(self):
        """
        Tests that points can be constructed correctly
        """
        point = Point("test2", -42.2808, 83.7430)
        self.assertEqual(point.name, "test2")
        self.assertEqual(point.lat, -42.2808)
        self.assertEqual(point.lon, 83.7430)

    def testPoint3(self):
        """
        Tests that points can be constructed correctly
        """
        point = Point("test3", 45, 90)
        self.assertEqual(point.name, "test3")
        self.assertEqual(point.lat, 45)
        self.assertEqual(point.lon, 90)

if __name__ == '__main__':
    unittest.main()