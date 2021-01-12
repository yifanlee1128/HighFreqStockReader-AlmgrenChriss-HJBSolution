import gzip
import _struct
from _collections import deque
 
class BinReader(object):
    
    def __init__(self, filePathName, conversionFmt, bufSizeInRecs ):
        self._c = _struct.Struct( conversionFmt )
        self._s = _struct.calcsize( conversionFmt )
        self._b = bytearray( bufSizeInRecs * self._s )
        self._o = 0
        self._in = gzip.open( filePathName, "rb" )
        self._m = len( self._b )
        self._sn = _struct.Struct( ">Q" )
        self._r = deque()
        self._read()
        
    def getSN(self):
        return self._sn.unpack_from( self._b, self._o )[ 0 ]

    def readThrough(self,sn):
        # V2 - Implement ALL, LAST, or applyFunc functionality to reduce object creation
        self._last = sn
        self._r.clear()
        while( self.getSN() <= sn ):
            self._r.append( self.next() )
            if( not self.hasNext() ):
                break
        return self._r
    
    # Read data into our buffer
    def _read(self):
        if self._m == len( self._b ):
            self._m = self._in.readinto( self._b )
            self._o = 0
            if self._m < len( self._b ):
                self.close()
                
    def hasNext( self ):
        return( self._o < self._m )
    
    # Process next record in our buffer or,
    # if at end of buffer, read more data
    # into buffer
    def next( self ):
        rec = self._c.unpack_from( self._b, self._o )
        self._o = self._o + self._s
        if self._o == self._m:
            self._read()
        return rec
    
    def close(self):
        if self._in != None:
            self._in.close()
            self._in = None
           
    # Get a deque of all records read
    def getRecs(self):
        return self._r
    
    # Return true if this reader has read through sn
    def hasRecs(self,sn):
        return self._last <= sn
    
    # Write all recs to a specified binary file
    def writeTo( self, outFile ):
        for rec in self._r:
            outFile.write( self._c.pack( *rec ) ) 
