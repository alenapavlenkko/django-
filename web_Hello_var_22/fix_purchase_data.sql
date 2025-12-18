-- fix_purchase_data.sql
-- Сначала очистим purchaseitem и purchase
DELETE FROM firstapp_var_22_purchaseitem;
DELETE FROM firstapp_var_22_purchase;

-- Сбросим последовательности
ALTER SEQUENCE firstapp_var_22_purchase_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_purchaseitem_id_seq RESTART WITH 1;

-- Заполнение Purchase с корректными статусами
INSERT INTO firstapp_var_22_purchase (status, payment_method, payment_status, shipping_address, total, notes, created, updated, customer_id) VALUES
('done', 'card', true, 'Москва, ул. Ленина, 10, кв. 5', 899.99, 'Доставить до 18:00', NOW(), NOW(), 1),
('done', 'paypal', true, 'Санкт-Петербург, Невский пр., 25, кв. 12', 1399.98, 'Звонок перед доставкой', NOW(), NOW(), 2),
('done', 'cash', true, 'Казань, ул. Баумана, 5, офис 3', 549.99, 'Оставить у двери', NOW(), NOW(), 3),
('process', 'card', true, 'Екатеринбург, ул. Малышева, 45, кв. 7', 999.98, 'Хрупкий груз', NOW(), NOW(), 4),
('done', 'bank', true, 'Новосибирск, Красный пр., 100, кв. 20', 799.99, 'Доставить в будний день', NOW(), NOW(), 5),
('sent', 'card', true, 'Ростов-на-Дону, ул. Большая Садовая, 15, офис 5', 1299.99, 'Срочная доставка', NOW(), NOW(), 6),
('done', 'paypal', true, 'Владивосток, ул. Светланская, 30, кв. 9', 1199.98, 'Позвонить за час', NOW(), NOW(), 7),
('done', 'cash', true, 'Краснодар, ул. Красная, 65, кв. 15', 999.99, 'Нет заметок', NOW(), NOW(), 8),
('process', 'card', false, 'Сочи, ул. Навагинская, 8, офис 2', 1499.99, 'Ожидает оплаты', NOW(), NOW(), 9),
('done', 'bank', true, 'Уфа, ул. Ленина, 70, кв. 11', 1799.99, 'Доставить вечером', NOW(), NOW(), 10);

-- Заполнение PurchaseItem
INSERT INTO firstapp_var_22_purchaseitem (quantity, price, book_id, purchase_id) VALUES
(1, 899.99, 1, 1),
(2, 699.99, 2, 2),
(1, 549.99, 3, 3),
(2, 499.99, 4, 4),
(1, 799.99, 5, 5),
(1, 1299.99, 6, 6),
(2, 599.99, 7, 7),
(1, 999.99, 8, 8),
(1, 1499.99, 9, 9),
(1, 1799.99, 10, 10);

-- Проверка данных
SELECT 'Purchase count:' as info, COUNT(*) as count FROM firstapp_var_22_purchase
UNION ALL
SELECT 'PurchaseItem count:', COUNT(*) FROM firstapp_var_22_purchaseitem;