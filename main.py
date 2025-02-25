from JobApplicationGUI import *
import sys


# Run the PyQt application
def run_app():
    app = QApplication(sys.argv)
    window = JobInfoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()