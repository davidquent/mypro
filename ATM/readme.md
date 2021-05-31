
### 2、分层设计的优势
    - 思路清晰
    - 不会推翻重写
    - 扩展性强
    - 便于维护

### 3、三层架构
#### 一 用户视图层
    - 用于与用户交互
        - 接受用户的输入
        - 打印接口返回的数据给用户

#### 二 逻辑接口层
    - 核心业务逻辑
        - 接受 <用户视图层> 传递过来的参数
        - 根据逻辑判断调用 <数据处理层> 加以处理
        - 返回一个结果给 <用户视图层>

#### 三 数据处理层
    - 接受 <逻辑接口层> 传递过来的参数，做数据的
        - 保存数据 save()
        - 查看数据 select()
        - 感谢数据
        - 删除数据

### 搭建项目
    - ATM 项目根目录
        -readme.md 项目说明书

        - start.py 项目启动代码

        - conf 配置文件
            - settings.py
        
        -lib 公共方法文件
            - common.py

        -core (用户视图层) 存放用户视图层文件
            - src.py

        - interface(逻辑接口层) 核心业务逻辑文件
            - user_interface.py 用户相关的接口
            - bank_interface.py 银行相关的接口
            - shop_interface.py 购物相关的接口
        
        - db(数据处理层) 数据与数据处理的代码
            -db_handler.py 数据处理层代码
            -user_data 用户数据
        
        - log 日志文件




# 统计代码
plugins-statistic