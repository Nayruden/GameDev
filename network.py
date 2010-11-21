import struct

def sendData( conn, data ):
	size = struct.pack( "I", len( data ) )
	conn.send( size + data )

def receiveData( conn ):
	size, = struct.unpack( "I", conn.recv( 4 ) )
	return conn.recv( size )
