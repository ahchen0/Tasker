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
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_MenuBar_addSatellite(self):
        self.app.menubar.addSatellite()
        self.assertTrue(True) # Test passes if it doesn't crash before this line

    def test_MenuBar_addSatelliteToTree(self):
        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 0
        self.app.menubar.addSatelliteToTree()
        self.assertEqual(self.app.treeview.satList[0].name, "CALSPHERE 1")

        self.app.menubar.listbox.selectedRow = 1
        self.app.menubar.addSatelliteToTree()
        self.assertEqual(self.app.treeview.satList[1].name, "CALSPHERE 2")

    def test_MenuBar_addPoint(self):
        self.app.menubar.addPoint()
        self.assertTrue(True) # Test passes if it doesn't crash before this line

    def test_MenuBar_addPointToTree(self):
        self.app.menubar.addPoint()
        self.app.menubar.pointName.delete(0, tk.END)
        self.app.menubar.pointName.insert(0, "test")
        self.app.menubar.pointLat.delete(0, tk.END)
        self.app.menubar.pointLat.insert(0, "42.2808")
        self.app.menubar.pointLon.delete(0, tk.END)
        self.app.menubar.pointLon.insert(0, "-83.7430")
        self.app.menubar.addPointToTree()
        self.assertEqual(self.app.treeview.pointList[0].name, "test")
        self.assertEqual(self.app.treeview.pointList[0].lat, 42.2808)
        self.assertEqual(self.app.treeview.pointList[0].lon, -83.7430)

    def test_pointer(self):
        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 1
        self.app.menubar.addSatelliteToTree()

        self.app.menubar.addPoint()
        self.app.menubar.pointName.delete(0, tk.END)
        self.app.menubar.pointName.insert(0, "test")
        self.app.menubar.pointLat.delete(0, tk.END)
        self.app.menubar.pointLat.insert(0, "42.2808")
        self.app.menubar.pointLon.delete(0, tk.END)
        self.app.menubar.pointLon.insert(0, "-83.7430")
        self.app.menubar.addPointToTree()

        self.app.menubar.pointer()
        self.app.menubar.ptrSatVar.set("CALSPHERE 2")
        self.app.menubar.ptrPointVar.set("test")

        self.app.menubar.calcVector()
        self.assertTrue(self.app.menubar.results.get(0)[4:] != "0")
        self.assertTrue(self.app.menubar.results.get(1)[4:] != "0")
        self.assertTrue(self.app.menubar.results.get(2)[4:] != "0")

    def test_scheduler(self):
        self.app.menubar.addSatellite()
        self.app.menubar.listbox.selectedRow = 2
        self.app.menubar.addSatelliteToTree()

        self.app.menubar.scheduler()
        self.app.menubar.satVar.set("LCS 1")
        self.app.menubar.search()

    def test_time2String(self):
        time = datetime(2012, 12, 21, 12, 00, 00)
        timeString = self.app.menubar.time2String(time)
        self.assertEqual(timeString, "2012:12:21:12:00:00")

    def test_string2Time(self):
        timeString = "2012:12:21:12:00:00"
        time = self.app.menubar.string2Time(timeString)
        self.assertEqual(time, datetime(2012, 12, 21, 12, 00, 00))

    def cleanUp(self):
        # Join the threads on close out
        self.thread.join()

class TestTaskerButtonBarMethods(unittest.TestCase):
    """
    Unit tests for button bar methods
    """

    def setUp(self):
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_zoomIn(self):
        self.app.buttonbar.zoomIn()
        self.assertTrue(self.app.buttonbar.zoomInEnabled)
        self.app.buttonbar.zoomIn()
        self.assertFalse(self.app.buttonbar.zoomInEnabled)

    def test_zoomOut(self):
        self.app.buttonbar.zoomOut()
        self.assertTrue(self.app.buttonbar.zoomOutEnabled)
        self.app.buttonbar.zoomOut()
        self.assertFalse(self.app.buttonbar.zoomOutEnabled)

    def test_setTime(self):
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

    def cleanUp(self):
        # Join the threads on close out
        self.thread.join()

class TestTaskerTreeViewMethods(unittest.TestCase):
    """
    Unit tests for tree view methods
    """

    def setUp(self):
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_addSatellite(self):
        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   19341.76426397  .00000123  00000-0  10168-4 0  9998"
        line2 = "2 25544  51.6434 220.7574 0006991  10.3191 120.6360 15.50092039202187"
        sat = spacecraft(name, line1, line2)
        self.app.treeview.addSatellite(sat)
        self.assertEqual(self.app.treeview.satList[-1].name, name)
        self.assertEqual(self.app.treeview.masterList[-1].name, name)

        name = "ORBCOMM FM27"
        line1 = "1 25481U 98053G   19340.54693811 -.00000035  00000-0  38449-4 0  9990"
        line2 = "2 25481  45.0083  64.2409 0001227 226.3801 133.6943 14.32857430107779"
        sat = spacecraft(name, line1, line2)
        self.app.treeview.addSatellite(sat)
        self.assertEqual(self.app.treeview.satList[-1].name, name)
        self.assertEqual(self.app.treeview.masterList[-1].name, name)

    def test_addPoint(self):
        point = Point("test", 42.2808, -83.7430)
        self.app.treeview.addPoint(point)
        self.assertEqual(self.app.treeview.pointList[-1].name, "test")
        self.assertEqual(self.app.treeview.pointList[-1].lat, 42.2808)
        self.assertEqual(self.app.treeview.pointList[-1].lon, -83.7430)
        self.assertEqual(self.app.treeview.masterList[-1].name, "test")

        point = Point("test2", -42.2808, 83.7430)
        self.app.treeview.addPoint(point)
        self.assertEqual(self.app.treeview.pointList[-1].name, "test2")
        self.assertEqual(self.app.treeview.pointList[-1].lat, -42.2808)
        self.assertEqual(self.app.treeview.pointList[-1].lon, 83.7430)
        self.assertEqual(self.app.treeview.masterList[-1].name, "test2")

    def cleanUp(self):
        # Join the threads on close out
        self.thread.join()


class TestTaskerCanvasMethods(unittest.TestCase):
    """
    Unit tests for canvas methods
    """

    def setUp(self):
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_enableDisableZoomIn(self):
        self.app.canvas.enableZoomIn()
        self.assertEqual(self.app["cursor"], "cross")
        self.app.canvas.disableZoomIn()
        self.assertEqual(self.app["cursor"], "arrow")

    def test_enableDisableZoomOut(self):
        self.app.canvas.enableZoomOut()
        self.assertEqual(self.app["cursor"], "cross")
        self.app.canvas.disableZoomOut()
        self.assertEqual(self.app["cursor"], "arrow")

    def test_onZoomIn(self):
        currentZoom = self.app.canvas.plotter.zoom
        event = MouseEvent(name = "button_press_event", button = MouseButton.LEFT, canvas = self.app.canvas.canvas, x = 503, y = 670)
        event.xdata = -90
        event.ydata = 45
        event.button = MouseButton.LEFT
        self.app.canvas.onZoomIn(event)
        self.assertEqual(self.app.canvas.plotter.zoom, currentZoom + 1)

    def test_onZoomOut(self):
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
        # Join the threads on close out
        self.thread.join()


class TestTaskerStatusBarMethods(unittest.TestCase):

    def setUp(self):
        root=tk.Tk()
        self.app=Application(master=root)

        # Run the GUI in a different thread so it can run simultaneously
        # with the unit tests
        self.thread = threading.Thread(target = self.app.mainloop)

    def test_update(self):
        time = datetime(2019, 12, 21, 12, 00, 00)
        self.app.statusbar.update(time)
        self.assertEqual(self.app.time, time)

    def cleanUp(self):
        # Join the threads on close out
        self.thread.join()


class TestMultiColumnListBox(unittest.TestCase):
    """
    Unit Test for multi-column listbox
    """
    
    def test_multiColumnListBox(self):
        root = tk.Tk()
        win = GUI(root)
        win.pack(fill=tk.BOTH, expand=True)

class TestSatCatScraper(unittest.TestCase):
    """
    Unit tests for satellite catalog scraper
    """

    def setUp(self):
        Scraper()

    def checkFileExists(self):
        self.assertTrue(os.path.exists("satCat.txt"))

    def test_Scraper1(self):
        file = open("satCat.txt", "r")
        lines = file.readlines()
        name = lines[0]
        line1 = lines[1]
        line2 = lines[2]

        self.assertEqual(name.strip(), "CALSPHERE 1")

    def test_Scraper2(self):
        file = open("satCat.txt", "r")
        lines = file.readlines()
        name = lines[3]
        line1 = lines[4]
        line2 = lines[5]

        self.assertEqual(name.strip(), "CALSPHERE 2")

    def testScraper3(self):
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
        Scraper()
        file = open("satCat.txt", "r")
        self.lines = file.readlines()
        file.close()

    def testSpacecraft(self):
        name = self.lines[0]
        line1 = self.lines[1]
        line2 = self.lines[2]

        sc = spacecraft(name, line1, line2)

        self.assertEqual(sc.name, "CALSPHERE 1")
        self.assertEqual(sc.catalogNumber.strip(), "00900U")
        self.assertEqual(sc.intlDesignator.strip(), "64063C")

class testPoint(unittest.TestCase):

    def testPoint(self):
        point = Point("test", 42.2808, -83.7430)
        self.assertEqual(point.name, "test")
        self.assertEqual(point.lat, 42.2808)
        self.assertEqual(point.lon, -83.7430)

if __name__ == '__main__':
    unittest.main()