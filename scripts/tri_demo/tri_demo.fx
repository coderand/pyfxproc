#include "..\..\fxproc.fxh"

DefBasicTechnique( RasterizeQuad )
{
	return float4( 0, 1, 0, 0 ); // green
}

DefBasicTechnique( RasterizeTri )
{
	return float4( 1, 0, 0, 0 ); // red
}
