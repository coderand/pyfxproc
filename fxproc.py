"""fxproc.py
Direct3D .fx file interface for GPU based data processing.
Created by Dmitry "AND" Andreev 2013-2015.
License Creative Commons Zero v1.0 Universal.
"""

__version__ = '0.1.7'
__all__ = ["Effect"]

import os
import sys
import atexit
import ctypes

from ctypes import WINFUNCTYPE, Structure
from ctypes.wintypes import *
from ctypes.wintypes import HRESULT

# Direct3D9 constants
D3D_SDK_VERSION = 32
D3DADAPTER_DEFAULT = 0
D3DDEVTYPE_HAL = 1
D3DDEVTYPE_REF = 2
D3DCREATE_SOFTWARE_VERTEXPROCESSING = 0x00000020
D3DCREATE_HARDWARE_VERTEXPROCESSING = 0x00000040
D3DCREATE_MIXED_VERTEXPROCESSING    = 0x00000080

D3DPT_TRIANGLELIST = 4
D3DPT_TRIANGLESTRIP = 5

D3DSWAPEFFECT = UINT
D3DSWAPEFFECT_DISCARD = 1

D3DX_DEFAULT = UINT(-1)
D3DX_DEFAULT_NONPOW2 = UINT(-2)
D3DXFX_NOT_CLONEABLE = (1 << 11)
D3DXSHADER_SKIPOPTIMIZATION = (1 << 2)

D3DPOOL = UINT
D3DPOOL_DEFAULT = 0
D3DPOOL_MANAGED = 1
D3DPOOL_SYSTEMMEM = 2

D3DUSAGE_RENDERTARGET = 0x00000001
D3DUSAGE_DEPTHSTENCIL = 0x00000002
D3DUSAGE_DYNAMIC = 0x00000200

D3DCLEAR_TARGET = 0x00000001

D3DCUBEMAP_FACE_POSITIVE_X = 0
D3DCUBEMAP_FACE_NEGATIVE_X = 1
D3DCUBEMAP_FACE_POSITIVE_Y = 2
D3DCUBEMAP_FACE_NEGATIVE_Y = 3
D3DCUBEMAP_FACE_POSITIVE_Z = 4
D3DCUBEMAP_FACE_NEGATIVE_Z = 5

D3DRESOURCETYPE = UINT
D3DRTYPE_SURFACE = 1
D3DRTYPE_VOLUME = 2
D3DRTYPE_TEXTURE = 3
D3DRTYPE_VOLUMETEXTURE = 4
D3DRTYPE_CUBETEXTURE = 5
D3DRTYPE_VERTEXBUFFER = 6
D3DRTYPE_INDEXBUFFER = 7


class D3DFORMAT :
	values = [
		("UNKNOWN", 0),
		("R8G8B8", 20),
		("A8R8G8B8", 21),
		("X8R8G8B8", 22),
		("R5G6B5", 23),
		("X1R5G5B5", 24),
		("A1R5G5B5", 25),
		("A4R4G4B4", 26),
		("R3G3B2", 27),
		("A8", 28),
		("A8R3G3B2", 29),
		("X4R4G4B4", 30),
		("A2B10G10R10", 31),
		("A8B8G8R8", 32),
		("X8B8G8R8", 33),
		("G16R16", 34),
		("A2R10G10B10", 35),
		("A16B16G16R16", 36),
		("A8P8", 40),
		("P8", 41),
		("L8", 50),
		("A8L8", 51),
		("A4L4", 52),
		("V8U8", 60),
		("L6V5U5", 61),
		("X8L8V8U8", 62),
		("Q8W8V8U8", 63),
		("V16U16", 64),
		("A2W10V10U10", 67),
		("L16", 81),
		("DXT1", 0x31545844),
		("DXT2", 0x32545844),
		("DXT3", 0x33545844),
		("DXT4", 0x34545844),
		("DXT5", 0x35545844),

		# Floating point surface formats
		# s10e5 formats (16-bits per channel)
		("R16F", 111),
		("G16R16F", 112),
		("A16B16G16R16F", 113),

		# IEEE s23e8 formats (32-bits per channel)
		("R32F", 114),
		("G32R32F", 115),
		("A32B32G32R32F", 116),
		]

	by_num = {}
	by_str = {}

	for x in values :
		by_num[x[1]] = x[0]
		by_str[x[0]] = x[1]


class D3DXIMAGE_FILEFORMAT :
	values = [
		("BMP", 0),
		("JPG", 1),
		("TGA", 2),
		("PNG", 3),
		("DDS", 4),
		("PPM", 5),
		("DIB", 6),
		("HDR", 7),
		("PFM", 8),
		]

	by_num = {}
	by_str = {}

	for x in values :
		name = x[0].lower()
		value = x[1]
		by_num[value] = name
		by_str[name] = value

D3DMULTISAMPLE_TYPE = UINT

class D3DPRESENT_PARAMETERS(Structure):
	_fields_ = [
		('BackBufferWidth', UINT),
		('BackBufferHeight', UINT),
		('BackBufferFormat', UINT), # D3DFORMAT
		('BackBufferCount', UINT),
		('MultiSampleType', D3DMULTISAMPLE_TYPE),
		('MultiSampleQuality', DWORD),
		('SwapEffect', D3DSWAPEFFECT),
		('hDeviceWindow', HWND),
		('Windowed', BOOL),
		('EnableAutoDepthStencil', BOOL),
		('AutoDepthStencilFormat', UINT), # D3DFORMAT
		('Flags', DWORD),
		('FullScreen_RefreshRateInHz', UINT),
		('PresentationInterval', UINT),
		]


class D3DXIMAGE_INFO(Structure):
	_fields_ = [
		('Width', UINT),
		('Height', UINT),
		('Depth', UINT),
		('MipLevels', UINT),
		('Format', UINT), # D3DFORMAT
		('ResourceType', D3DRESOURCETYPE),
		('ImageFileFormat', UINT), # D3DXIMAGE_FILEFORMAT
		]


class D3DSURFACE_DESC(Structure):
	_fields_ = [
		('Format', UINT), # D3DFORMAT
		('Type', D3DRESOURCETYPE),
		('Usage', DWORD),
		('Pool', D3DPOOL),
		('MultiSampleType', D3DMULTISAMPLE_TYPE),
		('MultiSampleQuality', DWORD),
		('Width', UINT),
		('Height', UINT),
		]


class D3DVOLUME_DESC(Structure):
	_fields_ = [
		('Format', UINT), # D3DFORMAT
		('Type', D3DRESOURCETYPE),
		('Usage', DWORD),
		('Pool', D3DPOOL),
		('Width', UINT),
		('Height', UINT),
		('Depth', UINT),
		]


class D3DXVECTOR4(Structure):
	_fields_ = [
		('x', FLOAT), ('y', FLOAT), ('z', FLOAT), ('w', FLOAT),
		]


class TRI_VTX(Structure):
	FVF = 0x00000104 # D3DFVF_XYZRHW | D3DFVF_TEXCOORDSIZE2( 0 ) | D3DFVF_TEX1
	_fields_ = [
		('x0', FLOAT), ('y0', FLOAT), ('z0', FLOAT), ('w0', FLOAT), ('u0', FLOAT), ('v0', FLOAT),
		('x1', FLOAT), ('y1', FLOAT), ('z1', FLOAT), ('w1', FLOAT), ('u1', FLOAT), ('v1', FLOAT),
		('x2', FLOAT), ('y2', FLOAT), ('z2', FLOAT), ('w2', FLOAT), ('u2', FLOAT), ('v2', FLOAT),
		]


class QUAD_VTX(Structure):
	FVF = 0x00000104 # D3DFVF_XYZRHW | D3DFVF_TEXCOORDSIZE2( 0 ) | D3DFVF_TEX1
	_fields_ = [
		('x0', FLOAT), ('y0', FLOAT), ('z0', FLOAT), ('w0', FLOAT), ('u0', FLOAT), ('v0', FLOAT),
		('x1', FLOAT), ('y1', FLOAT), ('z1', FLOAT), ('w1', FLOAT), ('u1', FLOAT), ('v1', FLOAT),
		('x2', FLOAT), ('y2', FLOAT), ('z2', FLOAT), ('w2', FLOAT), ('u2', FLOAT), ('v2', FLOAT),
		('x3', FLOAT), ('y3', FLOAT), ('z3', FLOAT), ('w3', FLOAT), ('u3', FLOAT), ('v3', FLOAT),
		]


# D3D9 Function Prototypes
COM_Release = WINFUNCTYPE(UINT)(2, "COM_Release")
D3D9_CreateDevice = WINFUNCTYPE(HRESULT, UINT, UINT, HWND, DWORD, LPVOID, LPVOID)(16, "D3D9_CreateDevice")
IDirect3DDevice9_CreateTexture = WINFUNCTYPE(HRESULT, UINT, UINT, UINT, DWORD, UINT, UINT, LPVOID, LPVOID)(23, "IDirect3DDevice9_CreateTexture")
IDirect3DDevice9_CreateVolumeTexture = WINFUNCTYPE(HRESULT, UINT, UINT, UINT, UINT, DWORD, UINT, UINT, LPVOID, LPVOID)(24, "IDirect3DDevice9_CreateVolumeTexture")
IDirect3DDevice9_CreateCubeTexture = WINFUNCTYPE(HRESULT, UINT, UINT, DWORD, UINT, UINT, LPVOID, LPVOID)(25, "IDirect3DDevice9_CreateCubeTexture")
IDirect3DDevice9_SetRenderTarget = WINFUNCTYPE(HRESULT, DWORD, LPVOID)(37, "IDirect3DDevice9_SetRenderTarget")
IDirect3DDevice9_BeginScene = WINFUNCTYPE(HRESULT)(41, "IDirect3DDevice9_BeginScene")
IDirect3DDevice9_EndScene = WINFUNCTYPE(HRESULT)(42, "IDirect3DDevice9_EndScene")
IDirect3DDevice9_Clear = WINFUNCTYPE(HRESULT, DWORD, LPVOID, DWORD, DWORD, FLOAT, DWORD)(43, "IDirect3DDevice9_Clear")
IDirect3DDevice9_DrawPrimitiveUP = WINFUNCTYPE(HRESULT, UINT, UINT, LPVOID, UINT)(83, "IDirect3DDevice9_DrawPrimitiveUP")
IDirect3DDevice9_SetFVF = WINFUNCTYPE(HRESULT, DWORD)(89, "IDirect3DDevice9_SetFVF")
Direct3DBaseTexture9_GetType = WINFUNCTYPE(DWORD)(10, "Direct3DBaseTexture9_GetType")
Direct3DBaseTexture9_GetLevelCount = WINFUNCTYPE(DWORD)(13, "Direct3DBaseTexture9_GetLevelCount")
IDirect3DTexture9_GetLevelDesc = WINFUNCTYPE(DWORD, UINT, LPVOID)(17, "IDirect3DTexture9_GetLevelDesc")
IDirect3DTexture9_GetSurfaceLevel = WINFUNCTYPE(DWORD, UINT, LPVOID)(18, "IDirect3DTexture9_GetSurfaceLevel")
IDirect3DCubeTexture9_GetLevelDesc = WINFUNCTYPE(DWORD, UINT, LPVOID)(17, "IDirect3DCubeTexture9_GetLevelDesc")
IDirect3DCubeTexture9_GetCubeMapSurface = WINFUNCTYPE(DWORD, UINT, UINT, LPVOID)(18, "IDirect3DCubeTexture9_GetCubeMapSurface")
IDirect3DVolumeTexture9_GetLevelDesc = WINFUNCTYPE(DWORD, UINT, LPVOID)(17, "IDirect3DVolumeTexture9_GetLevelDesc")
D3DXBUFFER_GetBufferPointer = WINFUNCTYPE(LPVOID)(3, "D3DXBUFFER_GetBufferPointer")
D3DXBUFFER_GetBufferSize = WINFUNCTYPE(DWORD)(4, "D3DXBUFFER_GetBufferSize")
ID3DXEffect_SetFloat = WINFUNCTYPE(HRESULT, LPCSTR, FLOAT)(30, "ID3DXEffect_SetFloat")
ID3DXEffect_SetVector = WINFUNCTYPE(HRESULT, LPCSTR, LPVOID)(34, "ID3DXEffect_SetVector")
ID3DXEffect_SetTexture = WINFUNCTYPE(HRESULT, LPCSTR, LPVOID)(52, "ID3DXEffect_SetTexture")
ID3DXEffect_SetTechnique = WINFUNCTYPE(HRESULT, LPCSTR)(58, "ID3DXEffect_SetTechnique")
ID3DXEffect_Begin = WINFUNCTYPE(HRESULT, LPVOID, DWORD)(63, "ID3DXEffect_Begin")
ID3DXEffect_BeginPass = WINFUNCTYPE(HRESULT, UINT)(64, "ID3DXEffect_BeginPass")
ID3DXEffect_EndPass = WINFUNCTYPE(HRESULT)(66, "ID3DXEffect_EndPass")
ID3DXEffect_End = WINFUNCTYPE(HRESULT)(67, "ID3DXEffect_End")

# Windows constants
CreateWindowEx = ctypes.windll.user32.CreateWindowExA
CreateWindowEx.argtypes = [DWORD, LPCSTR, LPCSTR, DWORD, UINT, UINT, UINT, UINT, HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowEx.restype = HWND

WS_OVERLAPPEDWINDOW = 0x00CF0000

# Load DLLs and import functions
d3d9_dll = ctypes.windll.LoadLibrary('d3d9.dll')

d3dx9_43_dll = None
d3dx9_43_warning = False

for d3dx_version in range(43, 31, -1):
	try:
		d3dx9_43_dll = ctypes.windll.LoadLibrary('d3dx9_%d.dll' % (d3dx_version))
		break
	except WindowsError:
		d3dx9_43_warning = True

if not d3dx9_43_dll :
	raise Exception("Failed to find d3dx9_*.dll")

if d3dx9_43_warning :
	print("WARNING: d3dx9_43.dll not found, falling back to lower version")

Direct3DCreate9 = getattr(d3d9_dll, 'Direct3DCreate9')

D3DXCreateEffectFromFile = getattr(d3dx9_43_dll, 'D3DXCreateEffectFromFileA')
D3DXCreateEffectFromFile.argtypes = [LPVOID, LPCSTR, LPVOID, LPVOID, DWORD, LPVOID, LPVOID, LPVOID]
D3DXCreateEffectFromFile.restype = HRESULT

D3DXCreateEffect = getattr(d3dx9_43_dll, 'D3DXCreateEffect')
D3DXCreateEffect.argtypes = [LPVOID, LPCSTR, UINT, LPVOID, LPVOID, DWORD, LPVOID, LPVOID, LPVOID]
D3DXCreateEffect.restype = HRESULT

D3DXGetImageInfoFromFile = getattr(d3dx9_43_dll, 'D3DXGetImageInfoFromFileA')
D3DXGetImageInfoFromFile.argtypes = [LPCSTR, LPVOID]
D3DXGetImageInfoFromFile.restype = HRESULT

D3DXCreateTextureFromFileEx = getattr(d3dx9_43_dll, 'D3DXCreateTextureFromFileExA')
D3DXCreateTextureFromFileEx.argtypes = [LPVOID, LPCSTR, UINT, UINT, UINT, DWORD, UINT, UINT, DWORD, DWORD, UINT, LPVOID, LPVOID, LPVOID]
D3DXCreateTextureFromFileEx.restype = HRESULT

D3DXCreateCubeTextureFromFileEx = getattr(d3dx9_43_dll, 'D3DXCreateCubeTextureFromFileExA')
D3DXCreateCubeTextureFromFileEx.argtypes = [LPVOID, LPCSTR, UINT, UINT, DWORD, UINT, UINT, DWORD, DWORD, UINT, LPVOID, LPVOID, LPVOID]
D3DXCreateCubeTextureFromFileEx.restype = HRESULT

D3DXSaveTextureToFile = getattr(d3dx9_43_dll, 'D3DXSaveTextureToFileA')
D3DXSaveTextureToFile.argtypes = [LPCSTR, UINT, LPVOID, LPVOID]
D3DXSaveTextureToFile.restype = HRESULT

# Initialize Direct3D
lpD3D9 = LPVOID(Direct3DCreate9(D3D_SDK_VERSION))

if not lpD3D9:
	raise Exception("Failed to create D3D")

hWnd = CreateWindowEx(0, "STATIC", "fxproc_window", WS_OVERLAPPEDWINDOW, 0, 0, 100, 100, 0, 0, 0, 0)

if hWnd == 0:
	raise Exception("Failed to create window")

NULL = LPVOID(0)
lpDevice = LPVOID(0)
d3dpp = D3DPRESENT_PARAMETERS(Windowed=1, SwapEffect=D3DSWAPEFFECT_DISCARD)

try:
	D3D9_CreateDevice(lpD3D9, D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, hWnd, D3DCREATE_HARDWARE_VERTEXPROCESSING, ctypes.byref(d3dpp), ctypes.byref(lpDevice))

	#:TODO: Try different configurations when one fails
	#D3D9_CreateDevice(lpD3D9, D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, hWnd, D3DCREATE_SOFTWARE_VERTEXPROCESSING, ctypes.byref(d3dpp), ctypes.byref(lpDevice))
	#D3D9_CreateDevice(lpD3D9, D3DADAPTER_DEFAULT, D3DDEVTYPE_REF, hWnd, D3DCREATE_HARDWARE_VERTEXPROCESSING, ctypes.byref(d3dpp), ctypes.byref(lpDevice))
except:
	raise Exception("Failed to create D3D device")


class Texture :

	all_textures = []

	def __init__(self, d3d_texture, name = ""):
		assert(d3d_texture)

		desc = D3DSURFACE_DESC()
		slices = 0

		ttype = Direct3DBaseTexture9_GetType(d3d_texture)

		if ttype == D3DRTYPE_TEXTURE:
			IDirect3DTexture9_GetLevelDesc(d3d_texture, 0, ctypes.byref(desc))

		elif ttype == D3DRTYPE_CUBETEXTURE:
			IDirect3DCubeTexture9_GetLevelDesc(d3d_texture, 0, ctypes.byref(desc))

		elif ttype == D3DRTYPE_VOLUMETEXTURE:
			volume_desc = D3DVOLUME_DESC()
			IDirect3DVolumeTexture9_GetLevelDesc(d3d_texture, 0, ctypes.byref(volume_desc))

			slices = volume_desc.Depth
			desc.Width = volume_desc.Width
			desc.Height = volume_desc.Height

		else:
			raise TypeError("Unknown resource type")

		format_name = D3DFORMAT.by_num[desc.Format]

		self.d3d_texture = d3d_texture
		self.format = format_name
		self.width = desc.Width
		self.height = desc.Height
		self.levels = Direct3DBaseTexture9_GetLevelCount(d3d_texture)
		self.slices = slices
		self.name = name

		Texture.all_textures.append(d3d_texture)

	def __del__(self):
		if self.d3d_texture and (self.d3d_texture in Texture.all_textures):
			COM_Release(self.d3d_texture)
			Texture.all_textures.remove(self.d3d_texture)

	def __str__(self):
		return (
			"width=" + str(self.width) +
			" height=" + str(self.height) +
			" format=" + self.format +
			" levels=" + str(self.levels) +
			" slices=" + str(self.slices) +
			" d3d_texture=" + hex(self.d3d_texture.value) +
			" name=" + '"' + self.name + '"'
			)

	@staticmethod
	def check_type_of(obj):
		assert isinstance(obj, Texture), "object %r is not a texture" % (obj)


class Effect :
	"""Essential bindings for Effect manipulation

- open                   ( file_name )
- fromstring             ( text )

- createRenderTarget     ( width, height, format_str, levels = 1 )
- createRenderTargetCube ( size,          format_str, levels = 1 )
- createVolumeTexture    ( width, height, format_str, levels = 1, slices = 1 )

- loadTexture            ( file_name )
- saveTexture            ( texture_or_render_target, file_name )

- setRenderTarget        ( render_target, level = 0, face = 0 )
- clear                  ( r_byte, g_byte, b_byte, a_byte )
- drawQuad               ( technique_name )
- createTris             ( tri_count )
- drawTris               ( tris, technique_name )
- copyLevelToVolumeSlice ( source, destination_volume, slice )

- setFloat               ( name, x )
- setFloat4              ( name, x, y, z, w )
- setTexture             ( name, texture_or_render_target )
"""

	all_effects = []
	curr_target_size = (0, 0)

	def __init__(self, d3d_effect, name = ""):
		assert(d3d_effect)

		self.d3d_effect = d3d_effect
		self.name = name
		Effect.all_effects.append(d3d_effect)

	def __del__(self):
		if self.d3d_effect and (self.d3d_effect in Effect.all_effects):
			COM_Release(self.d3d_effect)
			Effect.all_effects.remove(self.d3d_effect)

	@staticmethod
	def open(fx_name):
		errors = LPVOID(0)
		d3d_effect = LPVOID(0)

		try:
			D3DXCreateEffectFromFile(
				lpDevice, fx_name, NULL, NULL,
				D3DXFX_NOT_CLONEABLE | D3DXSHADER_SKIPOPTIMIZATION, NULL,
				ctypes.byref(d3d_effect), ctypes.byref(errors)
				)
		except WindowsError:
			Effect.__printD3DXBuffer(errors)
			raise IOError('Can\'t load effect file "%s"' % (fx_name))

		return Effect(d3d_effect, name=fx_name)

	@staticmethod
	def fromstring(text):
		errors = LPVOID(0)
		d3d_effect = LPVOID(0)

		try:
			D3DXCreateEffect(
				lpDevice, text, len(text), NULL, NULL,
				D3DXFX_NOT_CLONEABLE | D3DXSHADER_SKIPOPTIMIZATION, NULL,
				ctypes.byref(d3d_effect), ctypes.byref(errors)
				)
		except WindowsError:
			Effect.__printD3DXBuffer(errors)
			raise IOError('Can\'t create effect')

		return Effect(d3d_effect, name="<string>")

	@staticmethod
	def __printD3DXBuffer(d3dxbuffer):
		if d3dxbuffer:
			sz = D3DXBUFFER_GetBufferSize(d3dxbuffer)
			ptr = D3DXBUFFER_GetBufferPointer(d3dxbuffer)

			if sz > 0:
				text = ctypes.string_at(LPVOID(ptr), sz - 1)
				print("")
				print(text.rstrip())

	@staticmethod
	def loadTexture(file_name):
		texture = LPVOID(0)
		info = D3DXIMAGE_INFO()

		try:
			D3DXGetImageInfoFromFile(file_name, ctypes.byref(info))

			if info.ResourceType == D3DRTYPE_CUBETEXTURE:
				D3DXCreateCubeTextureFromFileEx(
					lpDevice, file_name, D3DX_DEFAULT_NONPOW2,
					0, 0, info.Format, D3DPOOL_MANAGED, D3DX_DEFAULT, D3DX_DEFAULT,
					0, NULL, NULL, ctypes.byref(texture)
					)

			elif info.ResourceType == D3DRTYPE_TEXTURE:
				D3DXCreateTextureFromFileEx(
					lpDevice, file_name, D3DX_DEFAULT_NONPOW2, D3DX_DEFAULT_NONPOW2,
					0, 0, info.Format, D3DPOOL_MANAGED, D3DX_DEFAULT, D3DX_DEFAULT,
					0, NULL, NULL, ctypes.byref(texture)
					)

			else:
				raise TypeError("Unsupported resource")

			return Texture(texture, name=file_name)

		except WindowsError:
			raise IOError("Can't load texture " '"%s"' % (file_name))

		return None

	@staticmethod
	def saveTexture(pyobj, file_name):
		Texture.check_type_of(pyobj)

		ext = os.path.splitext(file_name)[1]
		ext = ext[1:].lower()
		format = D3DXIMAGE_FILEFORMAT.by_str[ext]

		try:
			D3DXSaveTextureToFile(file_name, format, pyobj.d3d_texture, NULL)
		except:
			raise IOError("Can't save texture " '"%s"' % (file_name))

	@staticmethod
	def createRenderTarget(width, height, format_str, levels=1):
		format = D3DFORMAT.by_str[format_str]
		texture = LPVOID(0)

		try:
			IDirect3DDevice9_CreateTexture(lpDevice, width, height, levels, D3DUSAGE_RENDERTARGET, format, D3DPOOL_DEFAULT, ctypes.byref(texture), NULL)
		except:
			raise Exception("Can't create render target")

		return Texture(texture, name="<renderTarget>")

	@staticmethod
	def createRenderTargetCube(size, format_str, levels=1):
		format = D3DFORMAT.by_str[format_str]
		texture = LPVOID(0)

		try:
			IDirect3DDevice9_CreateCubeTexture(lpDevice, size, levels, D3DUSAGE_RENDERTARGET, format, D3DPOOL_DEFAULT, ctypes.byref(texture), NULL)
		except:
			raise Exception("Can't create render target cube")

		return Texture(texture, name="<renderTargetCube>")

	@staticmethod
	def createVolumeTexture(width, height, format_str, levels=1, slices=1):
		format = D3DFORMAT.by_str[format_str]
		texture = LPVOID(0)

		try:
			IDirect3DDevice9_CreateVolumeTexture(lpDevice, width, height, slices, levels, 0, format, D3DPOOL_MANAGED, ctypes.byref(texture), NULL)
		except:
			raise Exception("Can't create volume texture")

		return Texture(texture, name="<volumeTexture>")

	@staticmethod
	def copyLevelToVolumeSlice(src_pyobj, dest_pyobj, slice_index):
		Texture.check_type_of(src_pyobj)
		Texture.check_type_of(dest_pyobj)

		raise NotImplementedError("Not yet ported")

	@staticmethod
	def setRenderTarget(pyobj, level=0, face=0):
		Texture.check_type_of(pyobj)

		surface = LPVOID(0)
		ttype = Direct3DBaseTexture9_GetType(pyobj.d3d_texture)

		if ttype == D3DRTYPE_TEXTURE:
			IDirect3DTexture9_GetSurfaceLevel(pyobj.d3d_texture, level, ctypes.byref(surface))

		elif ttype == D3DRTYPE_CUBETEXTURE:
			faces = [
				D3DCUBEMAP_FACE_POSITIVE_X, D3DCUBEMAP_FACE_NEGATIVE_X,
				D3DCUBEMAP_FACE_POSITIVE_Y, D3DCUBEMAP_FACE_NEGATIVE_Y,
				D3DCUBEMAP_FACE_POSITIVE_Z, D3DCUBEMAP_FACE_NEGATIVE_Z,
				]

			dxface = faces[face]

			IDirect3DCubeTexture9_GetCubeMapSurface(pyobj.d3d_texture, dxface, level, ctypes.byref(surface))

		else:
			raise TypeError("Incorrect render target type")

		Effect.curr_target_size = (float(int(pyobj.width) >> level), float(int(pyobj.height) >> level))

		IDirect3DDevice9_SetRenderTarget(lpDevice, 0, surface)
		COM_Release(surface)

	@staticmethod
	def clear(r=0, g=0, b=0, a=0):
		ir = min(max(int(r), 0), 255)
		ig = min(max(int(g), 0), 255)
		ib = min(max(int(b), 0), 255)
		ia = min(max(int(a), 0), 255)

		argb = UINT((ia << 24) | (ir << 16) | (ig << 8) | ib)

		IDirect3DDevice9_Clear(lpDevice, 0, NULL, D3DCLEAR_TARGET, argb, 1.0, 0)

	def __beginScene(self, technique_name):
		w = Effect.curr_target_size[0]
		h = Effect.curr_target_size[1]

		IDirect3DDevice9_BeginScene(lpDevice)

		vec = D3DXVECTOR4(w, h, 1.0 / w, 1.0 / h)
		try:
			ID3DXEffect_SetVector(self.d3d_effect, "vTargetSize", ctypes.byref(vec))
		except:
			pass

		try:
			ID3DXEffect_SetTechnique(self.d3d_effect, technique_name)
		except WindowsError:
			raise ValueError('Can\'t set technique "%s"' % (technique_name))

	def drawQuad(self, technique_name):
		x = -0.5
		y = -0.5
		w = Effect.curr_target_size[0]
		h = Effect.curr_target_size[1]

		q = QUAD_VTX(
			x    , y    , 0, 1, 0, 0,
			x + w, y    , 0, 1, 1, 0,
			x    , y + h, 0, 1, 0, 1,
			x + w, y + h, 0, 1, 1, 1,
			)

		self.__beginScene(technique_name)
		IDirect3DDevice9_SetFVF(lpDevice, QUAD_VTX.FVF)

		pass_count = UINT(0)
		ID3DXEffect_Begin(self.d3d_effect, ctypes.byref(pass_count), 0)

		for p in range(pass_count.value):

			ID3DXEffect_BeginPass(self.d3d_effect, p)
			IDirect3DDevice9_DrawPrimitiveUP(lpDevice, D3DPT_TRIANGLESTRIP, 2, ctypes.byref(q), int(ctypes.sizeof(QUAD_VTX) / 4))
			ID3DXEffect_EndPass(self.d3d_effect)

		ID3DXEffect_End(self.d3d_effect)
		IDirect3DDevice9_EndScene(lpDevice)

	@staticmethod
	def createTris(tri_count):
		return (TRI_VTX * tri_count)()

	def drawTris(self, tri_list, technique_name): 
		assert isinstance(tri_list, ctypes.Array) and TRI_VTX == tri_list._type_, "object %r is not an array of TRI_VTX" % (tri_list)

		self.__beginScene(technique_name)
		IDirect3DDevice9_SetFVF(lpDevice, TRI_VTX.FVF)

		pass_count = UINT(0)
		ID3DXEffect_Begin(self.d3d_effect, ctypes.byref(pass_count), 0)

		for p in range(pass_count.value):

			ID3DXEffect_BeginPass(self.d3d_effect, p)
			IDirect3DDevice9_DrawPrimitiveUP(lpDevice,
				D3DPT_TRIANGLELIST, len(tri_list), ctypes.byref(tri_list), int(ctypes.sizeof(TRI_VTX) / 3))
			ID3DXEffect_EndPass(self.d3d_effect)

		ID3DXEffect_End(self.d3d_effect)
		IDirect3DDevice9_EndScene(lpDevice)

	def setFloat(self, name, x):
		try:
			ID3DXEffect_SetFloat(self.d3d_effect, name, x)
		except WindowsError:
			raise ValueError('Can\'t set float "%s"' % (name))

	def setFloat4(self, name, x, y=0.0, z=0.0, w=0.0):
		vec = D3DXVECTOR4(x, y, z, w)

		try:
			ID3DXEffect_SetVector(self.d3d_effect, name, ctypes.byref(vec))
		except WindowsError:
			raise ValueError('Can\'t set vector "%s"' % (name))

	def setTexture(self, name, pyobj):
		Texture.check_type_of(pyobj)

		try:
			ID3DXEffect_SetTexture(self.d3d_effect, name, pyobj.d3d_texture)
		except WindowsError:
			raise ValueError('Can\'t set texture "%s"' % (name))


def _cleanup():
	for p in Effect.all_effects:
		COM_Release(p)
	Effect.all_effects = []

	for p in Texture.all_textures:
		COM_Release(p)
	Texture.all_textures = []

	ref = 0

	if lpDevice:
		ref += COM_Release(lpDevice)

	if lpD3D9:
		ref += COM_Release(lpD3D9)

	if ref != 0:
		print("WARNING: leaking D3D resources")

atexit.register(_cleanup)
