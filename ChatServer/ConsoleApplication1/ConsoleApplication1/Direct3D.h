#ifndef DIRECT3D_H_
#define DIRECT3D_H_

#include <d3d9.h>
#include <d3dx9.h>
#include <windows.h>
#include <iostream>


using namespace std;

class DirectX
{
public:
	//单例获取
	static DirectX& instance()
	{
		static DirectX* pDirectX = new DirectX();
		return *pDirectX;
	}
	//初始化DirectX
	bool initialDirectX(HINSTANCE hInstance, HWND hWnd, int width, int height);
	void transformSetting();
	void snowmanRender();
	//析构
	~DirectX();

private:
	DirectX() :pD3DXDevice(nullptr){}

	IDirect3DDevice9* pD3DXDevice;

	float *z_buffer_;
	int width_;
	int height_;
	int buffer_size_;
	LPD3DXFONT font;
	RECT formatRect;
	LPD3DXMESH box;
};


#endif