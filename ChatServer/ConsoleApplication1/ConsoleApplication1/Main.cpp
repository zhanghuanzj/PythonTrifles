#include <iostream>
#include <string>
#include <cassert>
#include <Windows.h>
#include <windowsx.h>

#include "Direct3D.h"

using namespace std;

class GameWindow
{
public:
	GameWindow(const string name_t, const string title_t, int width = 800, int height = 600);
	~GameWindow();

	void message_dispatch();
	HWND get_hwnd() { return hwnd; }
private:
	string name;
	string title;
	const int WIDTH;
	const int HEIGHT;
	HWND hwnd;

	static LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wparam, LPARAM lParam);
};


GameWindow::GameWindow(const string name_t, const string title_t, int width, int height) :name(name_t), title(title_t), WIDTH(width), HEIGHT(height)
{
	//1.创建窗口类
	WNDCLASSEX wndClass = {};
	wndClass.cbSize = sizeof(WNDCLASSEX);
	wndClass.style = CS_HREDRAW | CS_VREDRAW;
	wndClass.lpfnWndProc = WndProc;
	wndClass.cbClsExtra = 0;
	wndClass.cbWndExtra = 0;
	wndClass.hInstance = GetModuleHandle(NULL);
	wndClass.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wndClass.hCursor = LoadCursor(NULL, IDC_ARROW);
	wndClass.hbrBackground = (HBRUSH)GetStockObject(BLACK_BRUSH);
	wndClass.lpszMenuName = NULL;
	wndClass.lpszClassName = name.c_str();

	//2.注册窗口类
	assert(RegisterClassEx(&wndClass));

	//3.创建窗口
	hwnd = CreateWindow(name.c_str(), title.c_str(), WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, WIDTH, HEIGHT, NULL, NULL, wndClass.hInstance, NULL);

	//4.调整大小，移动，显示，更新
	/*RECT window_rect = { 0,0,WIDTH,HEIGHT };
	AdjustWindowRectEx(&window_rect, GetWindowStyle(hwnd), GetMenu(hwnd) != NULL, GetWindowExStyle(hwnd));
	MoveWindow(hwnd, 300, 150, window_rect.right - window_rect.left, window_rect.bottom - window_rect.top, false);*/
	MoveWindow(hwnd, 250, 80, WIDTH, HEIGHT, true);
	ShowWindow(hwnd, SW_NORMAL);
	UpdateWindow(hwnd);

	DirectX::instance().initialDirectX(GetModuleHandle(nullptr),hwnd,WIDTH,HEIGHT);
	////5.隐藏鼠标，设为屏幕中心
	//ShowCursor(false);
	//center.x = WIDTH / 2;
	//center.y = HEIGHT / 2;
	//ClientToScreen(hwnd, &center);
	//SetCursorPos(center.x, center.y);
	////6.限定鼠标在窗口内
	//RECT rect;
	//GetClientRect(hwnd, &rect);
	//POINT left_top;
	//left_top.x = rect.left;
	//left_top.y = rect.top;
	//POINT right_bottom;
	//right_bottom.x = rect.right;
	//right_bottom.y = rect.bottom;
	//ClientToScreen(hwnd, &left_top);
	//ClientToScreen(hwnd, &right_bottom);
	//rect.left = left_top.x;
	//rect.top = left_top.y;
	//rect.right = right_bottom.x;
	//rect.bottom = right_bottom.y;
	//ClipCursor(&rect);
}

/* ==============================================================================
* TranslateMessage(&msg)对于大多数消息而言不起作用，但是有些消息，比如键盘按键按
* 下和弹起（分别对于KeyDown 和KeyUp 消息），却需要通过它解释，产生一个WM_CHAR消息。
* DispatchMessage(&msg)负责把消息分发到消息结构体中对应的窗口，交由窗口过程函数处理。
* ==============================================================================*/
void GameWindow::message_dispatch()
{
	//时间初始化
	DWORD curTime = GetTickCount();
	DWORD preTime = GetTickCount();
	//2.消息循环
	MSG msg = { 0 };
	while (msg.message != WM_QUIT)
	{
		//获取消息
		if (PeekMessage(&msg, 0, NULL, NULL, PM_REMOVE))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
		else
		{
			curTime = GetTickCount();
			if (curTime - preTime>30)
			{
				preTime = curTime;
				DirectX::instance().snowmanRender();
			}
		}
	}
}

LRESULT CALLBACK GameWindow::WndProc(HWND hwnd, UINT message, WPARAM wparam, LPARAM lParam)
{
	float units = 0.05f;
	static POINT point;

	switch (message)
	{
	case WM_PAINT:						// 若是客户区重绘消息
		ValidateRect(hwnd, NULL);		// 更新客户区的显示
		break;							//跳出该switch语句
	case WM_DESTROY:
		PostQuitMessage(0);
		break;
	case WM_KEYDOWN:
		if (wparam == VK_ESCAPE) DestroyWindow(hwnd);
		break;
	default:
		return DefWindowProc(hwnd, message, wparam, lParam);
	}
	return 0;
}

GameWindow::~GameWindow()
{
	//5.注销窗口类
	UnregisterClass(name.c_str(), GetModuleHandle(NULL));
}

int main()
{
	const int WIDTH = 800;
	const int HEIGHT = 800;
	GameWindow myWindow("Render", "3DRender", WIDTH, HEIGHT);
	myWindow.message_dispatch();
}


