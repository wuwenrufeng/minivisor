# Minivisor
Minivisor是一套通用的分布式爬虫进程管理程序，实时监测进程的状态，保证在服务器上启动一定数量的爬虫进程，并在其空跑时自动停止，异常退出时自动重启。大大提升了爬虫程序的健壮性和采集效率，减少一定的服务器性能消耗。

**运行环境**

+ 操作系统：Linux（不支持windows）
+ 运行环境：python3+

**使用手册**

- 配置Redis数据库信息

  ```shell
  vim settings.py
  ```

  ```python
  #redis 配置
  REDIS_HOST = '192.168.0.4'
  REDIS_PORT = 6379
  REDIS_PWD = 'hello'
  ```

- 配置爬虫进程信息

  ```shell
  vim minivisor_conf.py
  ```

  ```python
  spider_list =[
                  {
                      "cname": "百姓网整租列表页", # 中文名称，
                      "name": "[baixingwang]_zhengzu_list_crawl",	# 进程名称
                      "num": 4, # 进程数量
                      "delay": 1, # 停止前的延时时间，防止kill掉最后一次请求
                      "rediskeys": ['baixingwang_zhengzu_list_queue'], # 消费队列名称
                      "scrapy": "scrapy crawl baixingwang_zhengzu_list_crawl -s PROXIES=proxies &" # 启动命令
                  }
  ]
  ```

  

- 后台直接运行

  ```shell
  nohup python minivisor.py >/dev/null 2>&1 &
  ```

- 后台守护运行

  为了保证监控进程的稳定运行，我们可以使用supervisor将监控程序变为一个守护进程。

  ```shell
  vim minivisor.conf
  ```

  ```vim
  # supervisor的程序名字
  [program:minivisor]
  # supervisor执行的命令
  command=python minivisor.py
  # 项目的目录
  directory=/path 
  # 开始的时候等待多少秒
  startsecs=0
  # 停止的时候等待多少秒
  stopwaitsecs=0  
  # 自动开始
  autostart=true
  # 程序挂了后自动重启
  autorestart=true
  # 输出的log文件
  stdout_logfile=/path/log/minivisor.log
  # 输出的错误文件
  stderr_logfile=/path/log/minivisor.err
  [supervisord]
  # log的级别
  loglevel=info
  ```

**注意事项**

- 不适用于集成到定时任务管理系统中，因为会打断定时任务管理系统的任务运行周期，表现是前端显示该任务运行出错了。
