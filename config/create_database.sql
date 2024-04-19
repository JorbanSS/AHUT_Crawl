CREATE DATABASE IF NOT EXISTS `ahutoj`;

USE `ahutoj`;

CREATE TABLE IF NOT EXISTS `user`
(
    `UID`                 VARCHAR(20) comment '用户ID',
    `UserName`            VARCHAR(20) comment '用户名',
    `Pass`                VARCHAR(128) comment '密码',
    `School`              VARCHAR(40) comment '学校',
    `Year`                VARCHAR(4) comment '入学年份',
    `Classes`             VARCHAR(30) comment '班级',
    `Major`               VARCHAR(30) comment '专业',
    `Signature`           VARCHAR(128) comment '个性签名',
    `Email`               VARCHAR(30) comment '邮箱',
    `QQ`                  VARCHAR(20) comment 'QQ',
    `HeadUrl`             TEXT comment '头像地址',
    `LoginIP`             VARCHAR(20) comment '最近登录IP',
    `RegisterTime`        LONG comment '注册时间',
    `Submited`            INT(11) comment '提交次数' DEFAULT 0,
    `Solved`              INT(11) comment 'AC次数' DEFAULT 0,
    PRIMARY KEY(`UID`)
) DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS `rating`
(
    `UID`                 VARCHAR(20) COMMENT '用户 ID',
    `Rating`              INT(4) COMMENT '评分' DEFAULT 0,
    `CodeforcesID`        VARCHAR(20) COMMENT 'Codeforces 用户名',
    `CodeforcesRating`    INT(4) COMMENT 'Codeforces 评分' DEFAULT 0,
    `NowcoderID`          VARCHAR(20) COMMENT 'Nowcoder 用户名',
    `NowcoderRating`      INT(4) COMMENT 'Nowcoder 评分' DEFAULT 0,
    `AtcoderID`           VARCHAR(20) COMMENT 'Atcoder 用户名',
    `AtcoderRating`       INT(4) COMMENT 'Atcoder 评分' DEFAULT 0,
    `VirtualJudgeID`      VARCHAR(20),
    PRIMARY KEY(`UID`),
    CONSTRAINT `fk_rt_uid` FOREIGN KEY(`UID`) REFERENCES user(`UID`) ON UPDATE CASCADE ON DELETE CASCADE
) DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS `recentcontests`;

CREATE TABLE IF NOT EXISTS `recentcontests`
(
    `CID`                VARCHAR(20) COMMENT '比赛 ID',
    `Title`               VARCHAR(100) COMMENT '比赛名称',
    `Type`                VARCHAR(10) COMMENT '赛制',
    `StartTime`           LONG COMMENT '开始时间',
    `Duration`            INT COMMENT '持续时间',
    `OJ`                  VARCHAR(10) COMMENT '平台',
    `URL`                 VARCHAR(100) COMMENT '比赛链接',
    PRIMARY KEY(`CID`)
) DEFAULT CHARSET = 'utf8mb4';