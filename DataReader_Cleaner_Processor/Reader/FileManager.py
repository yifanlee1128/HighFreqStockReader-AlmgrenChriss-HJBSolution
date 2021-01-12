import os
from os import access, R_OK
from Reader.TAQTradesReader import TAQTradesReader
from Reader.TAQQuotesReader import TAQQuotesReader

# Version 1802181651 - See Test_FileManager
class FileManager(object):
    '''
    Class to manage TAQ files for ATQS 2019
    '''
    def __init__(
        self, 
        baseDir # eg /data/TAQ, assumes /data/TAQ/trades and quotes, and data sub-directories in each 
    ):
        '''
        Make sure baseDir has the proper structure. Save baseDir. 
        '''
        if not baseDir.endswith('/'):
            baseDir = baseDir + "/"
        if not os.path.exists( baseDir ):
            raise Exception( "%s does not exist" % baseDir )
        if( not access( baseDir, R_OK ) ):
            raise Exception( "You don't have access to directory %s" % baseDir )
        if( not( os.path.exists( baseDir + "quotes" ) and os.path.exists( baseDir + "trades" ) ) ):
            raise Exception( "%s must have sub-directories quotes and trades" % baseDir )
        if( not( access( baseDir + "quotes", R_OK ) and access( baseDir + "trades", R_OK ) ) ):
            raise Exception( "You don't have access to both the trades and quotes subdirectories of %s" % baseDir )
        self._baseDir = baseDir
        
    def getTradeDates(self, startDateString, endDateString ):
        return self._getDates( self._baseDir + "trades", startDateString, endDateString )
    
    def getQuoteDates(self, startDateString, endDateString ):
        return self._getDates( self._baseDir + "quotes", startDateString, endDateString )
    
    def getTradeTickers(self, dateString ):
        tickers = filter( lambda file: file.endswith( "_trades.binRT" ), os.listdir( self._baseDir + "trades/" + dateString ) )
        tickers = map( lambda ticker: ticker[:-13], tickers )
        return list( tickers )
    
    def getQuoteTickers(self, dateString ):
        tickers = filter( lambda file: file.endswith( "_quotes.binRQ" ), os.listdir( self._baseDir + "quotes/" + dateString ) )
        tickers = map( lambda ticker: ticker[:-13], tickers )
        return list( tickers )

    def _getDates(
        self,
        dir, # "/data/taq/quotes" or "/data/taq/trades"
        startDateString, # eg "20070620"
        endDateString # eg "20070630"
    ):
        if startDateString == None:
            startDateString = "20070620"
        if endDateString == None:
            endDateString = "20070930"
        try:
            startDate = int( startDateString )
            endDate = int( endDateString )
        except:
            raise Exception( "Could not convert date string to dates" )
        
        goodDirs = list(
            filter(
                lambda dirName: self._goodDate( startDate, endDate, dirName ),
                os.listdir( dir )
            )
        )
        return goodDirs
        
    def _goodDate(self, startDate, endDate, dateString ):
        try:
            date = int( dateString)
        except:
            return False
        return date >= startDate and date < endDate
        
    def getTradesFile(
        self, 
        dateString, # eg "20070620", a string
        ticker 
    ):
        filePathName = self._baseDir + "trades/" + dateString + "/" + ticker + "_trades.binRT"
        if( not( os.path.exists( filePathName ) ) ):
            raise Exception( "File %s doesn't exist" % filePathName )
        if( not( access( filePathName, R_OK ) ) ):
            raise Exception( "You don't have access to %s" % filePathName )
        return TAQTradesReader( filePathName )
        
    def getQuotesFile(
        self, 
        dateString, # eg "20070620", a string 
        ticker
    ):
        filePathName = self._baseDir + "quotes/" + dateString + "/" + ticker + "_quotes.binRQ"
        if( not( os.path.exists( filePathName ) ) ):
            raise Exception( "File %s doesn't exist" % filePathName )
        if( not( access( filePathName, R_OK ) ) ):
            raise Exception( "You don't have access to %s" % filePathName )
        return TAQQuotesReader( filePathName )
        
        
 
        