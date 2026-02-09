-- Company Database Creation Script
-- Creates DEPARTMENT and EMPLOYEE tables with sample data

-- Create the database
CREATE DATABASE IF NOT EXISTS company_db;
USE company_db;

-- Drop tables if they exist (in correct order due to foreign key)
DROP TABLE IF EXISTS EMPLOYEE;
DROP TABLE IF EXISTS DEPARTMENT;

-- Create DEPARTMENT table
CREATE TABLE DEPARTMENT (
    deptno INT PRIMARY KEY,
    dname VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL
);

-- Create EMPLOYEE table
CREATE TABLE EMPLOYEE (
    empno INT PRIMARY KEY,
    ename VARCHAR(50) NOT NULL,
    job VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    comm DECIMAL(10, 2) NULL,
    deptno INT NOT NULL,
    FOREIGN KEY (deptno) REFERENCES DEPARTMENT(deptno)
);

-- Insert data into DEPARTMENT table
INSERT INTO DEPARTMENT (deptno, dname, location) VALUES
(10, 'ACCOUNTING', 'NEW YORK'),
(20, 'RESEARCH', 'DALLAS'),
(30, 'SALES', 'CHICAGO'),
(40, 'OPERATIONS', 'BOSTON');

-- Insert data into EMPLOYEE table
INSERT INTO EMPLOYEE (empno, ename, job, dob, salary, comm, deptno) VALUES
(7839, 'KING', 'PRESIDENT', '1981-11-17', 5000, NULL, 10),
(7698, 'BLAKE', 'MANAGER', '1981-05-01', 2850, NULL, 30),
(7782, 'CLARK', 'MANAGER', '1981-09-06', 2450, NULL, 10),
(7566, 'JOHN', 'MANAGER', '1982-03-02', 2975, NULL, 20),
(7788, 'SCOTT', 'ANALYST', '1992-05-16', 3000, NULL, 20),
(7902, 'HENRY', 'ANALYST', '2001-12-01', 3000, NULL, 20),
(7369, 'BARBARA', 'CLERK', '1995-07-16', 800, NULL, 20),
(7299, 'ANDY', 'SALESMAN', '1999-08-12', 1600, 300, 30),
(7521, 'KEN', 'SALESMAN', '1992-04-15', 3250, 800, 30),
(7844, 'STEVE', 'SALESMAN', '1987-03-12', 1500, 0, 30),
(7816, 'ADAM', 'CLERK', '1987-06-12', 1100, NULL, 20),
(7934, 'CHRISTINE', 'SALESMAN', '1992-10-11', 4300, 1000, 10);

-- Verify the data
SELECT 'DEPARTMENT Table:' AS '';
SELECT * FROM DEPARTMENT;

SELECT 'EMPLOYEE Table:' AS '';
SELECT * FROM EMPLOYEE;
