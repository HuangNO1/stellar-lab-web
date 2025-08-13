-- MySQL 8.0 初始化脚本
-- 创建专用数据库用户而不是使用 root

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS lab_web CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建专用的应用用户
CREATE USER IF NOT EXISTS 'lab_web_user'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';

-- 授予数据库权限（只针对 lab_web 数据库）
GRANT ALL PRIVILEGES ON lab_web.* TO 'lab_web_user'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 确保可以从容器网络访问
SELECT user, host FROM mysql.user WHERE user = 'lab_web_user';