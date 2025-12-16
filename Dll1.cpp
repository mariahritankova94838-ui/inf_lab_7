// Dll1.cpp : Определяет экспортируемые функции для DLL.
//

#include "pch.h"
#include "framework.h"
#include "Dll1.h"


// Пример экспортированной переменной
DLL1_API int nDll1=0;

// Пример экспортированной функции.
DLL1_API int fnDll1(void)
{
    return 0;
}

// Конструктор для экспортированного класса.
CDll1::CDll1()
{
    return;
}
