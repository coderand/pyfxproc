#include "..\..\fxproc.fxh"

DefSampler2D_Basic( baseMap )
DefSampler2D_Basic( baseMap2 )

// Simple Box Filter
DefBasicTechnique( LowPass )
{
	float4 clr = 0;

	int r = 5;
	float w = 0;

	for ( int y = -r; y <= r; y++ )
	for ( int x = -r; x <= r; x++ )
	{
		clr.rgb += tex2Dlod( baseMap_Clamp, float4( tc + offsetPixel(x, y), 0, 0 ) );
		w += 1.0;
	}

	clr.rgb /= w;

	return float4( clr.rgb, 1.0f );
}

// Subtract images and add 0.5
DefBasicTechnique( HighPass )
{
	float4 clr1 = tex2D( baseMap, tc );
	float4 clr2 = tex2D( baseMap2, tc );

	float3 clr = clr2.rgb - clr1.rgb + 0.5;

	return float4( clr.rgb, 1.0f );
}
