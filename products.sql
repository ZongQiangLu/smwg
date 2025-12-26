/*
 Navicat Premium Data Transfer

 Source Server         : tt
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 26/12/2025 14:03:54
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS "products";
CREATE TABLE "products" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" VARCHAR(200) NOT NULL,
  "cover" VARCHAR(255) NOT NULL,
  "images" JSON NOT NULL,
  "description" TEXT,
  "base_price" VARCHAR(40) NOT NULL,
  "sales" INT NOT NULL DEFAULT 0,
  "status" INT NOT NULL DEFAULT 1,
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "category_id" INT NOT NULL,
  FOREIGN KEY ("category_id") REFERENCES "categories" ("id") ON DELETE CASCADE ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO "products" VALUES (1, 'iPhone 15 Pro Max', 'https://picsum.photos/seed/product1/400/400', '["https://picsum.photos/seed/product1/400/400"]', 'Apple iPhone 15 Pro Max，A17 Pro芯片，钛金属设计', '9999', 1234, 1, '2025-12-26 04:48:59.198761+00:00', 1);
INSERT INTO "products" VALUES (2, '华为 Mate 60 Pro', 'https://picsum.photos/seed/product2/400/400', '["https://picsum.photos/seed/product2/400/400"]', '华为Mate60 Pro，麒麟芯片回归，卫星通话', '6999', 2345, 1, '2025-12-26 04:48:59.217511+00:00', 1);
INSERT INTO "products" VALUES (3, 'MacBook Pro 14', 'https://picsum.photos/seed/product3/400/400', '["https://picsum.photos/seed/product3/400/400"]', 'Apple MacBook Pro 14英寸，M3 Pro芯片', '14999', 567, 1, '2025-12-26 04:48:59.230987+00:00', 2);
INSERT INTO "products" VALUES (4, 'iPad Pro 12.9', 'https://picsum.photos/seed/product4/400/400', '["https://picsum.photos/seed/product4/400/400"]', 'Apple iPad Pro 12.9英寸，M2芯片', '8999', 890, 1, '2025-12-26 04:48:59.244373+00:00', 3);
INSERT INTO "products" VALUES (5, 'AirPods Pro 2', 'https://picsum.photos/seed/product5/400/400', '["https://picsum.photos/seed/product5/400/400"]', 'Apple AirPods Pro 第二代，主动降噪', '1899', 3456, 1, '2025-12-26 04:48:59.258582+00:00', 4);
INSERT INTO "products" VALUES (6, 'Apple Watch Ultra 2', 'https://picsum.photos/seed/product6/400/400', '["https://picsum.photos/seed/product6/400/400"]', 'Apple Watch Ultra 2，钛金属表壳', '6499', 234, 1, '2025-12-26 04:48:59.268003+00:00', 5);
INSERT INTO "products" VALUES (7, '小米14 Ultra', 'https://picsum.photos/seed/product7/400/400', '["https://picsum.photos/seed/product7/400/400"]', '徕卡光学镜头，骁龙8 Gen3', '6499', 2345, 1, '2025-12-26 05:37:07.981225+00:00', 1);
INSERT INTO "products" VALUES (8, 'OPPO Find X7 Ultra', 'https://picsum.photos/seed/product8/400/400', '["https://picsum.photos/seed/product8/400/400"]', '哈苏影像，双潜望长焦', '5999', 1876, 1, '2025-12-26 05:37:07.995879+00:00', 1);
INSERT INTO "products" VALUES (9, 'vivo X100 Pro', 'https://picsum.photos/seed/product9/400/400', '["https://picsum.photos/seed/product9/400/400"]', '蔡司影像，天玑9300', '5299', 1543, 1, '2025-12-26 05:37:08.010484+00:00', 1);
INSERT INTO "products" VALUES (10, '联想小新Pro16', 'https://picsum.photos/seed/product10/400/400', '["https://picsum.photos/seed/product10/400/400"]', '酷睿i5-13500H，16GB内存', '5999', 987, 1, '2025-12-26 05:37:08.027926+00:00', 2);
INSERT INTO "products" VALUES (11, '华硕天选4', 'https://picsum.photos/seed/product11/400/400', '["https://picsum.photos/seed/product11/400/400"]', 'RTX4060，144Hz电竞屏', '6999', 765, 1, '2025-12-26 05:37:08.041932+00:00', 2);
INSERT INTO "products" VALUES (12, '小米平板6 Pro', 'https://picsum.photos/seed/product12/400/400', '["https://picsum.photos/seed/product12/400/400"]', '骁龙8+，144Hz高刷', '2499', 2134, 1, '2025-12-26 05:37:08.056549+00:00', 3);
INSERT INTO "products" VALUES (13, '荣耀平板V8 Pro', 'https://picsum.photos/seed/product13/400/400', '["https://picsum.photos/seed/product13/400/400"]', '天玑8100，12.1英寸大屏', '2999', 1567, 1, '2025-12-26 05:37:08.070096+00:00', 3);
INSERT INTO "products" VALUES (14, '索尼WH-1000XM5', 'https://picsum.photos/seed/product14/400/400', '["https://picsum.photos/seed/product14/400/400"]', '顶级降噪，30小时续航', '2499', 3456, 1, '2025-12-26 05:37:08.083497+00:00', 4);
INSERT INTO "products" VALUES (15, 'Bose QC45', 'https://picsum.photos/seed/product15/400/400', '["https://picsum.photos/seed/product15/400/400"]', '舒适佩戴，出色降噪', '2299', 2789, 1, '2025-12-26 05:37:08.096796+00:00', 4);
INSERT INTO "products" VALUES (16, '小米手表S3', 'https://picsum.photos/seed/product16/400/400', '["https://picsum.photos/seed/product16/400/400"]', 'eSIM独立通话，运动健康', '999', 4567, 1, '2025-12-26 05:37:08.109651+00:00', 5);
INSERT INTO "products" VALUES (17, 'OPPO Watch 4 Pro', 'https://picsum.photos/seed/product17/400/400', '["https://picsum.photos/seed/product17/400/400"]', '双擎混动，超长续航', '2199', 1234, 1, '2025-12-26 05:37:08.127937+00:00', 5);
INSERT INTO "products" VALUES (18, '倍思100W氮化镓充电器', 'https://picsum.photos/seed/product18/400/400', '["https://picsum.photos/seed/product18/400/400"]', '4口快充，小巧便携', '199', 8765, 1, '2025-12-26 05:37:08.141704+00:00', 6);
INSERT INTO "products" VALUES (19, '罗技MX Master 3S', 'https://picsum.photos/seed/product19/400/400', '["https://picsum.photos/seed/product19/400/400"]', '静音点击，8000DPI', '799', 3456, 1, '2025-12-26 05:37:08.155326+00:00', 6);
INSERT INTO "products" VALUES (20, '绿联Type-C扩展坞', 'https://picsum.photos/seed/product20/400/400', '["https://picsum.photos/seed/product20/400/400"]', '10合1，4K HDMI', '299', 5678, 1, '2025-12-26 05:37:08.176043+00:00', 6);

-- ----------------------------
-- Auto increment value for products
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 20 WHERE name = 'products';

PRAGMA foreign_keys = true;
