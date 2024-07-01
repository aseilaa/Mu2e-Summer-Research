## GUI for Mu2e Project
PyQt5 creates a graphical user interface (GUI) for displaying matrix data. 
It features a main window (MainWindow) with navigation controls to switch between different matrix displays (MatrixDisplay).

## Classes and Functions

MatrixDisplay Class

- Represents a widget displaying matrix data.
- Initializes with a title and data for channel numbers, current numbers, and voltage numbers.
- Uses PyQt5 layout managers (QVBoxLayout, QHBoxLayout, QGroupBox) to structure and display data.

  
MainWindow Class

- Represents the main application window.
- Initializes with a title and size.
- Uses QStackedWidget to stack multiple MatrixDisplay instances for display.
Includes navigation controls (Next button) to switch between matrix displays dynamically.

QPushButton
- Navigation between matrix displays

fetch_data()
- Simulates data retrieval.
- Returns a list of tuples, each containing lists of channel numbers, current (I) numbers, and voltage (V) numbers.
- Later will be replaced with actual data 

## Updates made
- Added logic to handle navigation beyond the initial set of matrix displays (self.max_pages)
- Fetches new data and adds new MatrixDisplay instances when the Next button is clicked.
- Compatibility between the RasberryPI (haven't been tested)

## What's next?
- Real-time data 
- Try to replace the data with the real data (already implemented), but I want to see if it works
