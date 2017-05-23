# -*- coding: utf-8 -*-
usage = '''\
pyqq

用法： ｛Progname｝ [-h] [-q QQ]

选项：
    -h, --help
    -q QQ, --qq QQ

'''

version = '1.0'


sampleConfStr = '''{

    # QQBot 的配置文件
    # 使用 qqbot -u somebody 启动程序时，依次加载：
    #     根配置 -> 默认配置 -> 用户 somebody 的配置 -> 命令行参数配置
    # 使用 qqbot 启动程序时，依次加载：
    #     根配置 -> 默认配置 -> 命令行参数配置
    
    # 用户 somebody 的配置
    "somebody" : {
        
        # QQBot-term （HTTP-API） 服务器端口号（该服务器监听 IP 为 127.0.0.1 ）
        "termServerPort" : 8188,
        
        # 二维码 http 服务器 ip，请设置为公网 ip 或空字符串
        "httpServerIP" : "",
        
        # 二维码 http 服务器端口号
        "httpServerPort" : 8189,
        
        # 自动登录的 QQ 号
        "qq" : "3497303033",
        
        # 接收二维码图片的邮箱账号
        "mailAccount" : "3497303033@qq.com",
        
        # 该邮箱的 IMAP/SMTP 服务授权码
        "mailAuthCode" : "feregfgftrasdsew",
        
        # 是否以文本模式显示二维码
        "cmdQrcode" : False,
    
        # 显示/关闭调试信息
        "debug" : False,

        # QQBot 掉线后自动重启
        "restartOnOffline" : False,
        
        # 完成全部联系人列表获取之后才启动 QQBot 
        "startAfterFetch" : False,
        
        # 插件目录
        "pluginPath" : ".",
        
        # 启动时需加载的插件
        "plugins" : ['sample1'],
        
        # 插件的配置（由用户自定义）
        "pluginsConf" : {},
    
    },
    
    # 可以在 默认配置 中配置所有用户都通用的设置
    "默认配置" : {
        "qq" : "",
        "pluginPath" : "",
        "plugins" : [],
    },
    
    # # 注意：根配置是固定的，用户无法修改（在本文件中修改根配置不会生效）
    # "根配置" : {
    #     "termServerPort" : 8188,
    #     "httpServerIP" : "",
    #     "httpServerPort" : 8189,
    #     "qq" : "",
    #     "mailAccount" : "",
    #     "mailAuthCode" : "",
    #     "cmdQrcode" : False,
    #     "debug" : False,
    #     "restartOnOffline" : False,
    #     "startAfterFetch" : False,
    #     "pluginPath" : "",
    #     "plugins" : [],
    #     "pluginsConf" : {}
    # },

}
'''


rootConf = {
    "termServerPort" : 8188,
    "httpServerIP" : "",
    "httpServerPort" : 8189,
    "qq" : "",
    "mailAccount" : "",
    "mailAuthCode" : "",
    "cmdQrcode" : False,
    "debug" : False,
    "restartOnOffline" : False,
    "startAfterFetch" : False,
    "pluginPath" : "",
    "plugins" : [],
    "pluginsConf" : {},
}