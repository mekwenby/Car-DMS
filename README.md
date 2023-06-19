# Car-DMS
可用于各种汽车修理厂的DMS系统



##### 开发语言: Python

##### 使用框架: Flask + Peewee + Bootstrap4

##### 数据库: MariaDB

##### 实现功能:

用户档案管理

维修接单

维修派工

零部件管理

车间管理

维修班组工时数据统计

维修产值统计



#### 用Docker-Compose部署:

```bash
# 克隆项目文件
git clone https://github.com/mekwenby/Car-DMS.git

# 启动
docker-compose up -d

# 初始化数据库
docker exec dms python main.py recover

```

#### 使用指南

- 数据库初始化完成后会显示管理员用户名和密码

- 用管理员账户创建普通账户

- 录入车辆档案 维修班组 工时项目 配件信息 等基础数据

- 维修开单-添加项目-派工-出库-结算

  