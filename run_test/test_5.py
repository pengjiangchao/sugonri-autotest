# IDE_变量普通写入_全局变量_基础变量
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from pynput.keyboard import Controller, Key
import pytest
from lib.actions import *
from playwright.sync_api import sync_playwright

keyboard = Controller()

@pytest.fixture(scope="session")
def connect_IDE(config):
    app_path = config['app_path']
    test_result_path = config['result_path']

    # 将类进行实例化
    app = AppStart()
    keyboard = Controller() 
    app.init(app_path)
    with sync_playwright() as case1:
            
            browser = case1.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            p = ProgramActions(page)
            time.sleep(5) 
            # 断言连接是否成功
            assert page is not None, '无法正常打开IDE'
            yield page, p, app # 将 page 和 ProgramActions 实例返回给测试函数

def test_case5_ProjectNew(connect_IDE, config):
    page, p ,app = connect_IDE
    project_path = config['project_path']  
    # 点击工程
    page.get_by_text("工程", exact=True).click()

    # 点击新建工程
    page.get_by_text("新建 SugonRI 工程").click()

    # 选择库工程
    page.get_by_label("库工程").check()

    # 输入工程名称
    page.locator('//*[@id="theia-dialog-shell"]/div/div[2]/div/fieldset/div[1]/input').fill('test_5')

    # 输入工程路径
    page.locator('//*[@id="theia-dialog-shell"]/div/div[2]/div/fieldset/div[2]/input').fill(project_path)

    # 确定
    page.get_by_role("button", name="确定").click()
    time.sleep(5)

def test_case5_FbNew(connect_IDE):
    page, p,app = connect_IDE
    # 新建功能块
    page.get_by_text("功能块", exact=True).click(button="right")
    page.get_by_text("新增功能块").click()
    page.locator('//*[@id="name"]').fill('fb1')
    page.keyboard.press('Enter')


def test_case5_FbCode(connect_IDE):
    page, p, app = connect_IDE
    # 双击功能块，编辑函数
    p.db_click('fb1')
    page.locator("#theia-main-content-panel").get_by_role("code").locator("div").filter(
        has_text="// TODO: 在此处添加实现代码").nth(4).click()
    page.keyboard.press('Enter')
    page.keyboard.type('if (in0) {')
    page.keyboard.press('Enter')
    page.keyboard.type('out0 += 1;')
    page.keyboard.press('Enter')
    page.keyboard.type('}')
    page.keyboard.press('Enter')
    page.keyboard.type('if (in1) {')
    page.keyboard.press('Enter')
    page.keyboard.type('out1 += 1;')
    page.keyboard.press('Enter')
    page.keyboard.type('}')
    time.sleep(5)
    p.save()


def test_case5_VarInput(connect_IDE):
    page, p, app = connect_IDE
    # 在输入变量中输入以下代码并保存：
    page.wait_for_selector('//*[@id="shell-tab-sugonri:variableDefine"]/div[1]/div[2]', state="visible")
    page.get_by_text("变量定义").click()
    page.locator("[id=\"sugonri\\:variableDefine\"]").get_by_role("code").locator("div").filter(
        has_text="#pragma VAR_INPUT").nth(4).click()
    page.keyboard.press('Enter')
    page.keyboard.type('bool in0 = 0, in1 = 0;')
    p.save()


def test_case5_OutInput(connect_IDE):
    page, p, app = connect_IDE
    # 在输出变量中输入以下代码并保存：
    page.wait_for_selector('//*[@id="shell-tab-sugonri:variableDefine"]/div[1]/div[2]', state="visible")
    page.get_by_text("变量定义").click()
    page.locator("[id=\"sugonri\\:variableDefine\"]").get_by_role("code").locator("div").filter(
        has_text="#pragma VAR_OUTPUT").nth(4).click()
    page.keyboard.press('Enter')
    page.keyboard.type('int out0 = 0,out1 = 0;')
    time.sleep(5)
    p.save()


def test_case5_Compile(connect_IDE):
    page, p ,app = connect_IDE
    # 编译工程
    page.get_by_text("编译").click()
    page.get_by_text("编译").nth(1).click()
    time.sleep(25)

    # 检查编译结果
    result_element = page.query_selector(
        '//*[@id="outputView"]/div/div[3]/div/div[1]/div[2]/div[1]/div[4]')
    assert result_element, "未找到编译结果元素"
    result_text = result_element.inner_text().strip()
    assert "退出代码为 0" in result_text, "编译测试失败"

def test_case5_ExportLibrary(connect_IDE):
    page, p, app = connect_IDE
    # 导出功能块库
    page.locator("#sugonri-project-tree-widget").click(button="right")
    page.get_by_text("导出功能块库").click()
    time.sleep(2)

    # page.keyboard.press('Enter')

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    

