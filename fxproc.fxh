// fxproc.fxh
// Useful .fx helpers.
// Created by Dmitry "AND" Andreev 2013-2015.
// License Creative Commons Zero v1.0 Universal.

#ifndef __FXPROC_FXH__
#define __FXPROC_FXH__

float4 vTargetSize;

//

#define offsetPixel(du, dv) float2((du), (dv)) * vTargetSize.zw

#define DefSampler2D_Custom(name, texname) \
	texture texname< \
	string UIName = #name; \
	string ResourceType = "2D"; \
	>; \
	sampler2D name = sampler_state { \
		Texture = <texname>;

#define DefSampler2D_Basic(name) \
	texture name##Texture< \
	string UIName = #name; \
	string ResourceType = "2D"; \
	>; \
	sampler2D name = sampler_state { \
		Texture = <name##Texture>; \
		Filter = MIN_MAG_MIP_LINEAR; \
		AddressU = Wrap; \
		AddressV = Wrap; }; \
	sampler2D name##_Clamp = sampler_state { \
		Texture = <name##Texture>; \
		Filter = MIN_MAG_MIP_LINEAR; \
		AddressU = Clamp; \
		AddressV = Clamp; };

#define DefSamplerCube_Basic(name) \
	texture name##Texture< \
	string UIName = #name; \
	string ResourceType = "Cube"; \
	>; \
	samplerCUBE name = sampler_state { \
		Texture = <name##Texture>; \
		Filter = MIN_MAG_MIP_LINEAR; \
		AddressU = Wrap; \
		AddressV = Wrap; }; \
	samplerCUBE name##_Clamp = sampler_state { \
		Texture = <name##Texture>; \
		Filter = MIN_MAG_MIP_LINEAR; \
		AddressU = Clamp; \
		AddressV = Clamp; };

#define DefBasicTechnique(name) \
	float4 PS##name(in float2 tc : TEXCOORD0, in float2 stc : VPOS) : COLOR; \
	technique name { pass P0 { \
		VertexShader = compile vs_3_0 VSQuadMain(); \
		PixelShader  = compile ps_3_0 PS##name(); \
	} } \
	float4 PS##name(in float2 tc : TEXCOORD0, in float2 stc : VPOS) : COLOR

//


void VSQuadMain(
	out float4 outPos : POSITION,
	out float2 outTc : TEXCOORD0,
	in float3 inPos : POSITION
	)
{
	outPos = float4(inPos.x * 2 - 1, inPos.y * 2 - 1, 0, 1);
	outTc.x = inPos.x;
	outTc.y = 1 - inPos.y;
}

#endif
