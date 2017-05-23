#include "Direct3D.h"

bool DirectX::initialDirectX(HINSTANCE hInstance, HWND hwnd, int width, int height)
{
	//1.�����ӿ�
	IDirect3D9* d3d9 = Direct3DCreate9(D3D_SDK_VERSION);

	//2.��ȡӲ����Ϣ��ȷ�����㴦��ʽ
	D3DCAPS9 caps;
	int vertexProcessing;
	d3d9->GetDeviceCaps(D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, &caps);    //(��ǰ�Կ���Ӳ���豸)
	if (caps.DevCaps & D3DDEVCAPS_HWTRANSFORMANDLIGHT)
	{
		vertexProcessing = D3DCREATE_HARDWARE_VERTEXPROCESSING;
	}
	else
	{
		vertexProcessing = D3DCREATE_SOFTWARE_VERTEXPROCESSING;
	}

	//3.��дD3D����
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

	//4.�����豸
	d3d9->CreateDevice(D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, hwnd, vertexProcessing, &d3dpp, &pD3DXDevice);
	if (pD3DXDevice == nullptr)
		cout << "ERROR" << endl;
	d3d9->Release();



	//������Ļ���ߡ�Z��������С
	width_ = width;
	height_ = height;

	//Font setting
	font = nullptr;
	D3DXCreateFont(pD3DXDevice, 36, 0, 0, 1, false, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, DEFAULT_QUALITY, 0, "΢���ź�", &font);
	GetClientRect(hwnd, &formatRect);

	D3DXCreateBox(pD3DXDevice, 2, 2, 2, &box, NULL);

	// ������Ⱦ״̬
	pD3DXDevice->SetRenderState(D3DRS_LIGHTING, false);   //�رչ���
	pD3DXDevice->SetRenderState(D3DRS_CULLMODE, D3DCULL_CCW);   //������������
	pD3DXDevice->SetRenderState(D3DRS_FILLMODE, D3DFILL_WIREFRAME);  //�����߿����ģʽ


	return true;
}

void DirectX::transformSetting()
{
	D3DXMATRIX matView; //����һ������
	D3DXVECTOR3 vEye(0.0f, 0.0f, -15.0f);  //�������λ��
	D3DXVECTOR3 vAt(0.0f, 0.0f, 0.0f); //�۲���λ��
	D3DXVECTOR3 vUp(0.0f, 1.0f, 0.0f);//���ϵ�����
	D3DXMatrixLookAtLH(&matView, &vEye, &vAt, &vUp); //�����ȡ���任����
	pD3DXDevice->SetTransform(D3DTS_VIEW, &matView); //Ӧ��ȡ���任����

													 //--------------------------------------------------------------------------------------
													 //���Ĵ�任֮������ͶӰ�任���������
													 //--------------------------------------------------------------------------------------
	D3DXMATRIX matProj; //����һ������
	D3DXMatrixPerspectiveFovLH(&matProj, D3DX_PI / 4.0f, 1.0f, 1.0f, 1000.0f); //����ͶӰ�任����
	pD3DXDevice->SetTransform(D3DTS_PROJECTION, &matProj);  //����ͶӰ�任����

															//--------------------------------------------------------------------------------------
															//���Ĵ�任֮�ġ����ӿڱ任������
															//--------------------------------------------------------------------------------------
	D3DVIEWPORT9 vp; //ʵ����һ��D3DVIEWPORT9�ṹ�壬Ȼ��������������������ֵ�Ϳ�����
	vp.X = 0;		//��ʾ�ӿ�����ڴ��ڵ�X����
	vp.Y = 0;		//�ӿ���ԶԴ��ڵ�Y����
	vp.Width = width_;	//�ӿڵĿ��
	vp.Height = height_; //�ӿڵĸ߶�
	vp.MinZ = 0.0f; //�ӿ�����Ȼ����е���С���ֵ
	vp.MaxZ = 1.0f;	//�ӿ�����Ȼ����е�������ֵ
	pD3DXDevice->SetViewport(&vp); //�ӿڵ�����
}
void DirectX::snowmanRender()
{
	pD3DXDevice->Clear(0, nullptr, D3DCLEAR_TARGET | D3DCLEAR_ZBUFFER, D3DCOLOR_XRGB(0, 0, 0), 1.0f, 0);
	pD3DXDevice->BeginScene();
	
	transformSetting();
	formatRect.top = 100;
	font->DrawText(0, "������������Ϩ�����Ϸ�������롿", -1, &formatRect, DT_CENTER,D3DCOLOR_XRGB(68, 139, 256));
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