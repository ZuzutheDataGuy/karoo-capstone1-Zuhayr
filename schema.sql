-- schema.sql
-- Database schema for Karoo Organics

CREATE Database KarooOrganics;

USE KarooOrganics;

-- =============================
-- Core Tables
-- =============================

CREATE TABLE IF NOT EXISTS Suppliers (
    supplier_id INT PRIMARY KEY,
    farm_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    contact_email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id INT PRIMARY KEY,
    supplier_id INT NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    total_price DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- =============================
-- New Tables for Q4 Report
-- =============================

-- Sales targets per region and quarter
CREATE TABLE IF NOT EXISTS Sales_Targets (
    region VARCHAR(50) NOT NULL,
    quarter VARCHAR(6) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL CHECK (target_amount > 0),
    PRIMARY KEY (region, quarter)
);

-- Certifications held by suppliers
CREATE TABLE IF NOT EXISTS Certifications (
    certification_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    certification_name VARCHAR(100) NOT NULL,
    issued_by VARCHAR(100),
    issue_date DATE,
    UNIQUE (supplier_id, certification_name),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- Harvest logging for operational tracking
CREATE TABLE IF NOT EXISTS Harvest_Log (
    harvest_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    harvest_date DATE NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    quantity_kg DECIMAL(10,2) NOT NULL CHECK (quantity_kg > 0),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- =============================
-- Indexes for Performance
-- =============================
CREATE INDEX idx_orders_supplier ON Orders(supplier_id);
CREATE INDEX idx_orders_date ON Orders(order_date);
CREATE INDEX idx_harvest_supplier ON Harvest_Log(supplier_id);

