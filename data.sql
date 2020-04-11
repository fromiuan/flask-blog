CREATE TABLE `sys_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fid` int(11) NOT NULL DEFAULT 0,
  'level' int(11) NOT NULL DEFAULT 0,
  `name` varchar(255) NOT NULL DEFAULT '',
  `tree` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `sys_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL DEFAULT '',
  `password` varchar(255) NOT NULL DEFAULT '',
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `sys_dictionary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) NOT NULL DEFAULT '',
  `value` text,
  `types` int(1) NOT NULL DEFAULT 0,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dict_key` (`key`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `sys_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL DEFAULT  0,
  `name` varchar(255) NOT NULL DEFAULT '',
  `path` varchar(255) NOT NULL DEFAULT '',
  `types` int(1) NOT NULL DEFAULT 0,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `sys_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `sys_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL DEFAULT 0,
  `title` varchar(255) NOT NULL  DEFAULT '',
  `content` text,
  `date` datetime DEFAULT NULL,
  `views` int(11) NOT NULL DEFAULT 0,
  `flag` int(11) NOT NULL DEFAULT 0,
  `description` varchar(255) NOT NULL  DEFAULT '',
  `img` varchar(255) NOT NULL  DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `sys_article_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL DEFAULT 0,
  `tag_id` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `sys_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL DEFAULT 0,
  `author` varchar(255) NOT NULL  DEFAULT '',
  `content` varchar(255) NOT NULL  DEFAULT '',
  `up` int(11) NOT NULL DEFAULT 0,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
