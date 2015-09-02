from fxproc import Effect

def triDemo():

	print('.load effect file')
	fx = Effect.open("tri_demo.fx")

	print('.create render target')
	out = fx.createRenderTarget(32, 32, "A8R8G8B8")

	print('.set render target')
	fx.setRenderTarget(out)

	print('.render green quad')
	fx.drawQuad("RasterizeQuad")

	print('.create two triangles')
	tris = fx.createTris( 2 )
	tris[0].x0 =  0; tris[0].y0 =  0; tris[0].z0 = 0; tris[0].w0 = 1
	tris[0].x1 = 10; tris[0].y1 =  0; tris[0].z1 = 0; tris[0].w1 = 1
	tris[0].x2 = 10; tris[0].y2 = 10; tris[0].z2 = 0; tris[0].w2 = 1

	tris[1].x0 = 20; tris[1].y0 =  0; tris[1].z0 = 0; tris[1].w0 = 1
	tris[1].x1 = 30; tris[1].y1 =  0; tris[1].z1 = 0; tris[1].w1 = 1
	tris[1].x2 = 30; tris[1].y2 = 10; tris[1].z2 = 0; tris[1].w2 = 1

	print('.render them red')
	fx.drawTris(tris, "RasterizeTri")

	print('.save output to out.tga')
	fx.saveTexture(out, "out.tga")

triDemo()
