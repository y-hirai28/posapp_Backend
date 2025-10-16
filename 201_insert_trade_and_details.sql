USE hirai_pos;

INSERT INTO product_master (code, name, price)
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
 ('4611111000023', '折りたたみ会議テーブル（180cm）', 4980);

ON DUPLICATE KEY UPDATE
  name  = VALUES(name),
  price = VALUES(price);
SELECT * FROM product_master;

INSERT INTO trade (datetime, emp_cd, store_cd, pos_no, total_amt)
VALUES (
    NOW(),                                       
    IFNULL(NULLIF('E001234567',''), '9999999999'), 
    '30',                                        
    '90',                                        
    0                                          
);

SET @p_trd_id = LAST_INSERT_ID();

START TRANSACTION;

SET @base = COALESCE((SELECT MAX(DTL_ID) FROM trade_detail WHERE TRD_ID = @p_trd_id), 0);

INSERT INTO trade_detail (TRD_ID, DTL_ID, PRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE)
SELECT
  @p_trd_id, @base + 1, pm.prd_id, pm.code, pm.name, pm.price
FROM product_master pm
WHERE pm.code = '4512345000042';

INSERT INTO trade_detail (TRD_ID, DTL_ID, PRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE)
SELECT
  @p_trd_id, @base + 2, pm.prd_id, pm.code, pm.name, pm.price
FROM product_master pm
WHERE pm.code = '4512345000011';

INSERT INTO trade_detail (TRD_ID, DTL_ID, PRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE)
SELECT
  @p_trd_id, @base + 3, pm.prd_id, pm.code, pm.name, pm.price
FROM product_master pm
WHERE pm.code = '4512345000035';

UPDATE trade t
SET t.total_amt = (
  SELECT COALESCE(SUM(td.PRD_PRICE),0)
  FROM trade_detail td
  WHERE td.TRD_ID = @p_trd_id
)
WHERE t.trd_id = @p_trd_id;

COMMIT;
