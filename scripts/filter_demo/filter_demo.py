from fxproc import Effect

def filterDemo():

	print('.load effect file')
	fx = Effect.open("filter_demo.fx")

	print('.load Lena')
	lena = fx.loadTexture("lena.jpg")

	print('.create render target')
	out = fx.createRenderTarget(lena.width, lena.height, "A8R8G8B8")
	out2 = fx.createRenderTarget(lena.width, lena.height, "A8R8G8B8")

	print('.assign texture')
	fx.setTexture("baseMapTexture", lena)

	print('.set render target')
	fx.setRenderTarget(out)

	print('.lowpass filter')
	fx.drawQuad("LowPass")

	print('.save output lena_lowpass.tga')
	fx.saveTexture(out, "lena_lowpass.tga")

	print('.highpass filter')
	fx.setRenderTarget(out2)
	fx.setTexture("baseMap2Texture", out)
	fx.drawQuad("HighPass")

	print('.save output lena_highpass.tga')
	fx.saveTexture(out2, "lena_highpass.tga")

filterDemo()
