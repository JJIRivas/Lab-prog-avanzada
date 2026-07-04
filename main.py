import incidentRepo
from fileHandlers import fileBrowser, parserSelector
from ui import MainApplication


class main:
    def __init__(self):
        self.app = MainApplication()
        self.browseFile = fileBrowser.browseFile
        self.parserChooser = parserSelector.getParser
        self.app.sidebar.fileBtn.config(command=self.fileImporting)

        self.app.mainloop()

    def fileImporting(self):
        incidentDB = incidentRepo.IncidentRepo()
        fp = fileBrowser.browseFile()
        if fp:
            parser = parserSelector.getParser(fp)
            incidentDB.load(parser, fp)


if __name__ == "__main__":
    main()
