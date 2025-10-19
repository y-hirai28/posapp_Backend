-- スキーマを選択（左で Set as Default していれば省略可）
USE hirai_pos;

ALTER TABLE product_master
  MODIFY code CHAR(13) NOT NULL;

SET SQL_SAFE_UPDATES = 0;
UPDATE product_master
SET code = LPAD(code, 13, '0')
WHERE CHAR_LENGTH(code) < 13;
SET SQL_SAFE_UPDATES = 1;

SELECT *
FROM product_master
WHERE CHAR_LENGTH(code) > 13;

SET @idx_cnt := (
  SELECT COUNT(*)
  FROM information_schema.statistics
  WHERE table_schema = DATABASE()
    AND table_name   = 'product_master'
    AND index_name   = 'ux_product_master_code'
);
SET @sql := IF(@idx_cnt = 0,
  'ALTER TABLE product_master ADD UNIQUE KEY ux_product_master_code (code);',
  'SELECT "ux_product_master_code already exists" AS msg;'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

INSERT INTO `product_master` (`code`, `name`, `price`)
VALUES
 ('4512345000011', 'ボールペン（黒・0.5mm）', 120),
 ('4512345000028', 'シャープペンシル（0.5mm）', 180),
 ('4512345000035', '消しゴム（小）', 80),
 ('4512345000042', 'A4コピー用紙（500枚）', 480),
 ('4987654000012', 'スティックのり', 150),
 ('4987654000029', 'ホッチキス（中型）', 520),
 ('4987654000036', 'ホッチキス針（1000本入り）', 250),
 ('4987654000043', 'はさみ（事務用）', 350),
 ('4611111000016', 'デスクチェア（メッシュ）', 6980),
 ('4611111000023', '折りたたみ会議テーブル（180cm）', 4980)
AS new
ON DUPLICATE KEY UPDATE
  `name`  = new.`name`,
  `price` = new.`price`;



/* ヘッダ */
INSERT INTO `trade` (`datetime`, `emp_cd`, `store_cd`, `pos_no`, `total_amt`, `TTL_AMT_EX_TAX`)
VALUES (
  NOW(),
  IFNULL(NULLIF('E001234567',''), '9999999999'),
  '30',
  '90',
  0,
  0
);

/* 新しい trd_id を取得 */
SET @p_trd_id := LAST_INSERT_ID();

/* 明細はトランザクションで */
START TRANSACTION;

/* 既存の最大 DTL_ID（取引内行番号）を取得 */
SET @base := COALESCE(
  (SELECT MAX(`DTL_ID`) FROM `trade_detail` WHERE `TRD_ID` = @p_trd_id), 0
);

-- 1行目：A4コピー用紙（TAX_CD を追加：例として '10' をセット）
INSERT INTO `trade_detail`
  (`TRD_ID`, `DTL_ID`, `PRD_ID`, `PRD_CODE`, `PRD_NAME`, `PRD_PRICE`, `TAX_CD`)
SELECT @p_trd_id, @base + 1, pm.`PRD_ID`, pm.`CODE`, pm.`NAME`, pm.`PRICE`, '10'
FROM `product_master` pm
WHERE pm.`CODE` = '4512345000042';

-- 2行目：ボールペン
INSERT INTO `trade_detail`
  (`TRD_ID`, `DTL_ID`, `PRD_ID`, `PRD_CODE`, `PRD_NAME`, `PRD_PRICE`, `TAX_CD`)
SELECT @p_trd_id, @base + 2, pm.`PRD_ID`, pm.`CODE`, pm.`NAME`, pm.`PRICE`, '10'
FROM `product_master` pm
WHERE pm.`CODE` = '4512345000011';

-- 3行目：消しゴム
INSERT INTO `trade_detail`
  (`TRD_ID`, `DTL_ID`, `PRD_ID`, `PRD_CODE`, `PRD_NAME`, `PRD_PRICE`, `TAX_CD`)
SELECT @p_trd_id, @base + 3, pm.`PRD_ID`, pm.`CODE`, pm.`NAME`, pm.`PRICE`, '10'
FROM `product_master` pm
WHERE pm.`CODE` = '4512345000035';

-- 合計金額をヘッダに反映
UPDATE `trade` t
SET t.`total_amt` = (
  SELECT COALESCE(SUM(td.`PRD_PRICE`), 0)
  FROM `trade_detail` td
  WHERE td.`TRD_ID` = @p_trd_id
)
WHERE t.`TRD_ID` = @p_trd_id;

COMMIT;