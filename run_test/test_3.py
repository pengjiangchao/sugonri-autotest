# IDE_变量普通写入_全局变量_基础变量
from playwright.sync_api import sync_playwright
from lib.actions import *
import lib.actions as actions
import time
import pytest


@pytest.fixture(scope="session")
def connect_IDE(config):
    app_path = config['app_path']
    app = actions.AppStart()
    app.init(app_path)
    with sync_playwright() as case1:
            browser = case1.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            p = ProgramActions(page)
            time.sleep(5)
            # 断言连接是否成功
            assert page is not None, '无法正常打开IDE'
            yield page, p  # 将 page 和 ProgramActions 实例返回给测试函数  

def test_3_2(connect_IDE,config):
    project_path = config['project_path']
    page, p = connect_IDE
    # 点击工程
    page.get_by_text("工程", exact=True).click()
    # 点击新建工程
    page.get_by_text("新建 SugonRI 工程").click() 
    # 输入工程名称
    page.locator('//*[@id="theia-dialog-shell"]/div/div[2]/div/fieldset/div[1]/input').fill('test_3')
    time.sleep(3)
    # 输入工程路径
    page.locator('//*[@id="theia-dialog-shell"]/div/div[2]/div/fieldset/div[2]/input').fill(project_path)
    time.sleep(3)
    # 确定
    page.get_by_role("button", name="确定").click() 
    time.sleep(10)

def test_3_3(connect_IDE):
    page, p = connect_IDE
    # 在全局变量中输入代码
    page.get_by_text("全局变量", exact=True).click()
    page.locator("#theia-main-content-panel").get_by_role("code").locator("div").filter(
        has_text="// 在此处定义全局变量").nth(4).click()
    page.keyboard.press('Enter')
    page.keyboard.type('#include<string>')
    page.keyboard.press('Enter')
    page.keyboard.type('bool glb_bool;')
    page.keyboard.press('Enter')
    page.keyboard.type('char glb_char;')
    page.keyboard.press('Enter')
    page.keyboard.type('short glb_short;')
    page.keyboard.press('Enter')
    page.keyboard.type('float glb_float;')
    page.keyboard.press('Enter')
    page.keyboard.type('double glb_double;')
    page.keyboard.press('Enter')
    page.keyboard.type('uint8_t glb_uint8;')
    page.keyboard.press('Enter')
    page.keyboard.type('int8_t glb_int8;')
    page.keyboard.press('Enter')
    page.keyboard.type('uint16_t glb_uint16;')
    page.keyboard.press('Enter')
    page.keyboard.type('int16_t glb_int16;')
    page.keyboard.press('Enter')
    page.keyboard.type('uint32_t glb_uint32;')
    page.keyboard.press('Enter')
    page.keyboard.type('int glb_int32;')
    page.keyboard.press('Enter')
    page.keyboard.type('uint64_t glb_uint64;')
    page.keyboard.press('Enter')
    page.keyboard.type('int64_t glb_int64;')
    page.keyboard.press('Enter')
    page.keyboard.type('std::string glb_string;')
    page.keyboard.press('Enter')
    page.keyboard.type('unsigned long long glb_ullong;')
    page.keyboard.press('Enter')
    page.keyboard.type('long double glb_ldouble;')
    page.keyboard.press('Enter')
    page.keyboard.type('long glb_long;')
    page.keyboard.press('Enter')
    page.keyboard.type('long long glb_llong;')
    p.save()


def test_3_4(connect_IDE):
    page, p = connect_IDE 
    # 新建功能块
    page.get_by_text("功能块", exact=True).click(button="right")
    page.get_by_text("新增功能块").click()
    page.locator('//*[@id="name"]').fill('fb1')
    page.keyboard.press('Enter')
    page.close()

# def test_3_5(connect_IDE):
#     page, p = connect_IDE
#     # 在普通变量中输入以下代码并保存：
#     page.get_by_text("变量定义").click()
#     page.locator("[id=\"sugonri\\:variableDefine\"]").get_by_role("code").locator("div").filter(
#         has_text="#pragma VAR_INPUT").nth(4).click()
#     page.keyboard.press('Enter')
#     page.keyboard.type('#include <string>')
#     page.keyboard.press('Enter')
#     page.keyboard.type('bool var_bool;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('char var_char;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('short var_short;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('float var_float;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('double var_double;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('uint8_t var_uint8;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('int8_t var_int8;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('uint16_t var_uint16;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('int16_t var_int16;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('uint32_t var_uint32;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('int var_int32;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('uint64_t var_uint64;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('int64_t var_int64;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('std::string var_string;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('unsigned long long var_ullong;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('long double var_ldouble;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('long var_long;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('long long var_llong;')
#     p.save()

# def test_3_6(connect_IDE):
#     page, p = connect_IDE
#     # 双击功能块，编辑函数
#     p.db_click('fb1')
#     page.locator("#theia-main-content-panel").get_by_role("code").locator("div").filter(
#         has_text="#include \"fb1.hpp\"").nth(4).click()
#     page.keyboard.press('Enter')
#     page.keyboard.type('#include <stdio.h>')
#     page.locator("#theia-main-content-panel").get_by_role("code").locator("div").filter(
#         has_text="// TODO: 在此处添加实现代码").nth(4).click()
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_bool = glb_bool;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_char = glb_char;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_short = glb_short;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_float = glb_float;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_double = glb_double;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_uint8 = glb_uint8;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_int8 = glb_int8;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_uint16 = glb_uint16;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_int16 = glb_int16;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_uint32 = glb_uint32;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_int32 = glb_int32;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_uint64 = glb_uint64;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_int64 = glb_int64;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_string = glb_string;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_ullong = glb_ullong;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_ldouble = glb_ldouble;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_long = glb_long;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('var_llong = glb_llong;')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_bool = %d", var_bool);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_char = %c", var_char);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_short = %d", var_bool);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_float = %f", var_float);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_double = %lf", var_double);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_uint8 = %d", var_uint8);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_int8 = %d", var_int8);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_uint16 = %d", var_uint16);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_int16 = %d", var_int16);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_uint32 = %d", var_uint32);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_int32 = %d", var_int32);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_uint64 = %ld", var_uint64);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_int64 = %ld", var_int64);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_string = %s", var_string.c_str());')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_ullong = %lld", var_ullong);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_ldouble = %lf", var_ldouble);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_long = %ld", var_long);')
#     page.keyboard.press('Enter')
#     page.keyboard.type('printf ("var_llong = %lld", var_llong);')
#     p.save()

# def test_3_7(connect_IDE):
#     page, p = connect_IDE
#     # 新建程序块
#     page.get_by_text("程序段", exact=True).click(button="right")
#     page.get_by_text("新增程序").click()
#     page.locator('//*[@id="dialog-name"]').fill('pr1')
#     page.keyboard.press('Enter')
#     time.sleep(5)

# def test_3_8(connect_IDE):
#     page, p = connect_IDE
#     # 向画布中拖拽添加功能块
#     p.drag_and_drop_with_coordinates('//*[@id="cfc-func-block-tree"]/div[1]/div/div/div/div/div[5]/div[4]',
#                                      700, 200)
#     # 添加n个输入块
#     n = 18  # 输入块的数量
#     y_position = 200  # 起始y坐标

#     for i in range(n):
#         # 添加输入块
#         page.mouse.move(400, y_position + i * 25)  # 根据循环索引调整y坐标
#         page.mouse.click(400, y_position + i * 25, button='left')
#         page.mouse.click(400, y_position + i * 25, button='right')
#         page.get_by_text('插入输入块').click()

#         # 输入块绑定变量
#         page.mouse.click(400, y_position + i * 25, button='left', click_count=2)
#         page.get_by_label('选择需要绑定的变量:').click()

#         # 根据循环索引选择不同的变量（例如：第i个变量）
#         for j in range(i + 1):
#             page.keyboard.press('ArrowDown')

#         page.keyboard.press('Enter')
#         page.keyboard.press('Enter')

#     p.save()
#     time.sleep(5)
#     page.pause()
