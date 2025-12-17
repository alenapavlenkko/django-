--
-- PostgreSQL database dump
--

\restrict saFy1tBA9ydhO38qjfaPPPDn9aED3jhiuV2a0Qn6nfL1D3XZRRtFPRBxYyalkbV

-- Dumped from database version 14.19 (Homebrew)
-- Dumped by pg_dump version 14.19 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    username character varying(150)
);


ALTER TABLE public.auth_user OWNER TO myuser;

--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_author; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_author (
    id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    bio text NOT NULL,
    photo character varying(100),
    birth_date date
);


ALTER TABLE public.firstapp_var_22_author OWNER TO myuser;

--
-- Name: firstapp_var_22_author_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_author ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_book; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_book (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    slug character varying(200) NOT NULL,
    isbn character varying(17) NOT NULL,
    description text NOT NULL,
    price numeric(10,2) NOT NULL,
    cover_type character varying(10) NOT NULL,
    pages integer NOT NULL,
    publication_year integer NOT NULL,
    stock integer NOT NULL,
    available boolean NOT NULL,
    image character varying(100),
    created timestamp without time zone DEFAULT now() NOT NULL,
    updated timestamp without time zone DEFAULT now() NOT NULL,
    category_id integer NOT NULL,
    publisher_id integer,
    CONSTRAINT firstapp_var_22_book_pages_check CHECK ((pages >= 0)),
    CONSTRAINT firstapp_var_22_book_publication_year_check CHECK ((publication_year >= 0)),
    CONSTRAINT firstapp_var_22_book_stock_check CHECK ((stock >= 0))
);


ALTER TABLE public.firstapp_var_22_book OWNER TO myuser;

--
-- Name: firstapp_var_22_book_author; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_book_author (
    id integer NOT NULL,
    book_id integer NOT NULL,
    author_id integer NOT NULL
);


ALTER TABLE public.firstapp_var_22_book_author OWNER TO myuser;

--
-- Name: firstapp_var_22_book_author_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_book_author ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_book_author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_book_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_book ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_category; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_category (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.firstapp_var_22_category OWNER TO myuser;

--
-- Name: firstapp_var_22_category_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_category ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_customer; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_customer (
    id integer NOT NULL,
    phone character varying(20) NOT NULL,
    address text NOT NULL,
    date_of_birth date,
    registration_date timestamp without time zone DEFAULT now() NOT NULL,
    user_id integer
);


ALTER TABLE public.firstapp_var_22_customer OWNER TO myuser;

--
-- Name: firstapp_var_22_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_customer ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_publisher; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_publisher (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    address text NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(254) NOT NULL,
    website character varying(200) NOT NULL
);


ALTER TABLE public.firstapp_var_22_publisher OWNER TO myuser;

--
-- Name: firstapp_var_22_publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_publisher ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_publisher_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_purchase; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_purchase (
    id integer NOT NULL,
    status character varying(20) NOT NULL,
    payment_method character varying(10) NOT NULL,
    payment_status boolean NOT NULL,
    shipping_address text NOT NULL,
    total numeric(12,2) NOT NULL,
    notes text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    updated timestamp without time zone DEFAULT now() NOT NULL,
    customer_id integer NOT NULL
);


ALTER TABLE public.firstapp_var_22_purchase OWNER TO myuser;

--
-- Name: firstapp_var_22_purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_purchase ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_purchase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_purchaseitem; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_purchaseitem (
    id integer NOT NULL,
    quantity integer NOT NULL,
    price numeric(10,2) NOT NULL,
    book_id integer NOT NULL,
    purchase_id integer NOT NULL,
    CONSTRAINT firstapp_var_22_purchaseitem_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.firstapp_var_22_purchaseitem OWNER TO myuser;

--
-- Name: firstapp_var_22_purchaseitem_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_purchaseitem ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_purchaseitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: firstapp_var_22_review; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.firstapp_var_22_review (
    id integer NOT NULL,
    rating smallint NOT NULL,
    title character varying(200) NOT NULL,
    comment text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    updated timestamp without time zone DEFAULT now() NOT NULL,
    approved boolean NOT NULL,
    book_id integer NOT NULL,
    customer_id integer NOT NULL,
    CONSTRAINT firstapp_var_22_review_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.firstapp_var_22_review OWNER TO myuser;

--
-- Name: firstapp_var_22_review_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

ALTER TABLE public.firstapp_var_22_review ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.firstapp_var_22_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.auth_user (id, username) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_author; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_author (id, first_name, last_name, bio, photo, birth_date) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_book; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_book (id, title, slug, isbn, description, price, cover_type, pages, publication_year, stock, available, image, created, updated, category_id, publisher_id) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_book_author; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_book_author (id, book_id, author_id) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_category; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_category (id, name, slug, description, created) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_customer; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_customer (id, phone, address, date_of_birth, registration_date, user_id) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_publisher; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_publisher (id, name, address, phone, email, website) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_purchase; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_purchase (id, status, payment_method, payment_status, shipping_address, total, notes, created, updated, customer_id) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_purchaseitem; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_purchaseitem (id, quantity, price, book_id, purchase_id) FROM stdin;
\.


--
-- Data for Name: firstapp_var_22_review; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.firstapp_var_22_review (id, rating, title, comment, created, updated, approved, book_id, customer_id) FROM stdin;
\.


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, false);


--
-- Name: firstapp_var_22_author_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_author_id_seq', 1, false);


--
-- Name: firstapp_var_22_book_author_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_book_author_id_seq', 1, false);


--
-- Name: firstapp_var_22_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_book_id_seq', 1, false);


--
-- Name: firstapp_var_22_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_category_id_seq', 1, false);


--
-- Name: firstapp_var_22_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_customer_id_seq', 1, false);


--
-- Name: firstapp_var_22_publisher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_publisher_id_seq', 1, false);


--
-- Name: firstapp_var_22_purchase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_purchase_id_seq', 1, false);


--
-- Name: firstapp_var_22_purchaseitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_purchaseitem_id_seq', 1, false);


--
-- Name: firstapp_var_22_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.firstapp_var_22_review_id_seq', 1, false);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_author firstapp_var_22_author_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_author
    ADD CONSTRAINT firstapp_var_22_author_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_book_author firstapp_var_22_book_author_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_book_author
    ADD CONSTRAINT firstapp_var_22_book_author_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_book firstapp_var_22_book_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_book
    ADD CONSTRAINT firstapp_var_22_book_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_book firstapp_var_22_book_slug_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_book
    ADD CONSTRAINT firstapp_var_22_book_slug_key UNIQUE (slug);


--
-- Name: firstapp_var_22_category firstapp_var_22_category_name_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_category
    ADD CONSTRAINT firstapp_var_22_category_name_key UNIQUE (name);


--
-- Name: firstapp_var_22_category firstapp_var_22_category_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_category
    ADD CONSTRAINT firstapp_var_22_category_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_category firstapp_var_22_category_slug_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_category
    ADD CONSTRAINT firstapp_var_22_category_slug_key UNIQUE (slug);


--
-- Name: firstapp_var_22_customer firstapp_var_22_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_customer
    ADD CONSTRAINT firstapp_var_22_customer_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_customer firstapp_var_22_customer_user_id_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_customer
    ADD CONSTRAINT firstapp_var_22_customer_user_id_key UNIQUE (user_id);


--
-- Name: firstapp_var_22_publisher firstapp_var_22_publisher_name_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_publisher
    ADD CONSTRAINT firstapp_var_22_publisher_name_key UNIQUE (name);


--
-- Name: firstapp_var_22_publisher firstapp_var_22_publisher_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_publisher
    ADD CONSTRAINT firstapp_var_22_publisher_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_purchase firstapp_var_22_purchase_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_purchase
    ADD CONSTRAINT firstapp_var_22_purchase_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_purchaseitem firstapp_var_22_purchaseitem_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_purchaseitem
    ADD CONSTRAINT firstapp_var_22_purchaseitem_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_review firstapp_var_22_review_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_review
    ADD CONSTRAINT firstapp_var_22_review_pkey PRIMARY KEY (id);


--
-- Name: firstapp_var_22_book_author uq_book_author; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_book_author
    ADD CONSTRAINT uq_book_author UNIQUE (book_id, author_id);


--
-- Name: firstapp_var_22_book_author firstapp_var_22_book_author_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_book_author
    ADD CONSTRAINT firstapp_var_22_book_author_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.firstapp_var_22_author(id);


--
-- Name: firstapp_var_22_book_author firstapp_var_22_book_author_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_book_author
    ADD CONSTRAINT firstapp_var_22_book_author_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.firstapp_var_22_book(id);


--
-- Name: firstapp_var_22_book firstapp_var_22_book_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_book
    ADD CONSTRAINT firstapp_var_22_book_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.firstapp_var_22_category(id);


--
-- Name: firstapp_var_22_book firstapp_var_22_book_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_book
    ADD CONSTRAINT firstapp_var_22_book_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES public.firstapp_var_22_publisher(id);


--
-- Name: firstapp_var_22_customer firstapp_var_22_customer_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_customer
    ADD CONSTRAINT firstapp_var_22_customer_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.auth_user(id);


--
-- Name: firstapp_var_22_purchase firstapp_var_22_purchase_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_purchase
    ADD CONSTRAINT firstapp_var_22_purchase_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.firstapp_var_22_customer(id);


--
-- Name: firstapp_var_22_purchaseitem firstapp_var_22_purchaseitem_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_purchaseitem
    ADD CONSTRAINT firstapp_var_22_purchaseitem_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.firstapp_var_22_book(id);


--
-- Name: firstapp_var_22_purchaseitem firstapp_var_22_purchaseitem_purchase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_purchaseitem
    ADD CONSTRAINT firstapp_var_22_purchaseitem_purchase_id_fkey FOREIGN KEY (purchase_id) REFERENCES public.firstapp_var_22_purchase(id);


--
-- Name: firstapp_var_22_review firstapp_var_22_review_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_review
    ADD CONSTRAINT firstapp_var_22_review_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.firstapp_var_22_book(id);


--
-- Name: firstapp_var_22_review firstapp_var_22_review_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.firstapp_var_22_review
    ADD CONSTRAINT firstapp_var_22_review_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.firstapp_var_22_customer(id);


--
-- PostgreSQL database dump complete
--

\unrestrict saFy1tBA9ydhO38qjfaPPPDn9aED3jhiuV2a0Qn6nfL1D3XZRRtFPRBxYyalkbV

