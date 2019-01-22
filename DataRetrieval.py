import requests
import pickle
import atexit
from bs4 import BeautifulSoup

ID_LOW = 1
ID_HIGH = 9999

BASE_URL = "https://www.runrocknroll.com/en/events/arizona/the-races/half-marathon/2019-results/athlete?id="

DATA_FILE = "datafile.txt"
METADATA_FILE = "metadata.txt"

# we record where we were at during the exit so we can get back to it; first line of file should be the line stopped
stoppedLine = 0
try:
    metadata = open( METADATA_FILE, "r" )
    stoppedLine = int( metadata.readline() )
    ID_LOW = stoppedLine
except:
    pass

@atexit.register
def recordLineStopped():
    print( stoppedLine )
    metadataWrite = open( METADATA_FILE, "w" )
    metadataWrite.write( str( stoppedLine ) )

class DataRetrieval:

    # PUBLIC FUNCTIONS

    def __init__( self ):
        self.retrievedRunners = []

    def retrieveData( self ):
        self._fileToAppend = open(DATA_FILE, "ab")
        self._retrieveDataWithScraping()

    def getPoints( self ):
        self._retrieveDataWithFile()
        return self.retrievedRunners

    # PRIVATE FUNCTIONS

    def _retrieveDataWithScraping( self ):
        for bibId in range( ID_LOW, ID_HIGH ):
            print( bibId )

            scrapeURL = BASE_URL + str( bibId )
            retrievedRunner = self._scrapeAtUrl( scrapeURL )

            # order matters; we want to make sure the request has finished
            global stoppedLine

            if( retrievedRunner != None ):
                pickle.dump( retrievedRunner, self._fileToAppend )

            stoppedLine = bibId + 1

    def _scrapeAtUrl( self, url ):
        currentPage = requests.get( url )

        soupParser = BeautifulSoup( currentPage.text, 'html.parser' )
        raceResults = soupParser.find( id = "race-results" )

        if( raceResults == None ):
            return None

        theDivs = raceResults.find_all('div')
        
        theRunner = self._parseRunnerResultDivs( theDivs )
        return None if theRunner == None else theRunner

    def _parseRunnerResultDivs( self, divs ):
        theRunner = {}

        theRunner['finishTime'] = divs[2].text.strip()

        if( theRunner['finishTime'] == '00:00:00' ):
            return None

        theRunner['paceTime'] = divs[5].text.strip()
        theRunner['overallRank'] = divs[10].text.strip()
        theRunner['divisionRank'] = divs[13].text.strip()
        theRunner['genderRank'] = divs[16].text.strip()

        print( theRunner )

        return theRunner

    def _retrieveDataWithFile( self ):
        with open( DATA_FILE, "rb" ) as dataFile:
            currentRunner = pickle.load( dataFile )
            self.retrievedRunners.append( currentRunner )