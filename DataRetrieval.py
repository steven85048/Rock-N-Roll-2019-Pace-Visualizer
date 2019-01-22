import requests
from bs4 import BeautifulSoup

ID_LOW = 1
ID_HIGH = 9999

BASE_URL = "https://www.runrocknroll.com/en/events/arizona/the-races/half-marathon/2019-results/athlete?id="

class DataRetrieval:
    def __init__( self, strategy ):
        self.retrievedRunners = []

        # should use strategy design but w/e
        if( strategy == 0 ):
            self._retrieveDataWithScraping()
        else:
            self._retrieveDataWithFile()

    def getPoints( self ):
        return self.retrievedRunners

    def _retrieveDataWithScraping( self ):
        for bibId in range( ID_LOW, ID_HIGH ):
            scrapeURL = BASE_URL + str( bibId )
            retrievedRunner = self._scrapeAtUrl( scrapeURL )
            if( retrievedRunner != None ):
                self.retrievedRunners.append( retrievedRunner )

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
        pass