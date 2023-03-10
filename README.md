# Airdoc C++代码规范

## 1. 命名规则
### 1.1 文件命名规则
- 文件名全部小写，用下划线进行连接。文件名应参考实现的功能进行描述，比如：`log_utils.cpp`、 `my_usefull_class.cpp`  
- 定义类的文件名一般是成对出现，如：`example_code.h`、 `example_code.cpp`
- 若是类中含大量内联函数，我们还可使用`-ini.h`文件单独放置内联函数，使之文件内容更加清晰，比如：`url_table.h`、 `url_table.cpp`、 `url_table-ini.h`

### 1.2 类命名规则
- 每个单词首字母大写，不含下划线，以名词形式。比如：`MyAwesomeClass`
- 结构体，枚举的定义也是如此，比如`MyExcitingEnum`、`MyTestStruct`

### 1.3 变量命名规则
- 变量名一律小写，单词用下划线相连，例如：`int player_id;`、 `std::string table_name;`
- 类成员变量，后跟下划线以区别普通变量，比如： `player_name_`、 `player_id_`
- 全局变量则以 `g_` 开头，比如 ： `g_system_time`
- 结构体成员变量和普通变量一样，比如：`string name;`、 `int num_entries;`

### 1.4 常量命名规则
- `k`后面跟大写字母开头的单词，比如：`const int k_days_in_a_week = 7;`、`const string k_company_name = "Airdoc";`

### 1.5 函数命名规则
- 常规函数每个单词首字母大写，使用命令式语气，比如：`OpenFile()`、 `CheckFileName()`
- get和set函数或短小的内联函数使用小写加下划线，比如 `set_num_errors();`
```
class Player{
public:
  void DoSomething(int par1, std::string par2) {
    // do something
  }
  void set_player_id(const int player_id) { 
    player_id_ = player_id;
  }
  int get_player_id() {
    return player_id_;
  }
private:
  int palyer_id_;
  int player_name_;
};
```
### 1.6 命名空间规则
- 命名空间全小写，并基于项目名称和目录结构，比如`airdoc_awesome_project`

### 1.7 枚举命名规则
- 枚举类名属于类型名，按类命名，比如：`MyEnum`
- 枚举值全大写加下划线，比如：`ENUM_NAME`
```C++
MyEnum {
  ENUM_VAL0 = 0,
  ENUM_VAL1 = 1,
  ENUM_VAL2
}
```

### 1.8 宏变量命名规则
- 宏全大写加下划线，比如：`define MY_PI 3.14159f`

## 2. 格式化工具
- 使用`clang-format`和`git-clang-format`统一C、C++、Objective-C代码风格
- 代码风格使用工程根目录下的`.clang-format`文件描述
- 在新增文件时，使用`clang-format`调整代码风格
```shell
clang-format -i /path/to/new_file
```
- 在修改文件时，使用`git-clang-format`调整新增部分的代码风格：
```shell
cd /path/to/app
git-clang-format
```

## 3. 代码风格
- 对于C、C++，我们整体使用Google代码风格
- 为了更好的适配项目需求，对下列项目作出调整

|项目|修改|
|---|---|
|AccessModifierOffset 访问权限修正偏移|	由-1改为-4|
|AlignConsecutiveAssignments 连续赋值对齐|	由false改为true|
|ColumnLimit 列宽限制	|由80改为120|
|IndentWidth 缩进宽度	|由2改为4|
|ObjCBlockIndentWidth ObjC Block缩进宽度	|由2改为4|
|ObjCSpaceAfterProperty ObjC属性后保留空格	|由false改为true|
|SpacesBeforeTrailingComments 行尾注释前空格数	|由2改为1|
- 参照公司提供的`.clang-format`配置文件
```
BasedOnStyle: Google
AccessModifierOffset: -4
AlignConsecutiveAssignments: true
ColumnLimit: 120 
IndentWidth: 4
ObjCBlockIndentWidth: 4
ObjCSpaceAfterProperty: true
SpacesBeforeTrailingComments: 1
```

## 4. 代码注释与文件编码
### 4.1 源文件头部注释
- 列出：版权、作者、编写日期和描述
- 每行不要超过120个字符的宽度
```
/*********************************************************************
 * Copyright (c) 2021-2022 Airdoc Co.,Ltd.. All rights reserved.
 * Author: test_user
 * Date: 2021-01-01
 * Description: 这是一个源文件头部注释的例子
 *********************************************************************/
```

### 4.2 函数头部注释
```
/**
 * @brief 对输入的信息进行处理
 * @param info, 信息内容
 * @return 事情的处理结果编号
 */
int DoSomething(std::string info);
```

### 4.3 对代码的注释其他说明
- 可以使用中文注释（鼓励使用英文注释，前提是清晰明了）
- 程序不易理解或易理解错的地方应该添加注释
- 注释应该简练、易懂而又含义准确，避免歧义
- 注释统一放在代码上方，避免在一行代码或表达式中间使用注释

### 4.4 文件编码
- 代码文件编码要求为`UTF-8`
- 换行符为`LF`

## 5. 其他约定
### 5.1 可见性
- 所有需要对外暴露的函数、类，都需要使用AIRDOC_PUBLIC标记。
```C++
#if defined(_MSC_VER) || defined(_WIN32) || defined(_WIN64)
#ifdef AIRDOC_EXPORTS
#define AIRDOC_PUBLIC __declspec(dllexport)
#else
#define AIRDOC_PUBLIC __declspec(dllimport)
#endif // AIRDOC_EXPORTS
#else  // defined (windows)
#define AIRDOC_PUBLIC
#endif

#include <iostream>

namespace airdoc_vision {
// 对外暴露DoSomething类的所有Public接口
class AIRDOC_PUBLIC DoSomething {
public:
    /**
     * @brief 创建DoSomething的一个对象，并返回对象的指针
     * @param id, 事情的ID
     * @return 对象的指针
     */
    static DoSomething *Create(int id);

    /**
     * @brief 销毁DoSomething对象
     * @param ptr, 待销毁的DoSomething对象指针
     */
    static void Destroy(DoSomething *ptr);
}

struct AirdocVersion {
    uint8_t major;
    uint8_t minor;
    uint8_t revision;
    char    tag[8];
};

// 对外暴露GetVersion接口
AIRDOC_PUBLIC AirdocVersion GetVersion();
```

### 5.2 临近释放原则
- 为降低内存泄露风险，申请临时内存和释放内存宜在相邻代码块内实现
- 推荐使用智能指针或AutoStorage类

### 5.3 防御式编程
- 对于外部入参，应明确判定入参有效性，如：
```C++
AIRDOC_PUBLIC struct AirdocNet* AirdocCreateNet(const char* path) {
    if (NULL == path) {
        AIRDOC_PRINT("input path is NULL, failed to create net!\n");
        return NULL;
    }
    // ...
}
```

- 对于内部入参，宜使用AIRDOC_ASSERT避免问题代码的产生，如：
```C++
void CopyFloats(const float* input, float* output, int size) {
    AIRDOC_ASSERT(NULL != input);
    AIRDOC_ASSERT(NULL != output);
    for (int i = 0; i < size; ++i) {
        output[i] = input[i];
    }
}
```

- 禁止在没有注释适当理由的情况下，忽略错误入参，如：
```C++
void SetUnitDimensions(const int* dims, int size) {
    if (NULL == dims) return; // should not directly return without comments
    for (int i = 0; i < size; ++i) {
        dims[i] = 1;
    }
}
```

### 5.4 头文件保护
- 采用预处理的方式对头文件进行保护
- 对于头文件example_code.h的头文件，保护方式为
```C++
#ifndef EXAMPLE_CODE_H_
#define EXAMPLE_CODE_H_
// ...
#endif // EXAMPLE_CODE_H_
```

### 5.5 其他
- 未尽项目，参照《Google编码规范》，大家讨论决定