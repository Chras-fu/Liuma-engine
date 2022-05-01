一、项目介绍<br><br>
    流马测试平台是一款低代码的自动化测试工具平台，支持API及UI自动化测试。平台地址: http://demo.liumatest.cn <br>
    为更好的随时随地、自由切换地支持自动化测试，流马测试平台将测试执行的核心独立出来，即本项目-流马测试引擎。平台提供配置化用例编写功能，测试引擎负责执行测试，即可满足各类复杂的使用场景。<br>
<br>
二、环境依赖<br><br>
    环境依赖: Python3.6+  Chrome以及对应的Chromedriver(详见目录/browser/chrome_setting.md)<br>
<br> 
三、使用步骤<br><br>
    1. git下载项目代码到本地<br> 
    2. 安装依赖包 pip3 install -r requirements.txt<br>
    3. 流马测试平台->引擎管理->注册引擎 保存engine-code和engine-secret<br>
    4. 将这两个字段填写到/config/config.ini文件对应处<br>
    5. 启动引擎 python3 startup.py<br>
    6. 平台引擎管理查看自己的引擎 显示在线 证明启动成功<br>
<br>
关注微信公众号：流马测试 <br>
![qr](https://user-images.githubusercontent.com/96771570/161195670-3868f409-ed49-431f-8650-185e3e179679.png)

	
