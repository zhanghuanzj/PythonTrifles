#include "Direct3D.h"

bool DirectX::initialDirectX(HINSTANCE hInstance, HWND hwnd, int width, int height)
{
	//1.创建接口
	IDirect3D9* d3d9 = Direct3DCreate9(D3D_SDK_VERSION);

	//2.获取硬件信息，确定顶点处理方式
	D3DCAPS9 caps;
	int vertexProcessing;
	d3d9->GetDeviceCaps(D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, &caps);    //(当前显卡，硬件设备)
	if (caps.DevCaps & D3DDEVCAPS_HWTRANSFORMANDLIGHT)
	{
		vertexProcessing = D3DCREATE_HARDWARE_VERTEXPROCESSING;
	}
	else
	{
		vertexProcessing = D3DCREATE_SOFTWARE_VERTEXPROCESSING;
	}

	//3.填写D3D参数
	D3DPRESENT_PARAMETERS d3dpp;
	d3dpp.BackBufferWidth = width;
	d3dpp.BackBufferHeight = height;
	d3dpp.BackBufferFormat = D3DFMT_A8R8G8B8;
	d3dpp.BackBufferCount = 1;
	d3dpp.MultiSampleType = D3DMULTISAMPLE_NONE;
	d3dpp.MultiSampleQuality = 0;
	d3dpp.SwapEffect = D3DSWAPEFFECT_DISCARD;
	d3dpp.hDeviceWindow = hwnd;
	d3dpp.Windowed = true;
	d3dpp.EnableAutoDepthStencil = true;
	d3dpp.AutoDepthStencilFormat = D3DFMT_D24S8;
	d3dpp.Flags = 0;
	d3dpp.FullScreen_RefreshRateInHz = D3DPRESENT_RATE_DEFAULT;
	d3dpp.PresentationInterval = D3DPRESENT_INTERVAL_IMMEDIATE;

	//4.创建设备
	d3d9->CreateDevice(D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, hwnd, vertexProcessing, &d3dpp, &pD3DXDevice);
	if (pD3DXDevice == nullptr)
		cout << "ERROR" << endl;
	d3d9->Release();



	//保存屏幕宽、高、Z缓冲区大小
	width_ = width;
	height_ = height;

	//Font setting
	font = nullptr;
	D3DXCreateFont(pD3DXDevice, 36, 0, 0, 1, false, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, DEFAULT_QUALITY, 0, "微软雅黑", &font);
	GetClientRect(hwnd, &formatRect);

	D3DXCreateBox(pD3DXDevice, 2, 2, 2, &box, NULL);

	// 设置渲染状态
	pD3DXDevice->SetRenderState(D3DRS_LIGHTING, false);   //关闭光照
	pD3DXDevice->SetRenderState(D3DRS_CULLMODE, D3DCULL_CCW);   //开启背面消隐
	pD3DXDevice->SetRenderState(D3DRS_FILLMODE, D3DFILL_WIREFRAME);  //设置线框填充模式


	return true;
}

void DirectX::transformSetting()
{
	D3DXMATRIX matView; //定义一个矩阵
	D3DXVECTOR3 vEye(0.0f, 0.0f, -15.0f);  //摄像机的位置
	D3DXVECTOR3 vAt(0.0f, 0.0f, 0.0f); //观察点的位置
	D3DXVECTOR3 vUp(0.0f, 1.0f, 0.0f);//向上的向量
	D3DXMatrixLookAtLH(&matView, &vEye, &vAt, &vUp); //计算出取景变换矩阵
	pD3DXDevice->SetTransform(D3DTS_VIEW, &matView); //应用取景变换矩阵

													 //--------------------------------------------------------------------------------------
													 //【四大变换之三】：投影变换矩阵的设置
													 //--------------------------------------------------------------------------------------
	D3DXMATRIX matProj; //定义一个矩阵
	D3DXMatrixPerspectiveFovLH(&matProj, D3DX_PI / 4.0f, 1.0f, 1.0f, 1000.0f); //计算投影变换矩阵
	pD3DXDevice->SetTransform(D3DTS_PROJECTION, &matProj);  //设置投影变换矩阵

															//--------------------------------------------------------------------------------------
															//【四大变换之四】：视口变换的设置
															//--------------------------------------------------------------------------------------
	D3DVIEWPORT9 vp; //实例化一个D3DVIEWPORT9结构体，然后做填空题给各个参数赋值就可以了
	vp.X = 0;		//表示视口相对于窗口的X坐标
	vp.Y = 0;		//视口相对对窗口的Y坐标
	vp.Width = width_;	//视口的宽度
	vp.Height = height_; //视口的高度
	vp.MinZ = 0.0f; //视口在深度缓存中的最小深度值
	vp.MaxZ = 1.0f;	//视口在深度缓存中的最大深度值
	pD3DXDevice->SetViewport(&vp); //视口的设置
}
void DirectX::snowmanRender()
{
	pD3DXDevice->Clear(0, nullptr, D3DCLEAR_TARGET | D3DCLEAR_ZBUFFER, D3DCOLOR_XRGB(0, 0, 0), 1.0f, 0);
	pD3DXDevice->BeginScene();
	
	transformSetting();
	formatRect.top = 100;
	font->DrawText(0, "【致我们永不熄灭的游戏开发梦想】", -1, &formatRect, DT_CENTER,D3DCOLOR_XRGB(68, 139, 256));
	//D3DXMATRIX d;
	//D3DXMatrixTranslation(&d, 3.0f, -3.0f, 0.0f);
	//pD3DXDevice->SetTransform(D3DTS_WORLD, &d);
	pD3DXDevice->SetRenderState(D3DRS_FILLMODE, D3DFILL_WIREFRAME);
	box->DrawSubset(0);

	pD3DXDevice->EndScene();
	pD3DXDevice->Present(nullptr, nullptr, nullptr, nullptr);
}
DirectX::~DirectX()
{
	if (pD3DXDevice != NULL)
	{
		pD3DXDevice->Release();
	}
}