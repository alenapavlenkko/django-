-- populate_data_final.sql
-- Очистка данных в правильном порядке (учитывая foreign keys)
DELETE FROM firstapp_var_22_review;
DELETE FROM firstapp_var_22_purchaseitem;
DELETE FROM firstapp_var_22_purchase;
DELETE FROM firstapp_var_22_order;
DELETE FROM firstapp_var_22_bookauthor;
DELETE FROM firstapp_var_22_bookdetail;
DELETE FROM firstapp_var_22_book;
DELETE FROM firstapp_var_22_category;
DELETE FROM firstapp_var_22_publisher;
DELETE FROM firstapp_var_22_author;
DELETE FROM firstapp_var_22_customer;

-- Сброс последовательностей
ALTER SEQUENCE firstapp_var_22_author_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_book_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_category_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_customer_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_publisher_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_order_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_purchase_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_review_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_bookdetail_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_bookauthor_id_seq RESTART WITH 1;
ALTER SEQUENCE firstapp_var_22_purchaseitem_id_seq RESTART WITH 1;

-- Заполнение Category
INSERT INTO firstapp_var_22_category (name, slug, description, created) VALUES
('Научная фантастика', 'sci-fi', 'Книги о будущем, технологиях и космосе', NOW()),
('Фэнтези', 'fantasy', 'Мистические миры, магия и приключения', NOW()),
('Детектив', 'detective', 'Загадки, расследования и преступления', NOW()),
('Роман', 'novel', 'Истории о любви и отношениях', NOW()),
('Бизнес', 'business', 'Книги о предпринимательстве и финансах', NOW()),
('Программирование', 'programming', 'Техническая литература для разработчиков', NOW()),
('Психология', 'psychology', 'Книги о поведении и мышлении человека', NOW()),
('История', 'history', 'Исторические исследования и хроники', NOW()),
('Кулинария', 'cooking', 'Книги о готовке и рецептах', NOW()),
('Путешествия', 'travel', 'Гид по странам и культурам мира', NOW());

-- Заполнение Author
INSERT INTO firstapp_var_22_author (first_name, last_name, bio, photo, birth_date) VALUES
('Айзек', 'Азимов', 'Американский писатель-фантаст, биохимик. Автор "Основания".', 'asimov.jpg', '1920-01-02'),
('Джоан', 'Роулинг', 'Британская писательница, автор серии о Гарри Поттере.', 'rowling.jpg', '1965-07-31'),
('Артур', 'Конан Дойл', 'Шотландский писатель, создатель Шерлока Холмса.', 'conan_doyle.jpg', '1859-05-22'),
('Лев', 'Толстой', 'Русский писатель, мыслитель, философ.', 'tolstoy.jpg', '1828-09-09'),
('Роберт', 'Кийосаки', 'Американский предприниматель, инвестор, писатель.', 'kiyosaki.jpg', '1947-04-08'),
('Мартин', 'Фаулер', 'Британский программист, автор книг о рефакторинге.', 'fowler.jpg', '1963-12-18'),
('Дейл', 'Карнеги', 'Американский писатель, лектор, педагог-психолог.', 'carnegie.jpg', '1888-11-24'),
('Юваль', 'Харари', 'Израильский историк-медиевист, профессор истории.', 'harari.jpg', '1976-02-24'),
('Джейми', 'Оливер', 'Британский повар и ресторатор.', 'oliver.jpg', '1975-05-27'),
('Тони', 'Уилер', 'Сооснователь издательства путеводителей Lonely Planet.', 'wheeler.jpg', '1946-10-20');

-- Заполнение Publisher
INSERT INTO firstapp_var_22_publisher (name, address, phone, email, website) VALUES
('Эксмо', 'Москва, ул. Зорге, 1', '+7 (495) 411-68-86', 'info@eksmo.ru', 'https://eksmo.ru'),
('АСТ', 'Москва, пр-т Мира, 106', '+7 (495) 956-39-11', 'contact@ast.ru', 'https://ast.ru'),
('Питер', 'Санкт-Петербург, ул. Благодатная, 50', '+7 (812) 336-16-65', 'office@piter.com', 'https://piter.com'),
('Манн, Иванов и Фербер', 'Москва, ул. Шаболовка, 31', '+7 (495) 775-60-18', 'mif@mif.ru', 'https://mann-ivanov-ferber.ru'),
('Альпина Паблишер', 'Москва, ул. Сретенка, 18', '+7 (495) 980-53-54', 'info@alpina.ru', 'https://alpinabook.ru');

-- Заполнение Book
INSERT INTO firstapp_var_22_book (title, slug, isbn, description, price, cover_type, pages, publication_year, stock, available, image, created, updated, category_id, publisher_id) VALUES
('Основание', 'osnovanie', '978-5-699-12345-6', 'Первая книга культовой серии Айзека Азимова о будущем человечества.', 899.99, 'Твердая', 320, 1951, 50, true, 'foundation.jpg', NOW(), NOW(), 1, 1),
('Гарри Поттер и философский камень', 'garri-potter-filosofskiy-kamen', '978-5-389-23456-7', 'Первая книга знаменитой серии о юном волшебнике.', 699.99, 'Твердая', 400, 1997, 100, true, 'harry_potter.jpg', NOW(), NOW(), 2, 2),
('Приключения Шерлока Холмса', 'priklyucheniya-sherloka-holmsa', '978-5-17-34567-8', 'Сборник рассказов о знаменитом детективе.', 549.99, 'Мягкая', 280, 1892, 75, true, 'sherlock.jpg', NOW(), NOW(), 3, 3),
('Анна Каренина', 'anna-karenina', '978-5-04-45678-9', 'Классический роман Льва Толстого о любви и морали.', 499.99, 'Твердая', 864, 1877, 60, true, 'anna_karenina.jpg', NOW(), NOW(), 4, 1),
('Богатый папа, бедный папа', 'bogatiy-papa-bedniy-papa', '978-5-001-56789-0', 'Книга о финансовой грамотности и инвестициях.', 799.99, 'Твердая', 336, 1997, 80, true, 'rich_dad.jpg', NOW(), NOW(), 5, 4),
('Рефакторинг', 'refactoring', '978-5-907-67890-1', 'Улучшение существующего кода без изменения его поведения.', 1299.99, 'Твердая', 448, 1999, 40, true, 'refactoring.jpg', NOW(), NOW(), 6, 5),
('Как завоёвывать друзей и оказывать влияние на людей', 'kak-zavoyovyvat-druzey', '978-5-001-78901-2', 'Классическая книга о межличностных отношениях.', 599.99, 'Твердая', 352, 1936, 90, true, 'how_to_win_friends.jpg', NOW(), NOW(), 7, 4),
('Sapiens: Краткая история человечества', 'sapiens-kratkaya-istoriya', '978-5-001-89012-3', 'Масштабное исследование истории человеческого вида.', 999.99, 'Твердая', 512, 2011, 55, true, 'sapiens.jpg', NOW(), NOW(), 8, 5),
('Счастливые дни с Джейми', 'schastlivye-dni-s-dzheymi', '978-5-446-90123-4', 'Кулинарная книга с рецептами от знаменитого шефа.', 1499.99, 'Твердая', 288, 2002, 35, true, 'jamie.jpg', NOW(), NOW(), 9, 3),
('Lonely Planet: Европа', 'lonely-planet-evropa', '978-5-17-01234-5', 'Подробный путеводитель по странам Европы.', 1799.99, 'Мягкая', 1200, 1973, 30, true, 'lonely_planet.jpg', NOW(), NOW(), 10, 2);

-- Заполнение BookAuthor
INSERT INTO firstapp_var_22_bookauthor (book_id, author_id) VALUES
(1, 1),  -- Азимов -> Основание
(2, 2),  -- Роулинг -> Гарри Поттер
(3, 3),  -- Конан Дойл -> Шерлок Холмс
(4, 4),  -- Толстой -> Анна Каренина
(5, 5),  -- Кийосаки -> Богатый папа
(6, 6),  -- Фаулер -> Рефакторинг
(7, 7),  -- Карнеги -> Как завоёвывать друзей
(8, 8),  -- Харари -> Sapiens
(9, 9),  -- Оливер -> Счастливые дни с Джейми
(10, 10); -- Уилер -> Lonely Planet

-- Заполнение BookDetail
INSERT INTO firstapp_var_22_bookdetail (language, dimensions, weight, created, book_id) VALUES
('Русский', '21x14x3 cm', '450g', NOW(), 1),
('Русский', '22x15x4 cm', '500g', NOW(), 2),
('Русский', '20x13x2 cm', '350g', NOW(), 3),
('Русский', '24x17x5 cm', '900g', NOW(), 4),
('Русский', '21x14x3 cm', '400g', NOW(), 5),
('Русский', '23x16x4 cm', '550g', NOW(), 6),
('Русский', '21x14x3 cm', '420g', NOW(), 7),
('Русский', '22x15x4 cm', '600g', NOW(), 8),
('Русский', '26x20x3 cm', '800g', NOW(), 9),
('Русский', '28x21x5 cm', '1200g', NOW(), 10);

-- Заполнение Customer (только обязательные поля)
INSERT INTO firstapp_var_22_customer (phone, address, registration_date, date_of_birth, avatar) VALUES
('+79161234567', 'Москва, ул. Ленина, 10', NOW(), '1990-05-15', 'avatar1.jpg'),
('+79162345678', 'Санкт-Петербург, Невский пр., 25', NOW(), '1985-08-22', 'avatar2.jpg'),
('+79163456789', 'Казань, ул. Баумана, 5', NOW(), '1992-11-30', 'avatar3.jpg'),
('+79164567890', 'Екатеринбург, ул. Малышева, 45', NOW(), '1988-03-12', 'avatar4.jpg'),
('+79165678901', 'Новосибирск, Красный пр., 100', NOW(), '1995-07-18', 'avatar5.jpg'),
('+79166789012', 'Ростов-на-Дону, ул. Большая Садовая, 15', NOW(), '1982-09-25', 'avatar6.jpg'),
('+79167890123', 'Владивосток, ул. Светланская, 30', NOW(), '1991-12-05', 'avatar7.jpg'),
('+79168901234', 'Краснодар, ул. Красная, 65', NOW(), '1987-04-20', 'avatar8.jpg'),
('+79169012345', 'Сочи, ул. Навагинская, 8', NOW(), '1993-06-14', 'avatar9.jpg'),
('+79160123456', 'Уфа, ул. Ленина, 70', NOW(), '1984-10-08', 'avatar10.jpg'),
('+79161234560', 'Волгоград, пр-т Ленина, 50', NOW(), '1994-02-28', 'avatar11.jpg'),
('+79162345670', 'Пермь, ул. Ленина, 60', NOW(), '1989-01-17', 'avatar12.jpg'),
('+79163456780', 'Омск, ул. Ленина, 40', NOW(), '1986-07-09', 'avatar13.jpg'),
('+79164567801', 'Самара, ул. Куйбышева, 95', NOW(), '1996-03-22', 'avatar14.jpg'),
('+79165678902', 'Челябинск, пр-т Ленина, 55', NOW(), '1983-05-11', 'avatar15.jpg'),
('+79166789023', 'Красноярск, ул. Карла Маркса, 120', NOW(), '1990-08-03', 'avatar16.jpg'),
('+79167890134', 'Воронеж, пр-т Революции, 35', NOW(), '1981-11-19', 'avatar17.jpg'),
('+79168901245', 'Тюмень, ул. Республики, 90', NOW(), '1997-04-07', 'avatar18.jpg'),
('+79169012356', 'Саратов, ул. Московская, 80', NOW(), '1980-09-16', 'avatar19.jpg'),
('+79160123467', 'Томск, пр-т Ленина, 75', NOW(), '1992-12-24', 'avatar20.jpg'),
('+79161234578', 'Иркутск, ул. Ленина, 1', NOW(), '1985-06-30', 'avatar21.jpg'),
('+79162345689', 'Барнаул, пр-т Ленина, 110', NOW(), '1988-02-14', 'avatar22.jpg'),
('+79163456790', 'Ульяновск, ул. Гончарова, 25', NOW(), '1993-10-05', 'avatar23.jpg'),
('+79164567891', 'Ярославль, ул. Кирова, 10', NOW(), '1987-07-21', 'avatar24.jpg');

-- Заполнение Order
INSERT INTO firstapp_var_22_order (order_date, total_amount, category_id, customer_id) VALUES
('2024-01-10', 899.99, 1, 1),
('2024-02-15', 1399.98, 2, 2),
('2024-03-20', 549.99, 3, 3),
('2024-04-25', 499.99, 4, 4),
('2024-05-30', 799.99, 5, 5),
('2024-06-05', 1299.99, 6, 6),
('2024-07-10', 599.99, 7, 7),
('2024-08-15', 999.99, 8, 8),
('2024-09-20', 1499.99, 9, 9),
('2024-10-25', 1799.99, 10, 10);

-- Заполнение Purchase
INSERT INTO firstapp_var_22_purchase (status, payment_method, payment_status, shipping_address, total, notes, created, updated, customer_id) VALUES
('completed', 'credit_card', true, 'Москва, ул. Ленина, 10, кв. 5', 899.99, 'Доставить до 18:00', NOW(), NOW(), 1),
('completed', 'paypal', true, 'Санкт-Петербург, Невский пр., 25, кв. 12', 1399.98, 'Звонок перед доставкой', NOW(), NOW(), 2),
('completed', 'cash', true, 'Казань, ул. Баумана, 5, офис 3', 549.99, 'Оставить у двери', NOW(), NOW(), 3),
('processing', 'credit_card', true, 'Екатеринбург, ул. Малышева, 45, кв. 7', 999.98, 'Хрупкий груз', NOW(), NOW(), 4),
('completed', 'bank_transfer', true, 'Новосибирск, Красный пр., 100, кв. 20', 799.99, 'Доставить в будний день', NOW(), NOW(), 5),
('shipped', 'credit_card', true, 'Ростов-на-Дону, ул. Большая Садовая, 15, офис 5', 1299.99, 'Срочная доставка', NOW(), NOW(), 6),
('completed', 'paypal', true, 'Владивосток, ул. Светланская, 30, кв. 9', 1199.98, 'Позвонить за час', NOW(), NOW(), 7),
('completed', 'cash', true, 'Краснодар, ул. Красная, 65, кв. 15', 999.99, 'Нет заметок', NOW(), NOW(), 8),
('processing', 'credit_card', false, 'Сочи, ул. Навагинская, 8, офис 2', 1499.99, 'Ожидает оплаты', NOW(), NOW(), 9),
('completed', 'bank_transfer', true, 'Уфа, ул. Ленина, 70, кв. 11', 1799.99, 'Доставить вечером', NOW(), NOW(), 10);

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

-- Заполнение Review
INSERT INTO firstapp_var_22_review (rating, title, comment, created, approved, book_id, customer_id, updated) VALUES
(5, 'Отличная книга!', 'Очень подробное руководство, рекомендую всем программистам.', NOW(), true, 6, 1, NOW()),
(4, 'Хорошая книга', 'Интересная история, но концовка предсказуема.', NOW(), true, 2, 2, NOW()),
(5, 'Шедевр!', 'Одна из лучших книг, которые я читал.', NOW(), true, 1, 3, NOW()),
(3, 'Нормально', 'Не самое лучшее произведение автора.', NOW(), true, 4, 4, NOW()),
(5, 'Изменение мышления', 'Эта книга изменила мой подход к финансам.', NOW(), true, 5, 5, NOW()),
(4, 'Полезно', 'Много полезных советов для разработчиков.', NOW(), true, 6, 6, NOW()),
(5, 'Классика!', 'Должна быть в библиотеке каждого.', NOW(), true, 7, 7, NOW()),
(5, 'Интересно', 'Очень познавательная книга об истории человечества.', NOW(), true, 8, 8, NOW()),
(4, 'Вкусные рецепты', 'Много интересных рецептов, но некоторые сложные.', NOW(), true, 9, 9, NOW()),
(5, 'Незаменимый гид', 'Лучший путеводитель по Европе.', NOW(), true, 10, 10, NOW());

-- Статистика базы данных
SELECT ' === СТАТИСТИКА БАЗЫ ДАННЫХ === ' as info;

SELECT 'Категории:' as type, COUNT(*) as count FROM firstapp_var_22_category
UNION ALL
SELECT 'Авторы:', COUNT(*) FROM firstapp_var_22_author
UNION ALL
SELECT 'Книги:', COUNT(*) FROM firstapp_var_22_book
UNION ALL
SELECT 'Клиенты:', COUNT(*) FROM firstapp_var_22_customer
UNION ALL
SELECT 'Издатели:', COUNT(*) FROM firstapp_var_22_publisher
UNION ALL
SELECT 'Заказы:', COUNT(*) FROM firstapp_var_22_order
UNION ALL
SELECT 'Покупки:', COUNT(*) FROM firstapp_var_22_purchase
UNION ALL
SELECT 'Отзывы:', COUNT(*) FROM firstapp_var_22_review;