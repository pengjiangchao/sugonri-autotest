import time
import subprocess
 

class AppStart:
    def init(self, app_path):
        # 存储Electron应用程序的路径
        self.app_path = app_path
        # 启动Electron应用程序，并开启远程调试端口
        self.electron_process = subprocess.Popen(
            [self.app_path, "--remote-debugging-port=9222"]
        )

    def close(self):
        # 终止Electron进程
        self.electron_process.terminate()
        self.electron_process.wait()

class ProgramActions:
    def __init__(self, page):
        self.page = page

    def click_xpath(self, xpath):
        # 如果输入的 xpath 不以 'xpath=' 开头，则自动添加 'xpath=' 前缀
        if not xpath.startswith("xpath="):
            xpath = f"xpath={xpath}"

        # 点击元素xpath
        self.page.wait_for_selector(xpath, timeout=10000)
        self.page.click(xpath)
        time.sleep(1)

    def drag_and_drop_with_element(self, source_xpath, target_xpath):
        # 拖拽元素，从 source_xpath 到 target_xpath
        try:
            source = self.page.locator(source_xpath)
            target = self.page.locator(target_xpath)

            # 检查源元素是否可见
            if not source.is_visible():
                raise Exception(f"源元素 {source_xpath} 不可见。")

            # 检查目标元素是否可见
            if not target.is_visible():
                raise Exception(f"目标元素 {target_xpath} 不可见。")

            # 执行拖拽操作
            source.drag_to(target)

        except Exception as e:
            print(f"操作失败: {e}")

    def drag_and_drop_with_coordinates(self, source_xpath, dest_x, dest_y):
        """
        拖拽元素到指定x,y坐标，xy为绝对路径
        获取源元素的位置信息
        """
        source = self.page.locator(source_xpath)
        bounding_box = source.bounding_box()

        if bounding_box:  # 计算元素的中心点坐标
            source_x = bounding_box['x'] + bounding_box['width'] / 2
            source_y = bounding_box['y'] + bounding_box['height'] / 2
            self.page.mouse.move(source_x, source_y)
            self.page.mouse.down()  # 按下鼠标左键
            self.page.mouse.move(dest_x, dest_y)  # 拖动到目标位置
            self.page.mouse.up()  # 释放鼠标左键

    def db_click(self, title: str, options: dict = None):
        """
        双击页面上的元素。
        :param title: 要查找的元素标题
        :param options: 可选参数
        """
        if options is None:
            options = {}
        self.page.get_by_title(title, exact=True).dblclick(**options)

    def save(self):
        """保存：按下 Ctrl + S"""
        self.page.keyboard.press('Control+S')
        time.sleep(0.1)

    def save_all(self):
        """全部保存：按下 Ctrl + Alt + S"""
        self.page.keyboard.press('Control+Alt+S')
        time.sleep(0.1)

    def re_start(self):
        """重启：按下 Ctrl + R"""
        self.page.keyboard.press('Control+R')
        time.sleep(3)