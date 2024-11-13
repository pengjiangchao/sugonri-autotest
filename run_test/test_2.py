from playwright.sync_api import sync_playwright, expect
from pynput.keyboard import Controller
import lib.actions as actions
import time

def test_2_1(config):
    app_path = config['app_path']
    project_path = config['project_path']
    test_result_path = config['result_path']
    
    # 将类进行实例化
    app = actions.AppStart()
    keyboard = Controller()
    app.init(app_path)

    with sync_playwright() as case1:
        browser = case1.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        p = actions.ProgramActions(page)
        time.sleep(8)
        project_path = config["project_path"]

        # 最大化窗口(click)
        # page.locator("#maximize-button").click()
        # time.sleep(5)

        # 点击工程
        page.get_by_text("工程", exact=True).click()
        # 点击新建工程
        page.get_by_text("新建 SugonRI 工程").click()
        # 输入工程名称 'test_scy'
        page.locator('//*[@id="theia-dialog-shell"]/div/div[2]/div/fieldset/div[1]/input').fill('test_2')
        time.sleep(2)
        # 输入工程路径
        page.locator('//*[@id="theia-dialog-shell"]/div/div[2]/div/fieldset/div[2]/input').fill(project_path)
        time.sleep(2)
        # 确定
        page.get_by_role("button", name="确定").click()
        time.sleep(8)

        # # 定义数据类型
        # page.get_by_text("数据类型", exact=True).click()
        # page.get_by_role("code").locator("div").filter(has_text="// 在此处定义数据类型").nth(4).click()
        # page.keyboard.press('Enter')
        # page.keyboard.type('int a;')
        # p.save()

        # 在全局变量中输入代码
        page.get_by_text("全局变量", exact=True).click()
        page.locator("#theia-main-content-panel").get_by_role("code").locator("div").filter(
            has_text="// 在此处定义全局变量").nth(4).click()
        page.keyboard.press('Enter')
        page.keyboard.type('int a=1;')
        p.save()
        time.sleep(5)


        # 新建功能块
        page.get_by_text("功能块", exact=True).click(button="right")
        page.get_by_text("新增功能块").click()
        page.locator('//*[@id="name"]').fill('fb1')
        page.keyboard.press('Enter')
        time.sleep(5)

        # 定义功能块变量
        page.get_by_text("变量定义").click()
        page.locator("[id=\"sugonri\\:variableDefine\"]").get_by_role("code").locator("div").filter(
            has_text="#pragma VAR_INPUT").nth(4).click()
        page.keyboard.press('Enter')
        page.keyboard.type('int in1;')
        p.save()
        time.sleep(2)

        # 双击功能块，编辑函数
        p.db_click('fb1')
        page.locator("#theia-main-content-panel").get_by_role("code").locator("div").filter(
            has_text="// TODO: 在此处添加实现代码").nth(4).click()
        page.keyboard.press('Enter')
        page.keyboard.type('a++;')
        p.save()
        time.sleep(2)

        # 新建程序块
        page.get_by_text("程序段", exact=True).click(button="right")
        page.get_by_text("新增程序").click()
        page.locator('//*[@id="dialog-name"]').fill('pr1')
        page.keyboard.press('Enter')
        time.sleep(2)

        # 向画布中拖拽添加功能块
        p.drag_and_drop_with_coordinates('//*[@id="cfc-func-block-tree"]/div[1]/div/div/div/div/div[5]/div[4]',
                                        800, 300)

        # 添加输入块
        page.mouse.move(400, 300)
        page.mouse.click(400, 300, button='right')
        page.get_by_text('插入输入块').click()

        # 输入块绑定变量
        page.mouse.click(400, 300, button='left', click_count=2)
        page.get_by_label('选择需要绑定的变量:').select_option('a')
        page.keyboard.press('Enter')
        p.save()
        time.sleep(2)

        # 功能块与输入块进行连线
        source = page.locator('path').nth(2)
        target = page.locator("path").nth(1)
        source.drag_to(target)
        p.save()

        # 编译
        page.get_by_text("编译").click()
        page.get_by_text("编译").nth(1).click()
        time.sleep(20)

        # 判断编译结果
        result_element = page.query_selector(
            'xpath=//*[@id="outputView"]/div/div[3]/div/div[1]/div[2]/div[1]/div[4]/div[16]/span/span')
        if result_element:
            result_text = result_element.inner_text().strip()
            print("找到编译结果，内容为：", result_text)
            if "完毕" in result_text:
                test_result = "编译测试通过"
            else:
                test_result = "编译测试失败"
        else:

            test_result = "编译测试失败 (未找到结果元素)"

        print("测试结果:", test_result)

        # 关闭IDE,断开连接
        # app.close()

        # page.pause()