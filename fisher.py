# -*- coding:utf-8 -*-
from app import create_app

# app
#     蓝图
#         视图函数
#         静态文件
#         模板
#     蓝图
#         视图函数
#         静态文件
#         模板

# flask路由
# URL --> endpoint（反向构建URL） -->视图函数


# 封装：以线程ID号作为key字典 -> Local -> LocalStack -> 线程隔离
# 上下文管理：AppContext RequestContext -> LocalStack  -> with as:
# 封装：Flask(app) -> AppContext   Request -> RequestContext
# 全局变量：current_app -> LocalStack AppContext(_app_ctx_stack.top)
# 全局变量：request -> LocalStack RequestContext(_request_ctx_stack.top)


# M:models（业务逻辑） V:templates C:视图函数


# Email邮件系统未测试（重置密码系统）

app = create_app()


# 生产环境：nginx + uwsgi
if __name__ == '__main__':
    # app.run加载flask自带的服务器
    # debug模式：代码改动时自动重启
    # processes 多进程 + threaded 多线程
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=5000, threaded=True)

