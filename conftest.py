import pytest
import xml.etree.ElementTree as ET
import fnmatch
import os
from datetime import datetime

def load_config(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    config = {
        "app_path": root.find("appPath").text,
        "result_path": root.find("resultPath").text,
        "project_path": root.find("projectPath").text,
        "test_cases": [tc.text for tc in root.findall("testCases/testCase")],
        "enable_wildcard": root.find("enableWildcard").text.lower() == 'true' if root.find("enableWildcard") is not None else False
    }
    return config

@pytest.fixture(scope='session')
def config():
    return load_config('test_conf.xml')

def pytest_collection_modifyitems(config, items):
    config_data = load_config('test_conf.xml')
    tests_to_run = config_data['test_cases']
    enable_wildcard = config_data['enable_wildcard']

    filtered_items = []
    for item in items:
        # 如果启用模糊匹配，则使用 fnmatch 匹配；否则使用精确匹配
        if any(fnmatch.fnmatch(item.name, pattern) for pattern in tests_to_run) if enable_wildcard else item.name in tests_to_run:
            filtered_items.append(item)

    # 更新 items 列表，仅保留匹配的测试项
    items[:] = filtered_items


def pytest_configure(config):
    # 获取报告路径，并将其传递给 pytest-html
    config_data = load_config('test_conf.xml') 
    result_path = config_data['result_path']  
 
    # 确保路径存在
    os.makedirs(result_path, exist_ok=True) 

    # 生成带有时间戳的报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(result_path, f"report_{timestamp}.html")

    # 设置 HTML 报告路径
    config.option.htmlpath = report_file  # 这里直接设置报告路径 

def pytest_sessionfinish(session, exitstatus):
    # 在测试会话结束时，可以添加其他处理逻辑
    print(f"报告已生成，存放在：{session.config.option.htmlpath}")


