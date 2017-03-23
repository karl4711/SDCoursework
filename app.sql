/*
Navicat SQLite Data Transfer

Source Server         : sd
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2017-03-23 14:46:08
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for bands
-- ----------------------------
DROP TABLE IF EXISTS "main"."bands";
CREATE TABLE "bands" (
"name"  TEXT,
"username"  TEXT,
"public"  INTEGER,
"captainId"  INTEGER,
"ensignId"  INTEGER DEFAULT 0,
"currency"  INTEGER,
"soldiers"  TEXT
);

-- ----------------------------
-- Table structure for items
-- ----------------------------
DROP TABLE IF EXISTS "main"."items";
CREATE TABLE "items" (
"name"  TEXT NOT NULL,
"type"  INTEGER,
"cost"  INTEGER NOT NULL,
PRIMARY KEY ("name" ASC)
);

-- ----------------------------
-- Table structure for members
-- ----------------------------
DROP TABLE IF EXISTS "main"."members";
CREATE TABLE "members" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"type"  INTEGER,
"move"  INTEGER,
"fight"  INTEGER,
"shoot"  INTEGER,
"shield"  INTEGER,
"morale"  INTEGER,
"health"  INTEGER,
"specialism"  TEXT,
"skills"  TEXT,
"experience"  INTEGER DEFAULT 0,
"weapons"  TEXT,
"items"  TEXT
);

-- ----------------------------
-- Table structure for specialisms
-- ----------------------------
DROP TABLE IF EXISTS "main"."specialisms";
CREATE TABLE "specialisms" (
"name"  TEXT NOT NULL,
"skill1"  TEXT,
"skill2"  TEXT,
"skill3"  TEXT,
PRIMARY KEY ("name")
);

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "main"."sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Table structure for troops
-- ----------------------------
DROP TABLE IF EXISTS "main"."troops";
CREATE TABLE "troops" (
"name"  TEXT NOT NULL,
"move"  INTEGER,
"fight"  INTEGER,
"shoot"  INTEGER,
"shield"  INTEGER,
"morale"  INTEGER,
"health"  INTEGER,
"cost"  INTEGER,
"notes"  TEXT,
PRIMARY KEY ("name")
);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "main"."users";
CREATE TABLE "users" (
"username"  TEXT NOT NULL,
"password"  TEXT,
PRIMARY KEY ("username")
);
