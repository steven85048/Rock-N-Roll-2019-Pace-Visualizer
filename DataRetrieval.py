import requests
import pickle
import atexit
from bs4 import BeautifulSoup
from enum import Enum

ID_LOW = 1
ID_HIGH = 9999

BASE_URL = "https://www.runrocknroll.com/en/events/arizona/the-races/half-marathon/2019-results/athlete?id="

DATA_FILE = "datafile.txt"
METADATA_FILE = "metadata.txt"

# we record where we were at during the exit so we can get back to it; first line of file should be the line stopped
stoppedLine = 1
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

class FilterType(Enum):
    GENDER = 0,
    DIVISION = 1

class Gender(Enum):
    MALE = "M",
    FEMALE = "F"

class Division(Enum):
    SC12_14 = "12-14",
    SC15_17 = "15-17",
    SC18_24 = "18-24",
    SC25_29 = "25-29",
    SC30_34 = "30-34",
    SC35_39 = "35-39",
    SC40_44 = "40-44",
    SC45_49 = "45-49",
    SC50_54 = "50-54",
    SC55_59 = "55-59",
    SC60_64 = "60-64",
    SC65_69 = "65-69",
    SC70_74 = "70-74"

class DataRetrieval:

    # PUBLIC FUNCTIONS

    def __init__( self ):
        self.retrievedRunners = []
        self.filterList = []

    def retrieveData( self ):
        self._fileToAppend = open(DATA_FILE, "ab")
        self._retrieveDataWithScraping()

    def getPoints( self ):
        self._retrieveDataWithFile()
        return self.retrievedRunners

    def addGenderFilter( self, genderType ):
        filter = {}
        filter['type'] = FilterType.GENDER
        filter['gender'] = genderType
        
        self.filterList.append(filter)

    def addDivisionFilter( self, divisionType ):
        filter = {}
        filter['type'] = FilterType.DIVISION
        filter['division'] = divisionType

        self.filterList.append(filter)

    # PRIVATE FUNCTIONS

    def _retrieveDataWithScraping( self ):
        for bibId in range( ID_LOW, ID_HIGH ):
            print( bibId )

            scrapeURL = BASE_URL + str( bibId )
            retrievedRunner = self._scrapeAtUrl( scrapeURL )

            if( retrievedRunner != None ):
                pickle.dump( retrievedRunner, self._fileToAppend )

            global stoppedLine
            stoppedLine = bibId + 1

    def _scrapeAtUrl( self, url ):
        currentPage = requests.get( url )

        soupParser = BeautifulSoup( currentPage.text, 'html.parser' )

        raceResults = soupParser.find( id = "race-results" )
        racerInfo = soupParser.find( id = "racer-info" )

        if( raceResults == None ):
            return None

        theResultsDivs = raceResults.find_all('div')
        theRacerInfoDivs = racerInfo.find_all('div')

        theRunnerResults = self._parseRunnerResultDivs( theResultsDivs )
        theRunnerInfo = self._parseRunnerInfoDivs( theRacerInfoDivs )

        if( theRunnerResults == None or theRunnerInfo == None ):
            return None

        theFinalRunner = {}
        theFinalRunner['results'] = theRunnerResults
        theFinalRunner['runnerInfo'] = theRunnerInfo

        print( theFinalRunner )

        return theFinalRunner

    def _parseRunnerInfoDivs( self, divs ):
        theRunner = {}

        theRunner['name'] = divs[4].text.strip()

        if( theRunner['name'] == '' ):
            return None

        theRunner['bibNumber'] = divs[7].text.strip()
        theRunner['gender'] = divs[10].text.strip()
        theRunner['division'] = divs[13].text.strip()

        return theRunner

    def _parseRunnerResultDivs( self, divs ):
        theRunner = {}

        theRunner['finishTime'] = divs[2].text.strip()

        if( theRunner['finishTime'] == '00:00:00' ):
            return None

        theRunner['paceTime'] = divs[5].text.strip()
        theRunner['overallRank'] = divs[10].text.strip()
        theRunner['divisionRank'] = divs[13].text.strip()
        theRunner['genderRank'] = divs[16].text.strip()

        return theRunner

    def _retrieveDataWithFile( self ):
        with open( DATA_FILE, "rb" ) as dataFile:
            try:
                while( True ):
                    currentRunner = pickle.load( dataFile )

                    if( self._filterRunner( currentRunner ) ):
                        self.retrievedRunners.append( currentRunner )
            except:
                pass

    def _filterRunner( self, runner ):
        for filter in self.filterList:
            if( filter['type'] == FilterType.GENDER and not runner['runnerInfo']['gender'] == filter['gender'].value[0] ):
                return False
            elif( filter['type'] == FilterType.DIVISION and filter['division'].value[0] not in runner['runnerInfo']['division'] ):
                return False

        return True