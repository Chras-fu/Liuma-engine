# 流马-低代码测试平台
## 一、项目概述

流马是一款低代码自动化测试平台，旨在采用最简单的架构统一支持API/WebUI/AppUI的自动化测试。平台采用低代码设计模式，将传统测试脚本以配置化实现，从而让代码能力稍弱的用户快速上手自动化测试。同时平台也支持通过简单的代码编写实现自定义组件，使用户可以灵活实现自己的需求。

本项目分为平台端和引擎端，采用分布式执行设计，可以将测试执行的节点(即引擎)注册在任意环境的任意一台机器上，从而突破资源及网络限制。同时，通过将引擎启动在本地PC上，方便用户快速调试测试用例，实时查看执行过程，带来传统脚本编写一致的便捷。

项目体验地址: [演示环境](http://demo.liumatest.cn)，用户名密码: demo/123456

官网地址: [流马官网](http://www.liumatest.cn)

社区地址: [流马社区](http://www.liumatest.cn/community)

如果本项目对您有帮助，请给我们一个Star，您的支持是我们前进的动力。


## 二、功能介绍

![system](https://user-images.githubusercontent.com/96771570/182859649-bf10af76-16ce-4961-bab6-a8ec36111daa.png)

1. API测试
```
(1) 支持单接口测试和链路测试。
(2) 支持接口统一管理，支持swagger导入。
(3) 支持一键生成字段校验的接口健壮性用例。
(4) 支持全局变量、关联、断言、内置函数、自定义函数。
(5) 支持前后置脚本、失败继续、超时时间、等待/条件/循环等逻辑控制器。
(6) 支持环境与用例解耦，多种方式匹配域名，让一套用例可以在多个环境上执行。
```

2. WebUI测试
```
(1) 支持关键字驱动，零代码编写用例。
(2) 支持UI元素统一管理，Excel模板批量导入。
(3) 支持自定义关键字，封装公共的操作步骤，提升用例可读性。
(4) 支持本地引擎执行，实时查看执行过程。
(5) 支持与API用例在同一用例集合顺序执行。
```

3. AppUI测试(1.1版本上线)
```
(1) 支持WebUI同等用例编写和执行能力
(2) 支持安卓和苹果系统
(3) 支持持真机管理、投屏和在线操作
(4) 支持控件元素在线获取，一键保存元素
(5) 支持实时查看执行过程
```

更多功能及详细请参考: [用户手册](https://docs.qq.com/doc/p/1e36932d41b40df896c1627a004068df9a28fc3f)


## 三、开发环境

环境依赖: Python3.6+、Chrome、ChromeDriver(参考:[驱动说明](./browser/readme.md))

IDE推荐: python使用pyCharm

1. 引擎启动
```
Step1: 安装依赖包 pip3 install -r requirements.txt

Step2: 流马测试平台->引擎管理->注册引擎 保存engine-code和engine-secret

Step3: engine-code和engine-secret填写在/config/config.ini文件中对应位置

Step4: 修改/config/config.ini文件中Platform->url为后端地址

Step5: 如linux启动，修改/config/config.ini文件中WebDriver->options为headless

Step6: 如linux/mac启动，修改/config/config.ini文件中WebDriver->path为chromedriver

Step7: 启动引擎 python3 startup.py
```

2. 验证启动

平台引擎管理查看自己的引擎，显示在线，证明启动成功。再编写一个简单的接口用例并执行，执行成功并返回报告，引擎注册完成。

## 四、容器部署

容器部署请参考: [部署手册](https://docs.qq.com/doc/p/c989fa8bf467eca1a1e0fa59b32ceab017407168)


## 五、关于我们

流马秉持着帮助中小企业的测试团队快速建立自动化体系的目标，将会不断迭代并吸取用户的建议，欢迎大家给我们提出宝贵的意见。

如需学习平台开发相关内容或在线交流，可关注个人微信公众号【流马测试】

![qr](https://user-images.githubusercontent.com/96771570/161195670-3868f409-ed49-431f-8650-185e3e179679.png)


